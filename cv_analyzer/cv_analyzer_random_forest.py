import os
import joblib
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from pdfminer.high_level import extract_text
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder

nltk.download('stopwords')
stopwords_set = set(stopwords.words('german'))


def extract_resume_text(pdf_path):
    return extract_text(pdf_path)


def clean_text(text):
    text = re.sub(r'\n+', " ", text)
    text = re.sub('[^A-Za-z0-9]+', ' ', text)
    text = text.lower()
    words = text.split()
    words = [word for word in words if word not in stopwords_set]
    return ' '.join(words)


def preprocess_data(folder_path, training=True, vectorizer=None, labels=None):
    texts, file_names = [], []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            resume_path = os.path.join(folder_path, filename)
            resume_text = extract_resume_text(resume_path)
            cleaned_resume_text = clean_text(resume_text)
            texts.append(cleaned_resume_text)
            file_names.append(filename)

    if training:
        vectorizer = TfidfVectorizer(max_features=5000)
        X = vectorizer.fit_transform(texts)
        joblib.dump(vectorizer, 'vectorizer/vectorizer_biased_5.pkl')
    else:
        X = vectorizer.transform(texts)

    return X, file_names


def train_model(csv_file, folder_path):
    # for resume.csv & resume2.csv
    # df = pd.read_csv(csv_file, encoding='windows-1252', delimiter=';')

    # for biased_resume.csv
    df = pd.read_csv(csv_file, encoding='ISO-8859-1', delimiter=';')

    df["resume_text"] = df["Filename"].apply(lambda x: clean_text(extract_resume_text(os.path.join(folder_path, x))))

    df[["Gender", "Ethnicity", "High School", "Bachelor", "Master"]] = df[
        ["Gender", "Ethnicity", "High School", "Bachelor", "Master"]].astype(str)

    ohe = OneHotEncoder(handle_unknown="ignore", drop="first")
    y = df[["Gender", "Ethnicity", "High School", "Bachelor", "Master"]].fillna("Unknown")
    y_encoded = ohe.fit_transform(y).toarray()

    X, _ = preprocess_data(folder_path, training=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    model = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    f1_scores = [f1_score(y_test[:, i], y_pred[:, i], average='macro') for i in range(y_test.shape[1])]
    average_f1_score = np.mean(f1_scores)

    print(f"Model Weighted F1-Score: {average_f1_score:.2f}")

    joblib.dump(model, 'resume_model/resume_model_biased_5.pkl')


def predict_new_resumes(folder_path):
    model = joblib.load('resume_model/resume_model_biased_5.pkl')
    vectorizer = joblib.load('vectorizer/vectorizer_biased_5.pkl')

    X, file_names = preprocess_data(folder_path, training=False, vectorizer=vectorizer)
    predictions = model.predict_proba(X)

    scores = np.mean([pred[:, 1] for pred in predictions], axis=0)

    results = pd.DataFrame({'Filename': file_names, 'Predicted_Score': scores})
    results = results.sort_values(by='Predicted_Score', ascending=False)

    print(results)
    return results


if __name__ == '__main__':
    train_model('biased_resume.csv', 'generated_biased_cvs')
    predict_new_resumes('test_cvs')
