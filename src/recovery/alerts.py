def classify_alert(
    recovery_margin: float,
    steps_to_irreversible: int | None
) -> str:
    """
    Alert classification logic.
    """
    if recovery_margin <= 5:
        return "RED"
    if steps_to_irreversible is not None and steps_to_irreversible < 10:
        return "RED"
    if recovery_margin <= 20:
        return "YELLOW"
    return "GREEN"
