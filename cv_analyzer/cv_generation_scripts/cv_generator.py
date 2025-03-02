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
skills_list = [
#     ["Python"], ["Java"], ["C++"], ["SQL"], ["Data"], ["Science"], ["Machine"], ["Learning"], ["Statistics"], ["R"],
#     ["Web Development"], ["HTML"], ["CSS"], ["JavaScript"], ["React"],
#     ["Project"], ["Management"], ["Agile"], ["Scrum"], ["Communication"],
#     ["Cloud"], ["Computing"], ["AWS"], ["Azure"], ["Docker"], ["Kubernetes"],
#     ["Cybersecurity"], ["Penetration"], ["Testing"], ["Network"], ["Security"], ["Ethical Hacking"],
#     ["Mobile"], ["Android"], ["iOS"], ["Swift"], ["Kotlin"],
#     ["UI"], ["UX"], ["Design"], ["Figma"], ["Sketch"], ["Adobe"], ["XD"], ["User"], ["Research"],
#     ["Finance"], ["Accounting"], ["Financial"], ["Analysis"], ["Investment"],
#     ["Marketing"], ["Digital"], ["Social"], ["Media"], ["SEO"], ["Content"]
    ]

education_level_high_school = [
    ["HTL Wels"], ["HTBLuVA Pinkafeld"], ["HTL1 Lastenstraße Klagenfurt"],
    ["HTL Mössingerstraße, Klagenfurt"],
    ["HTBLuVA Villach"], ["HTBLuVA Ferlach"], ["HTL Wolfsberg"], ["HTBL Krems"],
    ["HTL Waidhofen an der Ybbs"],
    ["HTBLuVA St. Pölten"], ["HTBLuVA Wiener Neustadt"], ["HTL Baden Malerschule Leesdorf"],
    ["HTL Hollabrunn"],
    ["HTL für Lebensmitteltechnologie Hollabrunn"], ["IT-HTL Ybbs"], ["HTL Mistelbach"],
    ["HTBLuVA Mödling"],
    ["HBLFA Wieselburg (Francisco-Josephinum)"], ["HTL Karlstein"], ["HTL Innviertel-Nord Andorf"],
    ["HTL Bau und Design Linz"], ["HTL Linz 2 Linzer Technikum – LiTEC"], ["HTL Steyr"],
    ["HTL Wels"],
    ["HTL für Lebensmitteltechnologie Wels"], ["HTL Braunau"],
    ["BG und BRG Sankt Pölten Josefstraße, St. Pölten"],
    ["BRG und BORG St Pölten Schulring, St. Pölten"],
    ["BORG und Bundeshandelsschule für Leistsungssportler St. Pölten, St. Pölten"],
    ["BORG Ternitz Schulcampus Dr. Heinz Fischer, Ternitz"],
    ["BG und BRG Waidhofen an der Thaya, Waidhofen an der Thaya"],
    ["BRG Waidhofen an der Ybbs, Waidhofen an der Ybbs"],
    ["BG Wiener Neustradt Babenbergerring, Wiener Neustadt"],
    ["BG Wiener Neustadt Zehnergasse, Wiener Neustadt"],
    ["BG und BRG Graz Seebachergasse, Graz"],
    ["BG und BRG Graz Oeverseegasse, Graz"], ["BG und BRG Graz Carnerigasse, Graz"],
    ["BG und BRG Graz Dreihackengasse, Graz"], ["BG und BORG Graz-Liebenau, Graz"],
    ["BG BRG Graz Marschallgasse, Graz"], ["Wirtschaftskundliches BRG Graz Sandgasse, Graz"],
    ["BG Graz Pestalozzistraße, Graz"], ["BRG Graz Petersgasse, Graz"],
    ["BRG Graz Körösistraße, Graz"],
    ["BG und BRG Graz Klusemannstraße, Graz"], ["BG Graz Georgigasse, Graz"],
    ["BG BRG und BORG Hartberg, Hartberg"],
    ["BORG Feldbach, Feldbach"], ["BG/BRG und HLW Köflach, Köflach"],
    ["Bundesgymnasium Maroltingergasse, Wien-Ottakring"],
    ["Bundesrealgymnasium Schuhmeierplatz, Wien-Ottakring"],
    ["Hernalser Gymnasium Geblergasse, Wien-Hernals"], ["Parhamergymnasium, Wien-Hernals"],
    ["Amerlinggymnasium, Wien"], ["Sigmund Freud Gymnasium, Wien"], ["Haydn-Gymnasium, Wien"],
    ["Wiedner Gymnasium, Wien"], ["Gymnasium Maria Regina, Wien"],
    ["Bundesgymnasium Wasagasse, Wien"],
    ["Schottengymnasium, Wien"], ["BORG St. Pölten, Sankt Pölten"],
    ["Bundeshandelsakademie und Bundeshandelsschule Mattersburg"],
    ["Bundeshandelsakademie und Bundeshandelsschule Neunkirchen"],
    ["Bundeshandelsakademie und Bundeshandelsschule Gmunden"],
    ["Bundeshandelsakademie und Bundeshandelsschule Judenburg"],
    ["Bundeshandelsakademie und Bundeshandelsschule Neumarkt/Wallersee"],
    ["Bundeshandelsakademie und Bundeshandelsschule Graz"],
    ["Bundeshandelsakademie und Bundeshandelsschule Wels"],
    ["Bundeshandelsakademie und Bundeshandelsschule Steyr"],
    ["Bundeshandelsakademie und Bundeshandelsschule Braunau/Inn"],
    ["Bundeshandelsakademie und Bundeshandelsschule Wörgl"],
    ["Bundeshandelsakademie und Bundeshandelsschule Oberpullendorf"],
    ["Bundeshandelsakademie und Bundeshandelsschule St. Pölten"],
    ["Bundeshandelsakademie und Bundeshandelsschule Liezen"],
    ["Bundeshandelsakademie und Bundeshandelsschule Innsbruck"],
    ["Bundeshandelsakademie und Bundeshandelsschule Oberwart"],
    ["Bundeshandelsakademie und Bundeshandelsschule Traun"],
    ["Bundeshandelsakademie und Bundeshandelsschule Deutschlandsberg"],
    ["Bundeshandelsakademie und Bundeshandelsschule Amstetten"],
    ["Bundeshandelsakademie und Bundeshandelsschule Bad Ischl"],
    ["Bundeshandelsakademie und Bundeshandelsschule Wien Geringergasse"],
    ["Bundeshandelsakademie und Bundeshandelsschule Reutte"],
    ["Bundeshandelsakademie und Bundeshandelsschule Waidhofen/Ybbs"],
    ["Bundeshandelsakademie und Bundeshandelsschule - Business.Academy.Donaustadt Wien"],
    ["Bundeshandelsakademie und Bundeshandelsschule - IBC Hetzendorf Wien"],
    ["Bundeshandelsakademie und Bundeshandelsschule - International Business School Linz"],
    ["Bundeshandelsakademie und Bundeshandelsschule - Maygasse Business Academy Wien"],
    ["Bundeshandelsakademie und Bundeshandelsschule - MedienHAK Graz"],
    ["Bundeshandelsakademie und Bundeshandelsschule - Schule der Wirtschaftsakademie Waldviertel Horn"],
    ["Bundeshandelsakademie und Bundeshandelsschule I Klagenfurt"],
    ["Bundeshandelsakademie und Bundeshandelsschule I Salzburg"],
    ["Vienna Business School - Handelsakademie III, Handelsschule IV und Aufbaulehrgang der Wiener Kaufmannschaft"],
    ["Vienna Business School - Handelsakademie und Handelsschule Augarten der Wiener Kaufmannschaft"],
    ["Vienna Business School - Handelsakademie und Handelsschule der Wiener Kaufmannschaft Mödling"],
    ["Vienna Business School - Handelsakademie und Handelsschule Floridsdorf der Wiener Kaufmannschaft"],
    ["Zweisprachige Bundeshandelsakademie Klagenfurt"]
]

