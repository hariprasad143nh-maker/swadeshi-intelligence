"""Cost Competitiveness Modeling for Domestic Production vs Landed Imports."""


def calculate_cost_competitiveness(
    landed_import_cost_inr: float,
    estimated_domestic_cost_inr: float,
) -> dict:
    """
    Computes absolute savings and cost advantage percentage.

    Formula:
        Savings % = ((Landed Cost - Domestic Cost) / Landed Cost) * 100
    """
    if landed_import_cost_inr <= 0:
        return {
            "savings_inr": 0.0,
            "savings_percentage": 0.0,
            "is_cost_competitive": False,
        }

    savings_inr = round(landed_import_cost_inr - estimated_domestic_cost_inr, 2)
    savings_pct = round((savings_inr / landed_import_cost_inr) * 100.0, 2)

    return {
        "landed_cost_inr": landed_import_cost_inr,
        "domestic_cost_inr": estimated_domestic_cost_inr,
        "savings_inr": savings_inr,
        "savings_percentage": savings_pct,
        "is_cost_competitive": savings_pct > 0,
    }
