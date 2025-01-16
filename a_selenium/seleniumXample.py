import time
from a_selenium.seleniumUtil import share_browser

from selenium import webdriver
from selenium.webdriver.common.by import By

#chromedriver 下载地址 https://chromedriver.storage.googleapis.com/index.html

# 浏览器驱动路径
# path = 'chromedriver.exe'


# 使用无介面浏览器
# browser = share_browser()

# 使用预设Chrome浏览器
browser = webdriver.Chrome()


url = 'https://www.baidu.com/'

browser.get(url)

# 获取当前页数据
content = browser.page_source
# print(content)

# ------------- 元素定位 ------------

# (常用) 根据ID取得 input
input = browser.find_element(By.ID,value='kw')
input.send_keys('关')

browser.save_screenshot('my_screenshot.png')

# (常用) 根据id找到"百度一下"
button = browser.find_element(By.ID,value='su')
button.click()

# 根据name找到搜索框
button = browser.find_element(by='name', value='wd')
print(button)

# (常用) 根据xpath路径寻找“百度一下”
button = browser.find_element(By.XPATH, value='/html/body/div[1]/div[1]/div[5]/div/div/form/span[2]/input')
print(button)

# 根据标签名字获取对象
button = browser.find_elements(by='tag name', value='input')
print(button)

# (常用) 使用bs4的语法来获取对象
button = browser.find_elements(by="css selector", value='#su')
print(button)

# 寻找链接文本（对应html的a标签）
button = browser.find_element(by='link text', value='地图')
print(button)



# ----------------- selenium的元素信息 ----------


# # 根据id找到“百度一下”
# input = browser.find_element(by='id', value='su')
#
# # 获取标签的属性
# result = input.get_attribute('class')
# print(result)
# # 获取标签的名字
# result = input.tag_name
# print(result)
#
# # 根据元素文本获取相应的链接
# input = browser.find_element(by='link text', value='新闻')
# # 获取元素文本
# result = input.text
# print(result)


time.sleep(30)
