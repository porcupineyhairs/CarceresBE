from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from classes.ListResource import ListResource
from classes.NestedWidthEmpty import NestedWithEmpty
from classes.SingleResource import SingleResource
from classes.auth import token_required, access_required, Rights
from models.user import User

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'user_type': fields.Integer,
    'uri': fields.Url('user', absolute=True),
    # 'password_hash': fields.String,
    'client': NestedWithEmpty({
        'id': fields.Integer,
        'name': fields.String,
        'surname': fields.String,
        'address': fields.String,
        'city': fields.String,
        'phone': fields.String,
        'user_id': fields.Integer,
        'uri': fields.Url('client', absolute=True),
    }, allow_null=True),
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('user_type', type=str)
parser.add_argument('password', type=str, required=False, nullable=False)


class UserResource(SingleResource):
    """
    Resources for 'user' (/api/users/<id>) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = User
        self.model_name = "user"
        self.marshal_fields = user_fields

    @access_required(Rights.MOD)
    @marshal_with(user_fields)
    def get(self, id):
        """
        Returns user's data.
        """
        return self.process_get_req(id)

    @access_required(Rights.ADMIN)
    def delete(self, id):
        """
        Delete user from database.
        """
        return self.process_delete_req(id)

    @access_required(Rights.ADMIN)
    @marshal_with(user_fields)
    def put(self, id):
        """
        Update user's data.
        """
        parsed_args = parser.parse_args()
        user = self.get_model(id)
        user.name = parsed_args['name']
        user.user_type = parsed_args['user_type']
        if parsed_args['password'] is not None:
            user.hash_password(parsed_args['password'])
        return self.finalize_put_req(user)


class UserListResource(ListResource):
    """
    Resources for 'users' (/api/users) endpoint.
    """

    def __init__(self):
        super().__init__()
        self.model_class = User
        self.model_name = "user"
        self.marshal_fields = user_fields

    @access_required(Rights.MOD)
    @token_required
    def get(self):
        """
        Returns data of all users.
        """
        return self.process_get_req()

    @access_required(Rights.ADMIN)
    @marshal_with(user_fields)
    def post(self):
        """
        Create new user.
        """
        parsed_args = parser.parse_args()
        user = User(name=parsed_args['name'], user_type=parsed_args['user_type'])
        if parsed_args['password'] is not None:
            user.hash_password(parsed_args['password'])
        return self.finalize_post_req(user)