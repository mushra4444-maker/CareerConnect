
# CareerConnect - Python Full Stack Job Portal

CareerConnect is a Django-based job portal that connects job seekers with employers.

## Features

### Candidate
- Candidate registration and login
- Browse available jobs
- Apply for jobs
- Upload PDF resumes
- Manage applications
- Create and update candidate profiles
- View interview schedules

### Employer
- Employer registration and login
- Post new jobs
- Edit and manage job postings
- View candidate applications
- Search and filter applications
- Update application status
- View candidate profiles
- Schedule interviews
- Reschedule and cancel interviews

## Technologies Used

- Python
- Django
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- SQLite
- Pillow

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mushra4444-maker/CareerConnect.git
```

### 2. Open the project folder

```bash
cd CareerConnect
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open:

http://127.0.0.1:8000/

## Project Structure

```text
CareerConnect/
│
├── config/
├── useraccounts/
├── jobportal/
├── jobapplications/
├── templates/
├── static/
├── media/
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Developer

GitHub: https://github.com/mushra4444-maker

## License

This project is created for educational and portfolio purposes.
