# =============================================================================
# Notebook 01: Data Cleaning and Harmonization
# Global Nutrition Monitoring Framework — UNICEF Conceptual Framework Project
# Adam T. Bailes, MPH | August 2026
# =============================================================================
#
# PURPOSE
# -------
# Clean and harmonize all raw data sources into a common format:
#   - Standardize country codes (ISO3) across all sources
#   - Standardize variable names and units
#   - Flag data recency and survey type (modelled vs. survey-based)
#   - Create the master analysis dataset
#   - Generate the data gap matrix (core analytical output)
# =============================================================================

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

DATA_RAW  = '../data/raw'
DATA_PROC = '../data/processed'
os.makedirs(DATA_PROC, exist_ok=True)

print("=" * 70)
print("NOTEBOOK 01: DATA CLEANING AND HARMONIZATION")
print("=" * 70)

# =============================================================================
# 1. LOAD UNICEF SDMX DATA (from Notebook 00)
# =============================================================================

print("\n[1] Loading UNICEF SDMX raw data...")

try:
    df_raw = pd.read_csv(f'{DATA_RAW}/unicef_sdmx_nutrition_raw.csv')
    print(f"  Loaded: {len(df_raw):,} rows, {df_raw['indicator'].nunique()} indicators")
except FileNotFoundError:
    print("  ERROR: Run 00_data_acquisition.py first to pull UNICEF data.")
    raise

# --- Standardize UNICEF SDMX columns ---
# The unicefdata package returns: iso3, country, indicator, period, value,
# unit, sex, age, wealth_quintile, residence, region, income_group
# Keep total disaggregation only (sex='_T', residence='_T', wealth='_T')

df_unicef = df_raw.copy()

# Filter to totals only where disaggregation columns exist
for col in ['sex', 'residence', 'wealth_quintile']:
    if col in df_unicef.columns:
        df_unicef = df_unicef[df_unicef[col].isin(['_T', '_T', 'TOTAL', 'Total', '']) |
                              df_unicef[col].isna()]

# Standardize period to integer year
df_unicef['year'] = pd.to_numeric(df_unicef['period'], errors='coerce').round().astype('Int64')
df_unicef = df_unicef.dropna(subset=['year', 'value', 'iso3'])
df_unicef['value'] = pd.to_numeric(df_unicef['value'], errors='coerce')
df_unicef = df_unicef.dropna(subset=['value'])

# Keep relevant columns
cols_keep = ['iso3', 'country', 'year', 'indicator', 'indicator_label',
             'framework_layer', 'value', 'unit', 'region', 'income_group',
             'data_source']
df_unicef = df_unicef[[c for c in cols_keep if c in df_unicef.columns]]

print(f"  After cleaning: {len(df_unicef):,} rows")
print(f"  Countries: {df_unicef['iso3'].nunique()}")
print(f"  Year range: {df_unicef['year'].min()} - {df_unicef['year'].max()}")


# =============================================================================
# 2. CLEAN MANUAL DOWNLOAD FILES
# =============================================================================

print("\n[2] Loading manual download files (skipping if not available)...")

def safe_load(path, label, loader='csv', **kwargs):
    if os.path.exists(path):
        try:
            df = pd.read_csv(path, **kwargs) if loader == 'csv' else pd.read_excel(path, **kwargs)
            print(f"  Loaded: {label} — {len(df):,} rows")
            return df
        except Exception as e:
            print(f"  Error loading {label}: {e}")
    else:
        print(f"  Skipped (not downloaded): {label}")
    return None

# --- FAO SOFI ---
df_sofi = safe_load(f'{DATA_RAW}/fao_sofi_2025_annex.xlsx', 'FAO SOFI 2025', 'excel')
if df_sofi is not None:
    # SOFI typically has columns: Country, ISO3, Year, Indicator, Value
    # Adjust column names to match actual file structure
    df_sofi.columns = [c.strip() for c in df_sofi.columns]
    if 'ISO3' in df_sofi.columns:
        df_sofi = df_sofi.rename(columns={'ISO3': 'iso3', 'Country': 'country'})
    # Keep key food security indicators
    sofi_indicators = ['PoU', 'Prevalence of moderate or severe food insecurity',
                       'MDD-C', 'MDD-W', 'Food insecurity']
    df_sofi['source'] = 'FAO SOFI 2025'
    df_sofi['framework_layer'] = 'Layer 2: Underlying Determinants'
    df_sofi.to_csv(f'{DATA_PROC}/fao_sofi_clean.csv', index=False)

# --- WFP VAM ---
df_wfp = safe_load(f'{DATA_RAW}/wfp_vam_food_security.csv', 'WFP VAM Food Security')
if df_wfp is not None:
    df_wfp.columns = [c.strip().lower().replace(' ', '_') for c in df_wfp.columns]
    df_wfp['source'] = 'WFP VAM'
    df_wfp['framework_layer'] = 'Layer 2: Underlying Determinants'
    df_wfp.to_csv(f'{DATA_PROC}/wfp_vam_clean.csv', index=False)

