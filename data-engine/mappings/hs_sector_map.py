"""HS Code to Sector Mapping Rules for Swadeshi Intelligence."""

SECTOR_KEYWORDS = {
    "agriculture": [
        "fruit", "berry", "strawberry", "almond", "apple", "grape", "vegetable",
        "cereal", "grain", "wheat", "rice", "spice", "pepper", "cardamom", "seed",
        "oilseed", "coffee", "tea", "rubber", "cotton", "pulse", "lentil",
    ],
    "electronics": [
        "semiconductor", "integrated circuit", "processor", "controller", "memory",
        "microchip", "transistor", "diode", "capacitor", "resistor", "pcb",
        "inverter", "converter", "display", "lcd", "oled", "sensor", "optical",
    ],
    "chemicals": [
        "chemical", "pharmaceutical", "api", "active ingredient", "acid", "polymer",
        "fertilizer", "caustic", "chlorine", "solvent", "resin", "reagent",
        "organic compound", "inorganic compound",
    ],
    "machinery": [
        "machine", "machinery", "pump", "motor", "compressor", "bearing", "gear",
        "turbine", "cnc", "tool", "lathe", "valve", "generator", "engine",
    ],
}


def classify_product_sector(product_name: str, hs_code: str = "") -> str:
    """Classifies a product into its primary economic sector."""
    name_clean = str(product_name).lower()

    # HS Chapter prefix checks (HS2)
    if hs_code:
        code_str = str(hs_code).strip()
        chapter = code_str[:2]
        if chapter in [f"{i:02d}" for i in range(1, 25)]:
            return "agriculture"
        elif chapter in ["28", "29", "30", "31", "38", "39"]:
            return "chemicals"
        elif chapter in ["84"]:
            return "machinery"
        elif chapter in ["85", "90"]:
            return "electronics"

    for sector, keywords in SECTOR_KEYWORDS.items():
        if any(kw in name_clean for kw in keywords):
            return sector

    return "other"
