from ..extensions import db


class TableRestaurant(db.Model):
    __tablename__ = 'tables_restaurant'

    id       = db.Column(db.Integer, primary_key=True)
    numero   = db.Column(db.String(10), unique=True, nullable=False)
    capacite = db.Column(db.Integer, nullable=False)
    zone     = db.Column(db.String(50))   # Terrasse, Intérieur, VIP

    reservations = db.relationship(
        'Reservation', backref='table_restaurant', lazy=True,
        foreign_keys='Reservation.table_id'
    )

    def __repr__(self):
        return f'<Table {self.numero} ({self.zone}) – {self.capacite} pers.>'
