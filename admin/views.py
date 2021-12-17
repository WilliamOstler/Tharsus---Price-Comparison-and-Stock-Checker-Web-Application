from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from app import db
from Supplier import Supplier


admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


@admin_blueprint.route('/add_supplier_to_blacklist', methods=['POST'])
@login_required
#@requires_roles('admin')
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



