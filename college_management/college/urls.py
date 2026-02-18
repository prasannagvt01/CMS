from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Student Management
    path('new-admission/', views.new_admission, name='new_admission'),
    path('search-student/', views.search_student, name='search_student'),
    path('student-detail/', views.student_detail, name='student_detail'),
    path('upgrade-semester/', views.upgrade_semester, name='upgrade_semester'),
    path('remove-student/', views.remove_student, name='remove_student'),


    # Faculty
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('search-teacher/', views.search_teacher, name='search_teacher'),

    # Departments
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.add_department, name='add_department'),

    # Subjects
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.add_subject, name='add_subject'),

    # Attendance
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/view/', views.view_attendance, name='view_attendance'),

    # Exam Results
    path('results/add/', views.add_result, name='add_result'),
    path('results/view/', views.view_results, name='view_results'),

    # Notices
    path('notices/', views.notice_board, name='notice_board'),
    path('notices/add/', views.add_notice, name='add_notice'),

    # Library
    path('library/', views.library_catalog, name='library_catalog'),
    path('library/add/', views.add_book, name='add_book'),
    path('library/issue/', views.issue_book, name='issue_book'),
    path('library/return/<int:issue_id>/', views.return_book, name='return_book'),

    # About
    path('about/', views.about, name='about'),
]
