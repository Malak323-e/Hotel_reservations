import secrets
from datetime import datetime
from ..extensions import db


def generer_reference():
    return 'HTL-' + secrets.token_hex(3).upper()


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id               = db.Column(db.Integer, primary_key=True)
    reference        = db.Column(db.String(12), unique=True, nullable=False,
                                 default=generer_reference)
    type_reservation = db.Column(db.String(20), nullable=False)   # chambre | restaurant | salle
    statut           = db.Column(db.String(20), nullable=False, default='confirmee')

    # Client
    nom_client       = db.Column(db.String(100), nullable=False)
    prenom_client    = db.Column(db.String(100), nullable=False)
    email_client     = db.Column(db.String(150), nullable=False)
    telephone_client = db.Column(db.String(20))

    # Dates / heures
    date_debut       = db.Column(db.Date, nullable=False)
    date_fin         = db.Column(db.Date)
    heure_debut      = db.Column(db.Time)
    heure_fin        = db.Column(db.Time)
    nombre_personnes = db.Column(db.Integer, nullable=False, default=1)
    commentaire      = db.Column(db.Text)

    # FK — une seule renseignée par ligne
    chambre_id = db.Column(db.Integer, db.ForeignKey('chambres.id'), nullable=True)
    table_id   = db.Column(db.Integer, db.ForeignKey('tables_restaurant.id'), nullable=True)
    salle_id   = db.Column(db.Integer, db.ForeignKey('salles_reunion.id'), nullable=True)

    cree_le = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Reservation {self.reference} – {self.type_reservation} – {self.statut}>'
