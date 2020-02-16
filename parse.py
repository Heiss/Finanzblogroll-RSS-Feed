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

		try:
			from datetime import datetime
			fe.published(datetime.strptime(item.find("span", {"class": "feed-date"}).contents, '%d. %m. %Y'))
		except:
			pass
		
		try:
			fe.author(item.find("span", {"class": "feed-source"}).contents)
		except:
			pass

fg = FeedGenerator()
fg.title('Feed')
fg.description("Feed description")

urls = []
with open("linklist.txt", "r") as file:
	url = file.readline()
	fg.link( href=url, rel='self')
	parse(fg, url)

fg.rss_str(pretty=True)
fg.rss_file('feed.xml')
