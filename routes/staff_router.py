from flask import Blueprint
from controllers.staff_controller import logout, register, login, ebook, get_ebook_id

staff_router = Blueprint("staff_router", __name__)

staff_router.route("/register", methods=["POST"])(register)
staff_router.route("/login", methods=["POST"])(login)
staff_router.route("/logout")(logout)

staff_router.route("/ebook", methods=["GET", "POST"])(ebook)
staff_router.route("/ebook/<int:ebook_id>", methods=["GET", "PUT", "DELETE"])(
    get_ebook_id
)
