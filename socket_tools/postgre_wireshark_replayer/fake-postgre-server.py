import SocketServer
import struct
from tcp_responses import *

def char_to_hex(char):
    retval = hex(ord(char))
    if len(retval) == 4:
        return retval[-2:]
    else:
        assert len(retval) == 3
        return "0" + retval[-1]

def str_to_hex(inputstr):
    return " ".join(char_to_hex(char) for char in inputstr)

class Player(SocketServer.BaseRequestHandler):
    def handle(self):
        print "handlint request..."
	self.authenticate()

        in_message=self.read_Socket()
	print "in_message = %s" %in_message
	response_type = raw_input("Enter response type: ")
	#response_type = response_type.strip()
	while (not response_type in tcp_responses):
		print "option doesn't exist"
		response_type = raw_input("Enter response type: ")
	print "out_message = %s" %tcp_responses[response_type]
        self.write_Socket(tcp_responses[response_type])

    def authenticate(self):
	authentication_steps=["R_password_request","R_response1","Q_response1"]
	for s in authentication_steps:
        	in_message=self.read_Socket()
		print "in_message = %s" %in_message
		print "out_message = %s" %tcp_responses[s]
        	self.write_Socket(tcp_responses[s])
	print "authenticated"
	
    def read_Socket(self):
        data = self.request.recv(2048)
        return data

    def write_Socket(self, data):
	#return "hola"
        print "Sending {} bytes: {}".format(len(data), repr(data))
        print "Hex: {}".format(str_to_hex(data))
        self.request.sendall(data)


if __name__ == "__main__":
    port=5432
    if(len(sys.argv)>1):port=sys.argv[1] 
    #server = SocketServer.TCPServer(("localhost", port), Player)
    server = SocketServer.TCPServer(("", port), Player)
    print "listening on %d" %port
    try:
        server.serve_forever()
    except:
        server.shutdown()
