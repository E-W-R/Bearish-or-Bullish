
"""
safari.py (step 1)

Uses Selenium Webdriver to perform a Google Image search and iteratively
load and download each image of a bear or bull using urllib.
"""


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib
import time


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(1)
print("Saved images:")

for species in ["Bear", "Bull"]:

    url = "https://www.google.com/search?tbm=isch&q=" + species
    driver.get(url)
    time.sleep(3)

    start, end = 1, 250
    for i in range(start, end):
        try:
            driver.find_element_by_xpath(
              '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img' % i).click()
            time.sleep(1)
            s = driver.find_element_by_xpath(
              '''//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]
              /div[1]/div[3]/div/a/img''').get_attribute("src")
            urllib.request.urlretrieve(s, "Documents/%ss/%s.png" % (species, i))
            print("%ss/%s.png" % (species, i))
        except:
            pass

driver.close()
