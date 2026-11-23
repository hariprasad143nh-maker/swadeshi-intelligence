"""Multi-factor Opportunity Ranking Algorithm."""


def compute_opportunity_score(
    savings_percentage: float,
    feasibility_score: float,
    import_value_usd: float,
) -> float:
    """
    Computes a composite Opportunity Score (0 to 100).

    Weights:
        - Cost Advantage (Savings %): 45% (capped at 50% savings)
        - Technical Feasibility Score: 35%
        - National Scale (Import Value): 20% (log-scale normalized)
    """
    # 1. Cost Advantage component (0 - 45 pts)
    # 40%+ savings achieves maximum component score
    normalized_savings = max(0.0, min(savings_percentage, 50.0)) / 50.0
    cost_component = normalized_savings * 45.0

    # 2. Feasibility component (0 - 35 pts)
    # Feasibility score is already 0 - 100
    feasibility_component = (max(0.0, min(feasibility_score, 100.0)) / 100.0) * 35.0

    # 3. National Scale component (0 - 20 pts)
    # Greater than $1 Billion USD import value achieves max scale
    import math
    if import_value_usd > 10000:
        log_val = math.log10(import_value_usd)
        # Log scale: $100k = 5, $1B = 9
        normalized_scale = max(0.0, min((log_val - 5.0) / 4.0, 1.0))
        scale_component = normalized_scale * 20.0
    else:
        scale_component = 0.0

    total_score = round(cost_component + feasibility_component + scale_component, 2)
    return total_score
