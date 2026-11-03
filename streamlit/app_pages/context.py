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

from demo.content import (BENEFITS, BON_GRAPH, CANONICAL, CODE_TERMS, CONFLICTS, CROSS, GAPS, POLICIES,
                          SV_ALREADY, SVS, TABLE_GROUPS)

# ------------------------------------------------------------------ What semantic views can't answer
st.header("What semantic views can't answer on their own")
st.write("Every agent in this demo gets the same three well-built semantic views, one per team. "
         "The only difference is whether it can consult the Business Ontology.")
st.success(" · ".join(SV_ALREADY) + ".", icon=":material/check_circle:",
           title="Semantic views already handle single-team rules well, so BON is not needed for these (Tier 1, the control)")

for g in GAPS:
    st.subheader(g["gap"])
    st.caption(g["why"])
    st.table(pd.DataFrame(g["examples"], columns=["Question", "Risk with semantic views alone", "With Business Ontology"]), hide_index=True)

with st.container(horizontal=True):
    for title, text in BENEFITS:
        with st.container(border=True):
            st.markdown(f"**{title}.** {text}")
st.caption("The middle column shows the defensible-but-wrong answer each semantic view metric gives if the agent picks it; "
           "a well-built baseline agent often avoids or hedges these, so measured rates are what count. "
           "Measured rates are on the Analysis page. Try any question live on the Comparison page.")

st.divider()

# ------------------------------------------------------------------ Semantic views
st.header("Semantic views: one per team, built well")
st.write("Each team owns an **enriched** semantic view with metrics, synonyms, code values, custom instructions and "
         "verified queries. Each is correct for its own team. The views can't join across teams, and their names "
         "overlap: several metrics answer to the same business word.")
for col, sv in zip(st.columns(len(SVS)), SVS):
    with col.container(border=True, height="stretch"):
        st.markdown(f"`{sv['name']}`")
        st.caption(sv["team"])
        st.markdown(f"**Tables:** {sv['tables']}")
        st.markdown("\n".join(f"- `{m}`" for m in sv["metrics"]))
st.subheader("Where the views disagree (each answer is defensible)")
st.table(pd.DataFrame(CONFLICTS, columns=["Question", "Semantic views say", "Business Ontology governs"]), hide_index=True)

st.divider()

# ------------------------------------------------------------------ Business Ontology
st.header("Business Ontology: what the numbers mean")
with st.container(horizontal=True):
    st.metric("Approved nodes", 40, border=True)
    st.metric("Typed relationships", 51, border=True)
    st.metric("Representations", 43, border=True)
    st.metric("Domains", 3, border=True, help="Procurement · Finance & Controlling · Sales & Distribution")
st.info("The BON agent has the *same* three enriched semantic views as the baseline, plus native `snowscope_search` "
        "over the `businessOntology` corpus. It looks up which metric is canonical, which policy applies, and how "
        "concepts connect across teams, then lets each semantic view compute its part.",
        icon=":material/hub:", title="Ontology governs, semantic views execute")

st.subheader("One definition, many implementations")
st.caption("Canonical metric → the semantic view metric that implements it, and its look-alike variant.")
cols = st.columns(2)
for i, c in enumerate(CANONICAL):
    with cols[i % 2].container(border=True):
        st.markdown(f"**{c['term']}** · `{c['value']}`")
        st.markdown(f"IMPLEMENTS: `{c['impl']}`  \nHAS_VARIANT: {c['variant']}")

left, mid, right = st.columns(3)
with left:
    st.subheader(f"Cross-domain metrics ({len(CROSS)})")
    for term, formula, source in CROSS:
        with st.container(border=True):
            st.markdown(f"**{term}**  \n`{formula}`")
            st.caption(source)
with mid:
    st.subheader(f"Policies ({len(POLICIES)})")
    for term, text in POLICIES:
        with st.container(border=True):
            st.markdown(f"**{term}**  \n{text}")
with right:
    st.subheader(f"Code-mapping terms ({len(CODE_TERMS)})")
    st.caption("One term per code field, not one per value.")
    st.dataframe(pd.DataFrame(CODE_TERMS, columns=["Code", "Term", "Column", "Code table"]), hide_index=True)

st.subheader("Ontology graph")
st.caption("Edges are Business Ontology relationship types. Blue nodes are metrics, amber nodes are policies.")
st.markdown(f"```mermaid\n{BON_GRAPH}\n```")

st.divider()

# ------------------------------------------------------------------ Source tables
tables = [t for _, group in TABLE_GROUPS for t in group]
st.header("SAP data (schema SAP)")
with st.container(horizontal=True):
    st.metric("Tables", len(tables), border=True)
    st.metric("Rows", sum(t[1] for t in tables), border=True)
    st.metric("Domains", 3, border=True)
st.warning("Three SAP domains (MM, FI/CO, SD), each served by its own team's semantic view. The views are individually "
           "correct but disagree on shared words (supplier count, revenue, on-time delivery, unit cost), and "
           "cross-domain questions (margin, profit, revenue at risk) need meaning from more than one view. Code-table "
           "meanings live in reference data (T077K, T023T), not in column names.",
           icon=":material/warning:", title="Key challenge")
st.dataframe(
    pd.DataFrame([(group, *t) for group, rows in TABLE_GROUPS for t in rows],
                 columns=["Group", "Table", "Rows", "Description"]),
    hide_index=True)
