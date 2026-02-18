from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Sum, Q
from datetime import date

from .models import (
    Student, Teacher, Department, Subject,
    Attendance, ExamResult, Notice, Book, BookIssue,
)
from .forms import (
    RegisterForm, StudentForm, TeacherForm,
    UpgradeSemesterForm, DepartmentForm, SubjectForm,
    AttendanceForm, ExamResultForm, NoticeForm,
    BookForm, BookIssueForm,
)


# ──────────────────── Authentication ────────────────────────────

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


# ──────────────────── Dashboard ─────────────────────────────────

@login_required
def dashboard(request):
    context = {
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'total_departments': Department.objects.count(),
        'total_subjects': Subject.objects.count(),
        'total_books': Book.objects.count(),
        'recent_notices': Notice.objects.all()[:3],
        'pending_returns': BookIssue.objects.filter(is_returned=False).count(),
    }
    return render(request, 'college/dashboard.html', context)


# ──────────────────── Student Management ────────────────────────

@login_required
def new_admission(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student "{student.full_name}" admitted! (ID: {student.id})')
            return redirect('new_admission')
    else:
        form = StudentForm()
    return render(request, 'college/new_admission.html', {'form': form})


@login_required
def search_student(request):
    query = request.GET.get('q', '')
    students = Student.objects.filter(id=query) if query else Student.objects.all()
    return render(request, 'college/search_student.html', {'students': students, 'query': query})


@login_required
def student_detail(request):
    query = request.GET.get('q', '')
    student = None
    if query:
        try:
            student = Student.objects.get(id=query)
        except Student.DoesNotExist:
            pass
    return render(request, 'college/student_detail.html', {'student': student, 'query': query})


@login_required
def upgrade_semester(request):
    form = UpgradeSemesterForm()
    if request.method == 'POST':
        form = UpgradeSemesterForm(request.POST)
        if form.is_valid():
            from_sem = form.cleaned_data['from_semester']
            to_sem = form.cleaned_data['to_semester']
            count = Student.objects.filter(semester=from_sem).update(semester=to_sem)
            messages.success(request, f'{count} students upgraded from Semester {from_sem} to {to_sem}.')
            return redirect('upgrade_semester')
    return render(request, 'college/upgrade_semester.html', {'form': form})


@login_required
def remove_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        try:
            student = Student.objects.get(id=student_id)
            name = student.full_name
            student.delete()
            messages.success(request, f'Student "{name}" (ID: {student_id}) removed.')
        except Student.DoesNotExist:
            messages.error(request, f'No student found with ID: {student_id}')
        return redirect('remove_student')
    students = Student.objects.all()
    return render(request, 'college/remove_student.html', {'students': students})




# ──────────────────── Faculty ───────────────────────────────────

@login_required
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f'Teacher "{teacher.full_name}" added!')
            return redirect('add_teacher')
    else:
        form = TeacherForm()
    return render(request, 'college/add_teacher.html', {'form': form})


@login_required
def search_teacher(request):
    query = request.GET.get('q', '')
    teachers = Teacher.objects.filter(id=query) if query else Teacher.objects.all()
    return render(request, 'college/search_teacher.html', {'teachers': teachers, 'query': query})


# ──────────────────── Department Management ─────────────────────

@login_required
def department_list(request):
    departments = Department.objects.annotate(
        student_count=Count('students'),
        teacher_count=Count('teachers'),
        subject_count=Count('subjects'),
    )
    return render(request, 'college/department_list.html', {'departments': departments})


@login_required
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save()
            messages.success(request, f'Department "{dept.name}" created!')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'college/add_department.html', {'form': form})


# ──────────────────── Subject Management ────────────────────────

@login_required
def subject_list(request):
    dept_filter = request.GET.get('dept', '')
    subjects = Subject.objects.select_related('department', 'teacher')
    if dept_filter:
        subjects = subjects.filter(department_id=dept_filter)
    departments = Department.objects.all()
    return render(request, 'college/subject_list.html', {
        'subjects': subjects, 'departments': departments, 'dept_filter': dept_filter,
    })


@login_required
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subj = form.save()
            messages.success(request, f'Subject "{subj.name}" added!')
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'college/add_subject.html', {'form': form})


# ──────────────────── Attendance ────────────────────────────────

