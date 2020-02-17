from flask import Flask, render_template, request, session, jsonify, make_response, redirect, url_for
from datetime import timedelta
import random
import string
from collections import deque

def generate_token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

def generate_chat_id():
    return ''.join(random.choice(string.digits) for _ in range(6))

app = Flask(__name__)
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(hours=6)

TOKEN_TO_NAME = {}
CHATROOMS = {}

@app.route('/')
def index():
	return render_template('form.html')

@app.route('/create', methods=['POST'])
def create():
	req = request.get_json(force=True)
	name = req['name']

	chat_id = req.get('chat_id', '')
	invitation_token = req.get('invitation_token', '')

	session_token = generate_token()
	while (session_token in TOKEN_TO_NAME):
		session_token = generate_token()

	TOKEN_TO_NAME[session_token] = name

	if (chat_id and invitation_token):
		# check if larger than 6
		if (len(CHATROOMS[chat_id]['session_token']) == 6):
				return make_response(jsonify({'error': 'Already 6 people in the Watch Party!'}), 200)

		# if no larger than 5, direct user to the room
		session['USERNAME'] = name
		session['TOKEN'] = session_token

		CHATROOMS[chat_id]['session_token'].append(session_token)

		data = {
			'chat_id': chat_id,
			'session_token': session_token
		}

		return make_response(jsonify(data), 200)

	else:
		session['USERNAME'] = name
		session['TOKEN'] = session_token

		chat_id = generate_chat_id()
		while (chat_id in CHATROOMS):
			chat_id = generate_chat_id()

		# if (chat_id not in CHATROOMS):
		CHATROOMS[chat_id] = {}
		CHATROOMS[chat_id]['session_token'] = []
		CHATROOMS[chat_id]['session_token'].append(session_token)
		CHATROOMS[chat_id]['messages'] = []

		data = {
			'chat_id': chat_id,
			'session_token': session_token
		}

		return make_response(jsonify(data), 200)



@app.route('/<chat_id>', methods=['GET', 'POST'])
def chat(chat_id):

	if request.method == "GET":
		# if chat_id does not exist
		if (chat_id not in CHATROOMS) or (session['TOKEN'] not in CHATROOMS[chat_id]['session_token']):
				return make_response(jsonify({'error': 'Chat does not exist!'}), 403)

		# get message for chat
		if (request.headers.get('Contenttype', False)):

			# print('I am printing......', chat_id)

			messages = CHATROOMS[chat_id]['messages']

			data = {
				'messages': messages
			}

			return jsonify(data)

		# passing all checks, render chatroom
		return render_template('chat.html', chat_id=chat_id, room=chat_id)

	# store new message and send to chat
	if request.method == "POST":
		req = request.get_json(force=True)

		chat_id = req['chat_id']
		message = req['message']
		
		session_token = session['TOKEN']

		name = TOKEN_TO_NAME[session_token]

		# print('I am printing......', CHATROOMS['1']['messages'])

		message = name + ': ' + message
		# print('I am printing......', message)

		message_queue = CHATROOMS[chat_id]['messages']
		message_queue.append(message)

		# if more than 30 messages, pop top one
		while (len(message_queue) > 30):
			message_queue.pop(0)

		data = {
			'message': message
		}

		return jsonify(data)

@app.route('/<chat_id>/invite', methods=['POST'])
def invite(chat_id):
	# return invitation link
	req = request.get_json(force=True)
	url = request.url_root
	# print('I am printing......', url)

	if 'invitation_token' not in CHATROOMS[chat_id]:
		invitation_token = generate_token()
		CHATROOMS[chat_id]['invitation_token'] = invitation_token
	else:
		invitation_token = CHATROOMS[chat_id]['invitation_token']

	magic_link = url + chat_id + '?magic=' + invitation_token
	# print('I am printing......', url)

	data = {
		'magic_link': magic_link
	}

	return make_response(jsonify(data), 200)


if __name__ == '__main__':
	app.run(debug=True)
