# Copyright 2026 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import streamlit as st

from demo.content import DEMO_QUESTIONS, EVAL_QUESTIONS, TIER_LABELS, TIER_PILLARS
from demo.snowflake import load_results

ARMS = {"B": "B: Enriched SVs", "C": "C: Enriched SVs + BON"}

st.header("How we measure BON uplift")
st.write("Two agents with the same model, semantic views, budget and instructions: **B = Enriched SVs only** "
         "(`ENRICHED_AGENT`) and **C = the same Enriched SVs + Business Ontology** (`BON_AGENT`). "
         "**BON uplift = C − B**: the only difference between B and C is the Business Ontology tool. Each question "
         "runs 5 times per agent in Tiers 2 to 3 (where uplift is expected) and 3 times in Tiers 1 and 4; answers that "
         "offer competing numbers without committing to one are graded wrong. Tier 1 is a control: well-built SVs "
         "should already get it right.")
for col, (tier, label) in zip(st.columns(len(TIER_LABELS)), TIER_LABELS.items()):
    with col.container(border=True, height="stretch"):
        st.markdown(f"**{TIER_PILLARS[tier]}**")
        st.caption(label)

try:
    run_id, per_q, consistency = load_results()
except Exception as e:
    st.error(f"Could not load results: {e}", icon=":material/error:")
    st.stop()

if not run_id:
    st.warning("The full run starts once the Business Ontology search index has refreshed (up to 6 hours after "
               "ontology edits). Run `python benchmark/run_benchmark.py`; results appear here automatically. "
               "Meanwhile, use the Comparison page to run any question live.",
               icon=":material/hourglass_top:", title="Benchmark results pending")
    st.stop()

# ------------------------------------------------------------------ Accuracy by value pillar
st.header("Accuracy by value pillar")
st.caption(f"Run `{run_id}`")
tier_of = {q["id"]: q["tier"] for q in EVAL_QUESTIONS}
scored = per_q.assign(TIER=per_q["QID"].map(tier_of)).dropna(subset=["TIER"])
totals = scored.groupby(["TIER", "ARM"])[["OK", "N"]].sum()
pct = (100 * totals["OK"] / totals["N"]).round().unstack("ARM").reindex(columns=list(ARMS)).fillna(0).astype(int)
pillars = pd.DataFrame({
    "Pillar": [TIER_PILLARS[t] for t in pct.index],
    ARMS["B"]: pct["B"].values,
    ARMS["C"]: pct["C"].values,
    "BON uplift (C − B)": (pct["C"] - pct["B"]).values,
})
st.dataframe(
    pillars, hide_index=True,
    column_config={
        ARMS["B"]: st.column_config.NumberColumn(format="%d%%"),
        ARMS["C"]: st.column_config.NumberColumn(format="%d%%"),
        "BON uplift (C − B)": st.column_config.NumberColumn(format="%+d pts"),
    },
)

# ------------------------------------------------------------------ Demo questions
st.header("Demo questions (correct runs / total)")
st.caption("Tier 1: three controls. Tiers 2 to 4: the questions where the Business Ontology was right and the SV-only "
           "agent was not. Tier scores above use all 20 benchmark questions.")
cells = per_q.set_index(["QID", "ARM"])


def score(qid, arm):
    if (qid, arm) not in cells.index:
        return "–"
    c = cells.loc[(qid, arm)]
    hedged = f" ({int(c['HEDGED'])} hedged)" if c["HEDGED"] else ""
    return f"{int(c['OK'])}/{int(c['N'])}{hedged}"


st.dataframe(
    pd.DataFrame([{"Q": q["id"], "Question": q["q"], "B": score(q["id"], "B"), "C": score(q["id"], "C"),
                   "Governed by": q["governed"]} for q in DEMO_QUESTIONS]),
    hide_index=True,
)

# ------------------------------------------------------------------ Consistency
if not consistency.empty:
    st.header("Do two teams get the same answer?")
    st.caption("Finance agent (Finance + Procurement SVs) vs Sales agent (Sales + Procurement SVs), same question, same run.")
    st.dataframe(
        consistency.assign(ARM=consistency["ARM"].map({"bon": "With BON"}).fillna("Without BON"))
        .rename(columns={"ARM": "Setup", "QID": "Question", "AGREE": "Agree", "BOTH_RIGHT": "Both right"}),
        hide_index=True,
        column_config={"Agree": st.column_config.NumberColumn(format="%d%%"),
                       "Both right": st.column_config.NumberColumn(format="%d%%")},
    )
