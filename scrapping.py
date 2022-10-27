def is_today(text):
    import locale
    import datetime
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    DATE_FORMAT = "%d %B %Y"
    return str(datetime.date.today().strftime(DATE_FORMAT))==text

def scrap_challenge():
    import requests
    from bs4 import BeautifulSoup

    articles=[]
    URL = "https://www.challenge.ma/category/economie/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    divs = soup.find_all("div", class_="vw-post-meta")
    for div in divs:
        url=div.find("a", class_="vw-post-date updated", href=True)['href']
        # if is_today(time=div.find("time").text):
        date=str(div.find("time").text).split()
        date=date[0]+' '+date[1]+' '+date[2]
        author=div.find("a", class_="author-name").text
        article=scrap_challenge_article_contents(url,author,date)
        articles.append(article)

    return articles

def scrap_challenge_article_contents(URL,author,date):
    import requests
    from bs4 import BeautifulSoup
    mydictionry={"author":author,"date":date,"url":URL,"website":"challenge","content":""}

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    title=soup.find("h1", class_="entry-title").text
    content=title+"\n"
    body = soup.find_all("p")
    for c in body:
        content=content+c.text+"\n"
    mydictionry["content"]=content
    return mydictionry

def scrap_matin():
    import requests
    from bs4 import BeautifulSoup
    articles=[]
    URL = "https://lematin.ma/journal/economie/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    divs = soup.find_all("div", class_="p-1 col-lg-3 col-sm-12 col-md-4")
    for div in divs:
        url=div.find("a", href=True)['href']
        # if is_today(time=div.find("time").text):
        article=scrap_matin_article_contents(url)
        articles.append(article)

    return articles

def scrap_matin_article_contents(URL):
    import requests
    from bs4 import BeautifulSoup
    mydictionry={"author":"Le matin","date":"","url":URL,"website":"Le matin","content":""}
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    title=soup.find("h1", { "id" : "title" }).text
    date=str(soup.find("time").text).split()
    date=date[0]+' '+date[1]+' '+date[2]
    mydictionry["date"]=date
    content=title+"\n"
    body = soup.find_all("p")
    for c in body:
        content=content+c.text+"\n"
    mydictionry["content"]=content
    return mydictionry

def scrap_lavieeco():
    import requests
    from bs4 import BeautifulSoup
    articles=[]
    URL = "https://www.lavieeco.com/economie/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    divs = soup.find_all("div", class_="item-inner")
    for div in divs:
        url=div.find("a",  class_="post-title post-url",href=True)['href']
        # if is_today(time=div.find("time").text):
        article=scrap_lavieeco_article_contents(url)
        articles.append(article)


    return articles

def scrap_lavieeco_article_contents(URL):
    import requests
    from bs4 import BeautifulSoup
    mydictionry={"author":"","date":"","url":URL,"website":"lavieeco","content":""}
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    date=str(soup.find("time").text).split()
    date=date[1]+' '+date[2].replace(',',' ')+date[3]

    author=soup.find("span",class_="post-author-name").find("b").text
    title=soup.find("h1", class_="single-post-title")
    title=title.find("span").text
    article=soup.find("article")
    content=title+"\n"
    body = article.find_all("p")
    for c in body:
        content=content+c.text+"\n"
    mydictionry["content"]=content
    mydictionry["date"]=date
    mydictionry["author"]=author
    return mydictionry


def scrap_articles():
    return scrap_lavieeco()+scrap_challenge()+scrap_matin()
