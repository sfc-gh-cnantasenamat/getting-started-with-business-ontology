# Getting Started with Business Ontology

Companion code for the Snowflake guide [Getting Started with Business Ontology](https://github.com/sfc-gh-cnantasenamat/sfguide-getting-started-with-business-ontology). It builds a small SAP-style supply chain dataset, a Semantic View, two Cortex Agents, and a Business Ontology glossary.

> **Private Preview:** Business Ontology must be enabled on your Snowflake account before use. Contact your Snowflake account team.

## Attribution

The SQL scripts are the V1 demo by Tianxia Jia, from [sfc-gh-tjia/business_ontology](https://github.com/sfc-gh-tjia/business_ontology) (`Demo/sql/01` to `05`, commit `7b4c82a`), copied without changes. For the fuller V2 benchmark that compares Business Ontology against enriched Semantic Views, see that repository's `Demo/sql/v2/`.

## Contents

| Script | What it creates |
|---|---|
| `sql/01_setup_database.sql` | Database `DB_ONTOLOGY_CONTROL_PLANE`, schema `SAP_PRODUCTION`, warehouse `ONTOLOGY_WH` |
| `sql/02_create_sap_tables.sql` | 15 SAP tables with 266 rows of sample data |
| `sql/03_create_semantic_view.sql` | `SAP_BASELINE_SV`, covering 14 tables with 12 relationships |
| `sql/04_create_agents.sql` | `SAP_BASELINE_AGENT` (Semantic View only) and `BON_SV_NATIVE_AGENT` (Semantic View plus Business Ontology search) |
| `sql/05_create_bon_glossary.sql` | SQL alternative to the guide's skill prompts: 3 domains, 29 terms, 8 relationships |

## Usage

Run the scripts in order in a Snowsight SQL worksheet, then follow the guide. Script 05 is optional if you build the ontology with the `$business-ontology` skill as the guide describes.

Ontology changes can take several hours to become searchable by agents.

## Clean up

Delete the ontology domains first (see the guide's Clean Up section), then:

```sql
DROP DATABASE IF EXISTS DB_ONTOLOGY_CONTROL_PLANE;
DROP WAREHOUSE IF EXISTS ONTOLOGY_WH;
```
