try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
import urllib
import re
import pyprind
import os
import urllib2
import zipfile
import shutil

#Generate the Mange Page
manga_source = 'http://www.mangapanda.com/'
print 'Enter the Manga Name:',
manga_name = raw_input()
manga_name = manga_name.lower()
manga_name = manga_name.replace(' ', '-')
manga_page = manga_source + manga_name
print ('Manga Link: ' + manga_page)
print ''

#Open the page
Soup_URL = urllib.urlopen(manga_page).read()
soup = BeautifulSoup(Soup_URL,'html.parser')

#Print Information About the Manga
sum = soup.find('div',{'id': 'readmangasum'})
sum1 = sum.find('p').getText()
print 'Summary'.center(40, '-')
print sum1
print 'Latest Chapters'.center(40, '-')
l_chap = soup.find('div',{'id': 'latestchapters'})
print l_chap.get_text().replace('LATEST CHAPTERS','').replace('\n\n','')

#Get the Chapter Number to Download
print 'Enter Starting Chapter Number:',
schap_num = raw_input()
print 'Enter Ending Chapter Number:',
echap_num = raw_input()
for crange in range(int(schap_num), int(echap_num)+1):
	chap_num = str(crange)
	chap_URL = manga_page + '/' + chap_num
	print 'Chapter {} URL is {}'.format(chap_num,chap_URL)

	#Calculate the Number of pages
	Soup_URL2 = urllib.urlopen(chap_URL).read()
	soup2 = BeautifulSoup(Soup_URL2,'html.parser')
	page_options = []
	for option in soup2.find_all('option'):
		page_options.append(option['value'])
	page_lenght = (len(page_options))
	print 'Total Pages in Chapter {} is {}'.format(chap_num,page_lenght)

	#Append Image Links
	image_links = []
	print ''
	print 'Getting Image Links:'
	bar = pyprind.ProgBar(page_lenght)
	for img in range(1 , page_lenght + 1):
		chap_URLN = chap_URL + '/' + str(img)
		Soup_URL2 = urllib.urlopen(chap_URLN).read()
		soup2 = BeautifulSoup(Soup_URL2,'html.parser')
		iLink = soup2.find('img')['src']
		image_links.append(str(iLink))
		bar.update()

	#Create Directory and Downloading Images
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }
	print ''
	print 'Downloading Chapter:' + str(chap_num)
	oman_name = manga_name.replace("-", " ")
	dir_name = './{0}/{1}'.format(oman_name, chap_num)
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)
	zf = zipfile.ZipFile(oman_name+'/'+chap_num+'.zip', "w")
	bar2 = pyprind.ProgBar(page_lenght)
	for imgget in range(1 , page_lenght + 1):
		timg_Url = str(image_links[imgget - 1])
		filename = os.path.join(dir_name, 'page' + str(imgget) + '.jpg')
		#urllib.urlretrieve(timg_Url, filename)
		imgRequest = urllib2.Request(timg_Url, headers=headers)
		imgData = urllib2.urlopen(imgRequest).read()
		output = open(filename ,'wb')
		output.write(imgData)
		output.close()
		zf.write(filename)
		bar2.update()	
	zf.close()
	shutil.rmtree(dir_name)
	print 'Downloaded {} Chapter {}'.format(oman_name, chap_num)