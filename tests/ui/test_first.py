import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome()
driver.get("https://www.saucedemo.com/")
driver.maximize_window()

# Задаем список доступных юзеров и пароль
list_of_users = ['standard_user', 'locked_out_user', 'problem_user', 'performance_glitch_user', 'error_user', 'visual_user']
password = 'secret_sauce'
def test_auth():

    # Прогоняем через цикл
    for i in list_of_users:
        print(f"Авторизация под пользователем {i}")
        username_field = WebDriverWait(driver, 10).until(expected_conditions.
                                                         element_to_be_clickable((By.XPATH, "//input[@id='user-name']")))
        password_field = WebDriverWait(driver, 10).until(expected_conditions.
                                                         element_to_be_clickable((By.XPATH, "//input[@id='password']")))
        login_button = WebDriverWait(driver, 10).until(expected_conditions.
                                                       element_to_be_clickable((By.XPATH, "//input[@id='login-button']")))
        username_field.send_keys(i)
        password_field.send_keys(password)
        login_button.click()
        if driver.current_url == 'https://www.saucedemo.com/inventory.html':
            print(f"Авторизация под пользователем {i} успешна \nВозвращаюсь на предыдущую страницу")
            driver.back()
        else:
            print(f"Авторизация под пользователем {i} неуспешна \nЗакрываю окно с ошибкой и очищаю поля ввода")
            error_button = driver.find_element(By.XPATH, "//button[@class = 'error-button']")
            error_button.click()
            # clear() не работает как должен - пришлось так очищать
            username_field.send_keys(Keys.CONTROL, "a")
            username_field.send_keys(Keys.BACKSPACE)
            password_field.send_keys(Keys.CONTROL, "a")
            password_field.send_keys(Keys.BACKSPACE)
