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

"""Business Ontology demo: semantic views alone vs. semantic views + Business Ontology."""

import streamlit as st

st.set_page_config(page_title="Business Ontology demo", page_icon=":material/hub:", layout="wide")

page = st.navigation(
    [
        st.Page("app_pages/context.py", title="Context", icon=":material/menu_book:"),
        st.Page("app_pages/comparison.py", title="Comparison", icon=":material/compare_arrows:"),
        st.Page("app_pages/analysis.py", title="Analysis", icon=":material/bar_chart:"),
    ],
    position="top",
)

st.title("Business Ontology demo")
st.caption("Same model, same semantic views, same instructions. The only difference is whether the agent can consult the Business Ontology.")

page.run()
