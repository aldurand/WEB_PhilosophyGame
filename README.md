## Lab of "INF344-Donnees du Web"  @ Telecom ParisTech - 2017/2018


**The objective of this Lab is to create a game based on Wikipedia.**

**The game is named "Tous les chemins mènent à la Philosophie" ("All roads lead to Philosophy").**

**The goal is to reach the Philosophy page in as few steps as possible, by following the internal links leading from one article to another.**

### Rules :
- To start, the gamer gives the name of an article (whatever he wants).
- Then the 10 first links to other articles for that given article are displayed.
- The gamer has to click on the one that may lead him as quickly as possible to Philosophy.
- Then the first 10 links for the new article are displayed ...
- etc ...
- Until Philosophy is in the list and the gamer select it.


---

The python code is composed of :

- *getPage.py* contains the functions created to request the Wikipedia API, parse and process the response and return (for a given page) the 10 first links to other Wiki pages.

- *philosophie.py* use the Flask framework to develop the web application.

---

# To play the game :
Fisrt, make sure you have Python 3 with the following packages : bs4, json, urllib, pprint, flask.
1) Download the repository as a ZIP file and Unzip
2) In a terminal window, browse to the directory where you have unzipped the archive and run the command:
```
$ python philosophie.py (or $ python3 philosophie.py, depending on your python configuration)
```
3) In your web browser, go to http://127.0.0.1:5000/ (or http://localhost:5000/)
4) Let's play !

When you want to stop the game, just close the tab on your browser and quit the python script on your terminal (CTRL+C).

