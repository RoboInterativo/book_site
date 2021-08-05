import urllib.parse
import requests
from bs4 import BeautifulSoup
import os
from pathvalidate import sanitize_filename
from transliterate import translit


def check_for_redirect(base_url,response):
    print(base_url,response.url)

    if len(response.history)>0:
        if response.history[0].status_code==302:

            raise Exception('HTTPError')
    else:
       pass

def download_image (base_url,book_id):
    url=urllib.parse.urljoin(base_url,'/b{}'.format(book_id) )
    response=requests.get(url)
    print (response)
    print ('GET IMAGE', response.url)
    soup = BeautifulSoup(response.text, 'lxml')
    book_image=soup.find(class_='bookimage')
    img_part_url=book_image.find('img')['src']
    if img_part_url.find('nopic.gif')<0:
        url_img=urllib.parse.urljoin(base_url,'/{}'.format(img_part_url) )
        response_img=requests.get(url)
        if response_img.status_code==200:
            filename=img_part_url.split('/')[-1]
            f=open(os.path.join('books',filename),'wb')
            f.write(response.content)
            f.close()


def get_book_title (base_url,book_id):
    url=urllib.parse.urljoin(base_url,'/b{}'.format(book_id) )
    response=requests.get(url)
    print ('GET BOOK TITLE', response.url)
    #print (response.text)
    soup = BeautifulSoup(response.text, 'lxml')
    book_name_and_author = soup.find(id = 'content').find('h1')
    book_title = book_name_and_author.get_text().split('::')[0].strip()

    print(response.url)
    print (book_title)
    return book_title


def get_book_author (base_url,book_id):
    url=urllib.parse.urljoin(base_url,'/b{}'.format(book_id) )
    print (response)
    soup = BeautifulSoup(response.text, 'lxml')
    book_name_and_author = soup.find(id = 'content').find('h1')

    book_author = book_name_and_author.get_text().split('::')[1].strip()
    print(response.url)
    print (book_author)
    return book_author


def download_book(base_url,book_id):
    url=urllib.parse.urljoin(base_url,'/txt.php?id={}'.format(book_id) )
    response=requests.get(url)
    print (url)
    try:
        check_for_redirect(base_url,response)

    except :
        print('Redirect')
    else:
        fname='{}.{}.txt'.format(book_id, translit( get_book_title(base_url,book_id) ,'ru',reversed=True) )
        filename=sanitize_filename(fname)
        print (filename)
        f=open(os.path.join('books',filename),'wb')
        f.write(response.content)
        f.close()
        #Download IMAGE
        download_image (base_url,book_id)
    #print (response.content)




if __name__ == '__main__':
    base_url = 'https://tululu.org'
    os.makedirs('books', exist_ok=True)
    for book_id in range(1,11):
        download_book(base_url,book_id)
