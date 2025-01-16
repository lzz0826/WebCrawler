from selenium import webdriver

from web.config.yaml_config import Global


def call_remote_webdriver(url, chrome_options=None):
    if chrome_options is None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")

    executor_url = Global.yml_data['webdriver']['url'] + ":" + str(Global.yml_data['webdriver']['port']) + '/wd/hub'

    driver = webdriver.Remote(
        command_executor=executor_url,
        options=chrome_options
    )

    try:
        driver.get(url)
        page_source = driver.page_source
    except Exception as e:
        print("發生錯誤: ", e)
        raise e
    finally:
        driver.quit()

    return page_source


def call_webdriver(url):
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        page_source = driver.page_source
    except Exception as e:
        print("發生錯誤: ", e)
        raise e
    finally:
        driver.quit()

    return page_source
