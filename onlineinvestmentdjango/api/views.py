from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup


# Create your views here.
def main(request):
    list = []
    URL = "https://ikman.lk/en/ads/sri-lanka/land?sort=date&order=desc&buy_now=0&urgent=0&page=1"
    r = requests.get(URL)
    # print(r.content)
    # If this line causes an error, run 'pip install html5lib' or install html5lib
    soup = BeautifulSoup(r.content, 'html5lib')
    print(soup.find_all('span'))
    # print(soup.prettify())
    return HttpResponse("hello123")
