/*
 * Copyright 2026 Snowflake Inc.
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import snowflake from "snowflake-sdk";

let connectionPromise: Promise<snowflake.Connection> | null = null;

async function createConnection(): Promise<snowflake.Connection> {
  const conn = snowflake.createConnection({
    account: process.env.SNOWFLAKE_ACCOUNT!,
    username: process.env.SNOWFLAKE_USER!,
    authenticator: "EXTERNALBROWSER",
    role: process.env.SNOWFLAKE_ROLE || "ACCOUNTADMIN",
    warehouse: process.env.SNOWFLAKE_WAREHOUSE || "COMPUTE_WH",
    database: process.env.SNOWFLAKE_DATABASE || "DB_ONTOLOGY_CONTROL_PLANE",
    schema: process.env.SNOWFLAKE_SCHEMA || "SAP_BON_V2",
  });

  await conn.connectAsync((err) => {
    if (err) throw err;
  });
  return conn;
}

export async function getConnection(): Promise<snowflake.Connection> {
  if (!connectionPromise) {
    connectionPromise = createConnection();
  }
  try {
    return await connectionPromise;
  } catch {
    connectionPromise = null;
    throw new Error("Failed to connect to Snowflake");
  }
}

export async function executeQuery(sql: string): Promise<any[]> {
  const conn = await getConnection();
  return new Promise((resolve, reject) => {
    conn.execute({
      sqlText: sql,
      complete: (err, _stmt, rows) => {
        if (err) reject(err);
        else resolve(rows || []);
      },
    });
  });
}
