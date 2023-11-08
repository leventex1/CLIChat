import requests
from application.parser import pre_symbol

class Commander:
    """
        User input functionalities.
    """

    #: Other connected client webserver's address.
    OTHER_IP_PORT: str = None
    #: Other clients pending connections, list of ip:port strings.
    PENDING_CONNECTIONS: list[str] = []
    #: This client pending connectinos. list of ip:port strings.
    MY_PENDING_CONNECTIONS: list[str] = []

    # webserver_port: the client webserver's port number.
    def __init__(self, webserver_port: int) -> None:
        self.webserver_port = webserver_port

    
    def help(self) -> None:
        print(
        f"""
{pre_symbol}help:                           Prints this help message.
{pre_symbol}exit:                           Exits out of the application.
{pre_symbol}pending:                        Prints the pending connections.
{pre_symbol}mypending:                      Prints my pending connections.
{pre_symbol}connect -param:                 Connects to another client.
                                            -param: IPv4:port address.
{pre_symbol}disconnect:                     Disconnects from the current connection.
{pre_symbol}connection:                     Prints the current connection.
        """)

    # Blocks the thread and get an input from the user.
    def get_input(self) -> str:
        _input_ = input("You > ")
        return _input_
    
    def get_pending_connections(self) -> None:
        print('pending connections:', len(Commander.PENDING_CONNECTIONS))
        for pending in Commander.PENDING_CONNECTIONS:
            print(pending)

    def get_my_pending_connections(self) -> None:
        print('my pending connections:', len(Commander.MY_PENDING_CONNECTIONS))
        for pending in Commander.MY_PENDING_CONNECTIONS:
            print(pending)

    def get_connection(self) -> None:
        print('Current connection:', Commander.OTHER_IP_PORT)
    
    # ip_port: Other client webserver's port number.
    def make_connection(self, ip_port: str) -> bool:
        if Commander.OTHER_IP_PORT != None:
            print(f'You are connected with: {Commander.OTHER_IP_PORT}')
            return False
        
        request = requests.post(f'http://{ip_port}/connect/127.0.0.1/{self.webserver_port}')
        if request.status_code == 200:
            Commander.OTHER_IP_PORT = ip_port
            if ip_port in Commander.MY_PENDING_CONNECTIONS:
                Commander.MY_PENDING_CONNECTIONS.remove(ip_port)
            if ip_port in Commander.PENDING_CONNECTIONS:
                Commander.PENDING_CONNECTIONS.remove(ip_port)
            print(f'Connection made with: {ip_port}')
            return True
        elif request.status_code == 201:
            Commander.MY_PENDING_CONNECTIONS.append(ip_port)
            Commander.MY_PENDING_CONNECTIONS = list(set(Commander.MY_PENDING_CONNECTIONS))
            print(f'Connection request is sent to: {ip_port}')
            return True
        else:
            print(f'Connection request failed to: {ip_port}')
            return False
        
    def make_disconnection(self) -> bool:
        if Commander.OTHER_IP_PORT == None:
            print('You are not connected')
            return False
        
        request = requests.delete(f'http://{Commander.OTHER_IP_PORT}/disconnect/127.0.0.1/{self.webserver_port}')
        if request.status_code == 200:
            print(f'You are disconnected from {Commander.OTHER_IP_PORT}')
            Commander.OTHER_IP_PORT = None
            return True
        else:
            Commander.OTHER_IP_PORT = None
            return False

    def send_message(self, message: str) -> bool:
        if Commander.OTHER_IP_PORT == None:
            print('You are not connected')
            return False
        
        request = requests.post(f'http://{Commander.OTHER_IP_PORT}/message/127.0.0.1/{self.webserver_port}', json={
            'message': message
        })
        if request.status_code == 200:
            return True
        else:
            print('Message is not received, disconnecting...')
            Commander.OTHER_IP_PORT = None
            return False
