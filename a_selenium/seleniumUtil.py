
from selenium import webdriver  # 导入selenium库
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# 封装的headless
def share_browser():
    # 无可视化界面设置
    chrome_options = Options()
    # 使用无头模式
    chrome_options.add_argument('--headless')
    # 禁用 GPU，防止无头模式出现问题from selenium.webdriver.chrome.options import Options
    chrome_options.add_argument('--disable-gpu')

    # 创建 Service 对象来指定 chromedriver 路径
    # service = Service('./chromedriver')  # 替换为实际 chromedriver 路径
    # 将参数传给浏览器
    browser = webdriver.Chrome(options=chrome_options)
    return browser

# 使用DriverManagerInstall 安装 Chrome Driver
def chromeDriverManagerInstall():
    driver_path = ChromeDriverManager().install()
    return driver_path


path = chromeDriverManagerInstall()
print(path)

browser = share_browser()
# 启动浏览器
url = "https://baidu.com"
browser.get(url)
browser.save_screenshot('baidu.png')

# 关闭浏览器
browser.quit()

