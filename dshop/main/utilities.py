from datetime import datetime
from os.path import splitext

def get_timestamp_path(instance, filename): # Тк эта функция не относится не к редакторам не к контроллерами не к моделям ,мы просто запишем её сюда
	return f'{datetime.now().timestamp()}{splitext(filename)[1]}'