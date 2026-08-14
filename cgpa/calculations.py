GRADE_POINTS = {
    "O": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C": 5,
    "RA": 0
}


def calculate_sgpa(subjects):

    total_points = 0
    total_credits = 0

    for subject in subjects:

        grade = subject["grade"]
        credit = subject["credit"]

        grade_point = GRADE_POINTS[grade]

        total_points += grade_point * credit
        total_credits += credit

    if total_credits == 0:
        return 0

    return total_points / total_credits


def calculate_cgpa(sgpa_list):

    if len(sgpa_list) == 0:
        return 0

    return sum(sgpa_list) / len(sgpa_list)
