# Cardio Chatbot

This is a Django-based application for the Cardio Chatbot project, designed to provide conversational AI for answering questions and offering guidance related to cardiac health.

## Features

- Conversational AI using a chatbot interface.
- Cardiac health-related insights and information.
- Backend built with Django for scalability and ease of use.

## Prerequisites

Before setting up the project, ensure you have the following installed:

- Python (>= 3.11)
- Django (>= 5.0)
- pip (Python package manager)
- A virtual environment manager (e.g., `venv` or `virtualenv`)

## Setup

1. **Clone the Repository**  
   Clone the project to your local machine:
   ```bash
   git clone https://github.com/Rapid-Labs-AI/Cardio-Chatbot.git
   cd Cardio-Chatbot

2. Create and activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```
3. Install the required Python packages

```bash
pip install -r requirements.txt
```
4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run the Development Server

```bash
python manage.py runserver
```


Access the application at http://127.0.0.1:8000.
