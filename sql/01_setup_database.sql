-- Copyright 2026 Snowflake Inc.
-- SPDX-License-Identifier: Apache-2.0
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.

-- Setup: Create database, schema, and warehouse
CREATE DATABASE IF NOT EXISTS DB_ONTOLOGY_CONTROL_PLANE;
CREATE SCHEMA IF NOT EXISTS DB_ONTOLOGY_CONTROL_PLANE.SAP_PRODUCTION;
CREATE WAREHOUSE IF NOT EXISTS ONTOLOGY_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

USE DATABASE DB_ONTOLOGY_CONTROL_PLANE;
USE SCHEMA SAP_PRODUCTION;
USE WAREHOUSE ONTOLOGY_WH;
