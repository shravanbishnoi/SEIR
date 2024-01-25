"""
In this script, I am extracting text content from a web page without any 
HTML tags using request Library. I have not used any HTML
parser here.

Author: Shravan
Date: 20-01-2024
"""
# Importing required library
import requests
import re

# reading website url from user
url = input("Enter the website url: ")
try:
    userChoice = int(input("What are you looking for: \nEnter 1 for Title,\nEnter 2 for body text,\nEnter 3 for urls,\nEnter 0 for all: "))
except:
    print("Enter a valid input!!")
    userChoice = int(input("What are you looking for: \nEnter 1 for Title,\nEnter 2 for body text,\nEnter 3 for urls,\nEnter 0 for all: "))
try:
    content = requests.get(url=url).text
except:
    print("Failed to load the content. Please try again.")
    exit()


def extractTitle(content):
    """Returns a string containing title of the website.
    
    Parameter: content is a HTML content of the site.
    Precondition: must be a string.
    """
    try:
        start = content.find("<title>") + len("<title>")
        end = content.find("</title>")
        title = content[start:end].strip()
        return title
    except:
        return "Title not found!!"


def extractBody(content):
    """Returns a string containing body content of the website.
    
    Parameter: content is a HTML content of the site.
    Precondition: must be a string.
    """
    try:
        start = content.find("<body>") + len("<body>")
        end = content.find("</body>")
        bodyHTML = content[start:end].strip()
        startidx = bodyHTML.find("<script")
        endidx = bodyHTML.find("</script>")
        while startidx!=-1:
            bodyHTML = bodyHTML[:startidx] + bodyHTML[endidx+8:]
            startidx = bodyHTML.find("<script")
            endidx = bodyHTML.find("</script>")
        contentWithoutTags = ""
        var = False
        for char in bodyHTML:
            if char=='>':
                var = True
            elif char=='<':
                var = False
            elif var:
                contentWithoutTags += char
        cleanedContent = ""
        previous = "-1"
        for line in contentWithoutTags.split("\n"):
            if line.strip()=="&nbsp;":
                continue
            if previous=="" and line.strip()=="":
                previous = line.strip()
                continue
            else:
                cleanedContent += "\n" + line.strip()
                previous = line.strip()
        return cleanedContent
    except:
        return "No body content found!!"


def extractURLs(content):
    """Prints all the URLs from the website HTML content.
    
    Parameter: content is a HTML content of the site.
    Precondition: must be a string.
    """
    content = content.split()
    for line in content:
        if "http" in line or "www" in line:
            if '"' in line:
                urlStart = line.find('="')
                urlEnd = line.find('"', urlStart+2)
                url = line[urlStart+2:urlEnd]
            elif "'" in line:
                urlStart = line.find("='")
                urlEnd = line.find("'", urlStart+2)
                url = line[urlStart+2:urlEnd]
            else:
                starturl = line.find("http")
                print(line[starturl:].strip())
            if ("http" in url) or ("www" in url):
                if url=="https:" or url=="http:":
                    continue
                else:
                    print(url)
            else:
                continue


title = extractTitle(content)
body = extractBody(content)
if userChoice==0:
    print(title)
    print(body)
    extractURLs(content)
elif userChoice==1:
    print(title)
elif userChoice==2:
    print(body)
elif userChoice==3:
    extractURLs(content)
else:
    print("Enter a valid input!!")
    userChoice = input("What are you looking for: \nEnter 1 for Title,\nEnter 2 for body text,\nEnter 3 for urls,\nEnter 0 for all:")