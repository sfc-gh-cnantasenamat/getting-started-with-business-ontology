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

"""Static demo content: benchmark questions, tiers, and the Context page data."""

# Benchmark questions (mirror SAP.BENCHMARK_QUESTIONS / BENCHMARK_GROUND_TRUTH).
EVAL_QUESTIONS = [
    {"id": "Q01", "tier": "1", "q": "What is our cost of goods sold for raw materials?",
     "expected": "$1,290,020: invoices minus credit memos on GL 0040100000.",
     "trap": "$1,417,360 if credit memos are added instead of subtracted.", "governed": "COGS Raw Materials"},
    {"id": "Q02", "tier": "1", "q": "What is the total cost allocated to US manufacturing?",
     "expected": "$419,750: cost object KS-MFG-US.", "trap": "Other cost objects included.", "governed": "Cost Center Total"},
    {"id": "Q03", "tier": "1", "q": "How much revenue are we losing to customer discounts?",
     "expected": "$34,085: condition type K007 only.", "trap": "$36,687.50 if freight surcharges (KF00) are counted.",
     "governed": "Customer Discounts"},
    {"id": "Q04", "tier": "1", "q": "How much have we spent on electronics materials?",
     "expected": "$505,400: material group 043.", "trap": "Wrong material group code.", "governed": "Procurement Spend"},
    {"id": "Q05", "tier": "1", "q": "What is our net freight cost of goods sold?",
     "expected": "$39,800: GL 0040200000, credit memos subtracted.", "trap": "Sign not applied to credit memos.",
     "governed": "COGS Freight"},

    {"id": "Q06", "tier": "2", "q": "How many suppliers do we have?",
     "expected": "14 active suppliers (ZSTR + ZSTD). Probationary ZPRB excluded by policy.",
     "trap": "15: Procurement's vendor_record_count, which also answers to \"supplier count\".", "governed": "Supplier Count"},
    {"id": "Q07", "tier": "2", "q": "What is our revenue?",
     "expected": "$711,915: net of K007 customer discounts (net_revenue).",
     "trap": "$746,000: Sales' gross_bookings, which carries the synonym \"revenue\".", "governed": "Revenue"},
    {"id": "Q08", "tier": "2", "q": "What is our on-time delivery rate?",
     "expected": "66.7%: delivered shipments with goods issue on or before the planned date.",
     "trap": "90%: carrier self-reported OTRAT (carrier_otd_rate).", "governed": "On-Time Delivery Rate"},
    {"id": "Q09", "tier": "2", "q": "What does it cost us to make one Integrated System Module (ASSY-004)?",
     "expected": "$286.60: BOM cost rollup over every purchased component.",
     "trap": "$520: the assembly's standard price STPRS (planning price, not cost).", "governed": "BOM Cost Rollup"},
    {"id": "Q19", "tier": "2", "q": "How much have we spent with our Tier A suppliers?",
     "expected": "$251,690: \"Tier A\" is company vocabulary for strategic partners (account group ZSTR).",
     "trap": "$1,331,190 (all active suppliers) or $1,353,690 (all suppliers): no semantic view knows the term.",
     "governed": "Tier A Supplier"},

    {"id": "Q10", "tier": "3", "q": "What is the gross margin on the Integrated System Module (ASSY-004)?",
     "expected": "$277,355: Revenue (net) minus BOM cost x units.",
     "trap": "$296,855 (gross bookings) or $221,000 (standard price as cost).", "governed": "Product Gross Margin"},
    {"id": "Q11", "tier": "3", "q": "If supplier V10089 (Advanced Silicon Solutions) has a force majeure, how much revenue is at risk?",
     "expected": "$597,450: net revenue of ASSY-003 (direct) and ASSY-004 (contains ASSY-003, BOM level 2).",
     "trap": "$226,950 (direct BOM only, misses ASSY-004) or $623,750 (gross bookings).", "governed": "Revenue at Risk"},
    {"id": "Q12", "tier": "3", "q": "What is our total revenue divided by our number of suppliers?",
     "expected": "$50,851: governed Revenue ($711,915, Sales) / governed Supplier Count (14, Finance).",
     "trap": "$49,733 (746,000/15), $47,461 (711,915/15) or $53,286 (746,000/14): one or both definitions wrong.",
     "governed": "Revenue + Supplier Count"},
    {"id": "Q13", "tier": "3", "q": "We need to cut procurement spend by 15%. Which materials should we cut without disrupting production of anything we sell?",
     "expected": "Only non-BOM materials, totalling at least $203,054 (15% of $1,353,690).",
     "trap": "Cutting any BOM input (MAT-001/003/004/007/008/013/015/016/018).", "governed": "BOM Input Protection"},
    {"id": "Q14", "tier": "3", "q": "Which customer contributes the most profit after material costs?",
     "expected": "C-1001 at about $223,498.", "trap": "C-1001 at $237,948 (gross bookings) or $177,600 (standard price).",
     "governed": "Customer Profit"},

    {"id": "Q15", "tier": "4", "q": "What counts as an active supplier, and why are some vendors excluded?",
     "expected": "Active = account group ZSTR or ZSTD; probationary ZPRB excluded by procurement policy.",
     "trap": "A vague answer without the probationary rule.", "governed": "Probationary Vendor Exclusion"},
    {"id": "Q16", "tier": "4", "q": "Should we report gross bookings or net revenue as our revenue, and why?",
     "expected": "Net revenue ($711,915, net of K007 discounts); gross bookings is a Sales pipeline and quota measure.",
     "trap": "Recommends gross bookings, or says either is fine.", "governed": "Revenue"},
    {"id": "Q17", "tier": "4", "q": "Why are credit memos subtracted when calculating COGS?",
     "expected": "Credit memos (BSCHL 34) reverse vendor invoices (BSCHL 31), so they reduce cost.",
     "trap": "No reason given.", "governed": "Credit Memo Sign Rule"},
    {"id": "Q18", "tier": "4", "q": "What is the difference between gross bookings and revenue?",
     "expected": "Gross bookings = order value before discounts (Sales pipeline); revenue = net of K007 discounts (canonical).",
     "trap": "Treats them as the same.", "governed": "Revenue"},
    {"id": "Q20", "tier": "4", "q": "What is our Supplier Resilience Score?",
     "expected": "No governed definition exists, so the agent should say so (it may point to related governed metrics).",
     "trap": "Invents a formula, or passes off another project's risk or quality score as this one.",
     "governed": "(none: guardrail)"},
]
QUESTIONS_BY_ID = {q["id"]: q for q in EVAL_QUESTIONS}

