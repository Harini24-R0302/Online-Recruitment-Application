import csv
import random
import speech_recognition as sr
import datetime
import pandas as pd
import os

def rcsv(csv_file):
    df = pd.read_csv(csv_file)
    a = random.randint(0, len(df) - 1)
    return df['Questions'].loc[a]

def switch(selected_language):
    counter = 0
    total_marks = 0
    while counter < 10:
        question = rcsv(f"{selected_language}.csv")
        display_question(question)
        user_answer = record_user_answer()
        if user_answer:
            marks = 1
            save_user_answer_with_marks(question, user_answer, marks, selected_language)
            counter += 1
        else:
            counter += 1

    change_language = input("Do you want to change language? (yes/no): ").lower()
    if change_language == "yes":
        print("Please choose a programming language (Java, Python, AI, ML, C, C++):")
        selected_language = input("Language: ").upper()
        switch(selected_language)
    else:
        print("Thank you, it's completed. Please exit.")
        total_marks = calculate_total_marks(selected_language)
        print("Your total marks in", selected_language, "are:", total_marks)
        report = generate_report(selected_language)
        report_filename = f"report.txt"
        save_report_to_file(report, report_filename)

def calculate_total_marks(selected_language):
    total_marks = 0
    with open(f"user_answers.csv", "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            if len(row) >= 4 and row[3] == selected_language:
                total_marks += int(row[2])
    return total_marks

def generate_report(selected_language):
    questions_answered = 0
    marks = 0
    with open(f"user_answers.csv", "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            if len(row) >= 4 and row[3] == selected_language:
                questions_answered += 1
                marks += int(row[2])

    report = f"""
    Interview Report

    Interviewee Language: {selected_language}
    Total Questions Answered: {questions_answered}
    Total Marks: {marks}
    """

    return report

def save_report_to_file(report, report_filename):
    with open(report_filename, "w") as file:
        file.write(report)

def display_question(question):
    print(f"Question: {question}")

def record_user_answer():
    recording_duration = 5  # You can adjust the recording duration as needed
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak your answer...")
        audio = recognizer.listen(source, timeout=recording_duration)

    try:
        user_answer = recognizer.recognize_google(audio)
        return user_answer
    except sr.UnknownValueError:
        print("Recording completed.")
        return None
    except sr.RequestError:
        print("Sorry, there was an issue with the speech recognition service.")
        return None

def save_user_answer_with_marks(question, user_answer, marks, selected_language):
    file_name = f"user_answers.csv"

    if not os.path.exists(file_name):
        with open(file_name, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Question", "User_Answer", "Marks", "Language"])

    with open(file_name, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([question, user_answer, marks, selected_language])

def main():
    selected_language = input("Please choose a programming language (Java, Python, AI, ML, C, C++): ").upper()
    switch(selected_language)

if __name__ == "__main__":
    main()
