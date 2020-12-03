#from flask import Flask
from splinter import Browser
import time
import re
import requests
import json

#flask init
#app = Flask(__name__)

#@app.route('/')
#def index():
#    return 'Hello World!'

#if __name__ == "__main__":
#    app.run(debug=True, host="0.0.0.0")

browser = Browser("chrome")

linksToRequest = ["https://piano.allepaginas.nl/", "https://bedrijf-overzicht.startbewijs.nl/", ]
email = "mathijs@marketingmadheads.com"
title = "Pianowebsite"
url = "https://pianowebsite.nl/online-pianoles/"




def requestLinks():
    for targetUrl in linksToRequest:

        #calls api request with current target url
        backLinks = getBackLinkURLs(targetUrl)

        print(backLinks)

        #modifies existing strings to fill form fields.
        domain = re.sub("http.*?://", "", targetUrl)
        subdomain = re.sub("\..*?/", "", domain)
        domain = re.sub("/", "", domain)

        #opens the link window and autofills everything
        browser.windows.current = browser.windows[0]
        browser.visit(targetUrl)
        time.sleep(1)

        #tries all possible texts and click it if it finds a hit.
        buttonText = ["submit Link", "Link aanmelden"]
        for text in buttonText:
            button = browser.find_by_value(text)
            if len(button) > 0:
                button.click()
                break


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

        for link in backLinks:
            #fills every backlink until one matches
            browser.find_by_name("backlink").fill(link)
            time.sleep(0.1)
            browser.check("agreement")
            time.sleep(0.1)

            #tries all variants of the button until it gets one that matches.
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
                break


def getBackLinkURLs(target):
    
    # request for 10 backlinks from majestic OpenApp API
    data = {
    'accesstoken': "AGBKACBKAFBGH",
    'privatekey': "",
    'Timeout': 10,
    'cmd': 'GetBackLinkData',
    'item': target,
    'datasource': 'fresh',
    'Count': 10,
    'Mode': 1,
    };
    
    #Sends GET request to majestic API
    #r = requests.get('https://developer.majestic.com/api/json', data)
    r = requests.get('https://api.majestic.com/api/json', data)

    #Filters response to get dictionary with just data from backlinks
    response = json.loads(r.text)
    response = response["DataTables"]
    response = response["BackLinks"]
    response = response["Data"]

    #New empty array for Backlink URLs
    backLinks = []

    #goes through response dictionary and adds backlink urls to the new array
    for i in range(len(response)):
        link = response[i]
        backLinks.append(link['SourceURL'])

    return backLinks

requestLinks()

        
