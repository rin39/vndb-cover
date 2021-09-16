#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests


def main():
    url, imgname = geturl()
    img, soup = parse(url)
    if img is None:
        url = vnsearch(soup)
        img, soup = parse(url)
        getimagelink(img, imgname)
    else:
        getimagelink(img, imgname)


def geturl():
    usertitle = input("Title: ")
    url = "https://vndb.org/v?sq=" + usertitle
    return url, usertitle


def parse(url):
    print(f"Parsing <{url}>")
    req = requests.get(url)
    src = req.text
    soup = BeautifulSoup(src, "html.parser")
    img = soup.find("div", class_="imghover--visible")
    return img, soup


def vnsearch(soup):
    links = soup.find("div", class_="mainbox browse vnbrowse").find_all("a")
    for i, item in enumerate(links[7:]):
        item_text = item.text
        print(f'{i+1}: {item_text}')
    while True:
        goto = input("Enter number: ")
        try:
            goto = int(goto)
        except ValueError:
            continue
        else:
            break
    url = "https://vndb.org" + links[6+goto].get("href")
    return url


def getimagelink(img, usertitle):
    link = img.img['src']
    with open(usertitle + '.jpg', 'wb') as f:
        img = requests.get(link)
        f.write(img.content)


main()

