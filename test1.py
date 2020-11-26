from splinter import Browser
import time
import re
import requests
import json

browser = Browser("chrome")

linksToRequest = ["http://bedrijf-overzicht.startbewijs.nl/","http://bedrijf-overzicht.startbewijs.nl/"]
email = "mathijs@marketingmadheads.com"
title = "testpagina"
url = "https://testpage.com/"

def requestLinks():
    for targetUrl in linksToRequest:

        #calls api request with current target url
        getBackLinkURLs(targetUrl)


        #modifies existing strings to fill form fields.
        domain = re.sub("http.*?://", "", targetUrl)
        subdomain = re.sub("\..*?/", "", domain)
        domain = re.sub("/", "", domain)

        #opens the link window and autofills everything
        browser.windows.current = browser.windows[0]
        browser.visit(targetUrl)
        time.sleep(1)
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
    r = requests.get('https://developer.majestic.com/api/json', data)
    #r = requests.get('https://api.majestic.com/api/json', data)

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

    print(backLinks)

requestLinks()
        
