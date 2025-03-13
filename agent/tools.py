from langchain_core.tools import tool

@tool
def check_gpa(student_id: str) -> str:
    """ONLY use this tool when the user explicitly asks for their GPA, grades, or academic performance.
    Do NOT use for general conversation, greetings, or unrelated questions.
    Returns a static GPA for demonstration purposes.
    """
    gpa_map = {
        "1": 3.8,
        "2": 3.5,
        "3": 4.0,
        "4": 3.2,
        "5": 3.9
    }

    if student_id in gpa_map:
        return f"Student with ID {student_id} has a GPA of {gpa_map[student_id]}."
    else:
        return f"Student with ID {student_id} has a GPA of 3.7 (demo data)."

@tool
def get_name(student_id: str) -> str:
    """ONLY use this tool when the user explicitly asks for their name or identity verification.
    Do NOT use for general conversation, greetings, or unrelated questions.
    Returns a static name for demonstration purposes.
    """
    name_map = {
        "1": "John Smith",
        "2": "Emma Johnson",
        "3": "Michael Brown",
        "4": "Sophia Davis",
        "5": "James Wilson"
    }

    if student_id in name_map:
        return f"Student with ID {student_id} has name: {name_map[student_id]}."
    else:
        return f"Student with ID {student_id} has name: Demo Student."
