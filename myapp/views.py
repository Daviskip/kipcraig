import requests
from requests.compat import quote_plus
from django.shortcuts import render
from . import models
from bs4 import BeautifulSoup

BASE_URL_FOR_CRAIGSLIST = 'https://bloomington.craigslist.org/search/sss?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


# Create your views here.


def home(request):
    return render(request, 'base.html')


def search(request):
    new_search = request.POST.get('search')
    models.Search.objects.create(search=new_search)
    final_url = BASE_URL_FOR_CRAIGSLIST.format(quote_plus(new_search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    posts = soup.find_all('li', {'class': 'result-row'})

    l_posts = []

    for post in posts:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        # prices from identified postings
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        # korom weri images in craiglist have been identified by data-ids this is sorting scrapped images
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        l_posts.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'l_posts': l_posts,
    }

    return render(request, 'myapp/search.html', stuff_for_frontend)
