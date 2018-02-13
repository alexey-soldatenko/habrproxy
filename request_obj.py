import re

class RequestObj:
	def __init__(self, person_request):
		self.person_request = person_request
		self.method = ''
		self.path = ''
		self.protocol_version = ''
		self.headers = dict()
		self.message = None
		self.parse_request()
		
		
	def parse_request(self):
		''' функция для парсинга заголовка и получения запрашиваемого пути'''
		if self.person_request:
			request_ls = self.person_request.split('\n')
			#парсим стартовую линию
			request_start_line = request_ls[0]
			self.method, self.path, self.protocol_version = request_start_line.split(' ')
			#определяем заголовки	
			for i in range(len(request_ls[1:])):
				if i != '':
					l = re.split(r':', request_ls[i].strip(), 1)
					if len(l) == 2:
						self.headers[l[0].strip()] = l[1].strip()
				else:
					break
			#если в сообщении передаются данные
			message = ''.join(request_ls[i:]).strip()
			if message:
				message = message.split('&')
				self.message = dict(map(lambda ls: ls.split('='), message))
			else:
				self.message = dict()
			
		else:
			raise ValueError("Неверный запрос")
