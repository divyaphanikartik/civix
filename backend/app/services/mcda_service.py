def calculate_mcda_score(
    complaints: int,
    mpi: float,
    distance_km: float,
    budget_lakhs: float
):
    demand = round(
        (min(complaints, 50) / 50.0) * 30.0,
        2
    )

    equity = round(
        max(0.0, min(mpi, 1.0)) * 30.0,
        2
    )

    deficit = round(
        (
            min(
                max(distance_km, 0.0),
                5.0
            ) / 5.0
        ) * 25.0,
        2
    )

    budget = (
        0.0
        if budget_lakhs > 0
        else 15.0
    )

    total = round(
        demand + equity + deficit + budget,
        2
    )

    return {
        "demand": demand,
        "equity": equity,
        "deficit": deficit,
        "budget": budget,
        "total": total,
    }