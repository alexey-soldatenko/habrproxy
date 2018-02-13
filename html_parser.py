from lxml import html
from lxml import etree
import re

class ParserHTML:
	def __init__(self, parse_file):
		self.parse_file = parse_file
		self.document = None
		self.html_to_tree()
		self.change_article_text()
		
	def html_to_tree(self):
		''' функция для создания dom-дерева'''
		self.document = html.parse(self.parse_file)
		return self.document
		
	def change_tag_text(self, text):
		''' функция для редактирования текста dom-элемента'''
		text_list = text.split(' ')
		for i in range(len(text_list)):
		#если элемент строки состоит из 6 алфавитных симоволов
			if '&plus;' in text_list[i]:
				text_list[i] = text_list[i].replace('&plus;', '+')
			if len(text_list[i])== 6 and re.match(r'[^\W\d]{6}', text_list[i]):
				text_list[i] = text_list[i] + '\u2122'
		
			#если количество символов более 6, проверяем 
			#содержит ли в себе элемент подстроку из 6 
			#алфавитных символов
			elif len(text_list[i]) > 6:
				long_word_list = re.split(r'([\W\d]+)', text_list[i])
				for item in range(len(long_word_list)):
					if len(long_word_list[item]) == 6:
						match_str = re.match(r'(\w{6})', long_word_list[item])
						if match_str and match_str.group(0):
							long_word_list[item] = match_str.group(0) + '\u2122'
				text_list[i] = ''.join(long_word_list)
						
		#окончательный исправленный вариант текста 
		return ' '.join(text_list)
		
	def change_article_text(self):
		''' функция для изменения содержимого dom-дерева'''
		#обрабатываем все элементы дерева
		for child in self.document.getiterator():
			#изменяем элементы, содержащие текст, но не скрипт
			if child.text and (child.tag != 'script'): 
				child.text = self.change_tag_text(child.text)
				
			if child.tail and (child.tag != 'script'):
				child.tail = self.change_tag_text(child.tail)
			#заменяем ссылки ведущие на сайт-оригинал	
			if child.tag == 'a' and child.get('href'):
				link = child.get('href')
				new_link = link.replace('https://habrahabr.ru', 'http://127.0.0.1:8232')
				child.set('href', new_link)
				
		#записываем содержимое дерева в файл	
		self.document.write(self.parse_file, encoding = 'utf-8', method="html")
