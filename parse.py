from bs4 import BeautifulSoup
import requests
from feedgen.feed import FeedGenerator

def parse(fg, url):
	req = requests.get(url)
	soup = BeautifulSoup(req.content)

	items = soup.find_all("li", {"class": "feed-item"})
	for item in items:
		print(f"current item: {item}")
		print("date: {}, author: {}".format(item.find("span", {"class": "feed-date"}).string, item.find("span", {"class": "feed-source"}).string))
		
		
		fe = fg.add_entry()
		fe.title(item.a.contents[0])
		fe.link(href=item.a["href"])

		try:
			from datetime import datetime
			from pytz import timezone
			
			datetime_obj = datetime.strptime(item.find("span", {"class": "feed-date"}).string, "%d. %m. %Y")
			datetime_obj_utc = datetime_obj.replace(tzinfo=timezone('UTC'))
			print(datetime_obj_utc)
			fe.published(datetime_obj_utc)
		except Exception as e:
			print(f"Error in pubDate: {e}")
		
		try:
			fe.author(name=item.find("span", {"class": "feed-source"}).string})
		except Exception as e:
			print(f"Error in author: {e}")

fg = FeedGenerator()
fg.title('Feed')
fg.description("Feed description")

urls = []
with open("linklist.txt", "r") as file:
	url = file.readline()
	fg.link( href=url, rel='self')
	parse(fg, url)

gist = {
	"files": {
		"feed.xml": {
			"content": fg.rss_str(pretty=True)
		}
	}
}

import sys
headers = {
	"Authorization": "token {}".format(sys.argv[2])
}
requests.patch("https://api.github.com/gists/{}".format(sys.argv[1]), headers=headers, json=gist)
