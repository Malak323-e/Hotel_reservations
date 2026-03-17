import pytest
from datetime import date, time

from app import create_app
from app.extensions import db as _db
from app.models.chambre import Chambre
from app.models.table_restaurant import TableRestaurant
from app.models.salle_reunion import SalleReunion
from app.models.reservation import Reservation


@pytest.fixture
def app():
    app = create_app(test_config={
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def chambre(app):
    c = Chambre(numero="101", type_chambre="Double", capacite=2, prix_nuit=120.0)
    _db.session.add(c)
    _db.session.commit()
    return c


@pytest.fixture
def table(app):
    t = TableRestaurant(numero="T1", capacite=4, zone="Intérieur")
    _db.session.add(t)
    _db.session.commit()
    return t


@pytest.fixture
def salle(app):
    s = SalleReunion(nom="Salle A", capacite=10, prix_heure=50.0)
    _db.session.add(s)
    _db.session.commit()
    return s
