#main program and imports for standalone purpose	   
import sys
import threading
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import ssl
from base64 import b64encode
import simplejson as json

# I don't want a .pyc file there.
sys.dont_write_bytecode = True
from HTTPWebSocketsHandler import HTTPWebSocketsHandler

port = 31313
credentials = ""

# what to do on websocket events

class ConnectHandler(HTTPWebSocketsHandler):
	def on_ws_message(self, message):
		if message is None:
			message = ''
		try:
			json_object = json.loads(message)
			print "JSON object received:", json_object
			print "action:", json_object["action"]
			print "name:", json_object["name"]
		except ValueError:
			print "Data is not JSON. Rejecting it."

		else:
			print "Unknown data incoming:\n", message

	def on_ws_connected(self):
		self.log_message('%s','websocket connected')

	def on_ws_closed(self):
		self.log_message('%s','websocket closed')

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""
   
def _ws_main():
	try:
		server = ThreadedHTTPServer(('', port), ConnectHandler)
		server.daemon_threads = True
		server.auth = b64encode(credentials)
		print('started http server at port %d' % (port,))
		server.serve_forever()
	except KeyboardInterrupt:
		print('^C received, shutting down server')
		server.socket.close()

if __name__ == '__main__':
	_ws_main()
