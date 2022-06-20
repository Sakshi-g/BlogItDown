import requests
import random
import time
import ssl
import certifi
from PIL import ImageFile
from bs4 import BeautifulSoup
import urllib.request as urlrq
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path= r'C:\SeleniumDrivers\chromedriver.exe')

def testing_links(driver):

    driver.get('http://localhost:8000/')
    links = driver.find_elements_by_css_selector("a")
    print("Testing links...")
    start = time.time()
    working_links = 0
    bad_links = 0
    bad_links_list = []
    for link in links:
        r = requests.head(link.get_attribute('href'))
        if r.status_code != 400:
            working_links += 1
        else:
            bad_links += 1
            bad_links_list.append((link.get_attribute('href'),r.status_code))
    #context = { "working_links":working_links,"bad_links_list":bad_links_list , "bad_links":bad_links ,"links_len":len(links), "time_links":round((time.time() - start),3) }
    #print(context)
    print("Working links: ", working_links)

    print("Bad links: ", bad_links)
    #return context


# def test_login_correct(driver):
#
#     test_case_failed = 0
#     test_case_pass = 0
#     driver.get("http://localhost:8000/login/")
#
#     try:
#         print("1")
#         username=driver.find_element(By.NAME,"username")
#         print("2")
#         username.send_keys ("admin")
#         print("3")
#         password=driver.find_element(By.NAME,"password")
#         print("4")
#         password.send_keys("123") # time.sleep (5)
#         print("5")
#         driver.find_element(By.NAME,"login").click()
#         print("6")
#         test_case_pass += 1
#         print("Login passed")
#     except:
#         test_case_failed += 1
#         print("Login test case failed")


def get_image_size(uri):
# get file size *and* image size (None if not known)
    file = urlrq.urlopen(uri,cafile=certifi.where())
    size = file.headers.get("content-length")
    if size:
        size = int(size)
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.size
    file.close()
    return size

def testing_imgs(driver):

    driver.get('http://localhost:8000/')
    links = driver.find_elements_by_css_selector("img")
    print("Testing images...")
    start = time.time()

    proper_image = 0
    bad_image = 0
    bad_image_list=[]
    for link in links:
        r = requests.head(link.get_attribute('src'))
        image_size = get_image_size(link.get_attribute('src'))[1]
        if image_size[0] == 0 or image_size[1] == 0:
            bad_image += 1
            bad_image_list.append((link.get_attribute('src'),r.status_code))
        else:
            proper_image += 1
    print("Proper Images: ",proper_image)
    print("Bad Images: ",bad_image)

    #context = { "proper_image":proper_image,"bad_image_list":bad_image_list , "bad_image":bad_image ,"imgs_len":len(links), "time_imgs":round((time.time() - start), 3) }
    #return context
testing_links(driver)
testing_imgs(driver)
