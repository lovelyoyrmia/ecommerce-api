from flask_login import LoginManager, current_user
from model import db
from flask import jsonify, request
from config import create_app
from model.models import Ebook, Orders, User
from routes.staff_router import staff_router
from routes.customer_router import customer_router

app = create_app()

app.app_context().push()
db.create_all(app=create_app())
login_manager = LoginManager(app)

app.register_blueprint(staff_router, url_prefix="/admin")
app.register_blueprint(customer_router, url_prefix="/customer")


@login_manager.user_loader
def load_user(user_id):
    login_user = User.query.get(int(user_id))
    return login_user


@app.route("/")
def home():
    user = current_user.is_authenticated
    if user:
        return f"{current_user.is_admin}"
    else:
        return "hai"


@app.route("/ebook")
def get_ebook():
    ebooks = Ebook.query.all()
    results = []
    for book in ebooks:
        data = {}
        data["judul"] = book.judul
        data["penulis"] = book.penulis
        data["sinopsis"] = book.sinopsis
        data["harga"] = book.harga
        data["image_url"] = book.image_url
        data["content_url"] = book.content_url

        results.append(data)

    return jsonify({"message": "Success", "data": results})


@app.route("/ebook/<int:ebook_id>")
def get_ebook_id(ebook_id):
    ebook = Ebook.query.filter_by(id=ebook_id).first()
    if ebook == None:
        return jsonify({"message": "No such data"})
    else:
        data = {
            "judul": ebook.judul,
            "penulis": ebook.penulis,
            "sinopsis": ebook.sinopsis,
            "harga": ebook.harga,
            "image_url": ebook.image_url,
            "content_url": ebook.content_url,
        }
        return jsonify({"message": "Success", "data": data})


@app.route("/order", methods=["POST"])
def order():
    if not current_user.is_authenticated:
        return jsonify({"message": "You need to login first"}), 401
    else:
        if not current_user.is_admin:
            req_data = request.get_json()
            if "id_buku" not in req_data:
                return jsonify({"message": "Book id is required"})
            else:
                ebook_id = req_data["id_buku"]
                customer_id = current_user.id
                if type(ebook_id) is str:
                    return jsonify({"message": "Id should be numbers"})
                else:
                    orders = Orders(ebook_id=int(ebook_id), customer_id=customer_id)
                    db.session.add(orders)
                    db.session.commit()
                    return jsonify({"message": "Added Successfully"})
        else:
            return jsonify({"message": "Only customer can access"}), 401


if __name__ == "__main__":
    app.run()
