import re
from typing import Union

# Pre command symbol.
pre_symbol = '!'

class Parser:
    """
        Parses the input 'messages' or commands.
        Sets the parser parameters that determines how the program will operate.
    """

    # message: some user inputed string.
    def __init__(self, message: str):
        self.message = message

        data: list[str] = self.message.split(' ')

        if len(data) == 0:
            raise Exception('Invalid message')

        # eleminate empty strings.
        data: list[str] = [d for d in data if d != '']


        """
            Command parsers.
        """
        self.quite = data[0] == f'{pre_symbol}exit'

        self.help = data[0] == f'{pre_symbol}help'

        self.get_connection = data[0] == f'{pre_symbol}connection'

        # Check for connection command.
        self.ip_port = None
        if data[0] == f'{pre_symbol}connect':
            # No param
            if len(data) == 1:
                raise Exception('ip:port param is needed for connection')
            
            # Invalid param.
            pattern = re.compile(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})$')
            match = pattern.match(data[1])
            if not match:
                raise Exception('ip:port param is not valid IPv4 format')
            self.ip_port = data[1]

        self.pending = data[0] == f'{pre_symbol}pending'

        self.mypending = data[0] == f'{pre_symbol}mypending'

        self.disconnect = data[0] == f'{pre_symbol}disconnect'
    



    def get_message(self) -> str:
        return self.message
    
    def is_quite(self) -> bool:
        return self.quite
    
    def is_help(self) -> bool:
        return self.help
    
    def is_get_connection(self) -> bool:
        return self.get_connection
    
    def is_pending(self) -> bool:
        return self.pending
    
    def is_my_pending(self) -> bool:
        return self.mypending
    
    # Returns the connection IPv4 address or None.
    def get_ip_port(self) -> Union[None, str]:
        return self.ip_port
    
    def is_disconnect(self) -> bool:
        return self.disconnect

    