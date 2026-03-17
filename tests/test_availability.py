"""Tests for availability overlap logic (app/utils/availability.py)."""
from datetime import date, time

from app.extensions import db
from app.models.reservation import Reservation
from app.utils.availability import (
    is_chambre_disponible,
    is_salle_disponible,
    is_table_disponible,
)


# ─── Chambre ──────────────────────────────────────────────────────────────────

class TestChambreDisponibilite:
    def test_chambre_libre_quand_aucune_reservation(self, app, chambre):
        with app.app_context():
            assert is_chambre_disponible(chambre.id, date(2030, 6, 1), date(2030, 6, 5))

    def test_chambre_indisponible_overlap_exact(self, app, chambre):
        with app.app_context():
            r = Reservation(
                type_reservation="chambre",
                chambre_id=chambre.id,
                nom_client="Dupont", prenom_client="Jean",
                email_client="jean@example.com",
                nombre_personnes=1,
                date_debut=date(2030, 6, 1),
                date_fin=date(2030, 6, 5),
            )
            db.session.add(r)
            db.session.commit()
            assert not is_chambre_disponible(chambre.id, date(2030, 6, 1), date(2030, 6, 5))

    def test_chambre_indisponible_overlap_partiel(self, app, chambre):
        with app.app_context():
            r = Reservation(
                type_reservation="chambre",
                chambre_id=chambre.id,
                nom_client="Dupont", prenom_client="Jean",
                email_client="jean@example.com",
                nombre_personnes=1,
                date_debut=date(2030, 6, 3),
                date_fin=date(2030, 6, 8),
            )
            db.session.add(r)
            db.session.commit()
            # Demande 1–6 chevauche la résa 3–8
            assert not is_chambre_disponible(chambre.id, date(2030, 6, 1), date(2030, 6, 6))

    def test_chambre_disponible_apres_checkout(self, app, chambre):
        with app.app_context():
            r = Reservation(
                type_reservation="chambre",
                chambre_id=chambre.id,
                nom_client="Dupont", prenom_client="Jean",
                email_client="jean@example.com",
                nombre_personnes=1,
                date_debut=date(2030, 6, 1),
                date_fin=date(2030, 6, 5),
            )
            db.session.add(r)
            db.session.commit()
            # Check-in exactement au checkout → pas de chevauchement
            assert is_chambre_disponible(chambre.id, date(2030, 6, 5), date(2030, 6, 8))

    def test_chambre_disponible_avant_checkin(self, app, chambre):
        with app.app_context():
            r = Reservation(
                type_reservation="chambre",
                chambre_id=chambre.id,
                nom_client="Dupont", prenom_client="Jean",
                email_client="jean@example.com",
                nombre_personnes=1,
                date_debut=date(2030, 6, 5),
                date_fin=date(2030, 6, 10),
            )
            db.session.add(r)
            db.session.commit()
            assert is_chambre_disponible(chambre.id, date(2030, 6, 1), date(2030, 6, 5))

    def test_reservation_annulee_ne_bloque_pas(self, app, chambre):
        with app.app_context():
            r = Reservation(
                type_reservation="chambre",
                chambre_id=chambre.id,
                nom_client="Dupont", prenom_client="Jean",
                email_client="jean@example.com",
                nombre_personnes=1,
                date_debut=date(2030, 6, 1),
                date_fin=date(2030, 6, 5),
                statut="annulee",
            )
            db.session.add(r)
            db.session.commit()
            assert is_chambre_disponible(chambre.id, date(2030, 6, 1), date(2030, 6, 5))


# ─── Table restaurant ─────────────────────────────────────────────────────────

class TestTableDisponibilite:
    def test_table_libre_quand_aucune_reservation(self, app, table):
        with app.app_context():
            assert is_table_disponible(table.id, date(2030, 6, 1), time(12, 0), time(14, 0))

    def test_table_indisponible_creneau_exact(self, app, table):
        with app.app_context():
            r = Reservation(
                type_reservation="restaurant",
                table_id=table.id,
                nom_client="Martin", prenom_client="Alice",
                email_client="alice@example.com",
                nombre_personnes=2,
                date_debut=date(2030, 6, 1),
                heure_debut=time(12, 0),
                heure_fin=time(14, 0),
            )
            db.session.add(r)
            db.session.commit()
            assert not is_table_disponible(table.id, date(2030, 6, 1), time(12, 0), time(14, 0))

    def test_table_disponible_autre_jour(self, app, table):
        with app.app_context():
            r = Reservation(
                type_reservation="restaurant",
                table_id=table.id,
                nom_client="Martin", prenom_client="Alice",
                email_client="alice@example.com",
                nombre_personnes=2,
                date_debut=date(2030, 6, 1),
                heure_debut=time(12, 0),
                heure_fin=time(14, 0),
            )
            db.session.add(r)
            db.session.commit()
            assert is_table_disponible(table.id, date(2030, 6, 2), time(12, 0), time(14, 0))

    def test_table_disponible_creneau_adjacent(self, app, table):
        with app.app_context():
            r = Reservation(
                type_reservation="restaurant",
                table_id=table.id,
                nom_client="Martin", prenom_client="Alice",
                email_client="alice@example.com",
                nombre_personnes=2,
                date_debut=date(2030, 6, 1),
                heure_debut=time(12, 0),
                heure_fin=time(14, 0),
            )
            db.session.add(r)
            db.session.commit()
            # Créneau commence exactement à la fin de la résa précédente
            assert is_table_disponible(table.id, date(2030, 6, 1), time(14, 0), time(16, 0))


# ─── Salle de réunion ─────────────────────────────────────────────────────────

class TestSalleDisponibilite:
    def test_salle_libre_quand_aucune_reservation(self, app, salle):
        with app.app_context():
            assert is_salle_disponible(salle.id, date(2030, 6, 1), time(9, 0), time(11, 0))

    def test_salle_indisponible_overlap(self, app, salle):
        with app.app_context():
            r = Reservation(
                type_reservation="salle",
                salle_id=salle.id,
                nom_client="Bernard", prenom_client="Paul",
                email_client="paul@example.com",
                nombre_personnes=5,
                date_debut=date(2030, 6, 1),
                heure_debut=time(9, 0),
                heure_fin=time(12, 0),
            )
            db.session.add(r)
            db.session.commit()
            assert not is_salle_disponible(salle.id, date(2030, 6, 1), time(10, 0), time(13, 0))

    def test_salle_disponible_apres_fin(self, app, salle):
        with app.app_context():
            r = Reservation(
                type_reservation="salle",
                salle_id=salle.id,
                nom_client="Bernard", prenom_client="Paul",
                email_client="paul@example.com",
                nombre_personnes=5,
                date_debut=date(2030, 6, 1),
                heure_debut=time(9, 0),
                heure_fin=time(12, 0),
            )
            db.session.add(r)
            db.session.commit()
            assert is_salle_disponible(salle.id, date(2030, 6, 1), time(12, 0), time(14, 0))
