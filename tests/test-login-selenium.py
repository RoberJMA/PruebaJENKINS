import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Configuración del WebDriver para usar Selenium Grid
grid_url = "http://192.168.56.10:31351/wd/hub"

# Configuración de opciones para Chrome
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-insecure-localhost')
chrome_options.add_argument('--headless')  # Opcional, si deseas ejecutar en modo headless
chrome_options.add_argument('--disable-gpu')

@pytest.mark.parametrize("username, password", [("root", "1234")])
def test_login(username, password):
    try:
        # Crear una instancia del WebDriver
        driver = webdriver.Remote(command_executor=grid_url, options=chrome_options)
        
        # URL de la página web
        base_url = "https://192.168.56.10:30443"
    
        # Navegar a la página de inicio de sesión
        driver.get(base_url)
    
        # Encontrar los campos de entrada y el botón de enviar
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.XPATH, "//button[text()='Enviar']")
    
        # Limpiar los campos de entrada y enviar los valores de prueba
        username_field.clear()
        password_field.clear()
        username_field.send_keys(username)
        password_field.send_keys(password)
    
        # Hacer clic en el botón de enviar
        login_button.click()
    
        # Esperar para observar el resultado (se puede ajustar el tiempo de espera según sea necesario)
        time.sleep(2)
    
        # Verificar si se muestra el mensaje de error o si se redirige a la página de libros
        assert "/libros.html" in driver.current_url, f"Test con usuario '{username}' y contraseña '{password}': Fallido (Inicio de sesión incorrecto)"
    
    except Exception as e:
        assert False, f"Test con usuario '{username}' y contraseña '{password}': Fallido (Error: {str(e)})"

    finally:
        # Cerrar el navegador
        driver.quit()
