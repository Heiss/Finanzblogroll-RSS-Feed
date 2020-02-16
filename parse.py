from bs4 import BeautifulSoup
import requests
from feedgen.feed import FeedGenerator

def parse(fg, url):
	req = requests.get(url)
	soup = BeautifulSoup(req.content)

	items = soup.find_all("li", {"class": "feed-item"})
	for item in items:
		fe = fg.add_entry()
		fe.title(item.a.contents)
		fe.link(href=item.a["href"])
		
		date = item.find("span", {"class": "feed-date"}).contents
		try:
			from datetime import datetime
			fe.published(datetime.strptime(date, '%d. %m. %Y'))
		except:
			pass
		
		try:
			fe.author(item.find("span", {"class": "feed-source"}).contents)
		except:
			pass


fg = FeedGenerator()
urls = []
with open("linklist.txt", "r") as file:
	parse(fg, file.readline())

fg.rss_str(pretty=True)
fg.rss_file('feed.xml')
