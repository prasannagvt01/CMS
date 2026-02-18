from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    Student, Teacher, Department, Subject,
    Attendance, ExamResult, Notice, Book, BookIssue,
)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'full_name', 'mother_name', 'gender', 'dob', 'mobile',
            'email', 'semester', 'program', 'department', 'school_name',
            'duration', 'address',
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.RadioSelect(choices=Student.GENDER_CHOICES),
            'address': forms.Textarea(attrs={'rows': 3}),
        }




class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'full_name', 'gender', 'dob', 'mobile', 'email',
            'program', 'department', 'semester', 'duration', 'address',
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.RadioSelect(choices=Teacher.GENDER_CHOICES),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class UpgradeSemesterForm(forms.Form):
    SEMESTER_CHOICES = [(f'{i}', f'Semester {i}') for i in range(1, 9)]
    from_semester = forms.ChoiceField(choices=SEMESTER_CHOICES, label='From Semester')
    to_semester = forms.ChoiceField(choices=SEMESTER_CHOICES, label='To Semester')


# ──────────────────── Advanced Feature Forms ────────────────────

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'hod', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['code', 'name', 'department', 'semester', 'credits', 'teacher']


class AttendanceForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), label='Subject')
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Date')


class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = ['student', 'subject', 'exam_type', 'marks_obtained', 'max_marks']


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'priority', 'posted_by']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publisher', 'quantity', 'available', 'department']


class BookIssueForm(forms.ModelForm):
    class Meta:
        model = BookIssue
        fields = ['book', 'student', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
