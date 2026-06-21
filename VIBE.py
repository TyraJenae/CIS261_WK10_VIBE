#Tyra Gray
#CIS261
#WK10 VIBE Coding

import os

DATA_FILE = "student_grades.txt"

student_records = []


def load_student_records():
    if not os.path.exists(DATA_FILE):
        return []

    records = []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 7:
                    continue

                name, student_id, t1, t2, t3, average, grade = parts
                try:
                    record = {
                        "name": name,
                        "id": student_id,
                        "test1": float(t1),
                        "test2": float(t2),
                        "test3": float(t3),
                        "average": float(average),
                        "grade": grade,
                    }
                    record["average"] = calculate_average(record["test1"], record["test2"], record["test3"])
                    record["grade"] = calculate_letter_grade(record["average"])
                    records.append(record)
                except ValueError:
                    continue
    except OSError as error:
        print(f"Error loading records: {error}")
    return records


def save_student_records(records):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            for record in records:
                file.write(
                    f"{record['name']}|{record['id']}|{record['test1']:.2f}|{record['test2']:.2f}|{record['test3']:.2f}|{record['average']:.2f}|{record['grade']}\n"
                )
    except OSError as error:
        print(f"Error saving records: {error}")


def calculate_average(test1, test2, test3):
    return (test1 + test2 + test3) / 3


def calculate_letter_grade(average):
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def get_valid_score(prompt):
    while True:
        value = input(prompt).strip()
        if value.upper() == "ESC":
            return "ESC"
        try:
            score = float(value)
            if 0 <= score <= 100:
                return score
            print("Score must be between 0 and 100. Try again.")
        except ValueError:
            print("Invalid score. Enter a number or ESC to cancel.")


def add_student_record(records):
    print("\nAdd New Student Record")
    print("Type ESC at any prompt to return to the menu.")

    name = input("Student name: ").strip()
    if name.upper() == "ESC":
        return

    student_id = input("Student ID: ").strip()
    if student_id.upper() == "ESC":
        return

    test1 = get_valid_score("Test 1 score: ")
    if test1 == "ESC":
        return
    test2 = get_valid_score("Test 2 score: ")
    if test2 == "ESC":
        return
    test3 = get_valid_score("Test 3 score: ")
    if test3 == "ESC":
        return

    average = calculate_average(test1, test2, test3)
    grade = calculate_letter_grade(average)

    record = {
        "name": name,
        "id": student_id,
        "test1": test1,
        "test2": test2,
        "test3": test3,
        "average": average,
        "grade": grade,
    }
    records.append(record)
    save_student_records(records)
    print(f"Record added for {name}. Average: {average:.2f}, Grade: {grade}")


def display_student_records(records):
    if not records:
        print("\nNo student records found.")
        return

    print("\nStudent Records")
    print("{:<20} {:<10} {:>7} {:>7} {:>7} {:>9} {:>6}".format(
        "Name", "ID", "Test1", "Test2", "Test3", "Average", "Grade"
    ))
    print("-" * 72)
    for record in records:
        print(
            "{:<20} {:<10} {:>7.2f} {:>7.2f} {:>7.2f} {:>9.2f} {:>6}".format(
                record["name"],
                record["id"],
                record["test1"],
                record["test2"],
                record["test3"],
                record["average"],
                record["grade"],
            )
        )


def display_class_statistics(records):
    if not records:
        print("\nNo records available to calculate statistics.")
        return

    averages = [record["average"] for record in records]
    highest = max(averages)
    lowest = min(averages)
    class_average = sum(averages) / len(averages)

    print("\nClass Statistics")
    print(f"Highest average: {highest:.2f}")
    print(f"Lowest average:  {lowest:.2f}")
    print(f"Class average:   {class_average:.2f}")


def search_student_by_name(records):
    if not records:
        print("\nNo student records available.")
        return

    name_search = input("Enter student name to search: ").strip()
    if name_search.upper() == "ESC":
        return

    matches = [record for record in records if name_search.lower() in record["name"].lower()]
    if not matches:
        print(f"No students found matching '{name_search}'.")
        return

    print(f"\nSearch results for '{name_search}':")
    print("{:<20} {:<10} {:>7} {:>7} {:>7} {:>9} {:>6}".format(
        "Name", "ID", "Test1", "Test2", "Test3", "Average", "Grade"
    ))
    print("-" * 72)
    for record in matches:
        print(
            "{:<20} {:<10} {:>7.2f} {:>7.2f} {:>7.2f} {:>9.2f} {:>6}".format(
                record["name"],
                record["id"],
                record["test1"],
                record["test2"],
                record["test3"],
                record["average"],
                record["grade"],
            )
        )


def show_menu():
    print("\nStudent Grade Calculator")
    print("1. Add new student record")
    print("2. Display all student records")
    print("3. Display class statistics")
    print("4. Search for student by name")
    print("5. Exit (type ESC or 5)")


def main():
    global student_records
    student_records = load_student_records()
    print("Loaded", len(student_records), "student records.")

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()
        if not choice:
            continue
        if choice.upper() == "ESC" or choice == "5":
            print("Exiting Student Grade Calculator. Goodbye!")
            save_student_records(student_records)
            break
        if choice == "1":
            add_student_record(student_records)
        elif choice == "2":
            display_student_records(student_records)
        elif choice == "3":
            display_class_statistics(student_records)
        elif choice == "4":
            search_student_by_name(student_records)
        else:
            print("Invalid option. Please enter 1-5 or ESC.")


if __name__ == "__main__":
    main()