# Questions shown in the demo. Tier 1: three controls (both agents correct).
# Tiers 2-4: only questions where BON was right and the SV-only agent was not, in run 20261023_072322_9764.
DEMO_QIDS = ["Q01", "Q03", "Q04", "Q06", "Q07", "Q19", "Q12", "Q17", "Q18"]
DEMO_QUESTIONS = [QUESTIONS_BY_ID[i] for i in DEMO_QIDS]
DEFAULT_QID = "Q06"

TIER_LABELS = {
    "1": "Tier 1: Business rules in one SV (control: enriched SVs already handle these)",
    "2": "Tier 2: Conflicting definitions & company vocabulary (which metric is official? what does our jargon mean?)",
    "3": "Tier 3: Cross-domain reasoning (Sales + Finance + Procurement)",
    "4": "Tier 4: Governed meaning (definitions, policies, and knowing what is not defined)",
}
TIER_PILLARS = {"1": "Baseline fairness", "2": "Canonical choice", "3": "Cross-domain meaning", "4": "Governed meaning"}

# ------------------------------------------------------------------ Context page
# "Without BON" values are what the named SV metric returns; "With BON" values are the governed answers
# (both verified against SAP.BENCHMARK_GROUND_TRUTH).
GAPS = [
    {"gap": "1. Two teams, two correct metrics, one business word (and company jargon)",
     "why": "Each team's semantic view is right for that team. Nothing in a semantic view says which one is the company's official answer.",
     "examples": [
         ("How many suppliers do we have?", "15 (Procurement SV: vendor_record_count) or 14 (Finance SV)",
          "14: Supplier Count, probationary vendors excluded by policy"),
         ("What is our revenue?", "$746,000: gross_bookings, which carries the synonym \"revenue\"",
          "$711,915: Revenue = net of customer discounts (net_revenue)"),
         ("What is our on-time delivery rate?", "90%: carrier self-reported rate",
          "66.7%: On-Time Delivery Rate, measured from actual delivery dates"),
         ("How much have we spent with our Tier A suppliers?",
          "No semantic view knows \"Tier A\": the agent has to ask or guess which vendor group is meant",
          "$251,690: Tier A = strategic partners (account group ZSTR)"),
     ]},
    {"gap": "2. Questions that cross team boundaries",
     "why": "No single semantic view holds both revenue and cost to build. The agent must know which metric from each view to combine, and how.",
     "examples": [
         ("Gross margin on ASSY-004?", "$296,855 (gross bookings) or $221,000 (standard price as cost)",
          "$277,355: Revenue − BOM Cost Rollup × units"),
         ("Which customer contributes the most profit after material costs?",
          "C-1001 at $237,948 (gross bookings) or $177,600 (standard price as cost)",
          "C-1001 at $223,498: Revenue − BOM Cost Rollup × units"),
     ]},
    {"gap": "3. Policies and meaning, not just numbers",
     "why": "A semantic view can encode a filter, but not the governed reason for it, who owns it, or where else it applies.",
     "examples": [
         ("Cut spend 15% without disrupting anything we sell?", "Nothing marks production inputs (BOM materials) as off-limits",
          "Only non-BOM materials, per BOM Input Protection policy"),
         ("Should we report gross bookings or net revenue?", "Both metrics are documented, but neither is marked official",
          "Net revenue ($711,915); gross bookings is a Sales pipeline measure"),
     ]},
]

