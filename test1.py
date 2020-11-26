from splinter import Browser
from selenium.webdriver.common.keys import Keys
import time
import re
browser = Browser("chrome")

targetUrl = "http://bedrijf-overzicht.startbewijs.nl/"
email = "mathijs@marketingmadheads.com"
title = "testpagina"
url = "https://testpage.com/"
desc = "lorem ipsum dolor sit amet"


domain = re.sub("http.*?://", "", targetUrl)
subdomain = re.sub("\..*?/", "", domain)
domain = re.sub("/", "", domain)



print(domain)
print(subdomain)



#opens the link window
browser.windows.current = browser.windows[0]
browser.visit(targetUrl)
time.sleep(1)
#navigates to the link submission page
submitButton = browser.find_by_text("Link aanmelden" or "Submit link")
submitButton.click()
time.sleep(1)

browser.find_by_name("email").fill(email)
time.sleep(0.1)
browser.find_by_name("pagename").fill(subdomain)
time.sleep(0.1)
browser.find_by_text(subdomain.capitalize()).click()
time.sleep(0.1)
browser.find_by_name("linktitel" or "linktitle").fill(title)
time.sleep(0.1)
browser.find_by_name("linkurl").fill(url)
time.sleep(2)
browser.find_by_name("description").click()
browser.find_by_name("description").type(desc)



