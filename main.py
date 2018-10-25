import logging
import os
from queue import Queue
from threading import Thread
from time import time
import json
import logging
from pathlib import Path
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup




def get_links(url):
    links = []
    linksToReturn = set()
    try:
        res = urlopen(url)
        html = res.read()
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            links.append(link.get('href'))
    except Exception:
        print("Couldn't open url!" + url)        
    for link in links:
        try:
            if 'https:' not in link:
                continue
            else:
                linksToReturn.add(link)
        except Exception:
            print("invalid url")
            continue

    return linksToReturn
    

def crawler(q):
    while True:
        link = q.get()
        visited = open('visited.txt','a')
        visited.write(link + "\n")
        links = get_links(link)
        for link in links :
            f= open('Tovisit.txt','a')
            f.write(link+ "\n")
        q.task_done()



def main(depth,link):
    open('Tovisit.txt', 'w').close()
    f= open('Tovisit.txt','a')
    f.write(link+ "\n")
    f.close()
    queue = Queue(maxsize = 0)
    for x in range(8):
        worker = Thread(target = crawler ,args=(queue,))
        worker.daemon = True
        worker.start()
    for i in range(depth):
        links = [line.rstrip('\n') for line in open('Tovisit.txt')]
        open('Tovisit.txt', 'w').close()
        visited = open('visited.txt','a')  
        if i == 0 :visited.write(links[0]+'\n')
        for link in links:
            queue.put(link)
        queue.join()
        visited.write("---------------------------batch done ------------------------\n")
   

if __name__ == '__main__':
    depth = int(input("enter depth level: "))
    link = str(input("Enter base url:"))
    main(depth = depth,link = link)




