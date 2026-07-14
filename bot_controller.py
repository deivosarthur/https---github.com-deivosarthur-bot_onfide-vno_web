_DRIVER = None


def set_driver(driver):

    global _DRIVER

    _DRIVER = driver


def get_driver():

    return _DRIVER


def cerrar_driver(driver):

    try:

        driver.quit()

    except:

        pass