"""
View functionality for admin-only features
"""
from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from app import db, requires_roles
from models import Supplier, User

# Instantiate blueprints
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin')
@login_required
@requires_roles('admin')
def admin():
    """
    Admin homepage
    """
    return render_template('admin.html')


@admin_blueprint.route('/view_all_users', methods=['POST'])
@login_required
@requires_roles('admin')
def view_all_users():
    """
    Allows the admin to view all users of the web application
    """
    return render_template('admin.html', name=current_user.firstname,
                           current_users=User.query.filter_by(role='user').all())


@admin_blueprint.route('/delete_user/<int:id>')
@login_required
@requires_roles('admin')
def delete_user(user_id):
    """
    Allows the admin to delete a user account from the system.
    :param user_id: The id of the user account which will be deleted.
    """
    # Retrieve the user data from the Users table
    user = User.query.get_or_404(user_id)
    try:
        # Delete from Users table
        db.session.delete(user)
        db.session.commit()
        return render_template('admin.html')
    except:
        flash("Failed.")


@admin_blueprint.route('/view_suppliers_Preferences', methods=['POST'])
@login_required
@requires_roles('admin')
def view_supplier_preferences():
    """
    Allows the admin to view all supplier preferences, this includes the suppliers which are
    blacklisted and favourited.
    """
    return render_template('admin.html', supplier_preferences=Supplier.query.all())


@admin_blueprint.route('/favourite_supplier', methods=['POST'])
@login_required
@requires_roles('admin')
def favourite_supplier():
    """
    Allows the admin to make a certain supplier 'favourited'
    """
    # retrieve the name of the supplier inputted
    favourite = request.form.get('favourite_supplier')

    # If the supplier does not already exist in the Supplier table, then add them to the  table
    # with Supplier.favourited = True
    if len((Supplier.query.filter_by(name=favourite).all())) == 0:
        new_favourite = Supplier(favourite, 0, 1)
        db.session.add(new_favourite)
        db.session.commit()

    # If the supplier already exists in the Supplier table, then remove the existing one and
    # replace the row. This is to avoid a supplier being blacklisted AND favourited simultaneously
    else:
        Supplier.query.filter_by(name=favourite).delete()
        new_favourite = Supplier(favourite, 0, 1)
        db.session.add(new_favourite)
        db.session.commit()

    flash("Supplier Favourited")
    return admin()


@admin_blueprint.route('/blacklist_supplier', methods=['POST'])
@login_required
@requires_roles('admin')
def blacklist_supplier():
    """
    Allows the admin to make a certain supplier 'blacklisted'
    """
    # retrieve the name of the supplier inputted
    blacklist = request.form.get('blacklist_supplier')

    # If the supplier does not already exist in the Supplier table, then add them to the  table
    # with Supplier.blacklisted = True
    if len((Supplier.query.filter_by(name=blacklist).all())) == 0:
        new_blacklist = Supplier(blacklist, 1, 0)
        db.session.add(new_blacklist)
        db.session.commit()

    # If the supplier already exists in the Supplier table, then remove the existing one and
    # replace the row. This is to avoid a supplier being blacklisted AND favourited simultaneously
    else:
        Supplier.query.filter_by(name=blacklist).delete()
        new_blacklist = Supplier(blacklist, 1, 0)
        db.session.add(new_blacklist)
        db.session.commit()

    flash("Supplier Blacklisted")
    return admin()


@admin_blueprint.route('/remove_preference/<string:name>')
@login_required
@requires_roles('admin')
def remove_preference(name):
    """
    Allows the admin to delete a supplier preference. This is either a supplier blacklist or a
    supplier favourite. Essentially, the supplier is removed from the Supplier table.
    :param name: The supplier to be removed.
    """
    # retrieve the name of the supplier inputted
    supplier = Supplier.query.get_or_404(name)

    try:
        # Rempve the supplier row in the Supplier table.
        db.session.delete(supplier)
        db.session.commit()
        return render_template('admin.html')
    except:
        flash("Failed.")
        return render_template('admin.html')
