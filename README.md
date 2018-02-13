# habrproxy
Приложение выполнено на python3 с использованием стандартных библиотек. И реализует поставленную задачу:

"""
Реализовать простой http-прокси-сервер, запускаемый локально (порт на ваше усмотрение), который показывает содержимое страниц Хабра. 
Прокси должен модицифировать текст на страницах следующим образом: после каждого слова из шести букв должен стоять значок «™». 

При этом:
    
    - страницы должны™ отображаться и работать полностью корректно, в точности так, как и оригинальные (за исключением модифицированного текста™);
    
    - при навигации по ссылкам, которые ведут на другие™ страницы хабра, браузер должен™ оставаться на адресе™ вашего™ прокси™;

"""

Запуск осуществляется командой python3 proxy_server.py (из директории проекта).

Работу приложения можно просмотреть по адресу 127.0.0.1:8232