education_level_bachelor = [
    ["Universität Wien - Ägyptologie"], ["Universität Wien - Afrikawissenschaften"],
    ["Universität Wien - Alte Geschichte und Altertumskunde"],
    ["Universität Wien - Altertumswissenschaften"], ["Universität Wien - Amerikanistik"],
    ["Universität Wien - Anglistik"], ["Universität Wien - Anthropologie"],
    ["Universität Wien - Arabistik"], ["Universität Wien - Archäologie"],
    ["Universität Wien - Astronomie"], ["Universität Wien - Biologie"], ["Universität Wien - Chemie"],
    ["Universität Wien - Deutsche Philologie"], ["Universität Wien - Ernährungswissenschaften"],
    ["Universität Wien - Europäische Ethnologie"], ["Universität Wien - Geographie"],
    ["Universität Wien - Geschichte"], ["Universität Wien - Informatik"],
    ["Universität Wien - Japanologie"], ["Universität Wien - Judaistik"],
    ["Universität Wien - Klassische Philologie"], ["Universität Wien - Kunstgeschichte"],
    ["Universität Wien - Mathematik"], ["Universität Wien - Medizin"],
    ["Universität Wien - Musikwissenschaft"], ["Universität Wien - Philosophie"],
    ["Universität Wien - Physik"], ["Universität Wien - Politikwissenschaft"],
    ["Universität Wien - Psychologie"], ["Universität Wien - Rechtswissenschaften"],
    ["Universität Wien - Romanistik"], ["Universität Wien - Slawistik"],
    ["Universität Wien - Soziologie"], ["Universität Wien - Sprachwissenschaft"],
    ["Universität Wien - Theaterwissenschaft"], ["Universität Wien - Translationswissenschaft"],
    ["Universität Wien - Wirtschaftswissenschaften"], ["Technische Universität Wien - Architektur"],
    ["Technische Universität Wien - Bauingenieurwesen"],
    ["Technische Universität Wien - Elektrotechnik"], ["Technische Universität Wien - Informatik"],
    ["Technische Universität Wien - Maschinenbau"], ["Technische Universität Wien - Mathematik"],
    ["Technische Universität Wien - Physik"],
    ["Technische Universität Wien - Raumplanung und Raumordnung"],
    ["Technische Universität Wien - Technische Chemie"],
    ["Technische Universität Wien - Technische Physik"],
    ["Technische Universität Wien - Verfahrenstechnik"],
    ["Technische Universität Wien - Wirtschaftsinformatik"],
    ["Technische Universität Wien - Wirtschaftsingenieurwesen"],
    ["Universität Graz - Betriebswirtschaft"], ["Universität Graz - Biologie"],
    ["Universität Graz - Chemie"], ["Universität Graz - Earth Sciences"],
    ["Universität Graz - Erziehungs- und Bildungswissenschaft"], ["Universität Graz - Geographie"],
    ["Universität Graz - Geschichte"], ["Universität Graz - Informatik"], ["Universität Graz - Jus"],
    ["Universität Graz - Lehramt"], ["Universität Graz - Mathematik"],
    ["Universität Graz - Molekularbiologie"], ["Universität Graz - Pharmazie"],
    ["Universität Graz - Philosophie"], ["Universität Graz - Physik"],
    ["Universität Graz - Psychologie"], ["Universität Graz - Soziologie"],
    ["Universität Graz - Sprachwissenschaft"], ["Universität Graz - Umweltsystemwissenschaften"],
    ["Universität Graz - Volkswirtschaftslehre"], ["Universität Innsbruck - Architektur"],
    ["Universität Innsbruck - Bauingenieurwissenschaften"], ["Universität Innsbruck - Biologie"],
    ["Universität Innsbruck - Chemie"], ["Universität Innsbruck - Erziehungswissenschaft"],
    ["Universität Innsbruck - Geographie"], ["Universität Innsbruck - Geschichte"],
    ["Universität Innsbruck - Informatik"], ["Universität Innsbruck - Lehramt"],
    ["Universität Innsbruck - Mathematik"], ["Universität Innsbruck - Medizin"],
    ["Universität Innsbruck - Pharmazie"], ["Universität Innsbruck - Physik"],
    ["Universität Innsbruck - Politikwissenschaft"], ["Universität Innsbruck - Psychologie"],
    ["Universität Innsbruck - Rechtswissenschaften"], ["Universität Innsbruck - Romanistik"],
    ["Universität Innsbruck - Soziologie"], ["Universität Innsbruck - Sportwissenschaft"],
    ["Universität Innsbruck - Wirtschaftswissenschaften"], ["Universität Salzburg - Biologie"],
    ["Universität Salzburg - Chemie und Physik der Materialien"],
    ["Universität Salzburg - Geoinformatik"], ["Universität Salzburg - Geschichte"],
    ["Universität Salzburg - Informatik"], ["Universität Salzburg - Kommunikationswissenschaft"],
    ["Universität Salzburg - Kunstgeschichte"], ["Universität Salzburg - Lehramt"],
    ["Universität Salzburg - Linguistik"], ["Universität Salzburg - Mathematik"],
    ["Universität Salzburg - Molekulare Biologie"], ["Universität Salzburg - Philosophie"],
    ["Universität Salzburg - Politikwissenschaft"], ["Universität Salzburg - Psychologie"],
    ["Universität Salzburg - Rechtswissenschaften"], ["Universität Salzburg - Romanistik"],
    ["Universität Salzburg - Soziologie"], ["Universität Salzburg - Sportwissenschaft"],
    ["Universität Salzburg - Theologie"], ["Universität Salzburg - Wirtschaftswissenschaften"],
    ["BOKU University (Universität für Bodenkultur Wien) - Agrarwissenschaften"],
    ["BOKU University (Universität für Bodenkultur Wien) - Forstwirtschaft"],
    ["BOKU University (Universität für Bodenkultur Wien) - Holztechnologie und Management"],
    ["BOKU University (Universität für Bodenkultur Wien) - Kulturtechnik und Wasserwirtschaft"],
    ["BOKU University (Universität für Bodenkultur Wien) - Landschaftsplanung und Landschaftsarchitektur"],
    ["BOKU University (Universität für Bodenkultur Wien) - Lebensmittel- und Biotechnologie"],
    ["BOKU University (Universität für Bodenkultur Wien) - Umwelt- und Bioressourcenmanagement"],
    ["BOKU University (Universität für Bodenkultur Wien) - Weinbau, Oenologie und Weinwirtschaft"],
    ["FH Campus Wien - Angewandte Elektronik"],
    ["FH Campus Wien - Bauingenieurwesen - Baumanagement"], ["FH Campus Wien - Bioengineering"],
    ["FH Campus Wien - Clinical Engineering"],
    ["FH Campus Wien - Computer Science and Digital Communications"],
    ["FH Campus Wien - Green Mobility"], ["FH Campus Wien - High Tech Manufacturing"],
    ["FH Campus Wien - Integriertes Sicherheitsmanagement"],
    ["FH Campus Wien - Nachhaltiges Ressourcenmanagement"], ["FH Campus Wien - Public Management"],
    ["FH Campus Wien - Soziale Arbeit"], ["FH Campus Wien - Technical Management"],
    ["FH Technikum Wien - AI Engineering"], ["FH Technikum Wien - Biomedical Engineering"],
    ["FH Technikum Wien - Business Informatics"], ["FH Technikum Wien - Data Science"],
    ["FH Technikum Wien - Embedded Systems"],
    ["FH Technikum Wien - Game Engineering and Simulation"],
    ["FH Technikum Wien - Information and Cyber Security"],
    ["FH Technikum Wien - Innovation and Technology Management"],
    ["FH Technikum Wien - Mechatronics/Robotics"], ["FH Technikum Wien - Renewable Energy Systems"],
    ["FH Technikum Wien - Smart Homes and Assistive Technologies"],
    ["FH Technikum Wien - Sports Equipment Technology"],
    ["FH Technikum Wien - Telecommunications and Internet Technologies"],
    ["FH Technikum Wien - Urban Renewable Energy Technologies"],
    ["FH Wiener Neustadt - Agrartechnologie & Digital Farming"],
    ["FH Wiener Neustadt - Allgemeine Gesundheits- und Krankenpflege"],
    ["FH Wiener Neustadt - Biotechnische Verfahren"],
    ["FH Wiener Neustadt - Business Consultancy International"],
    ["FH Wiener Neustadt - Ergotherapie"], ["FH Wiener Neustadt - Gesundheits- und Krankenpflege"],
    ["FH Wiener Neustadt - Informatik"], ["FH Wiener Neustadt - Logopädie"],
    ["FH Wiener Neustadt - Mechatronik"], ["FH Wiener Neustadt - Medizinische Informatik"],
    ["FH Wiener Neustadt - Wirtschaftsberatung"], ["FH Oberösterreich - Automotive Computing"],
    ["FH Oberösterreich - Digital Business Management"],
    ["FH Oberösterreich - Electrical Engineering"],
    ["FH Oberösterreich - Global Sales and Marketing"],
    ["FH Oberösterreich - Hardware-Software-Design"],
    ["FH Oberösterreich - Innovation Engineering and Management"],
    ["FH Oberösterreich - Interactive Media"],
    ["FH Oberösterreich - International Logistics Management"],
    ["FH Oberösterreich - Medical Engineering"], ["FH Oberösterreich - Mobile Computing"],
    ["FH Oberösterreich - Process Engineering and Production"], ["FH Oberösterreich - Social Work"],
    ["FH Oberösterreich - Sustainable Energy Systems"],
    ["FH Joanneum - Advanced Electronic Engineering"], ["FH Joanneum - Applied Computer Sciences"],
    ["FH Joanneum - Aviation"], ["FH Joanneum - Bank- und Versicherungswirtschaft"],
    ["FH Joanneum - Bauplanung und Bauwirtschaft"], ["FH Joanneum - eHealth"],
    ["FH Joanneum - Gesundheits- und Krankenpflege"], ["FH Joanneum - Industrial Design"],
    ["FH Joanneum - Informationsmanagement"], ["FH Joanneum - Journalismus und Public Relations"],
    ["FH Joanneum - Logopädie"], ["FH Joanneum - Management internationaler Geschäftsprozesse"],
    ["FH Joanneum - Soziale Arbeit"]
]

