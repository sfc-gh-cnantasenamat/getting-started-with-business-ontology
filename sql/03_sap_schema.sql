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

-- =====================================================================
-- Business Ontology demo, 03: SAP schema, cloned data, reference (code) tables
-- Built objects live in SAP; the source tables stay untouched in RAW.
-- =====================================================================
USE DATABASE BUSINESS_ONTOLOGY;

CREATE SCHEMA IF NOT EXISTS BUSINESS_ONTOLOGY.SAP
  COMMENT = 'Business Ontology demo: domain SVs (bare/enriched), governed BON, fair 3-agent benchmark';
USE SCHEMA BUSINESS_ONTOLOGY.SAP;

-- Zero-copy clone of the SAP source tables from RAW.
-- PREREQUISITE: run 01_setup.sql and 02_raw_data.sql first;
-- they create RAW and load the synthetic SAP data this script clones.
EXECUTE IMMEDIATE $$
DECLARE
  missing_source EXCEPTION (-20001, 'RAW.LFA1 not found. Run sql/01_setup.sql and sql/02_raw_data.sql first.');
BEGIN
  IF (NOT EXISTS (SELECT 1 FROM BUSINESS_ONTOLOGY.INFORMATION_SCHEMA.TABLES
                  WHERE TABLE_SCHEMA = 'RAW' AND TABLE_NAME = 'LFA1')) THEN
    RAISE missing_source;
  END IF;
  RETURN 'RAW source tables found';
END;
$$;

EXECUTE IMMEDIATE $$
DECLARE
  t ARRAY DEFAULT ARRAY_CONSTRUCT('LFA1','LFA2','LFB1','MARA','EKPO','LIKP','T001W','T320',
                                  'STPO','QALS','BSEG','COEP','VBAP','KONV','QUAL_MATRIX');
  i INTEGER DEFAULT 0;
  n VARCHAR;
BEGIN
  FOR i IN 0 TO ARRAY_SIZE(t)-1 DO
    n := t[i];
    EXECUTE IMMEDIATE 'CREATE OR REPLACE TABLE BUSINESS_ONTOLOGY.SAP.' || n ||
                      ' CLONE BUSINESS_ONTOLOGY.RAW.' || n;
  END FOR;
  RETURN 'cloned ' || ARRAY_SIZE(t);
END;
$$;

-- Reference (code) tables: BON holds one term per code field that points here.
-- New codes arrive via normal ETL into these tables; BON only changes when a rule changes.
CREATE OR REPLACE TABLE T077K (
  KTOKK VARCHAR(10) PRIMARY KEY COMMENT 'Vendor account group code',
  TXT30 VARCHAR(60) COMMENT 'Account group description',
  EXCLUDE_FROM_ACTIVE_COUNT BOOLEAN COMMENT 'TRUE if vendors in this group are excluded from the active supplier count'
) COMMENT = 'Vendor account group reference (code table)' AS
SELECT * FROM VALUES ('ZSTR','Strategic partner',FALSE),('ZSTD','Standard vendor',FALSE),('ZPRB','Probationary vendor',TRUE);

CREATE OR REPLACE TABLE T023T (
  MATKL VARCHAR(5) PRIMARY KEY COMMENT 'Material group code',
  WGBEZ VARCHAR(60) COMMENT 'Material group description'
) COMMENT = 'Material group texts (code table)' AS
SELECT * FROM VALUES ('043','Electronics'),('044','Chemicals'),('045','Metals'),('046','Packaging'),('047','Raw Materials'),('048','Assembly');
