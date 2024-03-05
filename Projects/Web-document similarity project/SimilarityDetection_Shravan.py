"""
In this script, I am extracting text content from a web page without 
any HTML tags using request Library. I have not used any HTML
parser here.
Then two urls are provided by input tag and detecting the similarity
between those pages.

How to use this script:
While running this script you need to provide two 
urls as command line input for which you want to
get the similarity

Author: Shravan
Date: 02-03-2024
"""

# Importing required library
import requests, re, sys
from time import time

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


###--------------Second Assignment-----------------###

def getFrequency(text):
    """
    returns a dict containing keys as 5 gram combined words
    and values as their occurence frequency
    """
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.lower().split()
    words = {}
    for i in range(0, len(text)-5, 3):
        nGram = ""
        for j in range(5):
            nGram += text[i+j]
        if nGram not in words:
            words[nGram] = 1
        else:
            words[nGram] += 1
    return words


def _hashFunction(word):
    p = 53  # choose 53 a prime number
    value = 0
    for char in range(len(word)):
        ASCII_value = ord(word[char])*(p**char)  # get the ASCII Value of the char
        value += ASCII_value
    value = value % 2**64
    # formatting to 64bit binary
    binValueBase = bin(value)[2:]
    binValue = binValueBase.zfill(64)
    return str(binValue)


def generateHashValue(wordFrequencies):
    hashValue = {}
    for word, frequency in wordFrequencies.items():
        wordHashValue = _hashFunction(word)
        hashValue[word] = (frequency, wordHashValue)

    # Calculating simhash values
    hashCode = ""
    for i in range(64):
        total = 0
        # for every bit
        for key in hashValue:
            binValue = hashValue[key][1]
            if (int(binValue[i]) == 1):
                c = 1
            else:
                c = -1
            total += c*hashValue[key][0]
        # -ve then consider 0 else 1
        if total < 0:
            hashCode = (hashCode + "0")
        else:
            hashCode = (hashCode + "1")
    return hashCode


def getSimilarity(b1, b2):
    """
    Returns the count of similar bits in two 64bit binary numbers
    otherwise raise error
    """
    bin1 = str(b1)
    bin2 = str(b2)
    if len(bin1)!=len(bin2):
        raise ("Length does not match")
    similarBits = 0
    for i in range(64):
        if bin1[i]==bin2[i]:
            similarBits += 1
    return similarBits


def main():
    url1 = sys.argv[1]
    url2 = sys.argv[2]
    startTime = time()

    textFirst = requests.get(url=url1).text
    textSecond = requests.get(url=url2).text

    content1 = extractBody(textFirst)
    content2 = extractBody(textSecond)

    hashedContent1 = generateHashValue(getFrequency(content1))
    hashedContent2 = generateHashValue(getFrequency(content2))
    similarBits = getSimilarity(hashedContent1, hashedContent2)
    print("Number of similar bits between given urls is: ", similarBits)
    print("Percentage of similarity: ", (similarBits/64)*100, "%")
    print("Time taken to calculate similarity is: ", time()-startTime, "seconds")


if __name__ == "__main__":
    main()