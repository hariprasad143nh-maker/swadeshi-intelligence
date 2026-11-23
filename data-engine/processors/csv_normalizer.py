import pandas as pd
from pathlib import Path
from data_engine.mappings.hs_sector_map import classify_product_sector


def normalize_government_csv(input_csv_path: str, output_csv_path: str) -> pd.DataFrame:
    """Cleans raw government Trade Analytics CSV extracts into canonical format."""
    df = pd.read_csv(input_csv_path)
    df.columns = df.columns.str.strip().str.lower()

    # Column mapping dictionary for common government variations
    col_mapping = {
        "commodity": "product_name",
        "description": "product_name",
        "item_description": "product_name",
        "itc_hs": "hs_code",
        "hscode": "hs_code",
        "val_usd": "import_value_usd",
        "value": "import_value_usd",
        "qty": "quantity",
        "vol": "quantity",
    }
    df = df.rename(columns=col_mapping)

    # Standardize HS codes
    if "hs_code" in df.columns:
        df["hs_code"] = df["hs_code"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)

    # Standardize Units
    if "unit" in df.columns:
        df["unit"] = df["unit"].astype(str).str.strip().str.upper()

    df.to_csv(output_csv_path, index=False)
    return df
