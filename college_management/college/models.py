from django.db import models


class Department(models.Model):
    """Engineering departments."""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    hod = models.CharField(max_length=100, blank=True, verbose_name='Head of Department')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Student(models.Model):
    """Maps to the original C# New_Admission table."""
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    SEMESTER_CHOICES = [(f'{i}', f'{i}') for i in range(1, 9)]

    full_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField(verbose_name='Date of Birth')
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    program = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    school_name = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.id} - {self.full_name}"




class Teacher(models.Model):
    """Maps to the original C# Teacher table."""
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]

    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField(verbose_name='Date of Birth')
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    program = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')
    semester = models.CharField(max_length=20, blank=True)
    duration = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.id} - {self.full_name}"


class Subject(models.Model):
    """Subjects/Courses per department per semester."""
    code = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=150)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    semester = models.CharField(max_length=5, choices=[(f'{i}', f'{i}') for i in range(1, 9)])
    credits = models.PositiveIntegerField(default=3)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')

    class Meta:
        ordering = ['department', 'semester', 'code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Attendance(models.Model):
    """Daily attendance per student per subject."""
    STATUS_CHOICES = [('Present', 'Present'), ('Absent', 'Absent')]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')

    class Meta:
        ordering = ['-date']
        unique_together = ['student', 'subject', 'date']

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.code} - {self.date} - {self.status}"


class ExamResult(models.Model):
    """Exam marks per student per subject."""
    EXAM_CHOICES = [
        ('Internal 1', 'Internal 1'),
        ('Internal 2', 'Internal 2'),
        ('Mid Sem', 'Mid Semester'),
        ('End Sem', 'End Semester'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='results')
    exam_type = models.CharField(max_length=20, choices=EXAM_CHOICES)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    grade = models.CharField(max_length=2, blank=True)

    class Meta:
        ordering = ['-id']
        unique_together = ['student', 'subject', 'exam_type']

    def save(self, *args, **kwargs):
        pct = (self.marks_obtained / self.max_marks) * 100 if self.max_marks else 0
        if pct >= 90: self.grade = 'O'
        elif pct >= 80: self.grade = 'A+'
        elif pct >= 70: self.grade = 'A'
        elif pct >= 60: self.grade = 'B+'
        elif pct >= 50: self.grade = 'B'
        elif pct >= 40: self.grade = 'C'
        else: self.grade = 'F'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.code} - {self.exam_type}: {self.marks_obtained}/{self.max_marks}"


class Notice(models.Model):
    """College-wide announcements."""
    PRIORITY_CHOICES = [('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Urgent', 'Urgent')]

    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    posted_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.priority}] {self.title}"


class Book(models.Model):
    """Library book catalog."""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20, unique=True, verbose_name='ISBN')
    publisher = models.CharField(max_length=150, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    available = models.PositiveIntegerField(default=1)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} by {self.author}"


class BookIssue(models.Model):
    """Library book issue/return tracking."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='book_issues')
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        status = 'Returned' if self.is_returned else 'Issued'
        return f"{self.book.title} → {self.student.full_name} ({status})"
