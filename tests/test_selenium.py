import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException

def test_selenium_docker_compose(url, username, password):
    try:
        # Configuración del navegador
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')  # Ignorar errores de certificado SSL
        
        # Inicializar el navegador apuntando al servicio de Selenium Hub en el Docker Compose
        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=options
        )
        
        # Acceder a la URL proporcionada
        driver.get(url)
        
        # Intentar iniciar sesión
        try:
            # Encontrar el campo de usuario e ingresar el nombre de usuario
            username_field = driver.find_element("id", "username")
            username_field.send_keys(username)
            
            # Encontrar el campo de contraseña e ingresar la contraseña
            password_field = driver.find_element("id", "password")
            password_field.send_keys(password)
            
            # Encontrar el botón de inicio de sesión y hacer clic en él
            login_button = driver.find_element("id", "login_button")
            login_button.click()
            
            # Esperar unos segundos para que se procese el inicio de sesión
            time.sleep(5)
            
            # Verificar si se ha iniciado sesión correctamente
            welcome_message = driver.find_element("id", "welcome_message")
            if welcome_message.text == "¡Bienvenido, usuario!":
                print("Inicio de sesión exitoso.")
            else:
                print("Fallo en el inicio de sesión.")
        except NoSuchElementException:
            print("No se encontraron elementos para iniciar sesión.")
        
        # Realizar alguna acción en la página después del inicio de sesión (por ejemplo, acceder a una sección específica)
        # Por ejemplo, esperar unos segundos para que la página cargue completamente
        time.sleep(5)
        
        # Imprimir el título de la página
        print("Título de la página:", driver.title)
        
        # Imprimir la URL actual
        print("URL actual:", driver.current_url)
        
        # Imprimir el contenido de la página
        print("Contenido de la página:", driver.page_source)
        
        # Cerrar el navegador al finalizar las pruebas
        driver.quit()
        
    except WebDriverException as e:
        print(f"Error al iniciar el navegador: {e}")

# URL a probar
url = "https://192.168.56.10:30443/"

# Credenciales de inicio de sesión
username = "root"
password = "1234"

# Ejecutar la prueba
test_selenium_docker_compose(url, username, password)
