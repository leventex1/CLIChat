# CLIChat
Command line chat application

## Commands
    !help:                           Prints this help message.
    !exit:                           Exits out of the application.
    !pending:                        Prints the pending connections.
    !mypending:                      Prints my pending connections.
    !connect -param:                 Connects to another client.
                                        -param: IPv4:port address.
    !disconnect:                     Disconnects from the current connection.
    !connection:                     Prints the current connection.

## How to use
Spin up two client with different port numbers

    A terminal >    python3 run.py 5000

and

    B terminal >    python3 run.py 5001

Connect to each other

    A terminal >    !connect 127.0.0.1:5001

    B terminal >    !connect 127.0.0.1:5000

The two client now connected and can send messages to each other.

To disconnect use <code>!disconnect</code> command

## The program

On the main thread the program is parsing the inputed 'messages' from the user and executes the corresponding commands. While on another thread a development WSGI webserver is running and listening on requests and processes them accordingly.
