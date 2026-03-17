from datetime import date, datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from ..extensions import db
from ..models.chambre import Chambre
from ..models.reservation import Reservation
from ..utils.availability import is_chambre_disponible

bp = Blueprint('chambres', __name__)


@bp.route('/')
def liste():
    chambres = Chambre.query.all()
    date_arrivee = request.args.get('date_arrivee', '')
    date_depart  = request.args.get('date_depart', '')
    type_filtre  = request.args.get('type', '')
    capacite_min = request.args.get('capacite', 0, type=int)

    if type_filtre:
        chambres = [c for c in chambres if c.type_chambre == type_filtre]
    if capacite_min:
        chambres = [c for c in chambres if c.capacite >= capacite_min]

    # Disponibilité si dates fournies
    disponibilite = {}
    if date_arrivee and date_depart:
        try:
            da = datetime.strptime(date_arrivee, '%Y-%m-%d').date()
            dd = datetime.strptime(date_depart, '%Y-%m-%d').date()
            for c in chambres:
                disponibilite[c.id] = is_chambre_disponible(c.id, da, dd)
        except ValueError:
            pass

    return render_template('chambres/liste.html',
                           chambres=chambres,
                           disponibilite=disponibilite,
                           date_arrivee=date_arrivee,
                           date_depart=date_depart,
                           type_filtre=type_filtre,
                           capacite_min=capacite_min)


@bp.route('/<int:chambre_id>')
def detail(chambre_id):
    chambre = Chambre.query.get_or_404(chambre_id)
    today = date.today().isoformat()
    return render_template('chambres/detail.html', chambre=chambre, today=today)


@bp.route('/<int:chambre_id>/reserver', methods=['POST'])
def reserver(chambre_id):
    chambre = Chambre.query.get_or_404(chambre_id)

    try:
        date_arrivee = datetime.strptime(request.form['date_arrivee'], '%Y-%m-%d').date()
        date_depart  = datetime.strptime(request.form['date_depart'],  '%Y-%m-%d').date()
    except (ValueError, KeyError):
        flash("Dates invalides. Veuillez réessayer.", 'error')
        return redirect(url_for('chambres.detail', chambre_id=chambre_id))

    if date_arrivee >= date_depart:
        flash("La date de départ doit être après la date d'arrivée.", 'error')
        return redirect(url_for('chambres.detail', chambre_id=chambre_id))

    if date_arrivee < date.today():
        flash("La date d'arrivée ne peut pas être dans le passé.", 'error')
        return redirect(url_for('chambres.detail', chambre_id=chambre_id))

    if not is_chambre_disponible(chambre_id, date_arrivee, date_depart):
        flash("Cette chambre n'est pas disponible pour les dates sélectionnées.", 'error')
        return redirect(url_for('chambres.detail', chambre_id=chambre_id))

    reservation = Reservation(
        type_reservation = 'chambre',
        chambre_id       = chambre_id,
        nom_client       = request.form.get('nom', '').strip(),
        prenom_client    = request.form.get('prenom', '').strip(),
        email_client     = request.form.get('email', '').strip(),
        telephone_client = request.form.get('telephone', '').strip(),
        nombre_personnes = int(request.form.get('personnes', 1)),
        date_debut       = date_arrivee,
        date_fin         = date_depart,
        commentaire      = request.form.get('commentaire', '').strip(),
    )

    if not reservation.nom_client or not reservation.email_client:
        flash("Veuillez remplir tous les champs obligatoires.", 'error')
        return redirect(url_for('chambres.detail', chambre_id=chambre_id))

    db.session.add(reservation)
    db.session.commit()

    return redirect(url_for('chambres.confirmation', ref=reservation.reference))


@bp.route('/confirmation/<ref>')
def confirmation(ref):
    reservation = Reservation.query.filter_by(reference=ref).first_or_404()
    return render_template('chambres/confirmation.html', reservation=reservation)


@bp.route('/api/disponibilite')
def api_disponibilite():
    chambre_id   = request.args.get('chambre_id', type=int)
    date_arrivee = request.args.get('date_arrivee', '')
    date_depart  = request.args.get('date_depart', '')

    if not all([chambre_id, date_arrivee, date_depart]):
        return jsonify({'disponible': None})

    try:
        da = datetime.strptime(date_arrivee, '%Y-%m-%d').date()
        dd = datetime.strptime(date_depart,  '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'disponible': None})

    return jsonify({'disponible': is_chambre_disponible(chambre_id, da, dd)})
