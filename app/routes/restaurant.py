from datetime import datetime, date, time
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from ..extensions import db
from ..models.table_restaurant import TableRestaurant
from ..models.reservation import Reservation
from ..utils.availability import is_table_disponible

bp = Blueprint('restaurant', __name__)


@bp.route('/')
def index():
    today = date.today().isoformat()
    return render_template('restaurant/index.html', today=today)


@bp.route('/disponibilites', methods=['POST'])
def disponibilites():
    date_str    = request.form.get('date', '')
    heure_debut = request.form.get('heure_debut', '')
    heure_fin   = request.form.get('heure_fin', '')
    personnes   = request.form.get('personnes', 2, type=int)

    tables_dispo = []
    erreur = None

    try:
        d  = datetime.strptime(date_str,    '%Y-%m-%d').date()
        hd = datetime.strptime(heure_debut, '%H:%M').time()
        hf = datetime.strptime(heure_fin,   '%H:%M').time()

        if hd >= hf:
            erreur = "L'heure de fin doit être après l'heure de début."
        elif d < date.today():
            erreur = "La date ne peut pas être dans le passé."
        else:
            tables = TableRestaurant.query.filter(
                TableRestaurant.capacite >= personnes
            ).all()
            for table in tables:
                if is_table_disponible(table.id, d, hd, hf):
                    tables_dispo.append(table)
    except ValueError:
        erreur = "Veuillez remplir tous les champs correctement."

    return render_template('restaurant/disponibilites.html',
                           tables=tables_dispo,
                           date_str=date_str,
                           heure_debut=heure_debut,
                           heure_fin=heure_fin,
                           personnes=personnes,
                           erreur=erreur)


@bp.route('/reserver', methods=['POST'])
def reserver():
    try:
        d  = datetime.strptime(request.form['date'],        '%Y-%m-%d').date()
        hd = datetime.strptime(request.form['heure_debut'], '%H:%M').time()
        hf = datetime.strptime(request.form['heure_fin'],   '%H:%M').time()
    except (ValueError, KeyError):
        flash("Données invalides.", 'error')
        return redirect(url_for('restaurant.index'))

    table_id  = request.form.get('table_id', type=int)
    personnes = request.form.get('personnes', 2, type=int)

    table = TableRestaurant.query.get_or_404(table_id)

    if not is_table_disponible(table_id, d, hd, hf):
        flash("Cette table n'est plus disponible pour ce créneau.", 'error')
        return redirect(url_for('restaurant.index'))

    reservation = Reservation(
        type_reservation = 'restaurant',
        table_id         = table_id,
        nom_client       = request.form.get('nom', '').strip(),
        prenom_client    = request.form.get('prenom', '').strip(),
        email_client     = request.form.get('email', '').strip(),
        telephone_client = request.form.get('telephone', '').strip(),
        nombre_personnes = personnes,
        date_debut       = d,
        heure_debut      = hd,
        heure_fin        = hf,
        commentaire      = request.form.get('commentaire', '').strip(),
    )

    if not reservation.nom_client or not reservation.email_client:
        flash("Veuillez remplir tous les champs obligatoires.", 'error')
        return redirect(url_for('restaurant.index'))

    db.session.add(reservation)
    db.session.commit()

    return redirect(url_for('restaurant.confirmation', ref=reservation.reference))


@bp.route('/confirmation/<ref>')
def confirmation(ref):
    reservation = Reservation.query.filter_by(reference=ref).first_or_404()
    return render_template('restaurant/confirmation.html', reservation=reservation)