SV_ALREADY = ["COGS with credit memos subtracted", "Discounts that exclude freight surcharges",
              "Spend by material group code", "Cost allocated to a cost center"]

BENEFITS = [
    ("Change once", "A steward edits a definition; every BON-enabled agent follows, with no edits to SVs or prompts."),
    ("Same answer across teams", "Finance's and Sales' agents answer the same question the same way."),
    ("Only approved meaning is served", "Draft definitions stay invisible to agents until reviewed."),
]

SVS = [
    {"name": "PROCUREMENT_ENRICHED_SV", "team": "Procurement team",
     "tables": "vendors, materials, purchase orders, shipments, carriers, inspections, bom (flattened)",
     "metrics": ["vendor_record_count (\"supplier count\") = 15", "carrier_otd_rate (\"on-time delivery\") = 90%",
                 "operational_otd_rate = 66.7%", "bom_material_cost (ASSY-004) = 286.60",
                 "avg_standard_price (\"unit cost\")", "procurement_spend"]},
    {"name": "FINANCE_ENRICHED_SV", "team": "Finance team",
     "tables": "ap_lines (BSEG), cost_postings (COEP), vendors, account groups",
     "metrics": ["active_supplier_count (\"supplier count\") = 14", "cogs_raw_materials (signed)",
                 "cogs_freight (signed)", "total_posted_cost"]},
    {"name": "SALES_ENRICHED_SV", "team": "Sales team",
     "tables": "sales_items (VBAP), pricing (KONV), products, customers",
     "metrics": ["gross_bookings (\"revenue\") = 746,000", "net_revenue = 711,915",
                 "customer_discounts (K007)", "list_price (PR00)", "units_sold"]},
]

CONFLICTS = [
    ("How many suppliers?", "Procurement 15 vs Finance 14", "Supplier Count = 14"),
    ("What is our revenue?", "gross_bookings 746,000 vs net_revenue 711,915", "Revenue = 711,915"),
    ("On-time delivery rate?", "carrier_otd_rate 90% vs operational_otd_rate 66.7%", "On-Time Delivery Rate = 66.7%"),
    ("Cost to make ASSY-004?", "avg_standard_price 520 vs bom_material_cost 286.60", "BOM Cost Rollup = 286.60"),
]

# Typed relationships from SAP (07_ontology.sql). Edge labels are BON relationship types.
BON_GRAPH = """graph LR
    subgraph proc [Procurement]
        Supplier
        Material
        Assembly
        BOM[Bill of Materials]
        PO[Purchase Order]
        SC[Supplier Count]:::metric
        VRC[Vendor Record Count]:::metric
        TIA[Tier A Supplier]
        BCR[BOM Cost Rollup]:::metric
        PVE[Probationary Vendor Exclusion]:::policy
        BIP[BOM Input Protection]:::policy
        PS[Procurement Spend]:::metric
    end
    subgraph fin [Finance and Controlling]
        AP[AP Line Item]
        PGM[Product Gross Margin]:::metric
        CP[Customer Profit]:::metric
        BED[Break-even Discount]:::metric
        CMR[Credit Memo Sign Rule]:::policy
        COGS[COGS Raw Materials]:::metric
    end
    subgraph sales [Sales and Distribution]
        SO[Sales Order]
        Customer
        REV[Revenue]:::metric
        GB[Gross Bookings]:::metric
        CD[Customer Discounts]:::metric
        RAR[Revenue at Risk]:::metric
    end
    Assembly -->|HAS_PART| BOM
    BOM -->|HAS_PART| Material
    PO -->|DERIVES| AP
    SO -->|RELATED_TO| Assembly
    SC -->|HAS_VARIANT| VRC
    SC -->|MEASURES| Supplier
    TIA -->|IS_A| Supplier
    PVE -->|APPLIES_TO| SC
    REV -->|HAS_VARIANT| GB
    CD -->|DERIVES| REV
    BOM -->|DERIVES| BCR
    REV -->|DERIVES| PGM
    BCR -->|DERIVES| PGM
    REV -->|DERIVES| CP
    BCR -->|DERIVES| CP
    CP -->|MEASURES| Customer
    BCR -->|DERIVES| BED
    REV -->|DERIVES| RAR
    BOM -->|DERIVES| RAR
    RAR -->|MEASURES| Supplier
    CMR -->|APPLIES_TO| COGS
    BIP -->|APPLIES_TO| PS
    classDef metric fill:#e0f2fe,stroke:#0284c7
    classDef policy fill:#fef3c7,stroke:#d97706"""

