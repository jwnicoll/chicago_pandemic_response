#Crawling through a website providing information on therapists in Chicago.
#The website url is provided below.

import bs4
import requests
import util
import csv

# Initial url:
# 'https://www.psychologytoday.com/us/therapists/il/chicago?sid=602d7d88d7062&rec_next=1'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

def find_links(soup):
    '''
    Given a bs4 BeautifulSoup object, find links to the next page of therapists.

    Inputs: 
        soup (BeautifulSoup object): self-explanatory

    Outputs:
        url_list (list of strings): the list of urls to crawl
    '''
    url_list = []
    links_on_page = soup.find_all('a', title = 'More Therapists')
    for link in links_on_page:
        url = link['href']
        url_list += [url]
    return url_list


def process_page(soup, dic):
    '''
    Adds to the count corresponding to a zip code for every therapist
    located in that zipcode listed on the webpage
    This double counts therapists because of the way the html is set up,
    and this will be accounted for later.

    Inputs:
        soup (BeautifulSoup object)
        dic (dictionary): populates an empty dictionary with zips as keys
            and number of therapists as values

    Outputs:
        dic (dictionary): the populated dictionary
    '''

    therapists = soup.find_all('a', class_= 'textNoLink')
    for therapist in therapists:
        zip_code = therapist['title'][-5:]
        count = dic.get(zip_code, 0)
        count += 1
        dic[zip_code] = count
    return dic

def crawl(initial_list):
    '''
    Crawls through the website, visiting every page linked to from the
    initial page, listed at the top of this document. Incremenets number
    of therapists in each zip code as necessary.

    Inputs:
        initial_list (list of Strings): initial list of urls

    Outputs:
        dic (dictionary): the final mapping of zip codes to number of therapists
    '''

    already_visited = []
    dic = {}
    for url in initial_list:
        if url not in already_visited:
            source = requests.get(url, headers=headers).text
            soup = bs4.BeautifulSoup(source, 'html5lib')
            initial_list += find_links(soup)
            dic = process_page(soup, dic)
            already_visited += [url]
    return dic

def gen_csv(dic, file_name):
    '''
    Write the dictionary produced in the webcrawling to a csv,
    with columns corresponding to zip codes and the number of therapists
    located in each zip code, as listed on the website.

    Inputs:
        dic (dictionary): the final dictionary output from the last function
        file_name (string): the file you want to save to

    Outputs:
        writes the csv
    '''
    
    with open(file_name, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        header = ['zip', 'number']
        writer.writerow(header)
        for zipcode, num in dic.items():
            # Therapists double counted in html for some reason.
            num = num / 2
            row = [zipcode, str(num)]
            writer.writerow(row)

