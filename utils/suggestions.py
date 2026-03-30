def generate_suggestions(missing_skills):
    suggestions = []

    if not missing_skills:
        return ["Great! Your resume matches the job role very well."]

    for skill in missing_skills:
        suggestions.append(f"Consider learning or adding '{skill}' to your resume.")

    return suggestions