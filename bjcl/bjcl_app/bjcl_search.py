import requests
import goodreads_api_client as gr
from bs4 import BeautifulSoup
from .models import result
from .models import searchers
import re
Main_url = "http://213.177.28.84/opac/search?q="
rx = re.compile(r'^\s+$')
done=False

def get_cover(title):
    client = gr.Client(developer_key='hqeLOWfIts8XH3EBK8eiJA')
    books = client.search_book(title)
    if int(dict(books).get('total-results')) == 0:
        return "http://213.177.28.84/covers.svc?h=140&rid=30565&sourceType=local&t=m&w=99"
    elif int(dict(books).get('total-results')) == 1:
        results = dict(dict(books).get('results')).get('work')
        id = dict(dict(dict(results).get('best_book')).get('id')).get('#text')
        book = client.Book.show(id)
        keys_wanted = ['link']
        book = {k: v for k, v in book.items() if k in keys_wanted}
        book_url = BeautifulSoup(requests.get(book.get('link')).text, 'html.parser')
        img = book_url.find('img', {'id': 'coverImage'}).get("src")
        return img
    else:
        results = list(dict(dict(books).get('results')).get('work'))[0]
        title_r = str(dict(dict(results).get('best_book')).get('title'))
        if (title == title_r):
            id = dict(dict(dict(results).get('best_book')).get('id')).get('#text')
            book = client.Book.show(id)
            keys_wanted = ['link']
            book = {k: v for k, v in book.items() if k in keys_wanted}
            book_url = BeautifulSoup(requests.get(book.get('link')).text, 'html.parser')
            img = book_url.find('img', {'id': 'coverImage'}).get("src")
        else:
            img = "http://213.177.28.84/covers.svc?h=140&rid=30565&sourceType=local&t=m&w=99"
        return img

def disponibility(respond):
    list2 = []
    #print(BeautifulSoup(str(respond), 'html.parser').findAll('li', {'class': 'avail_inf'}))
    for i in BeautifulSoup(str(respond), 'html.parser').findAll('li', {'class': 'avail_inf'}):
        k = BeautifulSoup(str(i), 'html.parser').findAll('a')
        k = str(k).split(", ")
        list2.append(BeautifulSoup(str(k[1]), 'html.parser').get_text())
        list2 = [item.strip() for item in list2 if not rx.match(item)]
    return list2

def visitor_ip_address(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def web_get(title, request):
    browser_info = request.user_agent.browser
    device_info = request.user_agent.device.family
    os_info = request.user_agent.os
    ip = visitor_ip_address(request)
    searchers_instance = searchers.objects.create(search=title, ip=ip, browser_info=browser_info, os_info=os_info,device_info=device_info)
    searchers_instance.save
    result.objects.all().delete()
    book_title_to_search = requests.get(Main_url + str(title).replace(" ", "+")).text
    soup = BeautifulSoup(book_title_to_search, 'html.parser').findAll("ul", {"class": "clear srch_reslt_list"})
    Book_list = []  # The big list witch contains all list of books
    diponibilitate = disponibility(soup)
    for i in (BeautifulSoup(str(soup), 'html.parser').findAll('table')):
        j = BeautifulSoup(str(i), 'html.parser').findAll('li')
        List = []  # The small list witch contains book info, like: title,author,lang and cover img
        for k in j:
            b_title = None
            b_author = None
            k = BeautifulSoup(str(k), 'html.parser')
            if k.find('a', {"name": "book_link"}) == None:
                pass
            else:
                b_title = str(k.find('a', {"name": "book_link"}).get_text())
                List.append(b_title)
            if  k.find('span', {'class': 'crs_author'}) == None:
                pass
            else:
                b_author = str(k.find('span', {'class': 'crs_author'}).get_text())
                List.append(b_author)
                b_author = b_author.split(' ')[0].replace(",", "")

            List = [item.strip() for item in List if not rx.match(item)]
        image_link = get_cover(List[0])
        List.append(image_link)
        Book_list.append(List)
    k=0
    for i in Book_list:
        i.append(diponibilitate[k])
        k=k+1
    for i in Book_list:
        i[3]= [int(word) for word in i[3].split() if word.isdigit()]
        i[3] = list(i[3])[0]
        while len(i[0]) >= 20:
            i[0] = ' '.join(i[0].split(' ')[:-1])
        while len(i[1]) >= 20:
            i[1] = ' '.join(i[1].split(' ')[:-1])

        if i[3] == 0:
            color='red'
        else:
            color='green'
        result_instance = result.objects.create(book_title=i[0], book_author=i[1], book_image=i[2], book_disponibility=i[3], disp_color=color)
        result_instance.save