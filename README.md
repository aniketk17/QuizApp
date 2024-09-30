# ThinkGuru

## Overview
ThinkGuru is an interactive learning platform designed to enhance knowledge acquisition and retention through engaging quizzes, articles, and discussion forums. It aims to foster a community of learners and educators by providing a space for collaboration and knowledge sharing.

## Features
- **Interactive Quizzes**: Users can take quizzes on various topics to test their knowledge.
- **Articles & Resources**: Access a library of articles to deepen understanding.
- **Discussion Forums**: Engage in discussions with peers and educators.
- **User Profiles**: Personalized profiles to track learning progress and achievements.

## Technologies Used
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (or PostgreSQL/MySQL)
- **Authentication**: Django’s built-in authentication system

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/aniketk17/ThinkGuru.git

2. Create Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
 
3. Install Dependencies:
   ```bash
   pip install -r requirements.txt

4. Apply Database migrations:
   ```bash
   python manage.py migrate
   python manage.py makemigrations

5. Create a superuser to access the admin dashboard:
   ```bash
   python manage.py createsuperuser

7. Start the Development Server:
   ```bash
   python manage.py runserver


   
