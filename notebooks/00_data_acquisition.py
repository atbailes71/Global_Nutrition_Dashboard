# =============================================================================
# Notebook 00: Data Acquisition
# Global Nutrition Monitoring Framework — UNICEF Conceptual Framework Project
# Adam T. Bailes, MPH | August 2026
# =============================================================================
#
# PURPOSE
# -------
# This script pulls all data required for the three-layer analysis:
#   Layer 1 — Nutrition Outcomes (WHA 6 Targets)
#   Layer 2 — Immediate Determinants (IYCF: diets and care)
#   Layer 3 — Underlying Determinants (food security, health services, WASH)
#   Layer 4 — Enabling Environment (Policy indicators — manual download required)
#
# HOW TO RUN
# ----------
# Run this script on your LOCAL MACHINE where outbound internet access is
# available. The unicefdata package accesses the UNICEF SDMX API. Manual
# download instructions are provided inline for WFP, JMP, and FAO data.
#
# REQUIREMENTS
# ------------
# pip install unicefdata pandas openpyxl requests
# =============================================================================

import pandas as pd
import os
import logging
import warnings

warnings.filterwarnings('ignore')
logging.disable(logging.WARNING)

# --- Setup ---
DATA_RAW = '../data/raw'
DATA_PROC = '../data/processed'
os.makedirs(DATA_RAW, exist_ok=True)
os.makedirs(DATA_PROC, exist_ok=True)

print("=" * 70)
print("GLOBAL NUTRITION MONITORING FRAMEWORK — DATA ACQUISITION")
print("=" * 70)

# =============================================================================
# SECTION 1: UNICEF SDMX API — Nutrition Outcomes and Programme Indicators
# =============================================================================
# The unicefdata package provides direct access to UNICEF's SDMX data warehouse.
# Reference: https://github.com/unicef-drp/unicefData
# Package documentation: https://pypi.org/project/unicefdata/
# =============================================================================

print("\n[1] Connecting to UNICEF SDMX API via unicefdata package...")
from unicefdata import unicefData, search_indicators, list_categories

# --- INDICATOR CODES REFERENCE ---
# All codes are from UNICEF SDMX NUTRITION dataflow.
# Use search_indicators(category='NUTRITION') to browse all 112 available.

INDICATORS = {

    # -------------------------------------------------------------------------
    # LAYER 1: NUTRITION OUTCOMES — WHA 6 TARGETS
    # -------------------------------------------------------------------------
    # These are the six WHO World Health Assembly global nutrition targets,
    # used in the GNMF as the primary outcome monitoring indicators.
    # Source: UNICEF-WHO-World Bank JME (stunting, wasting, overweight)
    #         WHO Global Anaemia Estimates (anaemia)
    #         UNICEF IYCF Database (exclusive breastfeeding)
    #         UNICEF-WHO LBW estimates (low birth weight)
    # -------------------------------------------------------------------------

    'NT_ANT_HAZ_NE2_MOD':   'Stunting (<-2SD HAZ), modelled estimate, %',
    'NT_ANT_WHZ_NE2_MOD':   'Wasting (<-2SD WHZ), modelled estimate, %',
    'NT_ANT_WHZ_PO2_MOD':   'Overweight (>+2SD WHZ), modelled estimate, %',
    'NT_ANE_WOM_15_49_MOD': 'Anaemia in women 15-49 years, %',
    'NT_BF_EXBF':           'Exclusive breastfeeding <6 months, %',
    'NT_BW_LBW':            'Low birth weight (<2500g), %',

    # -------------------------------------------------------------------------
    # LAYER 2A: UNDERLYING DETERMINANTS — IYCF INDICATORS
    # -------------------------------------------------------------------------
    # Core IYCF indicators from UNICEF IYCF Database (DHS, MICS, national surveys).
    # Definitions per WHO/UNICEF 2021 IYCF Indicators guidance.
    # -------------------------------------------------------------------------

    'NT_BF_EIBF':           'Early initiation of breastfeeding within 1 hour, %',
    'NT_CF_MAD':            'Minimum acceptable diet (6-23 months), %',
    'NT_CF_MDD':            'Minimum dietary diversity >=5/8 food groups (6-23 months), %',
    'NT_CF_MMF':            'Minimum meal frequency (6-23 months), %',
    'NT_BF_CBF12_23':       'Continued breastfeeding at 12-23 months, %',

    # -------------------------------------------------------------------------
    # LAYER 2B: UNDERLYING DETERMINANTS — HEALTH SERVICES / CARE
    # -------------------------------------------------------------------------
    # ANC coverage and skilled birth attendance as health service delivery
    # indicators. These sit at the underlying determinants level in the
    # UNICEF Conceptual Framework (services dimension).
    # -------------------------------------------------------------------------

    'MNCH_ANC4':           'Layer 3: Underlying Determinants',
    'MNCH_SAB':             'Skilled birth attendance, %',
    'IM_DTP3':              'DTP3 immunisation coverage, % (proxy for health system reach)',

    # -------------------------------------------------------------------------
    # LAYER 2C: UNDERLYING DETERMINANTS — PROGRAMME COVERAGE
    # -------------------------------------------------------------------------
    # Programme coverage indicators from UNICEF NutriDash administrative data
    # and coverage surveys. These track delivery of nutrition interventions
    # through health and community platforms.
    # -------------------------------------------------------------------------

    'NT_SAM_TR':            'SAM treatment coverage (children admitted/estimated caseload), %',
    'NT_VAS_12_59':         'Vitamin A supplementation coverage 6-59 months, %',
}

