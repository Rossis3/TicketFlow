# 🎫 TicketFlow

A lightweight issue tracking web app built with Flask, designed for small teams.

## Features

- User registration and login
- Create, assign, and prioritize tickets
- Status workflow: Open → In Progress → Resolved → Closed
- Comments on tickets
- Activity log for every ticket

## Tech Stack

- Python 3.10+
- Flask
- SQLite + SQLAlchemy
- Flask-Login + bcrypt
- pytest

## Setup

1. Clone the repo:

```bash
git clone https://github.com/YOUR_USERNAME/TicketFlow.git
cd TicketFlow
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up the database:

```bash
python setup_db.py
```

5. Run the app:

```bash
python run.py
```

6. Open your browser and go to `http://127.0.0.1:5000`

> **Note:** This runs locally on your machine. For production deployment, see Flask's deployment docs.

## Project Structure

```
TicketFlow/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── main.py
│   │   └── tickets.py
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── new_ticket.html
│       ├── view_ticket.html
│       ├── 404.html
│       └── 500.html
├── config.py
├── run.py
├── setup_db.py
├── requirements.txt
└── README.md
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.