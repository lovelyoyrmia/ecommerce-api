from flask import Blueprint
from controllers.customer_controller import register, login, logout, get_ebook

customer_router = Blueprint("customer_router", __name__)

customer_router.route("/register", methods=["POST"])(register)
customer_router.route("/login", methods=["POST"])(login)
customer_router.route("/logout")(logout)
customer_router.route("/orders", methods=["GET"])(get_ebook)