@login_required
def mark_attendance(request):
    students = []
    subject = None
    att_date = None

    if request.method == 'POST' and 'save_attendance' in request.POST:
        subject_id = request.POST.get('subject_id')
        att_date = request.POST.get('att_date')
        subject = get_object_or_404(Subject, id=subject_id)
        student_ids = Student.objects.filter(
            semester=subject.semester,
            department=subject.department
        ).values_list('id', flat=True)

        for sid in student_ids:
            status = request.POST.get(f'status_{sid}', 'Absent')
            Attendance.objects.update_or_create(
                student_id=sid, subject=subject, date=att_date,
                defaults={'status': status}
            )
        messages.success(request, f'Attendance saved for {subject.name} on {att_date}.')
        return redirect('mark_attendance')

    form = AttendanceForm(request.GET or None)
    if form.is_valid():
        subject = form.cleaned_data['subject']
        att_date = form.cleaned_data['date']
        students = Student.objects.filter(
            semester=subject.semester,
            department=subject.department
        )
        # Get existing attendance
        existing = Attendance.objects.filter(
            subject=subject, date=att_date
        ).values_list('student_id', 'status')
        existing_dict = dict(existing)
        for s in students:
            s.att_status = existing_dict.get(s.id, 'Present')

    return render(request, 'college/mark_attendance.html', {
        'form': form, 'students': students, 'subject': subject, 'att_date': att_date,
    })


@login_required
def view_attendance(request):
    query = request.GET.get('q', '')
    student = None
    records = []
    summary = {}

    if query:
        try:
            student = Student.objects.get(id=query)
            records = Attendance.objects.filter(student=student).select_related('subject')
            subjects = records.values('subject__name').annotate(
                total=Count('id'),
                present=Count('id', filter=Q(status='Present'))
            )
            for s in subjects:
                total = s['total']
                present = s['present']
                s['percentage'] = round((present / total) * 100, 1) if total > 0 else 0
            summary = subjects
        except Student.DoesNotExist:
            pass

    return render(request, 'college/view_attendance.html', {
        'student': student, 'records': records, 'summary': summary, 'query': query,
    })


# ──────────────────── Exam Results ──────────────────────────────

@login_required
def add_result(request):
    if request.method == 'POST':
        form = ExamResultForm(request.POST)
        if form.is_valid():
            result = form.save()
            messages.success(request, f'Result saved: {result.student.full_name} — {result.subject.name} — {result.grade}')
            return redirect('add_result')
    else:
        form = ExamResultForm()
    return render(request, 'college/add_result.html', {'form': form})


@login_required
def view_results(request):
    query = request.GET.get('q', '')
    student = None
    results = []
    gpa = None

    if query:
        try:
            student = Student.objects.get(id=query)
            results = ExamResult.objects.filter(student=student).select_related('subject')

            # Calculate GPA (10-point scale)
            grade_points = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'F': 0}
            total_credits = 0
            weighted_sum = 0
            for r in results:
                credits = r.subject.credits
                gp = grade_points.get(r.grade, 0)
                weighted_sum += gp * credits
                total_credits += credits
            gpa = round(weighted_sum / total_credits, 2) if total_credits > 0 else 0
        except Student.DoesNotExist:
            pass

    return render(request, 'college/view_results.html', {
        'student': student, 'results': results, 'gpa': gpa, 'query': query,
    })


# ──────────────────── Notice Board ──────────────────────────────

@login_required
def notice_board(request):
    notices = Notice.objects.all()
    return render(request, 'college/notice_board.html', {'notices': notices})


@login_required
def add_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice published!')
            return redirect('notice_board')
    else:
        form = NoticeForm()
    return render(request, 'college/add_notice.html', {'form': form})


# ──────────────────── Library ───────────────────────────────────

@login_required
def library_catalog(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query) | Q(isbn__icontains=query))
    else:
        books = Book.objects.all()
    return render(request, 'college/library_catalog.html', {'books': books, 'query': query})


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added to catalog!')
            return redirect('library_catalog')
    else:
        form = BookForm()
    return render(request, 'college/add_book.html', {'form': form})


@login_required
def issue_book(request):
    if request.method == 'POST':
        form = BookIssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            book = issue.book
            if book.available > 0:
                book.available -= 1
                book.save()
                issue.save()
                messages.success(request, f'Book "{book.title}" issued to {issue.student.full_name}.')
            else:
                messages.error(request, f'Book "{book.title}" is not available.')
            return redirect('issue_book')
    else:
        form = BookIssueForm()
    issued = BookIssue.objects.filter(is_returned=False).select_related('book', 'student')
    return render(request, 'college/issue_book.html', {
        'form': form, 'issued': issued, 'today': date.today()
    })


@login_required
def return_book(request, issue_id):
    issue = get_object_or_404(BookIssue, id=issue_id)
    if not issue.is_returned:
        issue.is_returned = True
        issue.return_date = date.today()
        issue.save()
        book = issue.book
        book.available += 1
        book.save()
        messages.success(request, f'Book "{book.title}" returned by {issue.student.full_name}.')
    return redirect('issue_book')


# ──────────────────── About ─────────────────────────────────────

@login_required
def about(request):
    return render(request, 'college/about.html')
