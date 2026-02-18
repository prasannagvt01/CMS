# College Management System (CMS)

A comprehensive web-based application for managing college operations, including students, teachers, departments, attendance, and library services. Built with Python and Django.

## 🚀 Features

- **Dashboard**: Overview of total students, teachers, departments, and subjects.
- **Student Management**: Add, view, update, and remove student records.
- **Teacher Management**: Maintain teacher profiles and departmental assignments.
- **Department & Subjects**: Organize academic structures with departments and associated subjects.
- **Attendance System**: Mark and view student attendance records.
- **Result Management**: Record and track student examination results.
- **Library Management**: Manage books, track issued books, and maintain library catalog.
- **Notice Board**: Post and view important announcements.
- **Fee Management**: Track student fee payments and status.

## 🛠️ Tech Stack

- **Backend**: Django 5.2 (Python)
- **Database**: SQLite (Development) / PostgreSQL (Production ready)
- **Frontend**: HTML5, CSS3, JavaScript (Bootstrap/Custom CSS)
- **Static Files**: Whitenoise for efficient static file serving

## ⚙️ Installation

### Prerequisites

- Python 3.10 or higher
- Git

### Steps

1.  **Clone the repository**
    ```bash
    git clone https://github.com/prasannagvt01/CMS.git
    cd CMS
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    
    # On Windows
    venv\Scripts\activate
    
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    cd college_management
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**
    - Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    - Open `.env` and configure your settings (DEBUG, SECRET_KEY).

5.  **Run migrations**
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser** (for admin access)
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server**
    ```bash
    python manage.py runserver
    ```

    Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## 📦 Deployment

The project is configured for deployment on platforms like Heroku, Render, or Railway.

1.  Ensure `PROCFILE` and `requirements.txt` are present (they are included).
2.  Set `DEBUG=False` and `SECRET_KEY` in your production environment variables.
3.  Connect your repository to your hosting provider and deploy.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