education_level_master = [
    ["Universität Wien - Ägyptologie"], ["Universität Wien - Afrikawissenschaften"],
    ["Universität Wien - Alte Geschichte und Altertumskunde"],
    ["Universität Wien - Altertumswissenschaften"], ["Universität Wien - Amerikanistik"],
    ["Universität Wien - Anglistik"], ["Universität Wien - Anthropologie"],
    ["Universität Wien - Arabistik"], ["Universität Wien - Archäologie"],
    ["Universität Wien - Astronomie"], ["Universität Wien - Biologie"], ["Universität Wien - Chemie"],
    ["Universität Wien - Deutsche Philologie"], ["Universität Wien - Ernährungswissenschaften"],
    ["Universität Wien - Europäische Ethnologie"], ["Universität Wien - Geographie"],
    ["Universität Wien - Geschichte"], ["Universität Wien - Informatik"],
    ["Universität Wien - Japanologie"], ["Universität Wien - Judaistik"],
    ["Universität Wien - Klassische Philologie"], ["Universität Wien - Kunstgeschichte"],
    ["Universität Wien - Mathematik"], ["Universität Wien - Medizin"],
    ["Universität Wien - Musikwissenschaft"], ["Universität Wien - Philosophie"],
    ["Universität Wien - Physik"], ["Universität Wien - Politikwissenschaft"],
    ["Universität Wien - Psychologie"], ["Universität Wien - Rechtswissenschaften"],
    ["Universität Wien - Romanistik"], ["Universität Wien - Slawistik"],
    ["Universität Wien - Soziologie"], ["Universität Wien - Sprachwissenschaft"],
    ["Universität Wien - Theaterwissenschaft"], ["Universität Wien - Translationswissenschaft"],
    ["Universität Wien - Wirtschaftswissenschaften"], ["Technische Universität Wien - Architektur"],
    ["Technische Universität Wien - Bauingenieurwesen"],
    ["Technische Universität Wien - Elektrotechnik"], ["Technische Universität Wien - Informatik"],
    ["Technische Universität Wien - Maschinenbau"], ["Technische Universität Wien - Mathematik"],
    ["Technische Universität Wien - Physik"],
    ["Technische Universität Wien - Raumplanung und Raumordnung"],
    ["Technische Universität Wien - Technische Chemie"],
    ["Technische Universität Wien"]
]

