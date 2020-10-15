from classes.auth import access_required
from db import session

from flask_restful import reqparse, inputs
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with

from models.subscription import Subscription

subscription_fields = {
    'id': fields.Integer,
    'start': fields.DateTime,
    'end': fields.DateTime,
    'type': fields.Integer,
    'place_id': fields.Integer,
    'car_id': fields.Integer,
    'uri': fields.Url('subscription', absolute=True),
}

parser = reqparse.RequestParser()
# parser.add_argument('start', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
parser.add_argument('start', type=inputs.datetime_from_iso8601, required=True, nullable=False)
parser.add_argument('end', type=inputs.datetime_from_iso8601, required=True, nullable=False)
parser.add_argument('type', type=int, required=True, nullable=False)
parser.add_argument('place_id', type=int, required=True, nullable=False)
parser.add_argument('car_id', type=int, required=True, nullable=False)


class SubscriptionResource(Resource):
    @access_required(2)
    @marshal_with(subscription_fields)
    def get(self, id):
        subscription = session.query(Subscription).filter(Subscription.id == id).first()
        if not subscription:
            abort(404, message="Subscription {} doesn't exist".format(id))
        return subscription

    @access_required(2)
    def delete(self, id):
        subscription = session.query(Subscription).filter(Subscription.id == id).first()
        if not subscription:
            abort(404, message="Subscription {} doesn't exist".format(id))
        session.delete(subscription)
        session.commit()
        return {}, 204

    @access_required(2)
    @marshal_with(subscription_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        subscription = session.query(Subscription).filter(Subscription.id == id).first()
        subscription.start = parsed_args['start']
        subscription.end = parsed_args['end']
        subscription.type = parsed_args['type']
        subscription.place_id = parsed_args['place_id']
        subscription.car_id = parsed_args['car_id']
        session.add(subscription)
        session.commit()
        return subscription, 201


class SubscriptionListResource(Resource):
    @access_required(2)
    @marshal_with(subscription_fields)
    def get(self):
        subscriptions = session.query(Subscription).all()
        return subscriptions

    @access_required(2)
    @marshal_with(subscription_fields)
    def post(self):
        parsed_args = parser.parse_args()
        subscription = Subscription(start=parsed_args['start'],
                                    end=parsed_args['end'],
                                    type=parsed_args['type'],
                                    place_id=parsed_args['place_id'],
                                    car_id=parsed_args['car_id']
                                    )
        session.add(subscription)
        session.commit()
        return subscription, 201
