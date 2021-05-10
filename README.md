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

http://{ваш_сайт}/admin/

SWAGGER с полным описанием:

Все endpoint'ы и взаимодействие с ними прописаны там

http://{ваш_сайт}/swagger/

Endpoints кратко:

[http://{ваш_сайт}/getActiveSurveys/](Получение списка активных опросов)

http://{ваш_сайт}/getSurvey/ - Пройти опрос

http://{ваш_сайт}/getUserOrCreate/ - Создание пользователя

http://{ваш_сайт}/getUserAnswers/ - Получение пройденных пользователем опросов с детализацией по ответам

http://{ваш_сайт}/createAnswer/ - Создание/приём ответа

http://{ваш_сайт}/createSurvey/ - Создание опроса

http://{ваш_сайт}/updateSurvey/ - Редактирование опроса

http://{ваш_сайт}/deleteSurvey/ - Удаление опроса

http://{ваш_сайт}/createQuestion/ - Создание вопроса

http://{ваш_сайт}/updateQuestion/ - Редактирование вопроса

http://{ваш_сайт}/deleteQuestion/ - Удаление вопроса
