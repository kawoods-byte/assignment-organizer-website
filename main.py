
from drafter import *
from dataclasses import dataclass


# --------------------------------
# DATA CLASSES
# --------------------------------

@dataclass
class Assignment:
    name: str
    course_name: str
    urgency: int
    current_grade: str
    days_until_due: int
    course_credits: int
    completion_time: float
    difficult: bool


@dataclass
class State:
    assignments: list[Assignment]
    completed_assignments: int
    student_name: str
    last_updated: str
    current_page: str


# --------------------------------
# URGENCY CALCULATION
# --------------------------------

def calculate_urgency(assignment: Assignment) -> int:
    score = 0

    if assignment.days_until_due <= 2:
        score += 10

    if assignment.days_until_due <= 5:
        score += 5

    if assignment.difficult:
        score += 5

    if assignment.completion_time >= 3:
        score += 3

    assignment.urgency = score

    return score


# --------------------------------
# HOME PAGE
# --------------------------------

@route
def index(state: State) -> Page:
    state.current_page = "Home"

    return Page(state, [
        Header("Student Assignment Planner"),

        "Welcome, " + state.student_name + "!",

        "Stay organized and know which assignments to complete first.",

        Button("Go to Dashboard", "dashboard"),

        Button("Scoring Guide", "scoring_guide"),

        Button("Add Assignment", "add_assignment")
    ])


# --------------------------------
# DASHBOARD
# --------------------------------

@route
def dashboard(state: State) -> Page:
    state.current_page = "Dashboard"

    # Calculate urgency for each assignment
    for assignment in state.assignments:
        calculate_urgency(assignment)

    # Sort from highest urgency to lowest
    state.assignments.sort(
        key=calculate_urgency,
        reverse=True
    )

    content = [
        Header("Assignment Dashboard"),

        "Here are your assignments, ranked by urgency:",

        "Completed assignments: " + str(state.completed_assignments)
    ]

    # Display all assignments
    for assignment in state.assignments:

        content.append(Header(assignment.name))

        content.append("Course: " + assignment.course_name)

        content.append(
            "Days until due: " + str(assignment.days_until_due)
        )

        content.append(
            "Urgency score: " + str(assignment.urgency)
        )

        content.append(
            "Difficult: " + str(assignment.difficult)
        )

        content.append(
            Button(
                "Mark Complete",
                "complete_assignment",
                Argument("assignment_name", assignment.name)
            )
        )

        content.append("------------------------------")

    content.append(Button("Add Assignment", "add_assignment"))

    content.append(Button("Home", "index"))

    content.append(Button("Scoring Guide", "scoring_guide"))

    return Page(state, content)


# --------------------------------
# ADD ASSIGNMENT PAGE
# --------------------------------

@route
def add_assignment(state: State) -> Page:
    state.current_page = "Add Assignment"

    return Page(state, [
        Header("Add a New Assignment"),

        "Assignment name:",
        TextBox("name"),

        "Course name:",
        TextBox("course_name"),

        "Current course grade:",

        # CHANGED TO A DROPDOWN MENU
        SelectBox("current_grade", [
            "A", "B", "C", "D", "F"
        ]),

        "Days until due:",
        TextBox("days_until_due"),

        "Course credits:",
        TextBox("course_credits"),

        "Expected completion time (hours):",
        TextBox("completion_time"),

        "Is this assignment difficult?",
        CheckBox("difficult"),

        Button("Save Assignment", "save_assignment"),

        Button("Back to Dashboard", "dashboard")
    ])


# --------------------------------
# SAVE ASSIGNMENT
# --------------------------------

@route
def save_assignment(
    state: State,
    name: str,
    course_name: str,
    current_grade: str,
    days_until_due: int,
    course_credits: int,
    completion_time: float,
    difficult: bool
) -> Page:

    new_assignment = Assignment(
        name,
        course_name,
        0,
        current_grade,
        days_until_due,
        course_credits,
        completion_time,
        difficult
    )

    state.assignments.append(new_assignment)

    return dashboard(state)


# --------------------------------
# SCORING GUIDE
# --------------------------------

@route
def scoring_guide(state: State) -> Page:
    state.current_page = "Scoring Guide"

    return Page(state, [
        Header("How Urgency Is Calculated"),

        "Your assignments receive points based on several factors.",

        "Due within 2 days: +10 points",

        "Due within 5 days: +5 points",

        "Difficult assignment: +5 points",

        "Takes 3 or more hours: +3 points",

        "The higher the score, the more urgent the assignment.",

        Button("Back to Dashboard", "dashboard"),

        Button("Home", "index")
    ])


# --------------------------------
# COMPLETE ASSIGNMENT
# --------------------------------

@route
def complete_assignment(
    state: State,
    assignment_name: str
) -> Page:

    for assignment in state.assignments:

        if assignment.name == assignment_name:

            state.assignments.remove(assignment)

            state.completed_assignments += 1

            break

    return dashboard(state)


# --------------------------------
# START WEBSITE
# --------------------------------

start_server(
    State(
        assignments=[],
        completed_assignments=0,
        student_name="Student",
        last_updated="Not updated yet",
        current_page="Home"
    )
)
