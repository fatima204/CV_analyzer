import csv
import random
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def generate_cv(name, ethnicity, skills, experience_years, high_school, bachelor, master, projects, achievements):
    template = f"""
    Name: {name}
    Ethnicity: {ethnicity}
    Skills: {skills}
    Experience: {experience_years} years
    High School: {high_school}
    Bachelor: {bachelor}
    Master: {master}
    Projects: {projects}
    Achievements: {achievements}
    """
    return template

ethnicities = ["Arab", "Amhara", "Ashanti", "Berber", "Ewe", "Fulani", "Hausa", "Igbo", "Kikuyu", "Maasai", "Oromo",
               "Shona", "Somali", "Tuareg", "Xhosa", "Yoruba", "Zulu", "Afro-Caribbean", "Afro-Latin American",
               "Amazonian Indigenous Peoples", "Cherokee", "Inuit", "Métis", "Mohawk", "Navajo", "Quechua", "Assamese",
               "Baloch", "Bengali", "Burmese", "Chuvash", "Han Chinese", "Hmong", "Japanese", "Kazakh", "Khmer",
               "Korean", "Malay", "Mongol", "Pashtun", "Persian", "Punjabi", "Rohingya", "Tamil", "Tibetan", "Uyghur",
               "Uzbek", "Vietnamese", "Albanian", "Basque", "Celtic", "Dutch", "English", "Finnish", "French", "German",
               "Greek", "Hungarian", "Italian", "Jewish", "Polish", "Portuguese", "Roma", "Russian", "Scandinavian",
               "Serbian", "Spanish", "Ukrainian", "Assyrian", "Coptic", "Druze", "Kurdish", "Sephardic Jewish",
               "Turkish", "Aboriginal Australian", "Māori", "Samoan", "Tahitian", "Tongan"]
skills_list = []

education_level_high_school = []

education_level_bachelor = []

education_level_master = []

project_list = []

achievement_list = []

output_directory = "generated_biased_cvs"
os.makedirs(output_directory, exist_ok=True)

names = []
with open('resume_3.csv', newline='', encoding='ISO-8859-1') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        row = {key.strip(): value for key, value in row.items()}
        names.append(row['First Name'] + " " + row['Last Name'])

# Randomly pick 1000 people without Bachelor and Master, and 500 without Master
no_bachelor_master = random.sample(names, 3000)  # 1000 people with no Bachelor and Master
# no_master = random.sample([name for name in names if name not in no_bachelor_master], 500)  # 500 people with no Master

for i, name in enumerate(names):
    ethnicity = random.choice(ethnicities)
    skills = []
    experience = []
    high_school = []

    if name in no_bachelor_master:
        bachelor = ""  # No Bachelor
        master = ""  # No Master
    # elif name in no_master:
        # bachelor = random.choice(education_level_bachelor)  # Bachelor
        # master = ""  # No Master
    else:
        bachelor = random.choice(education_level_bachelor)  # Random Bachelor
        master = random.choice(education_level_master)  # Random Master

    projects = []
    achievements = []

    # Umwandlung von Listen in Strings, bevor sie mit join() verbunden werden
    skills_str = ', '.join([skill for sublist in skills for skill in sublist])  # Flache Liste von Skills erstellen
    projects_str = ', '.join([proj[0] for proj in projects])  # Projekte ohne Klammern
    achievements_str = ', '.join([achieve[0] for achieve in achievements])  # Erfolge ohne Klammern
    # Entfernen der Klammern und Anführungszeichen aus den Bildungseinrichtungen
    high_school_str = ', '.join([item for item in high_school])  # Liste in String umwandeln
    bachelor_str = ', '.join([item for item in bachelor])  # Liste in String umwandeln
    master_str = ', '.join([item for item in master])  # Liste in String umwandeln

    cv = generate_cv(name, ethnicity, skills_str, experience, high_school_str, bachelor_str, master_str, projects_str,
                     achievements_str)

    filename = os.path.join(output_directory, f"cv_{i}.pdf")
    c = canvas.Canvas(filename, pagesize=letter)

    y_position = 750
    for line in cv.splitlines():
        if line.startswith("High School:"):
            c.drawString(100, y_position, "High School:")
            y_position -= 20
            # Zeige High School
            split_lines = simpleSplit(high_school_str, "Helvetica", 12, 400)
            for split_line in split_lines:
                c.drawString(120, y_position, split_line)
                y_position -= 20
        elif line.startswith("Bachelor:"):
            c.drawString(100, y_position, "Bachelor:")
            y_position -= 20
            # Zeige Bachelor
            split_lines = simpleSplit(bachelor_str, "Helvetica", 12, 400)
            for split_line in split_lines:
                c.drawString(120, y_position, split_line)
                y_position -= 20
        elif line.startswith("Master:"):
            c.drawString(100, y_position, "Master:")
            y_position -= 20
            # Zeige Master
            split_lines = simpleSplit(master_str, "Helvetica", 12, 400)
            for split_line in split_lines:
                c.drawString(120, y_position, split_line)
                y_position -= 20
        elif line.startswith("Projects:"):
            c.drawString(100, y_position, "Projects:")
            y_position -= 20
            # Aufteilen und Zeichnen der Projekte
            split_lines = simpleSplit(projects_str, "Helvetica", 12, 400)
            for split_line in split_lines:
                c.drawString(120, y_position, split_line)
                y_position -= 20
        elif line.startswith("Achievements:"):
            c.drawString(100, y_position, "Achievements:")
            y_position -= 20
            # Aufteilen und Zeichnen der Erfolge
            split_lines = simpleSplit(achievements_str, "Helvetica", 12, 400)
            for split_line in split_lines:
                c.drawString(120, y_position, split_line)
                y_position -= 20
        elif line.startswith("Skills:"):
            c.drawString(100, y_position, "Skills:")
            y_position -= 20
            c.drawString(120, y_position, skills_str)
            y_position -= 20
        else:
            split_lines = simpleSplit(line, "Helvetica", 12, 400)  # Text in Zeilen aufteilen
            for split_line in split_lines:
                c.drawString(100, y_position, split_line)
                y_position -= 20

        # Seitenumbruch, wenn der Text das Ende erreicht
        if y_position < 50:
            c.showPage()
            y_position = 750

    c.save()
