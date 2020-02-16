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
		fe.published(item.find("span", {"class": "feed-date"}).contents)
		fe.author(item.find("span", {"class": "feed-source"}).contents)


fg = FeedGenerator()
urls = []
with open("linklist.txt", "r") as file:
	parse(fg, file.readline())

fg.rss_str(pretty=True)
fg.rss_file('feed.xml')
