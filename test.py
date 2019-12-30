from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True

# you can use driver = webdriver.PhantomJS() 
# if you want a headless browser. 
# You need to have PhantomJS installed in path
print("a")
driver = webdriver.Firefox(options=options)
print("b")
driver.get("http://www.tarlabs.com")
print("c")
# will print the page source
print (driver.page_source)