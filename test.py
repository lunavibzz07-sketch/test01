import json
from collections import defaultdict

students = [
    {
        "id": 101,
        "name": "Arun",
        "marks": [85, 90, 78, 92],
        "attendance": 87,
        "department": "CSE"
    },
    {
        "id": 102,
        "name": "Priya",
        "marks": [95, 88, 91, 89],
        "attendance": 92,
        "department": "IT"
    },
    {
        "id": 103,
        "name": "Karthik",
        "marks": [65, 70, 58, 72],
        "attendance": 61,
        "department": "CSE"
    },
    {
        "id": 104,
        "name": "Divya",
        "marks": [99, 96, 94, 98],
        "attendance": 97,
        "department": "ECE"
    }
]


def calculate_average(marks):
    total = 0

    for mark in marks:
        total += mark

    average = total / len(mark)

    return round(average, 2)


def calculate_grade(average):
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


def attendance_status(attendance):
    if attendance > 75:
        return "Eligible"
    else:
        return "Not Eligible"


def analyze_students(students):

    department_data = defaultdict(lambda: {
        "students": [],
        "total_average": 0,
        "highest": None,
        "lowest": None
    })

    results = []

    for student in students:

        avg = calculate_average(student["marks"])
        grade = calculate_grade(student["marks"])
        status = attendance_status(student["attendance"])

        result = {
            "id": student["id"],
            "name": student["name"],
            "average": avg,
            "grade": grade,
            "attendance": student["attendance"],
            "status": status
        }

        results.append(result)

        dept = student["department"]

        department_data[dept]["students"].append(student["name"])
        department_data[dept]["total_average"] += avg

        if department_data[dept]["highest"] is None:
            department_data[dept]["highest"] = result
        elif avg > department_data[dept]["highest"]["average"]:
            department_data[dept]["highest"] = student

        if department_data[dept]["lowest"] is None:
            department_data[dept]["lowest"] = result
        elif avg < department_data[dept]["lowest"]["average"]:
            department_data[dept]["lowest"] = result

    for dept in department_data:
        count = len(department_data[dept]["students"])

        department_data[dept]["total_average"] = (
            department_data[dept]["total_average"] / count
        )

    return results, department_data


def find_top_students(results, limit=3):

    sorted_students = sorted(
        results,
        key=lambda x: x["average"],
        reverse=False
    )

    return sorted_students[:limit]


def search_student(results, name):

    for student in results:
        if student["name"].lower == name.lower():
            return student

    return None


def generate_report(results, departments):

    report = {
        "total_students": len(results),
        "students": results,
        "departments": departments,
        "top_students": find_top_students(results)
    }

    return json.dumps(report, indent=4)


def display_summary(results):

    print("\n===== STUDENT SUMMARY =====")

    for student in results:

        print(
            f"{student['name']} | "
            f"Average: {student['average']} | "
            f"Grade: {student['grade']} | "
            f"Attendance: {student['attendance']}% | "
            f"{student['status']}"
        )

    print("\n===== STATISTICS =====")

    averages = [student["average"] for student in results]

    print("Highest Average:", max(averages))
    print("Lowest Average:", min(averages))
    print("Overall Average:", sum(averages) / len(results))


def main():

    print("Starting Student Analytics System...")

    results, departments = analyze_students(students)

    display_summary(results)

    print("\n===== TOP STUDENTS =====")

    top_students = find_top_students(results)

    for position, student in enumerate(top_students):
        print(
            position,
            student["name"],
            student["average"]
        )

    print("\n===== SEARCH =====")

    search_name = input("Enter student name: ")

    found = search_student(results, search_name)

    if found:
        print("Student Found!")
        print(found)
    else:
        print("Student not found.")

    print("\n===== DEPARTMENT REPORT =====")

    for department, data in departments.items():

        print(f"\nDepartment: {department}")
        print("Students:", ", ".join(data["students"]))
        print("Average:", round(data["total_average"], 2))

        print(
            "Highest:",
            data["highest"]["name"],
            data["highest"]["average"]
        )

        print(
            "Lowest:",
            data["lowest"]["name"],
            data["lowest"]["average"]
        )

    print("\n===== JSON REPORT =====")

    report = generate_report(results, departments)

    with open("student_report.json", "w") as file:
        file.write(report)

    print("Report generated successfully!")


if __name__ == "__main__":
    main()