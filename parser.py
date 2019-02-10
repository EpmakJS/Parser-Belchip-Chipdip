import requests
from bs4 import BeautifulSoup as bs
import csv

headers = {'accept': '*/*',
		   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

query = 'трансформатор'

bc_url = f'https://belchip.by/search/?query={query}'
cd_url = f'https://www.chipdip.by/search?searchtext={query}'

def bc_parse(bc_url, headers):
	goods = []
	session = requests.Session()
	request = session.get(bc_url, headers=headers)
	if request.status_code == 200:
		soup = bs(request.content, 'lxml')
		divs = soup.find_all('div', attrs={'class': 'cat-item'})
		for div in divs:
			title = div.find('h3').next.text
			href = div.find('h3').next['href']
			href = 'https://belchip.by/' + href
			price = div.find('div', attrs={'class': 'denoPrice'}).text
			for char in '\n':
				price = price.replace(char,'')
			img = div.find('a', attrs={'class': 'product-image'}).img['src']
			img = 'https://belchip.by/' + img
			goods.append({
				'title': title,
				'href': href,
				'price': price,
				'img': img
			})
	else:
		print('ERROR')
	return goods


def cd_parse(cd_url, headers):
	goods = []
	urls = []
	session = requests.Session()
	request = session.get(cd_url, headers=headers)
	if request.status_code == 200:
		soup = bs(request.content, 'lxml')
		try:
			pagination = soup.find_all('li', attrs ={'class': 'pager__page'})
			count = int(pagination[-1].text)
			for i in range(1, count + 1):
				url = cd_url + f'&page={i}'
				if url not in urls:
					urls.append(url)
		except:
			pass

	for url in urls:
		request = session.get(url, headers=headers)
		soup = bs(request.content, 'lxml')
		trs = soup.find_all('tr', attrs={'class': 'with-hover'})
		for tr in trs:
			title = tr.find('a', attrs={'class': 'link'}).text
			href = tr.find('a', attrs={'class': 'link'})['href']
			href = 'https://www.chipdip.by/' + href
			price = tr.find('span', attrs={'class': 'price'}).text
			img = tr.find('span', attrs={'class': 'galery'}).img['src']
			goods.append({
				'title': title,
				'href': href,
				'price': price,
				'img': img
			})
	else:
		print('STATUS CODE ' + str(request.status_code))
	return goods


def write_files(goods):
	with open('parsed_jobs.csv', 'w') as file:
		a_pen = csv.writer(file)
		a_pen.writerow(('Title', 'URL', 'Price', 'Image'))
		for good in goods:
			a_pen.writerow((good['title'], good['href'], good['price'], good['img']))


def append_files(goods):
	with open('parsed_jobs.csv', 'a') as file:
		a_pen = csv.writer(file)
		for good in goods:
			a_pen.writerow((good['title'], good['href'], good['price'], good['img']))


bc_goods = bc_parse(bc_url, headers)
cd_goods = cd_parse(cd_url, headers)
print(bc_goods + cd_goods)