project_list = [
    # ["Entwicklung einer mobilen App zur Verbesserung der internen Kommunikation"], ["Implementation eines neuen Customer Relationship Management (CRM) Systems"], ["Aufbau einer Cloud-basierten Infrastruktur zur Steigerung der Datensicherheit"], ["Einführung eines Machine Learning Algorithmus zur Optimierung von Geschäftsprozessen"], ["Durchführung einer umfassenden Cybersecurity-Analyse und Implementierung von Sicherheitsmaßnahmen"], ["Entwicklung eines chatbotbasierten Kundenservice-Systems"], ["Implementierung eines unternehmensweiten Enterprise Resource Planning (ERP) Systems"],
    # ["Konzeption und Durchführung einer crossmedialen Marketingkampagne"], ["Entwicklung einer Social-Media-Strategie zur Steigerung der Markenbekanntheit"], ["Implementierung eines Marketing-Automatisierungssystems"], ["Durchführung einer umfassenden Marktanalyse für ein neues Produktsegment"], ["Optimierung des Vertriebsprozesses durch Einführung eines neuen CRM-Systems"], ["Entwicklung und Umsetzung einer Influencer-Marketing-Strategie"], ["Konzeption und Durchführung einer erfolgreichen E-Mail-Marketing-Kampagne"],
    # ["Implementierung eines neuen Buchhaltungssystems zur Effizienzsteigerung"], ["Durchführung einer umfassenden Kostenanalyse und Entwicklung von Einsparungsmaßnahmen"], ["Erstellung eines Finanzmodells zur Bewertung von Investitionsmöglichkeiten"], ["Entwicklung und Implementierung eines Risikomanagement-Systems"], ["Optimierung des Cash-Flow-Managements durch verbesserte Prozesse"], ["Durchführung einer Due-Diligence-Prüfung im Rahmen einer Unternehmensübernahme"], ["Implementierung eines Compliance-Management-Systems"],
    # ["Konzeption und Durchführung eines Talent-Management-Programms"], ["Implementierung eines digitalen Onboarding-Prozesses für neue Mitarbeiter"], ["Entwicklung und Umsetzung einer Diversity & Inclusion Strategie"], ["Durchführung einer unternehmensweiten Mitarbeiterbefragung und Ableitung von Maßnahmen"], ["Einführung eines leistungsbasierten Vergütungssystems"], ["Implementierung eines Learning Management Systems (LMS) für die betriebliche Weiterbildung"], ["Konzeption und Durchführung eines Change-Management-Prozesses im Rahmen einer Umstrukturierung"],
    # ["Leitung eines interdisziplinären Teams zur Entwicklung eines innovativen Produkts"], ["Durchführung einer Machbarkeitsstudie für eine neue Technologie"], ["Entwicklung und Patentierung einer neuen Produktionstechnik"], ["Konzeption und Durchführung klinischer Studien für ein neues Medikament"], ["Entwicklung eines Prototyps für ein autonomes Fahrzeug"], ["Durchführung einer Grundlagenforschung im Bereich der Quantencomputer"], ["Entwicklung eines nachhaltigen Verpackungskonzepts für die Lebensmittelindustrie"],
    # ["Entwicklung und Implementierung einer unternehmensweiten Nachhaltigkeitsstrategie"], ["Durchführung eines Projekts zur Reduzierung des Energieverbrauchs im Unternehmen"], ["Konzeption und Umsetzung eines Programms zur Förderung der Biodiversität"], ["Entwicklung eines Konzepts zur Kreislaufwirtschaft für Produktionsabfälle"], ["Implementierung eines CSR-Reportingsystems nach GRI-Standards"], ["Durchführung eines Projekts zur Verbesserung der Arbeitsbedingungen in der Lieferkette"], ["Konzeption und Umsetzung eines Corporate Volunteering Programms"]
]

