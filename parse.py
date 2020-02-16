from bs4 import BeautifulSoup
import requests

url = "https://finanzblogroll.de/rss-feed/"
req = requests.get(url)
soup = BeautifulSoup(req.content)
print(soup.title)

feed = []
items = soup.find_all("li", {"class": "feed-item"})
for item in items:
	obj = {
		"link": item.a["href"],
		"title": item.a.contents,
		"date": item.find("span", {"class": "feed-date"}).contents,
		"source": item.find("span", {"class": "feed-source"}).contents
	}
	feed.append(obj)

print(feed)

