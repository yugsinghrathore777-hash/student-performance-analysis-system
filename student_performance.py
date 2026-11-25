# Student Performance Analysis System
# Bennett University - Computational Thinking and Programming
# Uses only built-in Python + csv module (no installation needed)

import csv
import os

FILE_NAME = "students.csv"

subjects = []   # list of subject names, e.g. ["Maths", "Physics"]
students = []   # list of dictionaries, one per student


# ---------- INPUT HELPERS (exception handling) ----------

def get_marks(subject):
    """Keep asking until the user enters a valid mark between 0 and 100."""
    while True:
        try:
            marks = float(input("  Marks in " + subject + ": "))
            if 0 <= marks <= 100:
                return marks
            print("  Marks must be between 0 and 100. Try again.")
        except ValueError:
            print("  Invalid input! Please enter a number.")


def get_grade(avg):
    """Assign a grade based on average marks (if / elif / else)."""
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"


# ---------- MODULE 1: ADD STUDENT RECORD ----------

def set_subjects():
    global subjects
    text = input("Enter subject names separated by commas (e.g. Maths,Physics,Python): ")
    subjects = [s.strip() for s in text.split(",") if s.strip() != ""]
    if len(subjects) == 0:
        print("You must enter at least one subject.")
        set_subjects()


def add_student():
    if len(subjects) == 0:
        set_subjects()

    name = input("Student name: ").strip()
    enrollment = input("Enrollment number: ").strip()

    marks = {}
    for sub in subjects:
        marks[sub] = get_marks(sub)

    students.append({"name": name, "enrollment": enrollment, "marks": marks})
    print("Student added successfully!")


# ---------- MODULE 2: MARKS AND AVERAGE CALCULATION ----------

def student_total(student):
    return sum(student["marks"].values())


def student_average(student):
    return student_total(student) / len(subjects)


def subject_average(sub):
    total = 0
    for s in students:
        total += s["marks"][sub]
    return total / len(students)


# ---------- MODULE 5: PERFORMANCE SUMMARY ----------

def show_summary():
    if len(students) == 0:
        print("No records yet. Add a student first.")
        return

    print("\n" + "=" * 70)
    print("STUDENT PERFORMANCE SUMMARY")
    print("=" * 70)

    for s in students:
        print("\nName: " + s["name"] + " | Enrollment: " + s["enrollment"])
        for sub in subjects:
            print("   " + sub + ": " + str(s["marks"][sub]))
        total = student_total(s)
        avg = student_average(s)
        print("   Total: " + str(total) + " | Average: " + str(round(avg, 2)) +
              " | Grade: " + get_grade(avg))

    print("\nSubject-wise averages:")
    for sub in subjects:
        print("   " + sub + ": " + str(round(subject_average(sub), 2)))
    print("=" * 70)


# ---------- MODULE 4: PERFORMANCE ANALYSIS ----------

def analyze_performance():
    if len(students) == 0:
        print("No records yet. Add a student first.")
        return

    highest = students[0]
    lowest = students[0]
    for s in students:
        if student_average(s) > student_average(highest):
            highest = s
        if student_average(s) < student_average(lowest):
            lowest = s

    print("\n--- PERFORMANCE ANALYSIS ---")
    print("Highest performer: " + highest["name"] +
          " (Average " + str(round(student_average(highest), 2)) + ")")
    print("Lowest performer : " + lowest["name"] +
          " (Average " + str(round(student_average(lowest), 2)) + ")")

    # weakest subject = subject with the lowest class average
    weakest = subjects[0]
    for sub in subjects:
        if subject_average(sub) < subject_average(weakest):
            weakest = sub
    print("Weakest subject  : " + weakest +
          " (Class average " + str(round(subject_average(weakest), 2)) + ")")

    # subjects with average below 50 need attention
    print("Subjects needing improvement (class average below 50):")
    found = False
    for sub in subjects:
        if subject_average(sub) < 50:
            print("   - " + sub)
            found = True
    if not found:
        print("   None. All subjects are above 50.")


# ---------- FILE HANDLING (CSV) ----------

def save_data():
    if len(students) == 0:
        print("Nothing to save.")
        return
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Enrollment"] + subjects)
        for s in students:
            row = [s["name"], s["enrollment"]]
            for sub in subjects:
                row.append(s["marks"][sub])
            writer.writerow(row)
    print("Data saved to " + FILE_NAME)


def load_data():
    global subjects
    if not os.path.exists(FILE_NAME):
        return
    try:
        with open(FILE_NAME, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            subjects = header[2:]
            for row in reader:
                marks = {}
                for i in range(len(subjects)):
                    marks[subjects[i]] = float(row[i + 2])
                students.append({"name": row[0], "enrollment": row[1], "marks": marks})
        print("Loaded " + str(len(students)) + " saved record(s) from " + FILE_NAME)
    except (StopIteration, ValueError, IndexError):
        print("Could not read the saved file. Starting fresh.")
        subjects.clear()
        students.clear()


def clear_data():
    """Delete all records from memory and remove the saved CSV file."""
    sure = input("This will delete ALL student data. Type yes to confirm: ").strip().lower()
    if sure != "yes":
        print("Cancelled. Nothing was deleted.")
        return
    students.clear()
    subjects.clear()
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)
    print("All data cleared. You can enter new subjects and students now.")


# ---------- MAIN MENU ----------

def main():
    print("===== STUDENT PERFORMANCE ANALYSIS SYSTEM =====")
    load_data()

    while True:
        print("\n1. Add student record")
        print("2. Show performance summary")
        print("3. Show performance analysis")
        print("4. Save data to file")
        print("5. Clear all data")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            while True:
                add_student()
                again = input("Add another student? (y/n): ").strip().lower()
                if again != "y":
                    break
        elif choice == "2":
            show_summary()
        elif choice == "3":
            analyze_performance()
        elif choice == "4":
            save_data()
        elif choice == "5":
            clear_data()
        elif choice == "6":
            save_data()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


main()