from bs4 import BeautifulSoup
import requests
import re
lang = "fr"
# Please modify this according to the line above
end_url = "https://fr.wikipedia.org/wiki/Philosophie"

def isInParentheses(substring,parent):
    # Parameters are Tag Object. Have to convert them to string
    substring = str(substring)
    parent = str(parent)
    try:
        result = re.search('\(([^)]+)', str(parent)).group(1)
        return result.__contains__(str(substring))
    except:
        return False # Malformed parentheses

start_url = "https://"+lang+".wikipedia.org/wiki/Special:Random"

def getSoup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def getTheFirstLink(soup):

    first_paragraph = soup.find("div", {"class": "mw-parser-output"})
    p_list = first_paragraph.find_all('p',recursive=False)

    regular_a_list = []
    for p in p_list:
        a_list = p.find_all('a')
        for a in a_list:
            if a.parent.name == "p":
                regular_a_list.append(a)

    regular_a_list = [a for a in regular_a_list if not isInParentheses(a,a.parent)] # Remove all link in parentheses

    first_a = regular_a_list[0]

    link = first_a.get('href')

    full_link = "https://"+lang+".wikipedia.org"+link

    return full_link

def getNext(url):
    soup = getSoup(url)
    return getTheFirstLink(soup)

def checkIfPhilosophyreached(url):
    return url == end_url

url = start_url
saved_url = []
while not checkIfPhilosophyreached(url):
    print("URL : ",url)
    url = getNext(url)
    if (url in saved_url):
        print("loop")
        break
    else:
        saved_url.append(url)
print("final : ",url)
