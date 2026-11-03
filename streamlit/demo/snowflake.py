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

"""Snowflake access: connection, agent calls and benchmark results."""

import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import streamlit as st

DATABASE = os.environ.get("SNOWFLAKE_DATABASE", "BUSINESS_ONTOLOGY")
SCHEMA_NAME = os.environ.get("SNOWFLAKE_SCHEMA", "SAP")
SCHEMA = f"{DATABASE}.{SCHEMA_NAME}"
# Left panel: the same enriched SVs without BON, so the only difference between panels is the BON tool.
BASELINE_AGENT = f"{SCHEMA}.ENRICHED_AGENT"
BON_AGENT = f"{SCHEMA}.BON_AGENT"


def connection():
    # In Snowflake the app uses its own session. Locally, set SNOWFLAKE_CONNECTION_NAME to a connection
    # in ~/.snowflake/connections.toml, or define [connections.snowflake] in .streamlit/secrets.toml.
    return st.connection(os.environ.get("SNOWFLAKE_CONNECTION_NAME", "snowflake"), type="snowflake")


def sql_literal(value):
    """Quote a value as a SQL string literal."""
    return "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"


def parse_agent_response(raw):
    """Pull the answer text, the tools called, and any HTML artifacts out of a DATA_AGENT_RUN reply."""
    text_parts, tools, html = [], [], []
    try:
        resp = json.loads(raw) if isinstance(raw, str) else raw
    except (json.JSONDecodeError, TypeError):
        resp = {}
    for item in (resp or {}).get("content", []):
        if not isinstance(item, dict):
            continue
        kind = item.get("type")
        if kind == "tool_use":
            name = item.get("tool_use", {}).get("name")
            if name:
                tools.append(name)
        elif kind == "text" and item.get("text", "").strip():
            text_parts.append(item["text"].strip())
        elif kind == "tool_result":
            for tc in item.get("tool_result", {}).get("content", []):
                result = tc.get("json", {}).get("result", "") if isinstance(tc, dict) and tc.get("type") == "json" else ""
                if isinstance(result, str) and "<!DOCTYPE html>" in result:
                    html.append(result)
    return {"text": "\n\n".join(text_parts), "tools": tools, "html": html}


def _call_agent(raw_conn, agent_fqn, question):
    request = json.dumps({"messages": [{"role": "user", "content": [{"type": "text", "text": question}]}]})
    start = time.time()
    cur = raw_conn.cursor()
    try:
        # DATA_AGENT_RUN needs constant arguments, so pass them as escaped literals rather than bind variables.
        cur.execute(f"SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN({sql_literal(agent_fqn)}, {sql_literal(request)})")
        row = cur.fetchone()
        parsed = parse_agent_response(row[0] if row else "")
    except Exception as e:  # show the error in the panel rather than failing the page
        parsed = {"text": f"Error: {e}", "tools": [], "html": []}
    finally:
        cur.close()
    parsed["elapsed"] = round(time.time() - start, 1)
    return parsed


def ask_both_agents(question):
    """Ask the baseline and BON agents the same question in parallel."""
    raw_conn = connection().raw_connection
    with ThreadPoolExecutor(max_workers=2) as pool:
        baseline = pool.submit(_call_agent, raw_conn, BASELINE_AGENT, question)
        bon = pool.submit(_call_agent, raw_conn, BON_AGENT, question)
        return baseline.result(), bon.result()


@st.cache_data(ttl=600, show_spinner="Loading benchmark results...")
def load_results():
    """Latest full benchmark run: per-question accuracy per arm, plus team consistency."""
    conn = connection()
    exists = conn.query(
        "SELECT COUNT(*) FROM IDENTIFIER(?) WHERE TABLE_SCHEMA = ? AND TABLE_NAME = 'BENCHMARK_RESULTS'",
        params=[f"{DATABASE}.INFORMATION_SCHEMA.TABLES", SCHEMA_NAME], ttl=0,
    )
    if not exists.iloc[0, 0]:
        return None, pd.DataFrame(), pd.DataFrame()
    run = conn.query(
        f"""SELECT RUN_ID FROM {SCHEMA}.BENCHMARK_RESULTS WHERE EXPERIMENT = 'main'
            GROUP BY RUN_ID HAVING COUNT(*) >= 100 ORDER BY MAX(RUN_TS) DESC LIMIT 1""",
        ttl=0,
    )
    if run.empty:
        return None, pd.DataFrame(), pd.DataFrame()
    run_id = run.iloc[0, 0]
    per_q = conn.query(
        f"""SELECT QID, ARM, COUNT(*) N, SUM(IFF(CORRECT,1,0)) OK, SUM(IFF(HEDGED,1,0)) HEDGED,
                   ROUND(MEDIAN(LATENCY_S),1) P50
            FROM {SCHEMA}.BENCHMARK_RESULTS WHERE RUN_ID = ? AND EXPERIMENT = 'main'
            GROUP BY 1,2 ORDER BY 1,2""",
        params=[run_id], ttl=0,
    )
    consistency = conn.query(
        f"""WITH p AS (SELECT ARM, QID, RUN_NO, AGENT, HEADLINE_VALUE, CORRECT FROM {SCHEMA}.BENCHMARK_RESULTS
                       WHERE RUN_ID = ? AND EXPERIMENT = 'consistency')
            SELECT f.ARM, f.QID,
                   ROUND(100*AVG(IFF(ROUND(f.HEADLINE_VALUE,1) = ROUND(s.HEADLINE_VALUE,1),1,0)),0) AGREE,
                   ROUND(100*AVG(IFF(f.CORRECT AND s.CORRECT,1,0)),0) BOTH_RIGHT
            FROM p f JOIN p s ON f.ARM = s.ARM AND f.QID = s.QID AND f.RUN_NO = s.RUN_NO
                 AND f.AGENT LIKE 'FINANCE%' AND s.AGENT LIKE 'SALES%'
            GROUP BY 1,2 ORDER BY 1,2""",
        params=[run_id], ttl=0,
    )
    return run_id, per_q, consistency
