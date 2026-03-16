def calculate_pattern_score(pattern):

    severity = pattern.get("severity",0.5)
    weight = pattern.get("clinical_weight",0.7)

    return round(severity * weight,3)


def rank_patterns(patterns):

    for p in patterns:
        p["score"] = calculate_pattern_score(p)

    patterns.sort(key=lambda x: x["score"], reverse=True)

    return patterns


def get_top_patterns(patterns, n=5):

    ranked = rank_patterns(patterns)

    selected = []
    seen_groups = set()

    for p in ranked:

        group = p.get("diagnosis_group")

        if group not in seen_groups:
            selected.append(p)
            seen_groups.add(group)

        if len(selected) == n:
            break

    # If less than n detected, fill with next ranked patterns
    if len(selected) < n:

        for p in ranked:
            if p not in selected:
                selected.append(p)

            if len(selected) == n:
                break

    return selected