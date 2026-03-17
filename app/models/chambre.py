from ..extensions import db


class Chambre(db.Model):
    __tablename__ = 'chambres'

    id           = db.Column(db.Integer, primary_key=True)
    numero       = db.Column(db.String(10), unique=True, nullable=False)
    type_chambre = db.Column(db.String(50), nullable=False)   # Simple, Double, Suite
    capacite     = db.Column(db.Integer, nullable=False, default=1)
    prix_nuit    = db.Column(db.Float, nullable=False)
    description  = db.Column(db.Text)
    photo_url    = db.Column(db.String(255))

    reservations = db.relationship(
        'Reservation', backref='chambre', lazy=True,
        foreign_keys='Reservation.chambre_id'
    )

    def __repr__(self):
        return f'<Chambre {self.numero} – {self.type_chambre}>'
