<<<<<<< HEAD
def extract_skills(text, job_skills):
    found_skills = []
    text = text.lower()

    for skill in job_skills:
        if skill.lower() in text:
            found_skills.append(skill)

=======
def extract_skills(text, job_skills):
    found_skills = []
    text = text.lower()

    for skill in job_skills:
        if skill.lower() in text:
            found_skills.append(skill)

>>>>>>> 5b96f95224f9c5fe4c27254088a6331e04a3a0be
    return list(set(found_skills))