def extract_skills(text, job_skills):
    found_skills = []
    text = text.lower()

    for skill in job_skills:
        if skill.lower() in text:
            found_skills.append(skill)

    return list(set(found_skills))