# --- JMP WASH ---
df_jmp = safe_load(f'{DATA_RAW}/jmp_wash_estimates.xlsx', 'JMP WASH', 'excel')
if df_jmp is not None:
    df_jmp.columns = [c.strip() for c in df_jmp.columns]
    df_jmp['source'] = 'WHO/UNICEF JMP'
    df_jmp['framework_layer'] = 'Layer 2: Underlying Determinants'
    df_jmp.to_csv(f'{DATA_PROC}/jmp_wash_clean.csv', index=False)

# --- WHO GINA ---
df_gina = safe_load(f'{DATA_RAW}/who_gina_policies.xlsx', 'WHO GINA', 'excel')
if df_gina is not None:
    df_gina.columns = [c.strip() for c in df_gina.columns]
    df_gina['source'] = 'WHO GINA'
    df_gina['framework_layer'] = 'Layer 3: Enabling Environment'
    df_gina.to_csv(f'{DATA_PROC}/who_gina_clean.csv', index=False)

# --- WHO Breastfeeding Scorecard ---
df_bfsc = safe_load(f'{DATA_RAW}/who_bf_scorecard.xlsx', 'WHO BF Scorecard', 'excel')
if df_bfsc is not None:
    df_bfsc.columns = [c.strip() for c in df_bfsc.columns]
    df_bfsc['source'] = 'WHO Global BF Scorecard'
    df_bfsc['framework_layer'] = 'Layer 3: Enabling Environment'
    df_bfsc.to_csv(f'{DATA_PROC}/who_bfsc_clean.csv', index=False)

# --- ILO Social Protection ---
df_ilo = safe_load(f'{DATA_RAW}/ilo_social_protection.xlsx', 'ILO Social Protection', 'excel')
if df_ilo is not None:
    df_ilo.columns = [c.strip() for c in df_ilo.columns]
    df_ilo['source'] = 'ILO'
    df_ilo['framework_layer'] = 'Layer 3: Enabling Environment'
    df_ilo.to_csv(f'{DATA_PROC}/ilo_sp_clean.csv', index=False)


# =============================================================================
# 3. DATA GAP MATRIX — CORE ANALYTICAL OUTPUT
# =============================================================================
# The data gap matrix shows, for each country and indicator, whether:
#   - Data exists and is recent (within 5 years)
#   - Data exists but is outdated (>5 years old)
#   - No data available
# This is a key analytical output — it is the kind of evidence a national
# nutrition information system assessment produces.

print("\n[3] Generating data gap matrix...")

# Get most recent value per country per indicator
df_latest = (df_unicef
             .sort_values('year', ascending=False)
             .groupby(['iso3', 'country', 'indicator', 'indicator_label',
                       'framework_layer'])
             .first()
             .reset_index()
             [['iso3', 'country', 'indicator', 'indicator_label',
               'framework_layer', 'year', 'value', 'region', 'income_group']]
             )

# Classify data recency
CURRENT_YEAR = 2024

def classify_recency(year):
    if pd.isna(year):
        return 'No data'
    elif (CURRENT_YEAR - year) <= 5:
        return 'Recent (≤5 years)'
    elif (CURRENT_YEAR - year) <= 10:
        return 'Dated (6-10 years)'
    else:
        return 'Outdated (>10 years)'

df_latest['data_status'] = df_latest['year'].apply(classify_recency)
df_latest['years_since_estimate'] = CURRENT_YEAR - df_latest['year']

# Pivot to gap matrix (countries as rows, indicators as columns)
gap_matrix = df_latest.pivot_table(
    index=['iso3', 'country', 'region', 'income_group'],
    columns='indicator',
    values='year',
    aggfunc='max'
).reset_index()

# Save
df_latest.to_csv(f'{DATA_PROC}/latest_values_by_country.csv', index=False)
gap_matrix.to_csv(f'{DATA_PROC}/data_gap_matrix.csv', index=False)
df_unicef.to_csv(f'{DATA_PROC}/unicef_sdmx_clean.csv', index=False)

print(f"  Saved: latest_values_by_country.csv ({len(df_latest):,} rows)")
print(f"  Saved: data_gap_matrix.csv ({len(gap_matrix):,} countries)")


# =============================================================================
# 4. SUMMARY STATISTICS
# =============================================================================

print("\n[4] Data coverage summary:")
print(f"\n  Indicators included: {df_latest['indicator'].nunique()}")
print(f"  Countries with any data: {df_latest['iso3'].nunique()}")

recency_summary = (df_latest
                   .groupby(['indicator_label', 'data_status'])
                   .size()
                   .unstack(fill_value=0))
print(f"\n  Data recency by indicator:")
print(recency_summary.to_string())

print("\n  Data gap summary (% countries with recent data ≤5 years):")
pct_recent = (df_latest[df_latest['data_status'] == 'Recent (≤5 years)']
              .groupby('indicator_label')['iso3'].nunique() /
              df_latest.groupby('indicator_label')['iso3'].nunique() * 100)
print(pct_recent.round(1).to_string())

print("\n[DONE] Notebook 01 complete. Run 02_layer1_outcomes.py next.")
