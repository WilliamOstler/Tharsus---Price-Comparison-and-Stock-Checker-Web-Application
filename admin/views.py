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



    blacklistedSupplier = request.form.get("name")
    newBlacklistedSupplier = Supplier(name=blacklistedSupplier)

    db.session.add(newBlacklistedSupplier)
    db.session.commit()

    flash("New blacklisted supplier added")
    return admin()

def add_supplier_to_favourites():

    favouriteSupplier = request.form.get("name")
    newFavouriteSupplier = Supplier(name=favouriteSupplier)

    db.session.add(newFavouriteSupplier)
    db.session.commit()

    flash("New favourite supplier added")
    return admin()
