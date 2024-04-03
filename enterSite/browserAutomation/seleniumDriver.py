import os
import time
import json
import random
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha

DRIVER_PATH = str(Path(__file__).resolve().parent.joinpath('webdriverLinux/chromedriver'))
LINK = os.environ['LINK'] or 'https://stripchat.global/'
CAPTCHA_API_KEY = os.environ['CAPTCHA_API_KEY'] or '9fe3a62e9d89f6d358dbaa3facc553c7'


class AutomationEngine:
    """
        основной класс управления браузером
        здесь происходит поиск нужных кнопок и заполнение формы
        вызов метода решения капчи и после чего вход
    """

    def __init__(self,
                 user_data: dict,
                 driver_path: str = DRIVER_PATH,
                 link: str = LINK,
                 captcha_key: str = CAPTCHA_API_KEY, ):
        self.driver_path = driver_path
        self.link = link
        self.captcha_api_key = captcha_key
        self.uset_data = user_data
        options = Options()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/58.0.3029.110 Safari/537.3")
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.actionsWay = ActionChains(self.driver)

    @staticmethod
    def shuffle_cursor(button_to_move) -> dict:
        """
        сдвигаем курсор что бы не тыкать каждый раз ровно в центр
        :param button_to_move: элемент к которому хотим переместиться
        :return: dict: возвращаем словарь с координатами х и у на который сдвинуть курсор от цента
        """
        # делим на 3, что бы исключить всякие маргины и погрешности
        half_of_width = button_to_move.size['width'] // 3
        half_of_height = button_to_move.size['height'] // 3
        return {'x': random.randint(-half_of_width, half_of_width),
                'y': random.randint(-half_of_height, half_of_height)}

    def enter_process(self):
        """
        основная логика логина на сайт
        :return: возвращает JSON с кодом ответа и кратким результатом, для отображения на странице
        """
        returned_result = {
            'code': 500,
            'message': '-'
        }
        self.driver.get(self.link)
        # дожидаемся прогрузки стр
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        # проверяем просят ли нас подтвердить свой возрат или пускают уже просто так
        try:
            checkAgeQuestionButton = self.driver.find_element(By.CLASS_NAME, "btn-visitors-agreement-accept")
            cords = self.shuffle_cursor(checkAgeQuestionButton)
            self.actionsWay.move_to_element_with_offset(checkAgeQuestionButton, cords['x'],
                                                        cords['y']).click().perform()
        except Exception as e:
            returned_result['message'] = e
            return returned_result
        # на тот случай, если это была стр подтверждения возраста подождем прогрузки кнопки логина
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//a[@href='/login']"))
            )
        except Exception as e:
            returned_result['message'] = e
            return returned_result
        time.sleep(2)

        loginButton = self.driver.find_element(By.XPATH, "//a[@href='/login']")
        cords = self.shuffle_cursor(loginButton)
        self.actionsWay.move_to_element_with_offset(loginButton, cords['x'], cords['y']).click().perform()
        # выжидаем появления модалки с вводом
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "login_login_or_email"))
        )
        time.sleep(2)
        # двигаемся к вводу логина
        loginInput = self.driver.find_element(By.ID, "login_login_or_email")
        cords = self.shuffle_cursor(loginInput)
        self.actionsWay.move_to_element_with_offset(loginInput, cords['x'], cords['y']).click().perform()
        # вводим логин
        for letter in self.uset_data['username']:
            loginInput.send_keys(letter)
            time.sleep(random.uniform(0.2, 0.4))
        # двигаемся к вводу пароля
        passwordInput = self.driver.find_element(By.ID, "login_password")
        cords = self.shuffle_cursor(passwordInput)
        self.actionsWay.move_to_element_with_offset(passwordInput, cords['x'], cords['y']).click().perform()
        # воодим пароль)
        for letter in self.uset_data['password']:
            passwordInput.send_keys(letter)
            time.sleep(random.uniform(0.2, 0.4))

        # вызываем метод решения капчи
        try:
            self.solving_captcha_process()
        except Exception as e:
            returned_result['message'] = 'error during solve captcha: ' + str(e)
            return returned_result
        login_form_submit = self.driver.find_element(By.CLASS_NAME, "login-form__submit")
        cords = self.shuffle_cursor(login_form_submit)
        self.actionsWay.move_to_element_with_offset(login_form_submit, cords['x'], cords['y']).click().perform()

        # Если дошли до сюда, значит авторизация прошла успешно:
        returned_result = {
            'code': 200,
            'message': 'authorization was completed successfully'
        }
        time.sleep(25)
        return returned_result

    def solving_captcha_process(self):
        """
        метод, которым будет обходится капча. Пустой в базовом классе
        тк будет переопределяться в дальнейшем в зависимости от выбранного метода
        :return:
        """
        pass


# TODO:: еще можно наследуемые классы по разным файликам кинуть для красоты
class TwoCaptchaSolve(AutomationEngine):
    """
    наследуется от основного метода логина на сайт, тк логика работы с сайтом одинаковая
    обход капчи через пакет 2captcha. Который использует по сути является оберткой над 2captcha-API
    """

    def solving_captcha_process(self):
        """
        перегружаем метод определения капчи
        :return:
        """
        # по тайтлу находим нашу капчу и получаем из src ключ данной капчи
        captcha_element = self.driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")
        captcha_key = captcha_element.get_attribute('src').split('&')
        # находим ГЕТ_аргумент, начинающийся с k= (вдруг он не всегда будет вторым)
        captcha_key = next((get_arg for get_arg in captcha_key if get_arg.startswith('k=')), None)
        # убираем начало строки что бы остался только сам ключ
        captcha_key = captcha_key[2:]
        # # спрятанное поле для ответа на капчу upd: не понадобилось
        # hidden_answer = self.driver.find_element(By.CSS_SELECTOR, "#g-recaptcha-response")
        solver = TwoCaptcha(self.captcha_api_key)
        # отправляем запрос, можно особо не заморачиваться с аргументами
        solvers_answer = solver.recaptcha(sitekey=captcha_key, url=LINK)
        # hidden_answer.send_keys(solvers_answer['code'])
        self.driver.execute_script(
            f"___grecaptcha_cfg.clients['0']['X']['X']['callback']('{solvers_answer['code']}')")

        # TODO:: конкретно тут капча с колбеком, в теории могла бы быть с хиден_сабмитом или менять свое расположение
        #  относительно позиции Х Х, но что-то и так уже затянул


class resolveCaptchaBySoundAI(AutomationEngine):
    """
    наследуется от основного метода логина на сайт, тк логика работы с сайтом одинаковая
    обход капчи через аудиоформат whisperOpenAi
    """

    def solving_captcha_process(self):
        pass
