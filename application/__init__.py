from application.commander import Commander
from application.parser import Parser
from application.webserver import start_webserver, stop_webserver

def main(webserver_port: int):

    start_webserver(port=webserver_port)
    commander = Commander(webserver_port)

    commander.help()

    while True:

        _input_ = commander.get_input()

        try:
            parser = Parser(message=_input_)
        except Exception as e:
            #print(e)
            continue
        

        """
            Command processing.
        """
        if parser.is_quite():
            break
        
        elif parser.is_help():
            commander.help()

        elif parser.is_get_connection():
            commander.get_connection()

        elif parser.is_pending():
            commander.get_pending_connections()

        elif parser.is_my_pending():
            commander.get_my_pending_connections()
        
        elif parser.get_ip_port():
            commander.make_connection(parser.get_ip_port())

        elif parser.disconnect:
            commander.make_disconnection()

        else:
            commander.send_message(parser.get_message())


    commander.make_disconnection()
    stop_webserver()

