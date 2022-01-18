from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from app import db
from models import Supplier, User

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


@admin_blueprint.route('/view_suppliers_Preferences', methods=['POST'])
@login_required
def view_suppliers_Preferences():
    return render_template('admin.html', suppliers=Supplier.query.all())


@admin_blueprint.route('/view_users', methods=['POST'])
@login_required
def view_all_users():
    return render_template('admin.html', users=User.query.filter_by(role='user').all())


@admin_blueprint.route('/remove_user', methods=['POST'])
@login_required
def remove_user():
    user = request.form.get('remove_user')

    if len((User.query.filter_by(id=user).all())) == 0:
        flash(f"No preference registered for {user}")
    else:
        User.query.filter_by(id=user).delete()
        db.session.commit()

    flash("user Removed")
    return admin()


@admin_blueprint.route('/blacklist_supplier', methods=['POST'])
@login_required
def blacklist_supplier():
    blacklist = request.form.get('blacklisted_supplier')

    if len((Supplier.query.filter_by(name=blacklist).all())) == 0:
        new_blacklist = Supplier(blacklist, 1, 0)
        db.session.add(new_blacklist)
        db.session.commit()
    else:
        Supplier.query.filter_by(name=blacklist).delete()
        new_blacklist = Supplier(blacklist, 1, 0)
        db.session.add(new_blacklist)
        db.session.commit()

    flash("Supplier Blacklisted")
    return admin()


@admin_blueprint.route('/favourite_supplier', methods=['POST'])
@login_required
def favourite_supplier():
    favourite = request.form.get('favourite_supplier')
    print(favourite)

    if len((Supplier.query.filter_by(name=favourite).all())) == 0:
        new_favourite = Supplier(favourite, 0, 1)
        db.session.add(new_favourite)
        db.session.commit()
    else:
        Supplier.query.filter_by(name=favourite).delete()
        new_favourite = Supplier(favourite, 0, 1)
        db.session.add(new_favourite)
        db.session.commit()

    flash("Supplier Favourited")
    return admin()


@admin_blueprint.route('/remove_preference', methods=['POST'])
@login_required
def remove_preference():
    supplier = request.form.get('remove_preference')

    if len((Supplier.query.filter_by(name=supplier).all())) == 0:
        flash(f"No preference registered for {supplier}")
    else:
        Supplier.query.filter_by(name=supplier).delete()
        db.session.commit()

    flash("Preference Removed")
    return admin()