CANONICAL = [
    {"term": "Supplier Count", "impl": "FINANCE_ENRICHED_SV · vendors.active_supplier_count",
     "variant": "Vendor Record Count (scope: Procurement operations)", "value": "14"},
    {"term": "Revenue", "impl": "SALES_ENRICHED_SV · net_revenue (derived)",
     "variant": "Gross Bookings (scope: Sales pipeline)", "value": "711,915"},
    {"term": "On-Time Delivery Rate", "impl": "PROCUREMENT_ENRICHED_SV · shipments.operational_otd_rate",
     "variant": "Carrier Reported On-Time Rate (scope: Carrier scorecard)", "value": "66.7%"},
    {"term": "BOM Cost Rollup", "impl": "PROCUREMENT_ENRICHED_SV · bom.bom_material_cost",
     "variant": "not the assembly standard price STPRS", "value": "286.60 (ASSY-004)"},
]

CROSS = [
    ("Product Gross Margin", "Revenue − BOM Cost Rollup × units", "Sales + Procurement"),
    ("Customer Profit", "Σ (Revenue − BOM Cost Rollup × units) per customer", "Sales + Procurement"),
    ("Break-even Discount", "1 − BOM Cost Rollup / list price", "Sales + Procurement"),
    ("Revenue at Risk", "Revenue of assemblies whose BOM contains the supplier's materials", "Procurement → Sales"),
]

POLICIES = [
    ("Probationary Vendor Exclusion", "ZPRB vendors are not active suppliers."),
    ("Credit Memo Sign Rule", "BSCHL 34 credit memos are subtracted from every cost total."),
    ("BOM Input Protection", "Never cut a material that is in the BOM of anything we sell."),
]

CODE_TERMS = [
    ("KTOKK", "Vendor Account Group", "LFA1.KTOKK", "T077K"),  # also defines company term "Tier A Supplier" = ZSTR
    ("MATKL", "Material Group", "MARA.MATKL", "T023T"),
    ("BSCHL", "Posting Key", "BSEG.BSCHL", ""),
    ("HKONT", "GL Account", "BSEG.HKONT", ""),
    ("OBJNR", "Cost Object", "COEP.OBJNR", ""),
    ("KSCHL", "Condition Type", "KONV.KSCHL", ""),
    ("VKORG", "Sales Organization", "VBAP.VKORG", ""),
]

TABLE_GROUPS = [
    ("Master data", [("LFA1", 15, "Vendor master: LIFNR, KTOKK (ZSTR/ZSTD/ZPRB), KRAUS (DUNS)"),
                     ("MARA", 24, "Material master: MATNR, MATKL (043=Electronics...), STPRS"),
                     ("LFA2", 6, "Forwarding agents (carriers): VSART, LZEIT, OTRAT")]),
    ("Transactions", [("EKPO", 25, "PO items: NETWR (net value), BEDAT, STATU (O/C/R)"),
                      ("LIKP", 20, "Shipments: LFDAT vs WADAT (expected vs actual), FRTCO"),
                      ("LFB1", 15, "Vendor contracts: VTART (M/F/S), JWERT (annual value)"),
                      ("QALS", 10, "Inspection lots: QAESSION (defect rate), VCODE (A/R/C)")]),
    ("Structure", [("STPO", 15, "BOM items: STLNR/IDNRK (parent/child), 4-level hierarchy"),
                   ("T001W", 5, "Plants: manufacturing/distribution sites"),
                   ("T320", 8, "Storage locations (warehouses): LKAPA utilization"),
                   ("QUAL_MATRIX", 28, "Vendor-material qualifications: CERT_TYPE, STATUS, EXPIRY_DATE")]),
    ("Finance (FI/CO)", [("BSEG", 38, "AP line items: HKONT (GL acct), BSCHL (31=invoice, 34=credit memo)"),
                         ("COEP", 19, "Cost postings: OBJNR (cost object), KSTAR (cost element)")]),
    ("Sales (SD)", [("VBAP", 13, "Sales order items: finished assemblies sold to customers"),
                    ("KONV", 25, "Pricing conditions: KSCHL (PR00/K007/KF00)")]),
    ("Reference data", [("T077K", 3, "Vendor account groups: EXCLUDE_FROM_ACTIVE_COUNT flag (ZPRB)"),
                        ("T023T", 6, "Material group texts: 043 Electronics ... 048 Assembly")]),
]
