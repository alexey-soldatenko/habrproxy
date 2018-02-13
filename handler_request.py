import requests
from threading import Thread
import traceback
import os
from request_obj import RequestObj
from html_parser import ParserHTML
	
class HandlerRequest:
	def __init__(self, connection):
		self.conn = connection
		#обрабатываем каждый запрос в потоке
		self.thr = Thread(target = self.handle_request)
		self.thr.start()
		self.thr.join()
		
	def handle_request(self):
		''' функция для обработки входящего запроса'''
		request = self.conn.recv(1024)
		try:
			#парсим запрос
			current_request = RequestObj(request.decode('utf-8'))
			#перенаправляем запрос на сервер-оригинал 
			#и составляем ответ для пользователя
			response = self.send_request_to_origin_server(current_request)
		except Exception as err:
			#print(traceback.format_exc())
			if err == ValueError:
				message = "<html><body>Not Found</body></html>"
				headers = "Content-Type: text/html; charset=UTF-8\n\
							Content-Length: {}\n\n".format(len(message))
				status = "HTTP/1.1 404 Not Found\n"
			else:
				message = "<html><body>Internal server error</body></html>"
				headers = "Content-Type: text/html; charset=UTF-8\n\
							Content-Length: {}\n\n".format(len(message))
				status = "HTTP/1.1 500 Internal Server Error\n"
			response = status + headers + message
		else:
			print('Ok')
		self.conn.sendall(response.encode('utf-8'))	
		self.conn.close()			

	def send_request_to_origin_server(self, current_request):
		NOT_NEEDED_HEADERS = [
							'Content-Length', 'Public-Key-Pins', 
							'P3P',  'X-Frame-Options', 
							'Strict-Transport-Security',
							 'Transfer-Encoding', 'Vary', 'Content-Encoding', 
							 'X-Engine', 
							 ]
		
		#отправляем запрос на сайт-оригинал
		origin_request = 'https://habrahabr.ru{0}'.format(current_request.path)
		if current_request.method == 'GET':
			response = requests.get(origin_request, 
									allow_redirects=False)
		elif current_request.method == 'POST':
			response = requests.post(origin_request, 
									headers = current_request.headers, 
									data = current_request.message)
		headers = ''
		for k, v in response.headers.items():
			#убираем ненужные заголовки
			if k not in NOT_NEEDED_HEADERS:
				headers += k + ': ' + response.headers[k] + '\n'		
		status = 'HTTP/1.1 ' + str(response.status_code) + ' \n'
			
		message = response.text
		
		#для текущего запроса создаём файл, в котором будем хранить
		#и редактировать ответ для пользователя 
		file_current_request = origin_request.replace('/', '_')
		with open(file_current_request, 'w') as f:
			f.write(message)
				
		#обрабатываем html-файл
		if response.headers['Content-Type'] == 'text/html; charset=UTF-8':
			self.parse_obj = ParserHTML(file_current_request)
		
			with open(file_current_request, 'r') as f:
				message = f.read()
			
		headers += 'Content-Length: {}\n\n'.format(len(message.encode('utf-8')))
		answer = status + headers + message
		
		#удаляем текущий файл
		os.remove(file_current_request)
		return answer
