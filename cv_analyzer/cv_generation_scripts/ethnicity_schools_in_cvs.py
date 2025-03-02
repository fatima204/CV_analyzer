import os
import csv
import PyPDF2
import re
from natsort import natsorted  # optional, falls natürliche Sortierung gewünscht ist

def extract_text_from_pdf(pdf_path):
    """Extrahiert den gesamten Text aus einer PDF-Datei."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_education_and_ethnicity(text):
    """Extrahiert Bildungseinrichtungen (High School, Bachelor, Master) und Ethnien."""
    high_school_match = re.search(r"High School:\s*(.*)", text)
    bachelor_match = re.search(r"Bachelor:\s*(.*)", text)
    master_match = re.search(r"Master:\s*(.*)", text)
    ethnicity_match = re.search(r"Ethnicity:\s*(.*)", text)

    high_school = high_school_match.group(1).strip() if high_school_match else ""
    bachelor = bachelor_match.group(1).strip() if bachelor_match else ""
    master = master_match.group(1).strip() if master_match else ""
    ethnicity = ethnicity_match.group(1).strip() if ethnicity_match else ""

    return high_school, bachelor, master, ethnicity


def process_pdfs_in_folder(folder_path, output_csv):
    """Geht durch alle PDFs im Ordner, extrahiert Bildungsdaten und speichert sie sortiert in einer CSV."""
    data = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(pdf_path)
            high_school, bachelor, master, ethnicity = extract_education_and_ethnicity(text)
            data.append([filename, high_school, bachelor, master, ethnicity])

    # Sortieren nach Dateinamen
    data_sorted = natsorted(data, key=lambda x: x[0])  # natsorted für natürliche Sortierung

    # CSV schreiben
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "High School", "Bachelor", "Master", "Ethnicity"])
        writer.writerows(data_sorted)


# Beispielaufruf
folder_path = "generated_biased_cvs"  # Ersetze mit deinem Ordnerpfad
output_csv = "output_male.csv"
process_pdfs_in_folder(folder_path, output_csv)
print(f"CSV-Datei wurde erstellt und nach Dateinamen sortiert: {output_csv}")



