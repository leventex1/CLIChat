import sys

"""
    Cli chat application.

    Clients can connect to each other and send messages.
    A local webserver is listening for incoming messages.
"""

from application import main

if __name__ == '__main__':

    port = 5000
    if len(sys.argv) > 1:
        port = sys.argv[1]

    main(webserver_port=port)