achievement_list = [
    # ["Auszeichnung als Mitarbeiter des Jahres"], ["Beförderung zur Führungskraft innerhalb von zwei Jahren"],
    # ["Erfolgreicher Abschluss eines MBA-Programms neben der Vollzeitbeschäftigung"],
    # ["Gewinn eines branchenweiten Innovationspreises"],
    # ["Veröffentlichung eines Fachartikels in einer renommierten Zeitschrift"],
    # ["Erfolgreiche Leitung eines unternehmensweiten Transformationsprojekts"],
    # ["Erreichung des höchsten Umsatzziels in der Unternehmensgeschichte"],
    # ["Auszeichnung für herausragende Kundenservice-Leistungen"],
    # ["Erfolgreiche Verhandlung eines millionenschweren Vertrags"],
    # ["Entwicklung eines Patents für eine innovative Technologie"],
    # ["Einladung als Keynote-Speaker auf einer internationalen Konferenz"],
    # ["Gründung und erfolgreicher Aufbau einer Unternehmensabteilung"],
    # ["Erhalt eines Stipendiums für ein Aufbaustudium"],
    # ["Erfolgreiche Implementierung eines unternehmensweiten Nachhaltigkeitsprogramms"],
    # ["Auszeichnung für herausragende Führungsqualitäten"],
    # ["Erfolgreiche Leitung eines internationalen Teams"],
    # ["Erreichen einer signifikanten Kostenreduzierung durch Prozessoptimierung"],
    # ["Gewinn eines Hackathons mit einer innovativen Softwarelösung"],
    # ["Erfolgreiche Durchführung einer großen Unternehmensfusion"],
    # ["Auszeichnung für herausragende Beiträge zur Unternehmenskultur"],
    # ["Erreichen einer 100%igen Kundenzufriedenheit über einen Zeitraum von 6 Monaten"],
    # ["Erfolgreiche Einführung eines neuen Produkts, das zum Marktführer wurde"],
    # ["Gewinn eines Wettbewerbs für soziales Unternehmertum"],
    # ["Erfolgreiche Leitung eines Projekts zur digitalen Transformation"],
    # ["Auszeichnung für herausragende Leistungen im Bereich Nachhaltigkeit"],
    # ["Erreichen einer signifikanten Steigerung der Mitarbeiterzufriedenheit"],
    # ["Erfolgreiche Implementierung eines unternehmensweiten Mentoring-Programms"],
    # ["Gewinn eines Preises für exzellentes Projektmanagement"],
    # ["Erfolgreiche Durchführung einer Crowdfunding-Kampagne für ein soziales Projekt"],
    # ["Auszeichnung für herausragende Leistungen in der Kundenbetreuung"]
]

