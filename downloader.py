import urllib.parse
import requests
from bs4 import BeautifulSoup
import os


def get_book_title (base_url,book_id):
    url=urllib.parse.urljoin(base_url, 'b{}'.format(book_id, allow_fragments=True))
    response=requests.get(url)
    print (response)
    soup = BeautifulSoup(response.text, 'lxml')
    book = soup.find(id = 'content').find('h1')
    print (book)

def download_book(base_url,book_id):
    url=urllib.parse.urljoin(base_url,'/txt.php?id={}'.format(book_id) )
    response=requests.get(url)
    #print (response.content)

    f=open('books/b{}.txt'.format(book_id),'wb')
    f.write(response.content)
    f.close()

if __name__ == '__main__':
    base_url = 'https://tululu.org'
    os.makedirs('books', exist_ok=True)
    for book_id in range(1,11):
        download_book(base_url,book_id)
