"""
  A trivial web server in Python.

  Based largely on https://docs.python.org/3.4/howto/sockets.html
  This trivial implementation is not robust:  We have omitted decent
  error handling and many other things to keep the illustration as simple
  as possible.

  FIXME:
  Currently this program always serves an ascii graphic of a cat.
  Change it to serve files if they end with .html or .css, and are
  located in ./pages  (where '.' is the directory from which this
  program is run).
"""

import config    # Configure from .ini files and command line
import logging   # Better than print statements
import os        # to open files
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)
# Logging level may be overridden by configuration 

import socket    # Basic TCP/IP communication on the internet
import _thread   # Response computation runs concurrently with main program


def listen(portnum):
    """
    Create and listen to a server socket.
    Args:
       portnum: Integer in range 1024-65535; temporary use ports
           should be in range 49152-65535.
    Returns:
       A server socket, unless connection fails (e.g., because
       the port is already in use).
    """
    # Internet, streaming socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to port and make accessible from anywhere that has our IP address
    serversocket.bind(('', portnum))
    serversocket.listen(1)    # A real server would have multiple listeners
    return serversocket


def serve(sock, func):
    """
    Respond to connections on sock.
    Args:
       sock:  A server socket, already listening on some port.
       func:  a function that takes a client socket and does something with it
    Returns: nothing
    Effects:
        For each connection, func is called on a client socket connected
        to the connected client, running concurrently in its own thread.
    """
    while True:
        log.info("Attempting to accept a connection on {}".format(sock))
        (clientsocket, address) = sock.accept()
        _thread.start_new_thread(func, (clientsocket,))


##
# Starter version only serves cat pictures. In fact, only a
# particular cat picture.  This one.
##
CAT = """
     ^ ^
   =(   )=
"""

# HTTP response codes, as the strings we will actually send.
# See:  https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
# or    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
##
STATUS_OK = "HTTP/1.0 200 OK\n\n"
STATUS_FORBIDDEN = "HTTP/1.0 403 Forbidden\n\n"
STATUS_NOT_FOUND = "HTTP/1.0 404 Not Found\n\n"
STATUS_NOT_IMPLEMENTED = "HTTP/1.0 401 Not Implemented\n\n"

# takes in the file name and open it
def readFile(f,s):
    # checks if file exists and if it does, opens and transmits
    # if it doesnt exist it sends error 403
    # in ths case it checks 'pages' directory
    if os.path.isfile('pages'+f):
        inFile = open('pages'+f)
        inFile2 = inFile.read()
        transmit(inFile2, s)
    else:
        transmit(STATUS_NOT_FOUND,s)

# checks the ending of the input
def checkEnd(e):
    
    # only checks the ending
    if e.endswith(('.html', '.css')):
        return True

    else:
        return False

def respond(sock):
    """
    This server responds only to GET requests (not PUT, POST, or UPDATE).
    Any valid GET request is answered with an ascii graphic of a cat.
    """
    sent = 0
    request = sock.recv(1024)  # We accept only short requests
    request = str(request, encoding='utf-8', errors='strict')
    log.info("--- Received request ----")
    log.info("Request was {}\n***\n".format(request))

    parts = request.split()
    str1 = parts[1] # this is the input with / at the begining
    endStr = checkEnd(str1) # a boolean to validate the ending
    # added one more condition, if statement will only run with correct ending
    if len(parts) > 1 and parts[0] == "GET" and endStr == True:
        transmit(STATUS_OK, sock)
        #transmit(CAT, sock)
        bool1 = True # i used it for the purpose of the next elif statement
        # checks if there is on of these in the page input
        # it was asked to check the beginning but 1 of the test cases has it in middle
        # thats why now it will check for them anywhere
        #if str1.startswith(('/~', '///', '/..')):
        if '//' in str1 or '..' in str1 or '~' in str1:
            transmit(STATUS_FORBIDDEN, sock)
            bool1 = False
        # if it didnt use the charecters above it will call readFile 
        elif bool1:
            readFile(str1, sock)
        
    else:
        log.info("Unhandled request: {}".format(request))
        transmit(STATUS_NOT_IMPLEMENTED, sock)
        transmit("\nI don't handle this request: {}\n".format(request), sock)

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    return


def transmit(msg, sock):
    """It might take several sends to get the whole message out"""
    sent = 0
    while sent < len(msg):
        buff = bytes(msg[sent:], encoding="utf-8")
        sent += sock.send(buff)

###
#
# Run from command line
#
###


def get_options():
    """
    Options from command line or configuration file.
    Returns namespace object with option value for port
    """
    # Defaults from configuration files;
    #   on conflict, the last value read has precedence
    options = config.configuration()
    # We want: PORT, DOCROOT, possibly LOGGING

    if options.PORT <= 1000:
        log.warning(("Port {} selected. " +
                         " Ports 0..1000 are reserved \n" +
                         "by the operating system").format(options.port))

    return options


def main():
    options = get_options()
    port = options.PORT
    if options.DEBUG:
        log.setLevel(logging.DEBUG)
    sock = listen(port)
    log.info("Listening on port {}".format(port))
    log.info("Socket is {}".format(sock))
    serve(sock, respond)


if __name__ == "__main__":
    main()
