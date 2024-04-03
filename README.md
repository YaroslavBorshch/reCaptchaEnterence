<!-- Запуск -->
## Настройки

клонируем репозиторий и создаем внутри виртуальное окружение
```shell
    python3 -m venv venv
    source venv/bin/activate
```
Устанавливаем необходимые для работы библиотеки
```shell
    python3 -m pip install --upgrade pip 
    python3 -m pip install -r requirements.txt
```
## Далее важный момент насчет webdriver!
В проекте используется chromeDriver 123.0... с прямым указанием пути до вебдрайвера
Соответственно если у вас другая версия браузера, то стоит скачать драйвер под вышу версию:
[chrome driver download](https://chromedriver.chromium.org/downloads)
после чего распоковать полученный архив в папку webdriverLinux:
```shell
   reCaptchaEnterence/enterSite/browserAutomation/webdriverLinux
```
--p.s. нет, докер чот сложно >_<--

- - -

Для удобства стоит создать супер-пользователя, что бы использовать админку
(128:0:0:1:8000/admin)
```shell
    python3 manage.py createsuperuser
```


После этого можно приминить миграции и запускать сервер
```shell
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runserver
```
- - -
link: 127:0:0:1:8000
браузер будет закрывать после 20 секунд после того как закончил работу с логином
#### Автоматически будет создано 3 пользователя:
1. **wrong_pass_user** - пользователь, который есть в БД но его нет на сайте
2. **right_pass_us**   - пользователь, который успешно залогинится       
3. **coolSiteTwice**   - пользователь, который есть на сайте но с неккоректным паролем
соотвественно на них можно и проверить работу формы или создать своих через админку
