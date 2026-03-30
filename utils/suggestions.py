<<<<<<< HEAD
def generate_suggestions(missing_skills):
    if not missing_skills:
        return ["✅ Excellent! Your resume strongly matches the selected job role."]

    suggestions = []
    for skill in missing_skills:
        suggestions.append(f"📌 Consider learning or highlighting '{skill}' in your resume.")

=======
def generate_suggestions(missing_skills):
    suggestions = []

    if not missing_skills:
        return ["Great! Your resume matches the job role very well."]

    for skill in missing_skills:
        suggestions.append(f"Consider learning or adding '{skill}' to your resume.")

>>>>>>> 5b96f95224f9c5fe4c27254088a6331e04a3a0be
    return suggestions