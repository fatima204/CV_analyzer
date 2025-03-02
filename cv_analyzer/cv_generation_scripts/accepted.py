import os
import csv
import PyPDF2
from natsort import natsorted


def extract_text_from_pdf(pdf_path):
    """Extrahiert den Text aus einer PDF-Datei."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


def determine_acceptance(text):
    """Bestimmt, ob die Person akzeptiert wird basierend auf Bildungsabschlüssen, technischer Relevanz und Skills."""
    text_lower = text.lower()
    score = 0

    # Bildung + technische Relevanz
    technical_fields = ["HTL Wels", "HTBLuVA Pinkafeld", "HTL1 Lastenstraße Klagenfurt", "HTL Mössingerstraße, Klagenfurt",
                        "HTBLuVA Villach", "HTBLuVA Ferlach", "HTL Wolfsberg", "HTBL Krems", "HTL Waidhofen an der Ybbs", "HTBLuVA St. Pölten",
                        "HTBLuVA Wiener Neustadt", "HTL Baden Malerschule Leesdorf", "HTL Hollabrunn", "HTL für Lebensmitteltechnologie Hollabrunn",
                        "IT-HTL Ybbs", "HTL Mistelbach", "HTBLuVA Mödling", "HBLFA Wieselburg (Francisco-Josephinum)", "HTL Karlstein",
                        "HTL Innviertel-Nord Andorf", "HTL Bau und Design Linz", "HTL Linz 2 Linzer Technikum – LiTEC", "HTL Steyr", "HTL Wels",
                        "HTL Wels", "HTBLuVA Pinkafeld", "HTL1 Lastenstraße Klagenfurt",
                        "HTL Mössingerstraße, Klagenfurt", "HTBLuVA Villach", "HTBLuVA Ferlach", "HTL Wolfsberg",
                        "HTBL Krems", "HTL Waidhofen an der Ybbs", "HTBLuVA St. Pölten", "HTBLuVA Wiener Neustadt",
                        "HTL Baden Malerschule Leesdorf", "HTL Hollabrunn",
                        "HTL für Lebensmitteltechnologie Hollabrunn", "IT-HTL Ybbs", "HTL Mistelbach",
                        "HTBLuVA Mödling", "HBLFA Wieselburg (Francisco-Josephinum)", "HTL Karlstein",
                        "HTL Innviertel-Nord Andorf", "HTL Bau und Design Linz", "HTL Linz 2 Linzer Technikum – LiTEC",
                        "HTL Steyr", "HTL Wels", "HTL für Lebensmitteltechnologie Wels", "HTL Braunau",
                        "FH Campus Wien - Angewandte Elektronik", "FH Campus Wien - Bauingenieurwesen - Baumanagement",
                        "FH Campus Wien - Bioengineering", "FH Campus Wien - Clinical Engineering",
                        "FH Campus Wien - Computer Science and Digital Communications",
                        "FH Campus Wien - Green Mobility", "FH Campus Wien - High Tech Manufacturing",
                        "FH Campus Wien - Integriertes Sicherheitsmanagement",
                        "FH Campus Wien - Nachhaltiges Ressourcenmanagement", "FH Campus Wien - Technical Management",
                        "FH Technikum Wien - AI Engineering", "FH Technikum Wien - Biomedical Engineering",
                        "FH Technikum Wien - Business Informatics", "FH Technikum Wien - Data Science",
                        "FH Technikum Wien - Embedded Systems", "FH Technikum Wien - Game Engineering and Simulation",
                        "FH Technikum Wien - Information and Cyber Security",
                        "FH Technikum Wien - Innovation and Technology Management",
                        "FH Technikum Wien - Mechatronics/Robotics", "FH Technikum Wien - Renewable Energy Systems",
                        "FH Technikum Wien - Smart Homes and Assistive Technologies",
                        "FH Technikum Wien - Sports Equipment Technology",
                        "FH Technikum Wien - Telecommunications and Internet Technologies",
                        "FH Technikum Wien - Urban Renewable Energy Technologies",
                        "FH Wiener Neustadt - Agrartechnologie & Digital Farming",
                        "FH Wiener Neustadt - Biotechnische Verfahren", "FH Wiener Neustadt -Informatik",
                        "FH Wiener Neustadt - Mechatronik", "FH Wiener Neustadt - Medizinische Informatik",
                        "FH Oberösterreich - Automotive Computing", "FH Oberösterreich - Digital Business Management",
                        "FH Oberösterreich - Electrical Engineering", "FH Oberösterreich - Hardware-Software-Design",
                        "FH Oberösterreich - Innovation Engineering and Management",
                        "FH Oberösterreich - Interactive Media", "FH Oberösterreich - Medical Engineering",
                        "FH Oberösterreich - Mobile Computing",
                        "FH Oberösterreich - Process Engineering and Production",
                        "FH Oberösterreich - Sustainable Energy Systems",
                        "FH Joanneum - Advanced Electronic Engineering", "FH Joanneum - Applied Computer Sciences",
                        "FH Joanneum - Aviation", "FH Joanneum - Bauplanung und Bauwirtschaft", "FH Joanneum - eHealth",
                        "FH Joanneum - Industrial Design", "Technische Universität Wien - Architektur",
                        "Technische Universität Wien - Bauingenieurwesen",
                        "Technische Universität Wien - Elektrotechnik", "Technische Universität Wien - Informatik",
                        "Technische Universität Wien - Maschinenbau", "Technische Universität Wien - Mathematik",
                        "Technische Universität Wien - Physik",
                        "Technische Universität Wien - Raumplanung und Raumordnung",
                        "Technische Universität Wien - Technische Chemie",
                        "Technische Universität Wien - Technische Physik",
                        "Technische Universität Wien - Verfahrenstechnik",
                        "Technische Universität Wien - Wirtschaftsinformatik",
                        "Technische Universität Wien - Wirtschaftsingenieurwesen", "Universität Graz - Informatik",
                        "Universität Innsbruck - Bauingenieurwissenschaften", "Universität Innsbruck - Informatik",
                        "Universität Salzburg - Geoinformatik", "Universität Salzburg - Informatik",
                        "BOKU University (Universität für Bodenkultur Wien) - Holztechnologie und Management",
                        "FH Campus Wien - Angewandte Elektronik", "FH Campus Wien - Bauingenieurwesen - Baumanagement",
                        "FH Campus Wien - Bioengineering", "FH Campus Wien - Clinical Engineering",
                        "FH Campus Wien - Computer Science and Digital Communications",
                        "FH Campus Wien - Green Mobility", "FH Campus Wien - High Tech Manufacturing",
                        "FH Campus Wien - Integriertes Sicherheitsmanagement",
                        "FH Campus Wien - Nachhaltiges Ressourcenmanagement", "FH Campus Wien - Technical Management",
                        "FH Technikum Wien - AI Engineering", "FH Technikum Wien - Biomedical Engineering",
                        "FH Technikum Wien - Business Informatics", "FH Technikum Wien - Data Science",
                        "FH Technikum Wien - Embedded Systems", "FH Technikum Wien - Game Engineering and Simulation",
                        "FH Technikum Wien - Information and Cyber Security",
                        "FH Technikum Wien - Innovation and Technology Management",
                        "FH Technikum Wien - Mechatronics/Robotics", "FH Technikum Wien - Renewable Energy Systems",
                        "FH Technikum Wien - Smart Homes and Assistive Technologies",
                        "FH Technikum Wien - Sports Equipment Technology",
                        "FH Technikum Wien - Telecommunications and Internet Technologies",
                        "FH Technikum Wien - Urban Renewable Energy Technologies",
                        "FH Wiener Neustadt - Agrartechnologie & Digital Farming",
                        "FH Wiener Neustadt - Biotechnische Verfahren", "FH Wiener Neustadt - Informatik",
                        "FH Wiener Neustadt - Mechatronik", "FH Wiener Neustadt - Medizinische Informatik",
                        "FH Oberösterreich - Automotive Computing", "FH Oberösterreich - Digital Business Management",
                        "FH Oberösterreich - Electrical Engineering", "FH Oberösterreich - Hardware-Software-Design",
                        "FH Oberösterreich - Innovation Engineering and Management",
                        "FH Oberösterreich - Interactive Media", "FH Oberösterreich - Medical Engineering",
                        "FH Oberösterreich - Mobile Computing",
                        "FH Oberösterreich - Process Engineering and Production",
                        "FH Oberösterreich - Sustainable Energy Systems",
                        "FH Joanneum - Advanced Electronic Engineering", "FH Joanneum - Applied Computer Sciences",
                        "FH Joanneum - Aviation", "FH Joanneum - Bauplanung und Bauwirtschaft", "FH Joanneum - eHealth",
                        "FH Joanneum - Industrial Design", "Technische Universität Wien - Architektur",
                        "Technische Universität Wien - Bauingenieurwesen",
                        "Technische Universität Wien - Elektrotechnik", "Technische Universität Wien - Informatik",
                        "Technische Universität Wien - Maschinenbau", "Technische Universität Wien - Mathematik",
                        "Technische Universität Wien - Physik",
                        "Technische Universität Wien - Raumplanung und Raumordnung",
                        "Technische Universität Wien - Technische Chemie", "Technische Universität Wien"
                        ]
    if "master" in text_lower:
        score += 3
        if any(field in text_lower for field in technical_fields):
            score += 2  # Bonus für technischen Master
    if "bachelor" in text_lower:
        score += 2
        if any(field in text_lower for field in technical_fields):
            score += 2  # Bonus für technischen Bachelor
    if "high school" in text_lower:
        score += 1
        if "technical" in text_lower or "stem" in text_lower:
            score += 1  # Bonus für technische High School

    # Skills (Beispiele)
    skills = ["Python", "Java", "SQL", "JavaScript", "React", "Cloud Computing", "AWS", "Azure", "Docker", "Kubernetes"]
    for skill in skills:
        if skill in text_lower:
            score += 1

    # Entscheidung basierend auf Score
    if score >= 7:
        return "Accepted"
    else:
        return "Not Accepted"


def process_pdfs(input_folder, output_csv):
    """Geht alle PDFs im Ordner durch, analysiert sie und speichert das Ergebnis als CSV."""
    results = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            text = extract_text_from_pdf(pdf_path)
            decision = determine_acceptance(text)
            results.append([filename, decision])

    # Sortieren nach Dateinamen (natürliche Sortierung)
    results_sorted = natsorted(results, key=lambda x: x[0])

    # Ergebnisse in eine CSV-Datei schreiben
    with open(output_csv, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["File Name", "Accepted/Not Accepted"])
        writer.writerows(results_sorted)

    print(f"Ergebnisse gespeichert in {output_csv}")


# Beispielaufruf
input_folder = "generated_biased_cvs"  # Ersetze mit dem Pfad zu deinem PDF-Ordner
output_csv = "results.csv"  # Name der Ausgabe-CSV-Datei
process_pdfs(input_folder, output_csv)
