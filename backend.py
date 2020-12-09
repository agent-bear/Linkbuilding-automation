from splinter import Browser
import time
import re
import requests
import json

browser = Browser("chrome")

Completed = []
Failed = []

def init():
    browser.visit("http://127.0.0.1:8080/")

def init2(data):
    print(data)

def requestLinks(req_data):
    browser.driver.execute_script("window.open('');")

    for backlink in req_data["linksToRequest"]:

        #modifies existing strings to fill form fields.
        targetDomain = re.sub("http.*?://", "", backlink)
        targetSubdomain = re.sub("\..*?/", "", targetDomain)
        targetDomain = re.sub("/", "", targetDomain)

        #calls api request with current target url
        availableBackLinks = getBackLinkURLs(targetDomain, req_data)

        #switches to the new tab and visits the backlink
        browser.windows.current = browser.windows[1]
        browser.visit(backlink)
        time.sleep(1)

        #tries all possible texts and click it if it finds a hit.
        buttonText = ["submit Link", "Link aanmelden"]
        for text in buttonText:
            button = browser.find_by_value(text)
            if len(button) > 0:
                button.click()
                break

        time.sleep(1)
        browser.find_by_name("email").fill(req_data["targetEmail"])
        time.sleep(0.1)
        browser.find_by_name("pagename").fill(targetSubdomain)
        time.sleep(1)
        browser.find_by_text(targetSubdomain.capitalize()).click()
        time.sleep(0.1)
        browser.find_by_name("linktitel").fill(req_data["targetName"])
        time.sleep(0.1)
        browser.find_by_name("linkurl").fill(req_data["targetURL"])

        for link in availableBackLinks:
            #fills every backlink until one matches
            browser.find_by_name("backlink").fill(link)
            time.sleep(0.1)
            browser.check("agreement")
            time.sleep(0.1)

            #tries all names of the button until it gets one that matches.
            buttonText = ["Request Link", "Vraag link aan"]
            for text in buttonText:
                button = browser.find_by_value(text)
                if len(button) > 0:
                    button.click()
                    break
            
            time.sleep(2)

            #breaks the for loop if the link gets accepted.
            if browser.is_text_present("succesvol") == True:
                print("link successvol aangevraagd!")
                Completed.append(backlink)
                break
        
    if browser.is_text_present("succesvol") == False:
        Failed.append(backlink)

    print("Completed: ", Completed)
    print("Failed: ", Failed)

    browser.windows[1].close()


def getBackLinkURLs(targetDomain, req_data):
    
    # request for 10 backlinks from majestic OpenApp API
    data = {
    'accesstoken': req_data["accessToken"],
    'privatekey': req_data["privateKey"],
    'Timeout': 10,
    'cmd': 'GetBackLinkData',
    'item': targetDomain,
    'datasource': 'fresh',
    'Count': 10,
    'Mode': 1,
    };

    if req_data["devEnviroment"]:
        r = requests.get('https://developer.majestic.com/api/json', data)
    else:
        r = requests.get('https://api.majestic.com/api/json', data)

    #Filters response to get dictionary with just data from backlinks
    response = json.loads(r.text)
    response = response["DataTables"]
    response = response["BackLinks"]
    response = response["Data"]

    #New empty array for Backlink URLs
    availableBackLinks = []

    #goes through response dictionary and adds backlink urls to the new array
    for i in range(len(response)):
        link = response[i]
        availableBackLinks.append(link['SourceURL'])

    return availableBackLinks