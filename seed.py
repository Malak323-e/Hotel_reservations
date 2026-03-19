from app import create_app
from app.extensions import db
from app.models.chambre import Chambre
from app.models.table_restaurant import TableRestaurant
from app.models.salle_reunion import SalleReunion

app = create_app()

UNSPLASH = "https://images.unsplash.com/photo-"

CHAMBRES = [
    dict(numero="101", type_chambre="Simple", capacite=1, prix_nuit=80,
         description="Chambre simple confortable avec vue sur le jardin. Idéale pour un voyageur solo.",
         photo_url=UNSPLASH + "1631049307264-da0ec9d70304?w=800"),
    dict(numero="102", type_chambre="Simple", capacite=1, prix_nuit=85,
         description="Chambre simple lumineuse au premier étage, équipée d'un bureau et d'une douche italienne.",
         photo_url=UNSPLASH + "1618773928121-c32242e63f39?w=800"),
    dict(numero="201", type_chambre="Double", capacite=2, prix_nuit=140,
         description="Chambre double spacieuse avec lit queen-size et vue sur la piscine.",
         photo_url=UNSPLASH + "1566665797739-167bb9e39af3?w=800"),
    dict(numero="202", type_chambre="Double", capacite=2, prix_nuit=155,
         description="Chambre double supérieure avec balcon privé et vue panoramique sur la mer.",
         photo_url=UNSPLASH + "1582719478250-c89cae4dc85b?w=800"),
    dict(numero="301", type_chambre="Suite", capacite=4, prix_nuit=280,
         description="Suite junior avec salon séparé, jacuzzi et terrasse privée. Un séjour d'exception.",
         photo_url=UNSPLASH + "1631049421450-348ccd7f8949?w=800"),
    dict(numero="302", type_chambre="Suite", capacite=4, prix_nuit=350,
         description="Suite prestige avec deux chambres, kitchenette, et accès direct à la piscine VIP.",
         photo_url=UNSPLASH + "1578683010236-d716f9a3f461?w=800"),
]

TABLES = [
    dict(numero="T01", capacite=2, zone="Intérieur"),
    dict(numero="T02", capacite=2, zone="Intérieur"),
    dict(numero="T03", capacite=4, zone="Intérieur"),
    dict(numero="T04", capacite=4, zone="Terrasse"),
    dict(numero="T05", capacite=4, zone="Terrasse"),
    dict(numero="T06", capacite=6, zone="Terrasse"),
    dict(numero="T07", capacite=2, zone="VIP"),
    dict(numero="T08", capacite=8, zone="VIP"),
]

SALLES = [
    dict(nom="Salle Atlas", capacite=20, prix_heure=120,
         equipements="Projecteur HD, Tableau blanc, WiFi fibre, Climatisation, Micro sans fil",
         photo_url=UNSPLASH + "1517502884422-41eaead166d4?w=800"),
    dict(nom="Salle Sahara", capacite=50, prix_heure=250,
         equipements="Scène, Sono professionnelle, Projecteur 4K, WiFi fibre, Climatisation, Podium",
         photo_url=UNSPLASH + "1497366216548-37526070297c?w=800"),
    dict(nom="Salle Ziz", capacite=10, prix_heure=80,
         equipements="Écran TV 75\", Tableau blanc, WiFi fibre, Vidéoconférence, Climatisation",
         photo_url=UNSPLASH + "1600508774634-4e11d34730e2?w=800"),
    dict(nom="Salle Toubkal", capacite=100, prix_heure=400,
         equipements="Grande scène, Sono professionnelle, Éclairage scénique, Projecteurs doubles, WiFi fibre, Accueil dédié",
         photo_url=UNSPLASH + "1431540015161-0bf868a2d407?w=800"),
]


def seed():
    with app.app_context():
        db.create_all()

        for data in CHAMBRES:
            obj = Chambre.query.filter_by(numero=data["numero"]).first()
            if obj:
                for k, v in data.items():
                    setattr(obj, k, v)
            else:
                db.session.add(Chambre(**data))
        print(f"✓ {len(CHAMBRES)} chambres synchronisées")

        for data in TABLES:
            obj = TableRestaurant.query.filter_by(numero=data["numero"]).first()
            if obj:
                for k, v in data.items():
                    setattr(obj, k, v)
            else:
                db.session.add(TableRestaurant(**data))
        print(f"✓ {len(TABLES)} tables de restaurant synchronisées")

        for data in SALLES:
            obj = SalleReunion.query.filter_by(nom=data["nom"]).first()
            if obj:
                for k, v in data.items():
                    setattr(obj, k, v)
            else:
                db.session.add(SalleReunion(**data))
        print(f"✓ {len(SALLES)} salles de réunion synchronisées")

        db.session.commit()
        print("Base de données initialisée avec succès.")


if __name__ == '__main__':
    seed()
