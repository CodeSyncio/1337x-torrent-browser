import requests , os , termcolor , base64
from bs4 import BeautifulSoup ; from time import sleep ; from linecache import getline as gl

curdir = os.getcwd()
condir =curdir+'/configs/config.txt'
SleepTime = 2
MaxLinks = 20
cboardsetting = gl(condir, 2).strip()
qbitdownloadingsetting = gl(condir, 3).strip()

def cls():                                         
    os.system('cls' if os.name=='nt' else 'clear')  
    
def main(pagenum,oldreq,oldcat,oldorder):
    
    Domainencoded = gl(condir, 1).strip()
    cls()
    encutf = Domainencoded.encode("UTF-8")
    decced = base64.b64decode(encutf)
    finaldecoded = decced.decode("UTF-8")
    
    if len(str(pagenum)) == 0:
        pagenum = 1
    else:
        pass
    
    if len(oldreq) ==0:
        print('Please enter the text to search for\n')
        textinput = input()
    
    else:
        textinput = oldreq
    
    if len(oldcat) ==0:
        cls()
        print('Please enter the category to search in\n')
        print('[1] Movies')
        print('[2] Games')
        print('[3] Applications')
        print('[4] Music')
        print('[5] Documenteries')
        print('[6] Anime')
        print('[7] Wildcard')
        CatNumber = input('\n')
        Cats = ['movies','games','apps','music','documentaries','anime']
        
        if CatNumber != '7':
            SearchCategory = Cats[int(CatNumber)-1]
        
        else:
            SearchCategory = 'Wild'
    
    else:
        SearchCategory = oldcat
          
    if len(oldorder) ==0:
        cls()
        print('Please enter order to put torrents in\n')
        print('[1] by Seeders')
        print('[2] by size')
        print('[3] by time')
        
        OrderNumber = input('\n')
        Orders = ['seeders','size','time']   
        SortOrder = Orders[int(OrderNumber)-1]
        
    else:
         SortOrder = oldorder
        
    if SearchCategory != 'Wild':   
        BuildedReqLink = 'https://'+str(finaldecoded)+'/sort-category-search/'+str(textinput)+'/'+str(SearchCategory)+'/'+str(SortOrder)+'/desc/'+str(pagenum)+'/'
            
    else:
        BuildedReqLink = 'https://'+str(finaldecoded)+'/sort-search/'+str(textinput)+'/'+str(SortOrder)+'/'+'desc/'+str(pagenum)+'/'
            
    page = requests.get(BuildedReqLink) # Getting page HTML through request
    
    soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup
    
    Names = soup.select("table tbody tr td.coll-1.name a") # Selecting all of the anchors with titles
    Seeders = soup.select("table tbody tr td.coll-2")
    Sizes = soup.select("table tbody tr td.coll-4")
    Dates = soup.select("table tbody tr td.coll-date")
    namelist = []
    pathlinks = []
    Seederlist = []
    torrentlinksunfitered = []
    torrentlinks = []
    sizeslist = []
    Datelist = []
    
    for anchor in Names:
        namelist.append(anchor.text)
        
    while("\n" in namelist) :
        namelist.remove("\n")
    
    for anchor in Names:
        pathlinks.append(anchor.attrs)  
    
    for td in Seeders:
        Seederlist.append(td.text)
        
    for td in Sizes:
        sizeslist.append(td.text)
    
    for td in Dates:
        Datelist.append(td.text)

    for link in soup.find_all('a'):
          torrentlinksunfitered.append(link.get('href'))

    torrentlinks = [x for x in torrentlinksunfitered if x.startswith('/torrent/')]

    cls()
    counter = 1
    
    for x in range(len(namelist)):
        
        if counter != (int(MaxLinks) + 1):
            print (str(counter)+ '. '+namelist[x]),termcolor.cprint(' [Seeds: '+ Seederlist[x]+' Size: '+sizeslist[x]+ ' Upload Date: '+Datelist[x]+' ] \n', 'red')
            counter = counter + 1
           
    
    
    termcolor.cprint('\n\nchoose a link:    ','green'),termcolor.cprint('[type "b" to choose another section, "p" for a dif page] \n','cyan')
    
    chosenflwnmbr = input()
    cls()
    
    if chosenflwnmbr != 'b' and chosenflwnmbr != 'p':
        
        if int(chosenflwnmbr) < 20 + 1:
            chosentorrenttext =(namelist[int(chosenflwnmbr) - 1])
            chosentorrentpath = (torrentlinks[int(chosenflwnmbr) - 1])
            
            
        else:
            return main(0,'','','')
    
    elif chosenflwnmbr == 'p':
        cls()
        print('Type the page number you want')
        page = input()
        main(page,textinput,SearchCategory,SortOrder)
    
    else:
        main(0,'','','')
    
    buildedlink = ('https://www.1377x.to'+ chosentorrentpath)
    print(buildedlink)
    
    magnetpage = requests.get(buildedlink) # Getting page HTML through request
    magnetsoup = BeautifulSoup(magnetpage.content, 'html.parser') # Parsing content using beautifulsoup
    magnetunfiltered = []

    for link in magnetsoup.find_all('a'):
        magnetunfiltered.append(link.get('href'))

    magnetlink = [x for x in magnetunfiltered if x.startswith('magnet')]
    
    if qbitdownloadingsetting == 'True':
        from qbittorrent import Client
        qb = Client('http://127.0.0.1:8080/')

        qb.login()
            
        qb.download_from_link(magnetlink)
        
        print ('Qbittorrent has started downloading the chosen link, open the client to see progress...')
        sleep(3)
    else:
        pass
    cls()
    if cboardsetting == 'True':
        import pyperclip
        pyperclip.copy(magnetlink[0])
        print('The magnet link has been copied to your clipboard, returning to torrent chooser in ' +str(SleepTime)+ ' seconds' )
        sleep(int(SleepTime))
        
    else:
        print('This is the magnet link: \n'+magnetlink[0]+'\n\npress enter to return to main screen' )
        ghostedinput = input()
    cls()  
    main(0,'','','')  
    
main(0,'','','')

