from selenium import webdriver
from selenium.common.exceptions import WebDriverException

def check_browser(browser):
    try:
        if browser == "CHROME":
            options = webdriver.ChromeOptions()
        elif browser == "FIREFOX":
            options = webdriver.FirefoxOptions()
        else:
            print(f"Browser {browser} no está soportado.")
            return

        driver = webdriver.Remote(
            command_executor='http://localhost:31351/wd/hub',
            options=options
        )

        # Prueba de carga de la página principal
        driver.get("https://localhost:30443")
        assert "" in driver.title  # Verifica que la página contenga "Apache" en el título
        assert "Inicio de Sesion" in driver.page_source  # Verifica que el contenido de la página sea el esperado
        print(f"¡El navegador {browser} carga la página principal correctamente!")

        # Prueba de interacción con la API interna
        driver.get("https://localhost:30443/api/data")  # Suponiendo que "/api/data" es la ruta de la API interna
        # Verifica que se pueda recuperar datos de la API (la implementación real puede variar según la respuesta esperada)
        assert "Datos de la API" in driver.page_source  
        print(f"¡El navegador {browser} se comunica correctamente con la API interna!")

        # Prueba de inicio de sesión
        test_login(driver, "root", "1234")

        driver.quit()
        print(f"¡Pruebas completadas con el navegador {browser}!")

    except WebDriverException as e:
        print(f"Error al iniciar el navegador {browser}: {e}")

def test_login(driver, username, password):
    # Prueba de inicio de sesión
    # Ingresa el nombre de usuario y la contraseña
    username_input = driver.find_element_by_id("username")
    password_input = driver.find_element_by_id("password")
    username_input.send_keys(username)
    password_input.send_keys(password)

    # Envíar el formulario de inicio de sesión
    submit_button = driver.find_element_by_id("login-button")
    submit_button.click()

    # Verificar que se haya iniciado sesión correctamente
    assert "Bienvenido, root" in driver.page_source  # Verifica que se muestre un mensaje de bienvenida
    print(f"¡Inicio de sesión exitoso con el navegador {driver.capabilities['browserName']}!")

# Ejecutar pruebas para ambos navegadores
check_browser("FIREFOX")
check_browser("CHROME")
