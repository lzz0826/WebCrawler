"""
selenium的交互
"""
import time

from selenium import webdriver

# 创建浏览器对象
# path = 'msedgedriver.exe'
browser = webdriver.Chrome()

# 访问地址
url = 'https://www.baidu.com/'
# 打开地址
browser.get(url)
# 睡眠2s
time.sleep(2)

# 获取文本框对象
input = browser.find_element(by='id', value='kw')
# 在文本框中输入“周杰伦”
input.send_keys('周杰伦')
# 睡眠2s
time.sleep(2)

# 获取“百度一下”的按钮
button = browser.find_element(by='id', value='su')
# 点击“百度一下”的按钮
button.click()
# 睡眠2s
time.sleep(2)

# 滑倒底部
js_bottom = 'document.documentElement.scrollTop=100000'  # 距离顶部的距离为100，000
browser.execute_script(js_bottom)  # 执行操作
# 睡眠2s
time.sleep(2)

# 获取下一页的按钮
next = browser.find_element(by='a_xpath', value='//a[@class="n"]')
# 点击下一页
next.click()
# 睡眠2s
time.sleep(2)

# 回退到上一页
browser.back()
# 睡眠2s
time.sleep(2)

# 前进
browser.forward()
# 睡眠2s
time.sleep(2)

# 退出浏览器
browser.quit()

