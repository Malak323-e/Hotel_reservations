# Installation Guide

## Prerequisites

- [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed on your machine
- Git (to clone the repository)

## Steps

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/hotel_reservation.git
cd hotel_reservation
```

### 2. Create the conda environment

```bash
conda create -n python_3_11_13 python=3.11
conda activate python_3_11_13
```

### 3. Install dependencies

```bash
conda run -n python_3_11_13 pip install -r requirements.txt
```

### 4. Seed the database

Populate the database with sample data (rooms, restaurant tables, meeting rooms):

```bash
conda run -n python_3_11_13 python seed.py
```

Expected output:
```
✓ 6 chambres ajoutées
✓ 8 tables de restaurant ajoutées
✓ 4 salles de réunion ajoutées
Base de données initialisée avec succès.
```

> `seed.py` is idempotent — running it multiple times will not duplicate data.

### 5. Start the development server

```bash
conda run -n python_3_11_13 python run.py
```

The application will be available at **http://127.0.0.1:5000**

## Project structure

```
projet_majda/
├── app/
│   ├── models/        # SQLAlchemy models (Chambre, TableRestaurant, SalleReunion, Reservation)
│   ├── routes/        # Flask blueprints (main, chambres, restaurant, salles, reservations)
│   ├── templates/     # Jinja2 HTML templates
│   ├── static/        # CSS and static assets
│   └── utils/         # Availability helpers
├── instance/          # SQLite database (auto-created on first run)
├── requirements.txt
├── seed.py            # Database seeder
└── run.py             # Application entry point
```

## Notes

- The SQLite database is created automatically at `instance/hotel.db` on first run.
- Frontend dependencies (Tailwind CSS, Alpine.js) are loaded from CDN — no build step required.
- Do **not** use `python3-venv`; the project requires the `python_3_11_13` conda environment.
