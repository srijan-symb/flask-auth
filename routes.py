# routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from .models import db, User, Contact
from .helpers import validate_signup_data, validate_login_data, validate_contact_data

main_bp = Blueprint("main_bp", __name__)


# User Routes
@main_bp.route("/user/signup", methods=["POST"])
def signup():
    data = request.get_json()
    is_valid, message = validate_signup_data(data)
    if not is_valid:
        return jsonify({"message": message, "data": {}}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already registered", "data": {}}), 400

    hashed_password = generate_password_hash(data["password"])
    new_user = User(name=data["name"], email=data["email"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)
    user_data = {"id": new_user.id, "name": new_user.name, "email": new_user.email}

    return (
        jsonify(
            {
                "message": "User signup complete",
                "data": {"access_token": access_token, "user": user_data},
            }
        ),
        200,
    )


@main_bp.route("/user/login", methods=["POST"])
def login():
    data = request.get_json()
    is_valid, message = validate_login_data(data)
    if not is_valid:
        return jsonify({"message": message, "data": {}}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return jsonify({"message": "Email not registered", "data": {}}), 400

    if not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid credentials", "data": {}}), 401

    access_token = create_access_token(identity=user.id)
    user_data = {"id": user.id, "name": user.name, "email": user.email}

    return (
        jsonify(
            {
                "message": "Login successful",
                "data": {"access_token": access_token, "user": user_data},
            }
        ),
        200,
    )


@main_bp.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Authentication failed", "data": {}}), 401

    user_data = {"id": user.id, "name": user.name, "email": user.email}
    return jsonify({"message": "User detail", "data": user_data}), 200


# Contact Routes
@main_bp.route("/contact", methods=["POST"])
@jwt_required()
def add_contact():
    user_id = get_jwt_identity()
    data = request.get_json()
    is_valid, message = validate_contact_data(data)
    if not is_valid:
        return jsonify({"message": message, "data": {}}), 400

    new_contact = Contact(
        name=data["name"],
        email=data.get("email"),
        phone=data["phone"],
        address=data.get("address"),
        country=data.get("country"),
        user_id=user_id,
    )
    db.session.add(new_contact)
    db.session.commit()

    contact_data = {
        "id": new_contact.id,
        "name": new_contact.name,
        "email": new_contact.email,
        "phone": new_contact.phone,
        "country": new_contact.country,
        "address": new_contact.address,
    }

    return jsonify({"message": "Contact added", "data": contact_data}), 200


@main_bp.route("/contact", methods=["GET"])
@jwt_required()
def get_contacts():
    user_id = get_jwt_identity()

    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    sort_by = request.args.get("sort_by", "latest")

    # Filtering parameters
    name_filter = request.args.get("name", "").strip()
    email_filter = request.args.get("email", "").strip()
    phone_filter = request.args.get("phone", "").strip()

    query = Contact.query.filter_by(user_id=user_id)

    # Apply filters
    if name_filter:
        query = query.filter(Contact.name.ilike(f"%{name_filter}%"))
    if email_filter:
        query = query.filter(Contact.email.ilike(f"%{email_filter}%"))
    if phone_filter:
        query = query.filter(Contact.phone.ilike(f"%{phone_filter}%"))

    # Apply sorting
    if sort_by == "latest":
        query = query.order_by(Contact.id.desc())
    elif sort_by == "oldest":
        query = query.order_by(Contact.id.asc())
    elif sort_by == "alphabetically_a_to_z":
        query = query.order_by(Contact.name.asc())
    elif sort_by == "alphabetically_z_to_a":
        query = query.order_by(Contact.name.desc())

    pagination = query.paginate(page=page, per_page=limit, error_out=False)

    contacts = []
    for contact in pagination.items:
        contacts.append(
            {
                "id": contact.id,
                "name": contact.name,
                "email": contact.email,
                "phone": contact.phone,
                "country": contact.country,
                "address": contact.address,
            }
        )

    data = {
        "list": contacts,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "page": pagination.page,
        "pages": pagination.pages,
        "per_page": pagination.per_page,
        "total": pagination.total,
    }

    return jsonify({"message": "Contact list", "data": data}), 200
