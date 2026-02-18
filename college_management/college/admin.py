from django.contrib import admin
from .models import (
    Student, Teacher, Department, Subject,
    Attendance, ExamResult, Notice, Book, BookIssue,
)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'semester', 'program', 'department', 'mobile', 'email']
    search_fields = ['full_name', 'email', 'mobile']
    list_filter = ['semester', 'gender', 'department']




@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'program', 'department', 'mobile', 'email']
    search_fields = ['full_name', 'email']
    list_filter = ['department']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'hod']
    search_fields = ['name', 'code']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department', 'semester', 'credits', 'teacher']
    search_fields = ['name', 'code']
    list_filter = ['department', 'semester']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'date', 'status']
    list_filter = ['status', 'date', 'subject']


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'exam_type', 'marks_obtained', 'max_marks', 'grade']
    list_filter = ['exam_type', 'grade', 'subject']


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'posted_by', 'created_at']
    list_filter = ['priority']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'quantity', 'available', 'department']
    search_fields = ['title', 'author', 'isbn']


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ['book', 'student', 'issue_date', 'due_date', 'return_date', 'is_returned']
    list_filter = ['is_returned']
