from ..extensions import db


class SalleReunion(db.Model):
    __tablename__ = 'salles_reunion'

    id          = db.Column(db.Integer, primary_key=True)
    nom         = db.Column(db.String(100), nullable=False)
    capacite    = db.Column(db.Integer, nullable=False)
    equipements = db.Column(db.Text)    # comma-separated: "Projecteur, WiFi, Tableau blanc"
    prix_heure  = db.Column(db.Float, nullable=False)
    photo_url   = db.Column(db.String(255))

    reservations = db.relationship(
        'Reservation', backref='salle', lazy=True,
        foreign_keys='Reservation.salle_id'
    )

    def equipements_liste(self):
        if self.equipements:
            return [e.strip() for e in self.equipements.split(',')]
        return []

    def __repr__(self):
        return f'<SalleReunion {self.nom} – {self.capacite} pers.>'
