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

def test_register(driver):
    try:
        # Navegar a la página de registro
        driver.get(base_url + "/registro.html")

        # Encontrar los campos de entrada y el botón de registro
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        register_button = driver.find_element(By.XPATH, "//button[text()='Registrarse']")

        # Limpiar los campos de entrada y enviar los valores de prueba
        username_field.clear()
        password_field.clear()
        username_field.send_keys("nuevo_usuario")
        password_field.send_keys("nueva_contraseña")

        # Hacer clic en el botón de registro
        register_button.click()

        # Esperar para observar la alerta de registro
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            assert "Usuario registrado correctamente" in alert.text
            alert.accept()
        except TimeoutException:
            pass

        # Verificar si la URL actual es la página de inicio de sesión después de aceptar la alerta
        login_page_url = base_url + "/index.html"
        assert login_page_url == driver.current_url, "Después de aceptar la alerta, debería redirigir a la página de inicio de sesión"
    except Exception as e:
        assert False, f"El registro falló con error: {str(e)}"
