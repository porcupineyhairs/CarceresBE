from flask_restful import Resource, fields, abort
from flask_restful import marshal_with
from flask_restful import reqparse

from classes.NestedWidthEmpty import NestedWithEmpty
from classes.auth import token_required, auth
from classes.views import make_response_headers
from db import session
from models.client import Client

user_fields = {
    'name': fields.String,
    'user_type': fields.Integer,
    'uri': fields.Url('user_manage', absolute=True),
    'client': NestedWithEmpty({
        'name': fields.String,
        'surname': fields.String,
        'address': fields.String,
        'city': fields.String,
        'phone': fields.String,
        'uri': fields.Url('client_manage', absolute=True),
    }, allow_null=True),
}

client_fields = {
    'name': fields.String,
    'surname': fields.String,
    'address': fields.String,
    'city': fields.String,
    'phone': fields.String,
    'uri': fields.Url('client_manage', absolute=True),
    'cars': NestedWithEmpty({
        'plate': fields.String,
        'uri': fields.Url('car', absolute=True),
    }, allow_empty=True),
    'user': NestedWithEmpty({
        'name': fields.String,
        'user_type': fields.Integer,
        'uri': fields.Url('user_manage', absolute=True),
    }, allow_null=True),
}
parser_user = reqparse.RequestParser()
parser_user.add_argument('password', type=str, required=True, nullable=False)

parser_client = reqparse.RequestParser()
parser_client.add_argument('name', type=str, required=False, nullable=False)
parser_client.add_argument('surname', type=str, required=False, nullable=False)
parser_client.add_argument('address', type=str, required=False, nullable=True)
parser_client.add_argument('city', type=str, required=False, nullable=True)
parser_client.add_argument('phone', type=str, required=False, nullable=True)


class UserManageResource(Resource):
    """
    Resources for 'user_manage' (/api/user) endpoint.
    """

    @token_required
    @marshal_with(user_fields)
    def get(self):
        """
        Returns the data of the currently authenticated user.
        """
        return auth.user, 200, make_response_headers(auth.user)

    @token_required
    @marshal_with(user_fields)
    def put(self):
        """
        Update and returns the data of the currently authenticated user.
        """
        parsed_args = parser_user.parse_args()
        auth.user.hash_password(parsed_args['password'])
        session.add(auth.user)
        session.commit()
        return auth.user, 201, make_response_headers(auth.user)


class ClientManageResource(Resource):
    """
    Resources for 'client_manage' (/api/client) endpoint.
    """

    @token_required
    @marshal_with(client_fields)
    def get(self):
        """
        Returns the client data of the currently authenticated user.
        """
        if not auth.user.client:
            abort(404, message="Client doesn't exist")
        return auth.user.client, 200, make_response_headers(auth.user.client)

    @token_required
    @marshal_with(client_fields)
    def put(self):
        """
        Update and returns the client data of the currently authenticated user.
        """
        client = session.query(Client).filter(Client.user_id == auth.user.id).first()
        if not client:
            abort(404, message="Client doesn't exist")
        parsed_args = parser_client.parse_args()
        if parsed_args['name'] is not None:
            client.name = parsed_args['name']
        if parsed_args['surname'] is not None:
            client.surname = parsed_args['surname']
        if parsed_args['address'] is not None:
            client.address = parsed_args['address']
        if parsed_args['city'] is not None:
            client.city = parsed_args['city']
        if parsed_args['phone'] is not None:
            client.phone = parsed_args['phone']
        session.add(client)
        session.commit()
        return client, 201, make_response_headers(auth.user.client)
