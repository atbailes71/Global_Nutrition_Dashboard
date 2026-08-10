# Indicator Reference Guide
## Global Nutrition Monitoring Framework Dashboard

This document provides definitions, calculation methods, data sources, and
notes for all indicators used in this project, organized by the UNICEF
Conceptual Framework layer.

---

## LAYER 1: NUTRITION OUTCOMES (WHA 6 Targets)

| Code | Indicator | Definition | Cut-off | Data Source | SDG |
|---|---|---|---|---|---|
| NT_ANT_HAZ_NE2_MOD | Stunting | HAZ <-2SD, modelled estimate | <-2 SD WHO CGS | UNICEF/WHO/WB JME | 2.2.1 |
| NT_ANT_WHZ_NE2_MOD | Wasting | WHZ <-2SD OR bilateral oedema, modelled | <-2 SD WHO CGS | UNICEF/WHO/WB JME | 2.2.2 |
| NT_ANT_WHZ_PO2_MOD | Overweight | WHZ >+2SD, modelled | >+2 SD WHO CGS | UNICEF/WHO/WB JME | 2.2.2 |
| NT_ANE_WOM_15_49_MOD | Anaemia WRA | Hb <120 g/L (non-pregnant), <110 g/L (pregnant), women 15-49 | WHO thresholds | WHO Global Anaemia Estimates | 2.2.3 |
| NT_BF_EXBF | Exclusive BF | % infants 0-5m fed only breast milk previous day | Current status | UNICEF IYCF Database | — |
| NT_BW_LBW | Low Birth Weight | % livebirths <2500g | <2500g | UNICEF/WHO LBW Estimates | — |

**2030 Targets:** Stunting ≤10%; Wasting <3%; Overweight no increase; Anaemia 50% reduction; EBF ≥60%; LBW 30% reduction.

---

## LAYER 2: IMMEDIATE DETERMINANTS

### 2A. Diets and Care — IYCF Indicators
*(All definitions per WHO/UNICEF Indicators for Assessing IYCF Practices, 2021)*

| Code | Indicator | Numerator | Denominator | Age Group |
|---|---|---|---|---|
| NT_BF_EIBF | Early Initiation of BF | Children put to breast within 1 hour of birth | Children born last 24 months | 0-23 months |
| NT_BF_EXBF | Exclusive BF | Fed only breast milk previous day | Living infants 0-5 months | 0-5 months |
| NT_CF_MDD | Min. Dietary Diversity | Consumed ≥5 of 8 food groups previous day | Living children 6-23 months | 6-23 months |
| NT_CF_MMF | Min. Meal Frequency | Met age-specific minimum feeding frequency | Living children 6-23 months | 6-23 months |
| NT_CF_MAD | Min. Acceptable Diet | Met MDD AND MMF (AND MMFF if non-BF) | Living children 6-23 months | 6-23 months |
| NT_BF_CBF12_23 | Continued BF | Breastfed previous day | Living children 12-23 months | 12-23 months |

**Note on MDD:** 2021 update raised cut-off from ≥4/7 food groups (2008) to ≥5/8 food groups. MDD-C (≥5/8 food groups) is now SDG indicator 2.2.4 (approved March 2025).

## LAYER 3: UNDERLYING DETERMINANTS

### 3A. Services — Health and Programme Coverage

| Code | Indicator | Definition | Source |
|---|---|---|---|
| MNCH_ANC4 | ANC 4+ Visits | % women with live birth who attended ≥4 ANC visits | DHS, MICS |
| MNCH_SAB | Skilled Birth Attendance | % livebirths attended by skilled health personnel | DHS, MICS |
| IM_DTP3 | DTP3 Coverage | % children receiving 3rd dose of DTP vaccine | WHO/UNICEF estimates |
| NT_SAM_TR | SAM Treatment | % SAM children admitted to therapeutic feeding / estimated caseload | NutriDash, programme data |
| NT_VAS_12_59 | Vitamin A Supplementation | % children 6-59m receiving ≥1 dose VAS in last 6 months | UNICEF NutriDash |

---

## LAYER 4: ENABLING ENVIRONMENT

See `outputs/tables/layer3_enabling_environment_toolkit.csv` for the full reference
table with definitions, recommended data sources, collection frequency, and current
availability by indicator.

**Summary of enabling environment indicators by dimension:**

- **Governance (5 indicators):** National nutrition policy, multisectoral coordination mechanism, dedicated nutrition budget, WHO Code compliance, mandatory fortification legislation
- **Resources (4 indicators):** Maternity leave duration, maternity benefit coverage, social protection cash transfer coverage, health worker density
- **Norms (3 indicators):** Women's empowerment index (WEAI), breastfeeding workplace support, Cost of Healthy Diet

**Primary data sources:**
- WHO GINA: https://extranet.who.int/nutrition/gina/
- WHO Global Breastfeeding Scorecard: https://www.who.int/publications/i/item/9789240018389
- SUN Movement reporting: https://scalingupnutrition.org/
- ILO ILOSTAT: https://ilostat.ilo.org/
- Food Fortification Initiative: https://www.ffinetwork.org/country-profiles
- World Bank ASPIRE: https://www.worldbank.org/en/data/datatopics/aspire

---

## Key Conceptual References

1. UNICEF Conceptual Framework on the Determinants of Maternal and Child Nutrition, 2020:
   https://www.unicef.org/media/113291/file/UNICEFConceptualFramework.pdf

2. WHO/UNICEF Global Nutrition Monitoring Framework Operational Guidance, 2017:
   https://www.who.int/publications/i/item/9789241513609

3. WHO/UNICEF IYCF Indicators: Definitions and Measurement Methods, 2021:
   https://www.who.int/publications/i/item/9789240018389

4. FAO State of Food Security and Nutrition in the World (SOFI), 2025:
   https://www.fao.org/publications/fao-flagship-publications/the-state-of-food-security-and-nutrition-in-the-world/en

5. IPC Technical Manual v3.1:
   https://www.ipcinfo.org/ipc-country-analysis/ipc-manual/en/
