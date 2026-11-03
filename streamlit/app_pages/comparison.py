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

import streamlit as st

from demo.content import DEFAULT_QID, DEMO_QUESTIONS, TIER_LABELS
from demo.snowflake import BASELINE_AGENT, BON_AGENT, ask_both_agents

if "comparison" not in st.session_state:
    st.session_state.comparison = None  # {"question", "meta", "baseline", "bon"}

st.header("Ask both agents")
st.write(f"The left panel is `{BASELINE_AGENT.split('.')[-1]}` (enriched semantic views only). The right panel is "
         f"`{BON_AGENT.split('.')[-1]}`: the same semantic views plus Business Ontology search.")

labels = {q["id"]: f"{q['id']}: {q['q']}" for q in DEMO_QUESTIONS}
with st.form("curated"):
    qid = st.selectbox("Select a question", list(labels), index=list(labels).index(DEFAULT_QID),
                       format_func=lambda i: labels[i])
    picked = st.form_submit_button("Ask both agents", icon=":material/send:", type="primary")
custom = st.chat_input("Or type a custom question")

question, meta = None, None
if picked:
    meta = next(q for q in DEMO_QUESTIONS if q["id"] == qid)
    question = meta["q"]
elif custom:
    question = custom

if question:
    with st.spinner("Running both agents in parallel..."):
        baseline, bon = ask_both_agents(question)
    st.session_state.comparison = {"question": question, "meta": meta, "baseline": baseline, "bon": bon}

result = st.session_state.comparison
if result:
    meta = result["meta"]
    st.caption(f"{meta['id']} · {TIER_LABELS[meta['tier']]}" if meta else "Custom question")
    st.subheader(result["question"])

    for col, label, resp in zip(st.columns(2),
                                ["Enriched SVs only (no Business Ontology)", "Same enriched SVs + Business Ontology"],
                                [result["baseline"], result["bon"]]):
        with col.container(border=True, height="stretch"):
            st.markdown(f"**{label}**")
            with st.container(horizontal=True):
                st.badge(f"{resp['elapsed']}s", icon=":material/timer:", color="gray")
                for i, tool in enumerate(resp["tools"], 1):
                    st.badge(f"{i}. {tool}", color="blue" if tool == "business_ontology" else "gray")
            st.markdown(resp["text"] or "_No text response_")
            for html in resp["html"]:
                st.caption("Interactive graph (zoom, pan, drag)")
                st.iframe(html, height=450)

    if meta:
        st.success(f"{meta['expected']}\n\n**Plausible wrong answer:** {meta['trap']}\n\n**Governed by:** {meta['governed']}",
                   icon=":material/verified:", title="Expected answer")
