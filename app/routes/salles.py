from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from ..extensions import db
from ..models.salle_reunion import SalleReunion
from ..models.reservation import Reservation
from ..utils.availability import is_salle_disponible

bp = Blueprint('salles', __name__)


@bp.route('/')
def liste():
    salles = SalleReunion.query.all()
    return render_template('salles/liste.html', salles=salles)


@bp.route('/<int:salle_id>')
def detail(salle_id):
    salle = SalleReunion.query.get_or_404(salle_id)
    today = date.today().isoformat()
    return render_template('salles/detail.html', salle=salle, today=today)


@bp.route('/<int:salle_id>/reserver', methods=['POST'])
def reserver(salle_id):
    salle = SalleReunion.query.get_or_404(salle_id)

    try:
        d  = datetime.strptime(request.form['date'],        '%Y-%m-%d').date()
        hd = datetime.strptime(request.form['heure_debut'], '%H:%M').time()
        hf = datetime.strptime(request.form['heure_fin'],   '%H:%M').time()
    except (ValueError, KeyError):
        flash("Dates ou horaires invalides.", 'error')
        return redirect(url_for('salles.detail', salle_id=salle_id))

    if hd >= hf:
        flash("L'heure de fin doit être après l'heure de début.", 'error')
        return redirect(url_for('salles.detail', salle_id=salle_id))

    if d < date.today():
        flash("La date ne peut pas être dans le passé.", 'error')
        return redirect(url_for('salles.detail', salle_id=salle_id))

    if not is_salle_disponible(salle_id, d, hd, hf):
        flash("Cette salle n'est pas disponible pour ce créneau.", 'error')
        return redirect(url_for('salles.detail', salle_id=salle_id))

    reservation = Reservation(
        type_reservation = 'salle',
        salle_id         = salle_id,
        nom_client       = request.form.get('nom', '').strip(),
        prenom_client    = request.form.get('prenom', '').strip(),
        email_client     = request.form.get('email', '').strip(),
        telephone_client = request.form.get('telephone', '').strip(),
        nombre_personnes = int(request.form.get('personnes', 1)),
        date_debut       = d,
        heure_debut      = hd,
        heure_fin        = hf,
        commentaire      = request.form.get('commentaire', '').strip(),
    )

    if not reservation.nom_client or not reservation.email_client:
        flash("Veuillez remplir tous les champs obligatoires.", 'error')
        return redirect(url_for('salles.detail', salle_id=salle_id))

    db.session.add(reservation)
    db.session.commit()

    return redirect(url_for('salles.confirmation', ref=reservation.reference))


@bp.route('/confirmation/<ref>')
def confirmation(ref):
    reservation = Reservation.query.filter_by(reference=ref).first_or_404()
    return render_template('salles/confirmation.html', reservation=reservation)


@bp.route('/api/disponibilite')
def api_disponibilite():
    salle_id    = request.args.get('salle_id', type=int)
    date_str    = request.args.get('date', '')
    heure_debut = request.args.get('heure_debut', '')
    heure_fin   = request.args.get('heure_fin', '')

    if not all([salle_id, date_str, heure_debut, heure_fin]):
        return jsonify({'disponible': None})

    try:
        d  = datetime.strptime(date_str,    '%Y-%m-%d').date()
        hd = datetime.strptime(heure_debut, '%H:%M').time()
        hf = datetime.strptime(heure_fin,   '%H:%M').time()
    except ValueError:
        return jsonify({'disponible': None})

    return jsonify({'disponible': is_salle_disponible(salle_id, d, hd, hf)})
