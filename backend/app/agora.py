from flask_restx import Namespace, Resource, fields
from agora_token_builder import RtcTokenBuilder
import time
from flask import request
from .config import Config
from .redis_client import RedisClient
from uuid import uuid4
from datetime import datetime

api = Namespace('agora', description='Agora Video Call operations')
redis_client = RedisClient()

# In-memory storage for channel users (In production, use Redis or a database)
channel_users = {}

user_model = api.model('User', {
    'uid': fields.String(description='User ID'),
    'username': fields.String(description='Username'),
    'joined_at': fields.DateTime(description='Join timestamp')
})

channel_model = api.model('Channel', {
    'users': fields.List(fields.Nested(user_model)),
    'channel_name': fields.String(description='Channel name')
})

join_model = api.model('JoinChannel', {
    'channel_name': fields.String(required=True, description='Channel name'),
    'username': fields.String(required=True, description='Username of the joining user')
})

token_model = api.model('Token', {
    'channel_name': fields.String(required=True, description='Channel name for the video call')
})

@api.route('/token')
class AgoraToken(Resource):
    @api.expect(token_model)
    def post(self):
        """Generate an Agora token for video calling."""
        data = request.json
        channel_name = data.get('channel_name')
        uid = uuid4().__str__()

        # Set expiration time for the token (24 hours)
        expiration_time_in_seconds = 24 * 3600
        current_timestamp = int(time.time())
        privilege_expired_ts = current_timestamp + expiration_time_in_seconds

        # Generate token
        token = RtcTokenBuilder.buildTokenWithUid(
            appId=Config.AGORA_APP_ID,
            appCertificate=Config.AGORA_APP_CERTIFICATE,
            channelName=channel_name,
            uid=uid,
            role=1,
            privilegeExpiredTs=privilege_expired_ts
        )

        return {
            'token': token,
            'uid': uid,
            'channel_name': channel_name,
            'expires_in': expiration_time_in_seconds
        }


@api.route('/channels/<string:channel_name>/users')
class ChannelUsers(Resource):
    @api.marshal_with(channel_model)
    def get(self, channel_name):
        """Get list of users in a channel"""
        users = redis_client.get_channel_users(channel_name)

        # Filter out inactive users
        current_time = datetime.now()
        active_users = [
            user for user in users
            if (current_time - datetime.fromisoformat(user['last_active'])).seconds < 30
        ]

        return {
            'users': active_users,
            'channel_name': channel_name
        }


@api.route('/channels/join')
class JoinChannel(Resource):
    @api.expect(join_model)
    def post(self):
        """Join a channel"""
        data = request.json
        channel_name = data.get('channel_name')
        username = data.get('username')
        uid = str(uuid4())

        user = {
            'uid': uid,
            'username': username,
            'joined_at': datetime.now().isoformat(),
            'last_active': datetime.now().isoformat()
        }

        redis_client.add_channel_user(channel_name, user)

        return {
            'status': 'success',
            'uid': uid,
            'channel_name': channel_name
        }


@api.route('/channels/<string:channel_name>/leave')
class LeaveChannel(Resource):
    def delete(self, channel_name):
        """Leave a channel"""
        uid = request.args.get('uid')
        redis_client.remove_channel_user(channel_name, uid)
        return {'status': 'success'}


@api.route('/channels/<string:channel_name>/heartbeat')
class Heartbeat(Resource):
    def post(self, channel_name):
        """Update user's last active timestamp"""
        uid = request.json.get('uid')
        redis_client.update_user_heartbeat(channel_name, uid)
        return {'status': 'success'}
