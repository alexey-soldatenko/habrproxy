import socket
from handler_request import HandlerRequest
	
HOST = '127.0.0.1'
PORT = 8232
ADDR = (HOST, PORT)

#socket-сервер
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(ADDR)
sock.listen(10)

while True:
	conn, addr = sock.accept()
	#обрабатываем каждый запрос в потоке
	thr = HandlerRequest(conn)
	
	
	