# Pull all UNICEF SDMX indicators
print(f"\n  Pulling {len(INDICATORS)} indicators for all countries, 2000-2024...")
print("  This may take 2-3 minutes depending on connection speed.\n")

dfs = []
failed = []

for code, label in INDICATORS.items():
    print(f"  Fetching: {code} — {label[:55]}...")
    try:
        df = unicefData(
            indicator=code,
            year="2000:2024",
            add_metadata=["region", "income_group"],
            latest=False,
            dropna=True
        )
        if len(df) > 0:
            df['indicator_label'] = label
            LAYER1 = ['NT_ANT_HAZ_NE2_MOD','NT_ANT_WHZ_NE2_MOD',
                      'NT_ANT_WHZ_PO2_MOD','NT_ANE_WOM_15_49_MOD',
                      'NT_BF_EXBF','NT_BW_LBW']
            LAYER2 = ['NT_BF_EIBF','NT_BF_EXBF','NT_BF_CBF12_23',
                      'NT_CF_MAD','NT_CF_MDD','NT_CF_MMF']
            LAYER3 = ['MNCH_ANC4','MNCH_SAB','IM_DTP3',
                      'NT_SAM_TR','NT_VAS_12_59']
            if code in LAYER1:
                df['framework_layer'] = 'Layer 1: Nutrition Outcomes'
            elif code in LAYER2:
                df['framework_layer'] = 'Layer 2: Immediate Determinants'
            elif code in LAYER3:
                df['framework_layer'] = 'Layer 3: Underlying Determinants'
            else:
                df['framework_layer'] = 'Layer 3: Underlying Determinants'
            dfs.append(df)
            print(f"    OK — {len(df)} rows, {df['iso3'].nunique()} countries")
        else:
            print(f"    WARNING — empty response")
            failed.append(code)
    except Exception as e:
        print(f"    FAILED — {e}")
        failed.append(code)

# Combine all UNICEF SDMX data
if dfs:
    df_unicef = pd.concat(dfs, ignore_index=True)
    df_unicef.to_csv(f'{DATA_RAW}/unicef_sdmx_nutrition_raw.csv', index=False)
    print(f"\n  Saved: unicef_sdmx_nutrition_raw.csv")
    print(f"  Total rows: {len(df_unicef):,}")
    print(f"  Countries: {df_unicef['iso3'].nunique()}")
    print(f"  Indicators pulled: {df_unicef['indicator'].nunique()}")
    if failed:
        print(f"  Failed indicators: {failed}")
else:
    print("\n  ERROR: No data retrieved. Check internet connection.")


# =============================================================================
# SECTION 2: MANUAL DOWNLOADS REQUIRED
# =============================================================================
# The following data sources require manual download. Instructions below.
# After downloading, place files in data/raw/ as indicated.
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 2: MANUAL DOWNLOAD INSTRUCTIONS")
print("=" * 70)

