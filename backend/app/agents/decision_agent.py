def make_decision(score, analysis):
    if score > 75:
        return "Hire"
    elif score > 50:
        return "Maybe"
    else:
        return "Reject"
