from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..extensions import db
from ..models.reservation import Reservation

bp = Blueprint('reservations', __name__)


@bp.route('/')
def mes_reservations():
    return render_template('reservations/mes_reservations.html',
                           reservations=None, recherche=False)


@bp.route('/rechercher', methods=['POST'])
def rechercher():
    email     = request.form.get('email', '').strip()
    reference = request.form.get('reference', '').strip().upper()

    reservations = []
    if reference:
        r = Reservation.query.filter_by(reference=reference).first()
        if r:
            reservations = [r]
    elif email:
        reservations = Reservation.query.filter_by(email_client=email).order_by(
            Reservation.cree_le.desc()
        ).all()

    if not reservations:
        flash("Aucune réservation trouvée avec ces informations.", 'error')

    today = date.today()
    return render_template('reservations/mes_reservations.html',
                           reservations=reservations, recherche=True, today=today)


@bp.route('/annuler/<ref>', methods=['GET'])
def confirmer_annulation(ref):
    reservation = Reservation.query.filter_by(reference=ref).first_or_404()
    if reservation.statut == 'annulee':
        flash("Cette réservation est déjà annulée.", 'error')
        return redirect(url_for('reservations.mes_reservations'))
    return render_template('reservations/annulation.html', reservation=reservation)


@bp.route('/annuler/<ref>', methods=['POST'])
def annuler(ref):
    reservation = Reservation.query.filter_by(reference=ref).first_or_404()

    if reservation.statut == 'annulee':
        flash("Cette réservation est déjà annulée.", 'error')
        return redirect(url_for('reservations.mes_reservations'))

    reservation.statut = 'annulee'
    db.session.commit()

    flash(f"Réservation {ref} annulée avec succès.", 'success')
    return redirect(url_for('reservations.mes_reservations'))
