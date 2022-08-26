import re
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from model import User, db, Ebook
from flask_login import login_user, logout_user, login_required, current_user


def register():
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
        _hash_password = generate_password_hash(password)
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
                user = User.query.filter_by(email=email).first()
                if user and user.is_admin:
                    return jsonify({"message": "Email already exists"})
                else:
                    staff = User(
                        name=name,
                        email=email,
                        phone_number=phone_number,
                        address=address,
                        password=_hash_password,
                    )
                    db.session.add(staff)
                    db.session.commit()
                    return jsonify({"message": "Success Created"})
        else:
            return jsonify({"message": "All fileds can not be null"})
    else:
        return jsonify({"message": "All fileds are required"}), 400


def login():
    req_data = request.get_json()

    if "name" in req_data and "password" in req_data:
        name = req_data["name"]
        password = req_data["password"]
        if name != "" and password != "":
            staff = User.query.filter_by(name=name, is_admin=True).first()
            if staff and check_password_hash(staff.password, password):
                login_user(staff)
                return jsonify({"message": "login successfully"})
            elif staff and not check_password_hash(staff.password, password):
                return jsonify({"message": "Wrong password"})
            else:
                return jsonify({"message": "User not found"})
        else:
            return jsonify({"message": "All fileds can not be null"})
    else:
        return jsonify({"message": "All fileds are required"}), 400


@login_required
def logout():
    if current_user.is_admin:
        logout_user()
        return jsonify({"message": "Successfully logged out"})
    else:
        return jsonify({"message": "Already logout"})


@login_required
def ebook():
    if current_user.is_authenticated and current_user.is_admin:
        if request.method == "POST":
            req_data = request.get_json()
            if (
                "judul" in req_data
                and "penulis" in req_data
                and "sinopsis" in req_data
                and "harga" in req_data
                and "image_url" in req_data
                and "content_url" in req_data
            ):
                judul = req_data["judul"]
                penulis = req_data["penulis"]
                sinopsis = req_data["sinopsis"]
                harga = req_data["harga"]
                image_url = req_data["image_url"]
                content_url = req_data["content_url"]

                if (
                    judul != ""
                    and penulis != ""
                    and sinopsis != ""
                    and int(harga)
                    and image_url != ""
                    and content_url != ""
                ):
                    ebook = Ebook(
                        judul=judul,
                        penulis=penulis,
                        sinopsis=sinopsis,
                        harga=harga,
                        image_url=image_url,
                        content_url=content_url,
                    )
                    db.session.add(ebook)
                    db.session.commit()

                    data = {
                        "id_buku": ebook.id,
                        "judul": ebook.judul,
                        "penulis": ebook.penulis,
                        "sinopsis": ebook.sinopsis,
                        "harga": ebook.harga,
                        "image_url": ebook.image_url,
                        "content_url": ebook.content_url,
                    }

                    return jsonify({"message": "Success", "data": data})

                else:
                    return jsonify({"message": "All fields cannot be null"})

            else:
                return jsonify({"message": "All fields are required"})

        if request.method == "GET":
            ebooks = Ebook.query.all()
            results = []
            for book in ebooks:
                data = {}
                data["id_buku"] = book.id
                data["judul"] = book.judul
                data["penulis"] = book.penulis
                data["sinopsis"] = book.sinopsis
                data["harga"] = book.harga
                data["image_url"] = book.image_url
                data["content_url"] = book.content_url

                results.append(data)

            return jsonify({"message": "Success", "data": results})
    else:
        return jsonify({"message": "Not Allowed"}), 401


@login_required
def get_ebook_id(ebook_id):
    if current_user.is_authenticated and current_user.is_admin:
        if request.method == "GET":
            ebook = Ebook.query.filter_by(id=ebook_id).first()
            if ebook == None:
                return jsonify({"message": "No such data"})
            else:
                data = {
                    "id_buku": ebook.id,
                    "judul": ebook.judul,
                    "penulis": ebook.penulis,
                    "sinopsis": ebook.sinopsis,
                    "harga": ebook.harga,
                    "image_url": ebook.image_url,
                    "content_url": ebook.content_url,
                }
                return jsonify({"message": "Success", "data": data})
        elif request.method == "PUT":
            req_data = request.get_json()
            if (
                "judul" in req_data
                and "penulis" in req_data
                and "sinopsis" in req_data
                and "harga" in req_data
                and "image_url" in req_data
                and "content_url" in req_data
            ):
                judul = req_data["judul"]
                penulis = req_data["penulis"]
                sinopsis = req_data["sinopsis"]
                harga = req_data["harga"]
                image_url = req_data["image_url"]
                content_url = req_data["content_url"]

                ebook = Ebook.query.filter_by(id=ebook_id).first()
                if ebook == None:
                    return jsonify({"message": "No such data"})
                else:
                    ebook.judul = judul
                    ebook.penulis = penulis
                    ebook.sinopsis = sinopsis
                    ebook.harga = harga
                    ebook.image_url = image_url
                    ebook.content_url = content_url
                    db.session.commit()

                    data = {
                        "id_buku": ebook_id,
                        "judul": ebook.judul,
                        "penulis": ebook.penulis,
                        "sinopsis": ebook.sinopsis,
                        "harga": ebook.harga,
                        "image_url": ebook.image_url,
                        "content_url": ebook.content_url,
                    }

                    return jsonify({"message": "Success", "data": data})

            else:
                return jsonify({"message": "All fields are required"})

        elif request.method == "DELETE":
            ebook = Ebook.query.filter_by(id=ebook_id).first()
            if ebook is None:
                return jsonify({"message": "No such data"})
            else:
                ebook.delete()
                db.session.commit()
                return jsonify({"message": "Successfully deleted"})
    else:
        return jsonify({"message": "Not Allowed"}), 401
