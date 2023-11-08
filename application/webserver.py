from flask import Flask, request
import threading
import logging

from application.commander import Commander

thread = None

flask_app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True

@flask_app.post("/connect/<ip>/<port>")
def connect(ip: str, port: int):
    ip_port = f'{ip}:{port}'
    if ip_port in Commander.MY_PENDING_CONNECTIONS:
        if Commander.OTHER_IP_PORT is None:
            Commander.OTHER_IP_PORT = ip_port
            if ip_port in Commander.MY_PENDING_CONNECTIONS:
                Commander.MY_PENDING_CONNECTIONS.remove(ip_port)
            if ip_port in Commander.PENDING_CONNECTIONS:
                Commander.PENDING_CONNECTIONS.remove(ip_port)
            print(f'Connection made with: {ip_port}')
            return { 'message': f'Connection made with ({ip}:{port}).' }, 200
        else:
            return { 'message': f'Connection failed with ({ip}:{port}).' }, 400
    else:
        Commander.PENDING_CONNECTIONS.append(ip_port)
        Commander.PENDING_CONNECTIONS = list(set(Commander.PENDING_CONNECTIONS))
        return { 'message': f'Connection of ({ip}:{port}) is pending.' }, 201
    
@flask_app.delete('/disconnect/<ip>/<port>')
def disconnect(ip: str, port: int):
    ip_port = f'{ip}:{port}'

    if ip_port == Commander.OTHER_IP_PORT:
        Commander.OTHER_IP_PORT = None
        print(f'{ip_port} has disconnected')
        return { 'message': 'Disconnection is made.'}, 200
    else:
        return { 'message': 'Disconnection failed.' }, 400
    
@flask_app.post('/message/<ip>/<port>')
def read_message(ip: str, port: int):
    ip_port = f'{ip}:{port}'
    data: dict = request.json

    if ip_port == Commander.OTHER_IP_PORT:
        print()
        print('Other >', data.get('message'))
        return { 'message': 'Received.' }, 200
    else:
        return { 'message': 'Message failed.' }, 400


def run_flask_app(host, port):
    flask_app.run(host=host, port=port, debug=False)

def start_webserver(port: int):
    global thread
    thread = threading.Thread(target=run_flask_app, args=('127.0.0.1', port))
    thread.setDaemon(True)
    thread.start()
    
def stop_webserver():
    pass