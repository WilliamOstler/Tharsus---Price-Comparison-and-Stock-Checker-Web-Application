from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required

from app import db, requires_roles

from models import Supplier, User

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin')
@login_required
@requires_roles('admin')
def admin():
    return render_template('admin.html')


@admin_blueprint.route('/view_all_users', methods=['POST'])
@login_required
@requires_roles('admin')
def view_all_users():
    # get list of all users
    return render_template('admin.html', name=current_user.firstname,
                           current_users=User.query.filter_by(role='user').all())


@admin_blueprint.route('/delete_user/<int:id>')
@login_required
@requires_roles('admin')
def delete_user(id):
    usr = User.query.get_or_404(id)
    try:
        db.session.delete(usr)
        db.session.commit()
        return render_template('admin.html')
    except:
        flash("Failed.")


@admin_blueprint.route('/add_supplier_to_blacklist', methods=['POST'])
@login_required
@requires_roles('admin')
def add_supplier_to_blacklist():
    blackistedSupplier = request.form.get("name")
    newBlacklistedSupplier = Supplier(name=blackistedSupplier)

    db.session.add(newBlacklistedSupplier)
    db.session.commit()

    flash("New blacklisted supplier added")
    return admin()


@admin_blueprint.route('/view_suppliers_Preferences', methods=['POST'])
@login_required
def view_suppliers_Preferences():
    return render_template('admin.html', suppliers=Supplier.query.all())



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