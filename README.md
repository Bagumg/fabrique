# fabrique
Тестовое задание от Фабрики Решений


Комманды для запуска:
```
sudo apt install git pipenv
```

Создайте папку для проекта в папке и запустите терминал и введите комманду
```
git clone https://github.com/Bagumg/fabrique.git
```
После того как скопируется проект запустите виртуальную среду командой 
```
pipenv shell
```
Произойдёт запуск оболочки и установка необходимых пакетов.
После этого по-очереди введите комманды
```python
python manage.py makemigrations
python manage.py migrate
```
Создайте администратора системы коммандой и следуйте подсказкам.
```python
python manage.py createsuperuser
```
Запустите сервер командой
```python
python manage.py runserver
```
Перейдите по адресу и войдите в систему с логином и паролем, который вы создали ранее

http://127.0.0.1:8000/admin/
