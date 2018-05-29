#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Ne pas se soucier de ces imports
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode, unquote
from pprint import pprint


# Si vous écrivez des fonctions en plus, faites-le ici
def isValid(link):
    '''
    Return True only if the given link is a valid Wikipedia article link
    '''
    if not link.startswith('/wiki/'):  # elimine les liens externes
        return False
    elif 'redlink=1' in link:   # elimine les liens rouges (page inexistante)
        return False
    elif (link.startswith('/wiki/API_') or   # elimine liens hors de l’espace de noms principal
          link.startswith('/wiki/Aide:') or 
          link.startswith('/wiki/Wikip%C3%A9dia:') or
          link.startswith('/wiki/Utilisateur:')):
        return False
    else:
        return True
    
    
def clean(link):
    '''     Return a clear, readable link    '''
    link_wOut_wiki = link.split(sep='/wiki/', maxsplit=1)[1]  # delete '/wiki/'
    link_decoded = unquote(link_wOut_wiki)  # convert %XX non-ascii chars
    link_wOutfragment = link_decoded.split(sep='#', maxsplit=1)[0]  # suppress fragment
    link_cleaned = link_wOutfragment.replace('_', ' ')  # replace '_' by regular space
    return link_cleaned


def getJSON(page):
    params = urlencode({
      'format': 'json',
      'action': 'parse',
      'prop': 'text',
      'redirects': 'true',
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php"
    response = urlopen(API + "?" + params)
    return response.read().decode('utf-8')


def getRawPage(page):
    parsed = loads(getJSON(page))
    try:
        title = parsed['parse']['title']
        content = parsed['parse']['text']['*']
        return title, content
    except KeyError:
        # La page demandée n'existe pas
        return None, None


def getPage(page, limit=None):
    '''
    If exists, return the title (after redirection) and the links of a given page.
    If limit is given, return only the first limit links.
    '''
    
    title, html = getRawPage(page)
    
    if html is not None:
        soup = BeautifulSoup(html, 'html.parser')
        first_div = soup.find('div')
        all_direct_p_firstDiv = first_div.find_all("p", recursive=False)
        links = []
        for p in all_direct_p_firstDiv:
            for link_tag in p.findAll('a', href=True):
                link = link_tag.get('href')
                if not isValid(link):  # keep only Wikipedia valid article link
                    continue
                link_cleaned = clean(link)  # make link readable
                if link_cleaned in links:  # avoid duplicate links
                    continue
                links.append(link_cleaned)
                if (limit is not None and len(links) >= limit):
                    break
            if (limit is not None and len(links) >= limit):
                break
        return title, links
    
    else:
        return title, []
    
    


if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    
    print("Ça fonctionne !")
    
    # Voici des idées pour tester vos fonctions :
    #pprint(getJSON("Utilisateur:A3nm/INF344"))
    #pprint(getRawPage("Utilisateur:A3nm/INF344"))
    #pprint(getRawPage("Histoire"))
    
    page = "Utilisateur:A3nm/INF344"  #"Geoffrey Miller"
    
    title, links = getPage(page, limit=10)

    print(title)
    print('--------------')
    pprint(links)
