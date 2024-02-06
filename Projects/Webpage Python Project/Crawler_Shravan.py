"""
In this script, I am extracting text content from a web page without 
any HTML tags using request Library. I have not used any HTML
parser here.

Author: Shravan
Date: 20-01-2024
"""

"""
Some of the URLs that I worked on:
> https://en.m.wikipedia.org/wiki/Hanging_Stone
> https://en.wikipedia.org/wiki/Cricket
> https://en.wikipedia.org/wiki/Big_Apple
> https://en.wikipedia.org/wiki/NPR
> https://en.wikipedia.org/wiki/Tourism
> https://en.wikipedia.org/wiki/Finance
> https://en.wikipedia.org/wiki/Economy
"""
# Importing required library
import requests, re, sys


def main():
    if len(sys.argv) != 2:
        print("Use as: python filename.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    try:
        content = requests.get(url=url).text
    except:
        print("Failed to load the content. Please try again.")
        exit()
    title = extractTitle(content)
    body = extractBody(content)
    urls = extractURLs(content)
    print("Title: \n", title.strip())
    print("\nBody: \n", body)
    print("\nURLs: \n")
    for url in urls:
        print(url)
    

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
        # Removing all script tag and content
        startidx = bodyHTML.find("<script")
        endidx = bodyHTML.find("</script>")
        while startidx!=-1:
            bodyHTML = bodyHTML[:startidx] + bodyHTML[endidx+8:]
            startidx = bodyHTML.find("<script")
            endidx = bodyHTML.find("</script>")
        # Removing all style tags and content
        startidx = bodyHTML.find("<style")
        endidx = bodyHTML.find("</style>")
        while startidx!=-1:
            bodyHTML = bodyHTML[:startidx] + bodyHTML[endidx+8:]
            startidx = bodyHTML.find("<style")
            endidx = bodyHTML.find("</style>")
        
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
        cleanedContent = re.sub(r'&#[^;]+;', '', cleanedContent)
        try:
            cleanedContent = cleanedContent[cleanedContent.index("From Wikipedia, the free encyclopedia"):]
        except:
            None
        return cleanedContent
    except:
        return "No body content found!!"


def extractURLs(content):
    """Returns all the URLs from the website HTML content
    in a list.
    
    Parameter: content is a HTML content of the site.
    Precondition: must be a string.
    """
    content = content.split()
    links = []
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
                links.append(line[starturl:].strip())
            if ("http" in url) or ("www" in url):
                if url=="https:" or url=="http:":
                    continue
                else:
                    links.append(url)
            else:
                continue
    urlsSet = set(links) # removing duplicate urls
    links = list(urlsSet) # converting back to list
    urls = []
    for url in links:
        if url.startswith("http") or url.startswith("www"):
            urls.append(url)
    return urls


if __name__ == "__main__":
    main()