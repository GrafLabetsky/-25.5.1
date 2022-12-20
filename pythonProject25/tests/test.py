import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:/Users/grafg/Desktop/Python/chromedriver_win32/chromedriver.exe')

    # Устанавливаем разрешение окна браузера
    pytest.driver.set_window_size(1920, 1080)
    pytest.driver.maximize_window()
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('graflabetsky@gmail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('ne[ksqvbh')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Переходи на страницу Мои питомцы
    pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
    # Записываем в переменную количество питомцев
    pets = int(pytest.driver.find_element(By.XPATH, '//div[1]/div/div[1]').text.split("\n")[1].split(": ")[1])
    # Добавляем неявные ожидание элемента фото
    pytest.driver.implicitly_wait(20)
    pytest.driver.find_element(By.XPATH, '//tbody//th/img')
    # Записываем в переменную фотографии питомцев
    images = pytest.driver.find_elements(By.XPATH, '//tbody//th/img')
    # Добавляем неявные ожидание элемента имя
    pytest.driver.implicitly_wait(20)
    pytest.driver.find_element(By.XPATH, '//tbody//td[1]')
    # Записываем в переменную имена питомцев
    names = pytest.driver.find_elements(By.XPATH, '//tbody//td[1]')
    # Добавляем неявные ожидание элемента порода
    pytest.driver.implicitly_wait(20)
    pytest.driver.find_element(By.XPATH, '//tbody//td[2]')
    # Записываем в переменную породы питомцев
    breed = pytest.driver.find_elements(By.XPATH, '//tbody//td[2]')
    # Добавляем неявные ожидание элемента возраст
    pytest.driver.implicitly_wait(20)
    pytest.driver.find_element(By.XPATH, '//tbody//td[3]')
    # Записываем в переменную возраст питомцев
    age = pytest.driver.find_elements(By.XPATH, '//tbody//td[3]')

    a = []
    imgnone = 0

    for i in range(len(names)):
        namepet = names[i].text
        # Создаем список имен питомцев
        a.append(namepet)
        # Считаем количество питомцев без фото
        if images[i].get_attribute('src') == '': imgnone += 1
        # Проверяем что, у питомца есть имя
        assert names[i].text != ''
        # Проверяем что, у питомца есть порода
        assert breed[i].text != ''
        # Проверяем что, у питомца есть возраст
        assert age[i].text != ''
    # Количество питомцев совпадает с фактическим.
    assert pets == (len(names))
    # Количество питомцев без фото не больше половины (Присутствуют все питомцы)
    assert imgnone <= (i + 1) // 2
    # Проверяем что у всех питомцев разные имена
    setarr = set(a)
    assert len(a) == len(setarr)

def test_show_all_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('graflabetsky@gmail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('ne[ksqvbh')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Записываем в переменную фотографии питомцев
    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .text-center align-self-center align-middle')
    # Записываем в переменную имена питомцев
    names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    # Записываем в переменную имена питомцев
    descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')
    # Записываем в переменную порода / возраст
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Добавляем неявные ожидание
    WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, "navbarNav")))


    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ", " in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0
