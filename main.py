import pyperclip
import requests
from bs4 import BeautifulSoup
from time import sleep
from linecache import getline as gl
import os

curdir = os.getcwd()
condir =curdir+'/configs/config.txt'
SleepTime = 2
MaxLinks = 20
cboardsetting = gl(condir, 2).strip()


def cls():                                         
    os.system('cls' if os.name=='nt' else 'clear')  
    
def main(pagenum,oldreq):
    Domain = gl(condir, 1)
    cls()
    if len(oldreq) ==0:
        print('Please enter the text to search for\n')
        textinput = input()
        
    else:
        textinput = oldreq
    if int(pagenum) > 0:
        BuildedReqLink = 'https://'+Domain+'/sort-search/'+textinput+'/seeders/desc/'+pagenum+'/'
    else:
        BuildedReqLink = 'https://www.1377x.to/sort-search/'+textinput+'/seeders/desc/1/'
    
    
    page = requests.get(BuildedReqLink) # Getting page HTML through request
    soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup
    
    Names = soup.select("table tbody tr td.coll-1.name a") # Selecting all of the anchors with titles
    Seeders = soup.select("table tbody tr td.coll-2")
    namelist = []
    pathlinks = []
    Seederlist = []
    torrentlinksunfitered = []
    torrentlinks = []
    for anchor in Names:
        namelist.append(anchor.text)
        
    while("\n" in namelist) :
        namelist.remove("\n")
    
    for anchor in Names:
        pathlinks.append(anchor.attrs)  
    
    for td in Seeders:
        Seederlist.append(td.text)
    



    for link in soup.find_all('a'):
          torrentlinksunfitered.append(link.get('href'))

    torrentlinks = [x for x in torrentlinksunfitered if x.startswith('/torrent/')]

    cls()
    counter = 1
    for x in range(len(namelist)):
        if counter != (int(MaxLinks) + 1):
            print (str(counter)+ '. '+namelist[x]+' S: '+ Seederlist[x])
            counter = counter + 1

    
    chosenflwnmbr = input('\n\nchoose a link:    \n[type "b" to choose another section, "p" for a dif page] \n')
    cls()
    if chosenflwnmbr != 'b' and chosenflwnmbr != 'p':
        
        if int(chosenflwnmbr) < int(MaxLinks) + 1:
            
            chosentorrenttext =(namelist[int(chosenflwnmbr) - 1])
            chosentorrentpath = (torrentlinks[int(chosenflwnmbr) - 1])
        else:
    
            return main(0,'')
    
    elif chosenflwnmbr == 'p':
        cls()
        print('Type the page number you want')
        page = input()
        main(page,textinput)
    else:
        main(0,'')
    
    buildedlink = ('https://www.1377x.to'+ chosentorrentpath)
    print(buildedlink)
    
    
    
    
    magnetpage = requests.get(buildedlink) # Getting page HTML through request
    magnetsoup = BeautifulSoup(magnetpage.content, 'html.parser') # Parsing content using beautifulsoup
    magnetunfiltered = []

    for link in magnetsoup.find_all('a'):
        magnetunfiltered.append(link.get('href'))

    magnetlink = [x for x in magnetunfiltered if x.startswith('magnet')]

    cls()
    if cboardsetting == 'True':
        pyperclip.copy(magnetlink[0])
        print('The magnet link has been copied to your clipboard, returning to torrent chooser in ' +str(SleepTime)+ ' seconds' )
        sleep(int(SleepTime))
        
    else:
        print('This is the magnet link: \n'+magnetlink[0]+'\n\npress enter to return to main screen' )
        ghostedinput = input()
    cls()  
    main(0,'')  
    
main(0,'')