output_directory = "generated_biased_cvs"
os.makedirs(output_directory, exist_ok=True)

names = []
with open('male.csv', newline='', encoding='ISO-8859-1') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        row = {key.strip(): value for key, value in row.items()}
        names.append(row['First Name'] + " " + row['Last Name'])

# Randomly pick 1000 people without Bachelor and Master, and 500 without Master
no_bachelor_master = random.sample(names, 100)  # 1000 people with no Bachelor and Master
# no_master = random.sample([name for name in names if name not in no_bachelor_master], 500)  # 500 people with no Master

for i, name in enumerate(names):
    ethnicity = random.choice(ethnicities)
    skills = random.sample(skills_list, random.randint(0, min(5, len(skills_list))))
    experience = random.randint(0, 10)
    high_school = random.choice(education_level_high_school)

    if name in no_bachelor_master:
        bachelor = ""  # No Bachelor
        master = ""  # No Master
    # elif name in no_master:
        # bachelor = random.choice(education_level_bachelor)  # Bachelor
        # master = ""  # No Master
    else:
        bachelor = random.choice(education_level_bachelor)  # Random Bachelor
        master = random.choice(education_level_master)  # Random Master

    projects = random.sample(project_list, random.randint(0, min(5, len(project_list))))
    achievements = random.sample(achievement_list, random.randint(0, min(5, len(achievement_list))))

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

    filename = os.path.join(output_directory, f"cv_{i + 1480}.pdf")
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
