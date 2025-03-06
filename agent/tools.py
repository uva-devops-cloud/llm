from langchain_core.tools import tool
import os
import pg8000

@tool
def check_gpa(student_id: str) -> str:
    """ONLY use this tool when the user explicitly asks for their GPA, grades, or academic performance.
          Do NOT use for general conversation, greetings, or unrelated questions.
          Queries the database to retrieve a student's GPA given their student ID.
          """
    conn = pg8000.connect(
        host=os.getenv('PGHOST'),
        user=os.getenv('PGUSER'),
        password=os.getenv("PGPASSWORD"),
        port=int(os.getenv("PGPORT", "5432")),  # Pass as string with default
        database=os.getenv("PGDATABASE", "mydb")
    )
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT gpa FROM students WHERE id = %s", (student_id,))
            row = cur.fetchone()
            if row:
                return f"Student with ID {student_id} has a gpa of {row[0]}."
            else:
                return f"No record found for student with ID: {student_id}"
    finally:
        conn.close()


@tool
def get_name(student_id: str) -> str:
    """ONLY use this tool when the user explicitly asks for their name or identity verification.
    Do NOT use for general conversation, greetings, or unrelated questions.
    Queries the database to retrieve a student's name given their student ID.
    """
    conn = pg8000.connect(
        host=os.getenv('PGHOST'),
        user=os.getenv('PGUSER'),
        password=os.getenv("PGPASSWORD"),
        port=int(os.getenv("PGPORT", "5432")),  # Pass as string with default
        database=os.getenv("PGDATABASE", "mydb")
    )
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT name FROM students WHERE id = %s", (student_id,))
            row = cur.fetchone()
            if row:
                return f"Student with ID {student_id} has name: {row[0]}."
            else:
                return f"No record found for student with ID: {student_id}"
    finally:
        conn.close()
