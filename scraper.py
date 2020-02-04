from bs4 import BeautifulSoup
import requests
import json

def get_html(url):

    r = requests.get(url)
    return r.content
    """
    Retrieve the HTML from the website at `url`.
    """

def get_clubs_html():
    """
    Get the HTML of online clubs with Penn.
    """
    url = 'https://ocwp.apps.pennlabs.org'
    return get_html(url)

def soupify(html):
    """
    Load HTML into BeautifulSoup so we can extract data more easily

    Note that for the rest of these functions, whenever we refer to a "soup", we're refering
    to an HTML document or snippet which has been parsed and loaded into BeautifulSoup so that
    we can query what's inside of it with BeautifulSoup.
    """
    return BeautifulSoup(html, "html.parser") 


def get_elements_with_class(soup, elt, cls):
    """
    Returns a list of elements of type "elt" with the class attribute "cls" in the
    HTML contained in the soup argument.

    For example, get_elements_with_class(soup, 'a', 'navbar') will return all links
    with the class "navbar". 

    Important to know that each element in the list is itself a soup which can be
    queried with the BeautifulSoup API. It's turtles all the way down!
    """ 
    return soup.find_all(elt, {'class': cls})

def get_clubs(soup):

    elts = get_elements_with_class(soup, 'div', 'box')
    elts2 = [item for item in elts if item is not None]

    """
    This function should return a list of soups which each correspond to the html
    for a single club.
    """
    return elts2

def get_club_name(club):
    """
    Returns the string of the name of a club, when given a soup containing the data for a single club.

    We've implemented this method for you to demonstrate how to use the functions provided.
    """
    elts = get_elements_with_class(club, 'strong', 'club-name')
    if len(elts) < 1:
        return ''
    return elts[0].get_text().strip()

def get_club_description(club):

    elt = club.find('em')
    if elt is None: 
        return ''
    return elt.get_text().strip()
    """
    Extract club description from a soup of 
    """ 

def get_club_tags(club):
    elts = get_elements_with_class(club, 'span', 'tag is-info is-rounded')
    if len(elts) < 1:
        return []
    else: 
        elts = [item.text for item in elts]
        return elts

class CObj: 
    def __init__(self, name, tags, description):
        self.name = name
        self.tags = tags
        self.description = description

def get_club_objects():
    htmlInfo = get_clubs_html()
    soup = soupify(htmlInfo)
    elts = get_clubs(soup)
    clubs = []
    for i in elts: 
        clubs.append(CObj(get_club_name(i), get_club_tags(i), get_club_description(i)))
    return clubs
