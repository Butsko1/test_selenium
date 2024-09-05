import random

from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_store():
    fake = Faker()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome() # Запускаем в headless, чтобы браузер не мешал вводить данные

    # Переходим на страницу авторизации и авторизуемся
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    login_username_field = driver.find_element(By.XPATH, "//input[@id='user-name']")
    login_username_password = driver.find_element(By.XPATH, "//input[@id='password']")
    login_button = driver.find_element(By.XPATH, "//input[@id='login-button']")
    login_username_field.send_keys("standard_user")
    login_username_password.send_keys("secret_sauce")
    login_button.click()

    # Проверяем, что попали на страницу с товарами
    assert driver.current_url == "https://www.saucedemo.com/inventory.html"

    # Находим все товары на странице
    items = driver.find_elements(By.XPATH, "//div[@class='inventory_item_name ']")
    print("Приветствую тебя в нашем интернет - магазине")

    # Выводим список товаров
    print("Выбери один из следующих товаров и укажи его номер:")
    for i in range(1, len(items) + 1):
        item = driver.find_element(By.XPATH,f"(//div[@class='inventory_item_name '])[{i}]")
        print(f"{i} - {item.text}")

    # Получаем пользовательский ввод с проверками на корректность ввода
    product = random.randint(1,5)

    # Выбираем товар и переходим в корзину
    selected_product = driver.find_element(By.XPATH, f"(//div[@class='inventory_item_name '])[{product}]").text
    selected_product_price_on_page = driver.find_element(By.XPATH, f"(//div[@class = "
                                                                   f"'inventory_item_price'])[{product}]").text[1:]
    print(f"Цена товара {selected_product}: {selected_product_price_on_page} долларов")
    add_to_cart_button = driver.find_element(By.XPATH,f"(//div/following-sibling::button)[{product}]")
    add_to_cart_button.click()
    cart_button = driver.find_element(By.XPATH, "//a[@class='shopping_cart_link']")
    cart_button.click()

    # Проверяем, что мы оказались в корзине
    assert driver.current_url == "https://www.saucedemo.com/cart.html"

    # Проверяем, что наименование товара и цена в корзине совпадают с изначальными
    product_in_the_cart = driver.find_element(By.XPATH, "//div[@class = 'inventory_item_name']").text
    assert product_in_the_cart == selected_product
    price_of_the_product_in_the_cart = driver.find_element(By.XPATH, "//div[@class = 'inventory_item_price']").text[1:]
    assert selected_product_price_on_page == price_of_the_product_in_the_cart
    print(f"В корзине лежит {product_in_the_cart} стоимостью {price_of_the_product_in_the_cart} долларов")

    # Переходим к вводу пользовательских данных
    checkout_button = driver.find_element(By.XPATH, "//button[@id = 'checkout']")
    checkout_button.click()

    # Проверяем, что мы оказались на странице ввода пользовательских данных
    assert driver.current_url == "https://www.saucedemo.com/checkout-step-one.html"

    # Заполняем данные и переходим на финальную страницу
    first_name_field = driver.find_element(By.XPATH, "//input[@id = 'first-name']")
    first_name_field.send_keys(fake.first_name())
    last_name_field = driver.find_element(By.XPATH, "//input[@id = 'last-name']")
    last_name_field.send_keys(fake.last_name())
    postal_code_field = driver.find_element(By.XPATH, "//input[@id = 'postal-code']")
    postal_code_field.send_keys(fake.postalcode())
    continue_button = driver.find_element(By.XPATH, "//input[@id = 'continue']")
    continue_button.click()

    # Проверяем, что мы оказались на финальной странице
    assert driver.current_url == "https://www.saucedemo.com/checkout-step-two.html"

    # Проверяем, что финальные наименование и стоимость товара равны изначальным
    final_product_name = driver.find_element(By.XPATH, "//div[@class='inventory_item_name']").text
    assert final_product_name == selected_product
    final_product_price = driver.find_element(By.XPATH, "//div[@class='inventory_item_price']").text[1:]
    assert final_product_price == selected_product_price_on_page

    # Проверяем, что финальная сумма правильно посчитана
    total_price = driver.find_element(By.XPATH, "//div[@class='summary_subtotal_label']").text[13:]
    print(f"Суммарная стоимость товаров в корзине: {total_price} долларов")
    tax = driver.find_element(By.XPATH, "//div[@class='summary_tax_label']").text[6:]
    print(f"Налог: {tax} долларов")
    total = driver.find_element(By.XPATH, "//div[@class='summary_total_label']").text[8:]
    print(f"Итого к оплате: {total} долларов")
    assert float(total) == float(total_price) + float(tax)

