try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
import urllib.request
import pyprind
import os
import argparse

# User Agent
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}


def soup_read(url):
    # Open And Read HTML
    soup_req = urllib.request.Request(url, headers=headers)
    soup_open = urllib.request.urlopen(soup_req).read()
    return BeautifulSoup(soup_open, 'html.parser')


def manga_download():
    # Website Link
    manga_source = 'http://www.mangapanda.com/'

    # Argument Parser
    parser = argparse.ArgumentParser(description='Source: ' + manga_source)
    parser.add_argument('name', help='Manga Name')
    parser.add_argument('start', type=int, help='Starting Chapter Number')
    parser.add_argument('end', type=int, help='Ending Chapter Number')
    parser.add_argument('path', help='Download Location')
    args = parser.parse_args()

    # Make Manga Link From Name
    manga_name = args.name
    manga_name = manga_name.lower()
    manga_name = manga_name.replace(' ', '-')
    manga_page = manga_source + manga_name
    print('Manga Link: ' + manga_page, end='\n\n')

    # Prepare Chapter Links
    schap_num = args.start
    echap_num = args.end
    for crange in range(schap_num, echap_num + 1):
        chap_num = str(crange)
        chap_url = manga_page + '/' + chap_num

        # Calculate the Number of pages
        soup = soup_read(chap_url)
        page_options = []
        for option in soup.find_all('option'):
            page_options.append(option['value'])
        page_lenght = (len(page_options))
        print('Total Pages in Chapter {} is {}'.format(chap_num, page_lenght))

        # Append Image Links
        image_links = []
        print('Getting Image Links:')
        bar = pyprind.ProgBar(page_lenght)
        for img in range(1, page_lenght + 1):
            chap_url2 = chap_url + '/' + str(img)
            soup2 = soup_read(chap_url2)
            image_link = soup2.find('img')['src']
            image_links.append(str(image_link))
            bar.update()

        # Create Directory and Downloading Images
        print('Downloading Chapter:' + str(chap_num))
        oman_name = manga_name.replace("-", " ")
        dir_name = '{0}/{1}/{2}'.format(args.path, oman_name, chap_num)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        bar2 = pyprind.ProgBar(page_lenght)
        for img_get in range(1, page_lenght + 1):
            timg_Url = str(image_links[img_get - 1])
            filename = os.path.join(dir_name, 'page' + str(img_get) + '.jpg')
            img_req = urllib.request.Request(timg_Url, headers=headers)
            img_data = urllib.request.urlopen(img_req).read()
            output = open(filename, 'wb')
            output.write(img_data)
            output.close()
            bar2.update()
        print('Downloaded {} Chapter {}'.format(
            oman_name, chap_num), end='\n\n')