print("""
The following datasets are publicly available but require manual download.
After downloading, save each file to data/raw/ with the filename shown.

------------------------------------------------------------------------
2A. FAO SOFI 2025 Data Annex — Food Security and Dietary Diversity
------------------------------------------------------------------------
  Provides: Prevalence of Undernourishment (PoU), food insecurity (FIES),
            MDD-C and MDD-W (new SDG 2.2.4 indicators, 2025 edition)
  URL:      https://www.fao.org/publications/fao-flagship-publications/
            the-state-of-food-security-and-nutrition-in-the-world/en
  Download: Click "Data Annex" or "Statistical Annex" Excel file
  Save as:  data/raw/fao_sofi_2025_annex.xlsx

------------------------------------------------------------------------
2B. WFP VAM Country Food Security Indicators
------------------------------------------------------------------------
  Provides: FCS (Food Consumption Score), rCSI, food insecurity prevalence
            from WFP-supported household surveys
  URL:      https://dataviz.vam.wfp.org/economic_explorer/food-security
  Download: Export → Download CSV from the country comparison tool
  Save as:  data/raw/wfp_vam_food_security.csv
  Note:     Select all available countries, most recent survey year

------------------------------------------------------------------------
2C. WHO/UNICEF JMP WASH Data
------------------------------------------------------------------------
  Provides: Safely managed drinking water and sanitation service coverage
            (SDG 6.1.1 and 6.2.1 indicators)
  URL:      https://washdata.org/data/downloads#table-data
  Download: Country files → "All countries" → Download estimates (Excel)
  Save as:  data/raw/jmp_wash_estimates.xlsx

------------------------------------------------------------------------
2D. WHO GINA Policy Indicators
------------------------------------------------------------------------
  Provides: Country-level nutrition policy existence, BFMS code compliance,
            breastfeeding legislation, food fortification mandates
  URL:      https://extranet.who.int/nutrition/gina/en/report
  Download: Generate → All countries → Download Excel
  Save as:  data/raw/who_gina_policies.xlsx

------------------------------------------------------------------------
2E. WHO Global Breastfeeding Scorecard
------------------------------------------------------------------------
  Provides: Country scores on breastfeeding policy environment:
            maternity leave, code compliance, health system support
  URL:      https://www.who.int/publications/i/item/9789240018389
  Download: See Annex or supplementary data table
  Save as:  data/raw/who_bf_scorecard.xlsx

------------------------------------------------------------------------
2F. ILO Social Protection Coverage
------------------------------------------------------------------------
  Provides: Coverage of social protection floors, maternity benefit coverage
  URL:      https://www.social-protection.org/gimi/gess/ShowTheme.action?th.themeId=10
  Download: Data → Download dataset (Excel)
  Save as:  data/raw/ilo_social_protection.xlsx
""")


# =============================================================================
# SECTION 3: LOAD AND VALIDATE MANUAL DOWNLOADS
# =============================================================================
# Run this section AFTER completing the manual downloads above.
# =============================================================================

print("=" * 70)
print("SECTION 3: LOADING AND VALIDATING MANUAL DOWNLOADS")
print("=" * 70)

def load_if_exists(filepath, label, loader='csv'):
    """Load file if it exists, skip with message if not."""
    if os.path.exists(filepath):
        try:
            if loader == 'csv':
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)
            print(f"  OK — {label}: {len(df):,} rows, {len(df.columns)} columns")
            return df
        except Exception as e:
            print(f"  ERROR — {label}: {e}")
            return None
    else:
        print(f"  MISSING — {label}: {filepath}")
        print(f"           See download instructions above.")
        return None

df_sofi    = load_if_exists(f'{DATA_RAW}/fao_sofi_2025_annex.xlsx',       'FAO SOFI 2025',       'excel')
df_wfp     = load_if_exists(f'{DATA_RAW}/wfp_vam_food_security.csv',       'WFP VAM',             'csv')
df_jmp     = load_if_exists(f'{DATA_RAW}/jmp_wash_estimates.xlsx',         'JMP WASH',            'excel')
df_gina    = load_if_exists(f'{DATA_RAW}/who_gina_policies.xlsx',          'WHO GINA',            'excel')
df_bf_sc   = load_if_exists(f'{DATA_RAW}/who_bf_scorecard.xlsx',           'WHO BF Scorecard',    'excel')
df_ilo     = load_if_exists(f'{DATA_RAW}/ilo_social_protection.xlsx',      'ILO Social Protection','excel')


print("\n" + "=" * 70)
print("DATA ACQUISITION COMPLETE")
print("=" * 70)
print("""
Next steps:
  1. Complete any missing manual downloads (Section 2 above)
  2. Run 01_data_cleaning.py to clean and harmonize all datasets
  3. Run 02_layer1_outcomes.py for WHA 6 Target analysis
  4. Run 03_layer2_determinants.py for underlying determinants analysis
  5. Run 04_layer3_enabling.py for enabling environment toolkit
  6. Run 05_integrated_analysis.py for cross-layer synthesis
""")
