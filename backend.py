from splinter import Browser
import time
import re
import requests
import json

browser = Browser("chrome")

Completed = []
Failed = []

#loads the webpage as soon as the webserver has started
def init():
    browser.visit("http://127.0.0.1:8080/")


#the main loop that navigates to the page and requests the backlink
def requestLinks(req_data):
    #opens a new tab to do all of the requesting
    browser.driver.execute_script("window.open('');")

    for backlink in req_data["linksToRequest"]:

        #modifies the TargetURL form the request to fill form fields on the webpage
        targetDomain = re.sub("http.*?://", "", backlink)
        targetSubdomain = re.sub("\..*?/", "", targetDomain)
        targetDomain = re.sub("/", "", targetDomain)

        #sends GET request to Majestic API to retrieve backlinks to fill the form
        availableBackLinks = getBackLinkURLs(targetDomain, req_data)

        #switches to the new tab and visits the targetURL
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

        #fills the request form
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

        #tries all potential backlinks
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

            #breaks the for loop if the link gets accepted and adds it to a list if it succeeds
            if browser.is_text_present("succesvol") == True:
                print("link successvol aangevraagd!")
                Completed.append(backlink)
                break
    #if it fails to request the backlink using the retrieved backlinks it adds the link to the failed list
    if browser.is_text_present("succesvol") == False:
        Failed.append(backlink)

    #prints the links that failed and succeeded
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

    #uses a diffferent request URL if the value in webserver response is set to true
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