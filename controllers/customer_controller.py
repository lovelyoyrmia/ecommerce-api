import re
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from model import User, db
from flask_login import login_user, logout_user, current_user, login_required

from model.models import Ebook, Orders


def register():
    if current_user.is_authenticated and current_user.is_admin:
        req_data = request.get_json()
        if (
            "name" in req_data
            and "email" in req_data
            and "phone_number" in req_data
            and "address" in req_data
            and "password" in req_data
        ):
            name = req_data["name"]
            email = req_data["email"]
            phone_number = req_data["phone_number"]
            address = req_data["address"]
            password = req_data["password"]
            if (
                name != ""
                and email != ""
                and address != ""
                and password != ""
                and int(phone_number)
            ):
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    return jsonify({"message": "Email is invalid"})
                else:
                    _hash_password = generate_password_hash(password)
                    print(_hash_password)
                    user = User.query.filter_by(email=email, is_admin=False).first()
                    print(user)
                    if user and not user.is_admin:
                        return jsonify({"message": "Email already exists"})
                    else:
                        customer = User(
                            name=name,
                            email=email,
                            phone_number=phone_number,
                            address=address,
                            password=_hash_password,
                            is_admin=False,
                        )
                        db.session.add(customer)
                        db.session.commit()
                        return jsonify({"message": "Success Created"})
            else:
                return jsonify({"message": "All fileds can not be null"})

        else:
            return jsonify({"message": "All fileds are required"}), 400
    else:
        return jsonify({"message": "Admin is not logged in"}), 401


def login():
    if current_user.is_authenticated and current_user.is_admin:
        req_data = request.get_json()

        if "name" in req_data and "password" in req_data:
            name = req_data["name"]
            password = req_data["password"]
            if name != "" and password != "":
                customer = User.query.filter_by(name=name, is_admin=False).first()
                if customer and check_password_hash(customer.password, password):
                    login_user(customer)
                    data = {
                        "name": customer.name,
                        "email": customer.email,
                        "phone_number": customer.phone_number,
                        "address": customer.address,
                    }
                    return jsonify({"message": "login successfully", "data": data})
                elif customer and not check_password_hash(customer.password, password):
                    return jsonify({"message": "Wrong password"})
                else:
                    return jsonify({"message": "User not found"})
            else:
                return jsonify({"message": "All fileds can not be null"})
        else:
            return jsonify({"message": "All fileds are required"}), 400
    else:
        return jsonify({"message": "Admin is not logged in"}), 401


@login_required
def logout():
    if current_user.is_authenticated and not current_user.is_admin:
        logout_user()
        return jsonify({"message": "Successfully logged out"})
    else:
        return jsonify({"message": "Already logged out"})


@login_required
def get_ebook():
    if current_user.is_authenticated and not current_user.is_admin:
        customer = User.query.filter_by(id=current_user.id, is_admin=False).first()
        if customer == None:
            return jsonify({"message": "User not found"}), 401
        else:
            orders = Orders.query.all()
            customer_order = []
            for order in orders:
                customer_id = order.customer_id
                if customer_id == current_user.id:
                    ebook_id = order.ebook_id
                    ebook = Ebook.query.filter_by(id=ebook_id).first()
                    data = {}
                    data["order_id"] = order.id
                    data["harga"] = ebook.harga
                    data["waktu_pembelian"] = order.ordered_date
                    data["judul"] = ebook.judul
                    data["penulis"] = ebook.penulis
                    data["sinopsis"] = ebook.sinopsis
                    data["image_url"] = ebook.image_url
                    data["content_url"] = ebook.content_url
                    customer_order.append(data)
            customer_order.sort(key=lambda order: order["waktu_pembelian"])
            return jsonify({"message": "Success", "data": customer_order})

    else:
        return jsonify({"message": "Not Allowed"}), 401
