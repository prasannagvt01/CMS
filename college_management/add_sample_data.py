import os
import django
from datetime import date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_management.settings')
django.setup()

from college.models import Department, Subject, Teacher, Student, Book, Notice

def add_sample_data():
    print("Adding sample data...")

    # 1. Departments
    cs, _ = Department.objects.get_or_create(name="Computer Science", code="CS", hod="Dr. Alan Turing")
    me, _ = Department.objects.get_or_create(name="Mechanical Engineering", code="ME", hod="Dr. Nikola Tesla")
    ee, _ = Department.objects.get_or_create(name="Electrical Engineering", code="EE", hod="Dr. Thomas Edison")

    # 2. Teachers
    t1, _ = Teacher.objects.get_or_create(
        full_name="Prof. John Doe", 
        email="john@example.com", 
        department=cs,
        gender="Male",
        dob="1980-01-01",
        mobile="1234567890"
    )

    # 3. Subjects
    Subject.objects.get_or_create(code="CS101", name="Data Structures", department=cs, semester="1", credits=4, teacher=t1)
    Subject.objects.get_or_create(code="CS202", name="Operating Systems", department=cs, semester="2", credits=4, teacher=t1)
    Subject.objects.get_or_create(code="ME101", name="Thermodynamics", department=me, semester="1", credits=3)

    # 4. Books
    Book.objects.get_or_create(title="Clean Code", author="Robert C. Martin", isbn="978-0132350884", quantity=5, available=5, department=cs)
    Book.objects.get_or_create(title="The Pragmatic Programmer", author="Andrew Hunt", isbn="978-0201616224", quantity=3, available=3, department=cs)

    # 5. Notices
    Notice.objects.get_or_create(
        title="Annual Tech Fest 2026", 
        content="The annual technical festival will be held on March 15th. All students are invited to participate.",
        priority="High",
        posted_by="Administrative Office"
    )
    Notice.objects.get_or_create(
        title="Mid-Term Exams Schedule", 
        content="Mid-term exams for all semesters will start from March 1st. Check the detailed schedule on the board.",
        priority="Urgent",
        posted_by="Academic Cell"
    )

    print("Sample data added successfully!")

if __name__ == "__main__":
    add_sample_data()
