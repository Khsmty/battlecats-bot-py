import requests
#import urllib.request
from bs4 import BeautifulSoup
from PIL import Image

def get_icon(url):
    #use BeatufulSoup to make it easier to get information
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    #find image in the html
    table_info = soup.findAll("table")[1]
    img_info = table_info.find("img")
    icon_url = img_info["data-src"]

    #open image and return it
    icon = Image.open(requests.get(icon_url, stream = True).raw)
    return icon

def search_site(keyword):
    #go to the page of the search and 
    url = "https://game8.jp/battlecats/search?q=" + keyword
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.findAll("li", {"class" : "c-archiveSearchListItem"})
    for result in results:
        anchor = result.find("a")
        result_header = anchor.find("p")
        result_name = result_header.string

        if result_name.endswith("の評価と使い道"):
            url = anchor["href"]
            return(url)


def search_icon(keyword):
    url = search_site(keyword)
    if url == None:
        return  None
    
    icon = get_icon(url)
    return icon.convert("RGBA")