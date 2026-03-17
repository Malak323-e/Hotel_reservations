"""Tests for HTTP routes — status codes and JSON API endpoints."""
from datetime import date, time

from app.extensions import db
from app.models.chambre import Chambre
from app.models.reservation import Reservation


# ─── Pages principales ────────────────────────────────────────────────────────

def test_homepage(client):
    r = client.get("/")
    assert r.status_code == 200


def test_liste_chambres(client):
    r = client.get("/chambres/")
    assert r.status_code == 200


def test_liste_restaurant(client):
    r = client.get("/restaurant/")
    assert r.status_code == 200


def test_liste_salles(client):
    r = client.get("/salles/")
    assert r.status_code == 200


def test_mes_reservations(client):
    r = client.get("/mes-reservations/")
    assert r.status_code == 200


def test_chambre_inexistante_404(client):
    r = client.get("/chambres/9999")
    assert r.status_code == 404


# ─── API disponibilité chambres ───────────────────────────────────────────────

def test_api_disponibilite_chambre_params_manquants(client):
    r = client.get("/chambres/api/disponibilite")
    assert r.status_code == 200
    assert r.get_json()["disponible"] is None


def test_api_disponibilite_chambre_dates_invalides(client, chambre):
    r = client.get(
        f"/chambres/api/disponibilite?chambre_id={chambre.id}"
        "&date_arrivee=not-a-date&date_depart=not-a-date"
    )
    assert r.status_code == 200
    assert r.get_json()["disponible"] is None


def test_api_disponibilite_chambre_libre(client, chambre):
    r = client.get(
        f"/chambres/api/disponibilite?chambre_id={chambre.id}"
        "&date_arrivee=2030-06-01&date_depart=2030-06-05"
    )
    assert r.status_code == 200
    assert r.get_json()["disponible"] is True


def test_api_disponibilite_chambre_prise(client, app, chambre):
    with app.app_context():
        resa = Reservation(
            type_reservation="chambre",
            chambre_id=chambre.id,
            nom_client="Test", prenom_client="User",
            email_client="test@example.com",
            nombre_personnes=1,
            date_debut=date(2030, 6, 1),
            date_fin=date(2030, 6, 5),
        )
        db.session.add(resa)
        db.session.commit()
        cid = chambre.id

    r = client.get(
        f"/chambres/api/disponibilite?chambre_id={cid}"
        "&date_arrivee=2030-06-01&date_depart=2030-06-05"
    )
    assert r.status_code == 200
    assert r.get_json()["disponible"] is False


# ─── Réservation chambre ──────────────────────────────────────────────────────

def test_reserver_chambre_success(client, app, chambre):
    with app.app_context():
        cid = chambre.id

    r = client.post(
        f"/chambres/{cid}/reserver",
        data={
            "date_arrivee": "2030-07-01",
            "date_depart":  "2030-07-05",
            "nom":          "Durand",
            "prenom":       "Marie",
            "email":        "marie@example.com",
            "telephone":    "0612345678",
            "personnes":    "2",
        },
        follow_redirects=False,
    )
    # Doit rediriger vers la page de confirmation
    assert r.status_code == 302
    assert "/confirmation/" in r.headers["Location"]


def test_reserver_chambre_dates_invalides(client, app, chambre):
    with app.app_context():
        cid = chambre.id

    r = client.post(
        f"/chambres/{cid}/reserver",
        data={
            "date_arrivee": "not-a-date",
            "date_depart":  "not-a-date",
            "nom": "Test", "prenom": "User", "email": "t@t.com",
        },
        follow_redirects=False,
    )
    assert r.status_code == 302
    assert f"/chambres/{cid}" in r.headers["Location"]


def test_reserver_chambre_depart_avant_arrivee(client, app, chambre):
    with app.app_context():
        cid = chambre.id

    r = client.post(
        f"/chambres/{cid}/reserver",
        data={
            "date_arrivee": "2030-07-05",
            "date_depart":  "2030-07-01",
            "nom": "Test", "prenom": "User", "email": "t@t.com",
        },
        follow_redirects=False,
    )
    assert r.status_code == 302
    assert f"/chambres/{cid}" in r.headers["Location"]


def test_reserver_chambre_champs_obligatoires_manquants(client, app, chambre):
    with app.app_context():
        cid = chambre.id

    r = client.post(
        f"/chambres/{cid}/reserver",
        data={
            "date_arrivee": "2030-07-01",
            "date_depart":  "2030-07-05",
            "nom": "", "prenom": "User", "email": "",
        },
        follow_redirects=False,
    )
    assert r.status_code == 302
    assert f"/chambres/{cid}" in r.headers["Location"]
