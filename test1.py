from splinter import Browser
import time
import re
browser = Browser("chrome")

url = "http://bedrijf-overzicht.startbewijs.nl/"
email = "mathijs@marketingmadheads.com"


domain =  re.sub("http.*?://", "", url)
subdomain = re.sub("", "", domain)


print(domain)
print(subdomain)



#opens the link window
browser.windows.current = browser.windows[0]
browser.visit(url)
time.sleep(1)
#navigates to the link submission page
submitButton = browser.find_by_text("Link aanmelden" or "Submit link")
submitButton.click()
time.sleep(1)

browser.find_by_name("email").fill(email)
