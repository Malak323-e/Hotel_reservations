from ..extensions import db
from ..models.reservation import Reservation


def is_chambre_disponible(chambre_id, date_debut, date_fin):
    """Retourne True si la chambre est libre sur la période donnée."""
    conflit = Reservation.query.filter(
        Reservation.chambre_id == chambre_id,
        Reservation.statut == 'confirmee',
        Reservation.date_debut < date_fin,
        Reservation.date_fin > date_debut,
    ).first()
    return conflit is None


def is_table_disponible(table_id, date, heure_debut, heure_fin):
    """Retourne True si la table est libre pour le créneau donné."""
    conflit = Reservation.query.filter(
        Reservation.table_id == table_id,
        Reservation.statut == 'confirmee',
        Reservation.date_debut == date,
        Reservation.heure_debut < heure_fin,
        Reservation.heure_fin > heure_debut,
    ).first()
    return conflit is None


def is_salle_disponible(salle_id, date, heure_debut, heure_fin):
    """Retourne True si la salle est libre pour le créneau donné."""
    conflit = Reservation.query.filter(
        Reservation.salle_id == salle_id,
        Reservation.statut == 'confirmee',
        Reservation.date_debut == date,
        Reservation.heure_debut < heure_fin,
        Reservation.heure_fin > heure_debut,
    ).first()
    return conflit is None
