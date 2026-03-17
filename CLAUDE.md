# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the application

```bash
# First-time setup: populate the database with sample data
conda run -n python_3_11_13 python seed.py

# Start the development server (http://127.0.0.1:5000)
conda run -n python_3_11_13 python run.py
```

The conda environment `python_3_11_13` has Flask and Flask-SQLAlchemy installed. Do not use venv (`python3-venv` is not available on this system).

## Architecture

Flask app using the **factory pattern** (`create_app()` in `app/__init__.py`), SQLite via SQLAlchemy, server-side Jinja2 templates with Tailwind CSS (CDN) and Alpine.js (CDN) for interactivity.

### Data model

One central `Reservation` table holds all booking types. Each row has a `type_reservation` discriminator (`chambre` | `restaurant` | `salle`) and three nullable FKs — only one is populated per row:

```
Chambre ──┐
TableRestaurant ──┼──> Reservation (reference, statut, date_debut, date_fin, heure_debut, heure_fin, ...)
SalleReunion ────┘
```

Reservation references are auto-generated (`HTL-XXXXXX`) via `secrets.token_hex(3)` in `app/models/reservation.py`.

### Availability logic

`app/utils/availability.py` contains the three overlap-detection functions (`is_chambre_disponible`, `is_table_disponible`, `is_salle_disponible`). They are used by both the form POST handlers (server-side validation) and the JSON API endpoints (live UI feedback via `fetch()`).

Overlap query pattern for rooms:
```sql
date_debut < :date_fin AND date_fin > :date_debut AND statut = 'confirmee'
```
For restaurant/salles, `date_debut = :date` and `heure_debut`/`heure_fin` replace the date range.

### Blueprints and URL structure

| Blueprint | Prefix | Module |
|---|---|---|
| `main` | `/` | `app/routes/main.py` |
| `chambres` | `/chambres` | `app/routes/chambres.py` |
| `restaurant` | `/restaurant` | `app/routes/restaurant.py` |
| `salles` | `/salles` | `app/routes/salles.py` |
| `reservations` | `/mes-reservations` | `app/routes/reservations.py` |

Each blueprint also exposes a JSON availability endpoint (e.g. `GET /chambres/api/disponibilite`).

### Templates

All templates extend `app/templates/base.html`, which defines the navbar, flash message system (Alpine.js `x-show`), and footer. CSS utility classes (`btn-gold`, `btn-navy`, `input-field`, `form-label`) are defined in `app/static/css/custom.css` using Tailwind's `@apply`.

### Database

SQLite file is created at `instance/hotel.db` on first run (`db.create_all()` is called in `create_app()`). `seed.py` is idempotent — it checks `query.count()` before inserting.
