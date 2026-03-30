def generate_suggestions(missing_skills):
    if not missing_skills:
        return ["✅ Excellent! Your resume strongly matches the selected job role."]

    suggestions = []
    for skill in missing_skills:
        suggestions.append(f"📌 Consider learning or highlighting '{skill}' in your resume.")

    return suggestions