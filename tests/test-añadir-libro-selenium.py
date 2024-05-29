import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configuración del WebDriver para usar Selenium Grid
grid_url = "http://192.168.56.10:31351/wd/hub"

# Configuración de opciones para Chrome
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-insecure-localhost')
chrome_options.add_argument('--headless')  # Opcional, si deseas ejecutar en modo headless
chrome_options.add_argument('--disable-gpu')

# URL de la página web
base_url = "https://192.168.56.10:30443"

@pytest.fixture(scope="module")
def driver():
    # Crear una instancia del WebDriver
    driver = webdriver.Remote(command_executor=grid_url, options=chrome_options)
    yield driver
    # Cerrar el navegador
    driver.quit()

def login(driver, username, password):
    # Navegar a la página de inicio de sesión
    driver.get(base_url + "/index.html")

    # Encontrar los campos de entrada y el botón de inicio de sesión
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.XPATH, "//button[text()='Enviar']")

    # Limpiar los campos de entrada y enviar los datos de inicio de sesión
    username_field.clear()
    password_field.clear()
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Hacer clic en el botón de inicio de sesión
    login_button.click()

    # Esperar hasta que se cargue la página de inicio de sesión
    WebDriverWait(driver, 5).until(EC.url_to_be(base_url + "/libros.html"))

def test_add_book(driver):
    try:
        # Realizar inicio de sesión
        login(driver, "root", "1234")

        # Navegar a la página de agregar libro
        driver.get(base_url + "/agregar_libro.html")

        # Encontrar los campos de entrada y el botón de guardar
        titulo_field = driver.find_element(By.ID, "titulo")
        descripcion_field = driver.find_element(By.ID, "descripcion")
        precio_field = driver.find_element(By.ID, "precio")
        imagen_field = driver.find_element(By.ID, "imagen")
        guardar_button = driver.find_element(By.XPATH, "//button[text()='Guardar']")

        # Limpiar los campos de entrada y enviar los valores de prueba
        titulo_field.clear()
        descripcion_field.clear()
        precio_field.clear()
        imagen_field.clear()
        titulo_field.send_keys("Nuevo Libro")
        descripcion_field.send_keys("Descripción del nuevo libro")
        precio_field.send_keys("20.00")
        imagen_field.send_keys("url_de_la_imagen_del_libro")

        # Hacer clic en el botón de guardar
        guardar_button.click()

        # Esperar para observar la alerta de "Libro guardado"
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            assert "Libro guardado" in alert.text
            alert.accept()
        except TimeoutException:
            pytest.fail("La alerta de 'Libro guardado' no apareció")

        # Verificar si se redirige a la página de libros después de aceptar la alerta
        assert base_url + "/libros.html" == driver.current_url, "Después de aceptar la alerta, debería redirigir a la página de libros"
    except Exception as e:
        pytest.fail(f"La prueba falló con el siguiente error: {str(e)}")
