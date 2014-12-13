from __future__ import with_statement
from bs4 import BeautifulSoup
from models import Tweet
import requests


class Scraper():

    def __init__(self):
        self.root_url = 'http://www.reddit.com/r/quotesporn'

    def fetch_and_persist(self, db_session):
        self.db_session = db_session
        self._persist(self._fetch())

    def _fetch(self):
        for soup in self._generate_soup():
            yield self._parse_page(soup)

    def _generate_soup(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        soup = BeautifulSoup(requests.get(self.root_url, headers=headers).text)
        while not self._end_of_soup(soup):
            yield soup
            url = self._next_soup_url(soup)
            soup = BeautifulSoup(requests.get(url, headers=headers).text)

    def _next_soup_url(self, soup):
        return soup.select('.nextprev a')[-1]['href']

    def _end_of_soup(self, soup):
        return 'prev' in soup.select('.nextprev a')[-1].text

    def _parse_page(self, soup):
        links = []
        for row in soup.select('.link'):
            parsed_link = self._parse_link_row(row)
            if parsed_link is not None:
                links += [parsed_link]
        return links

    def _parse_link_row(self,row):
        if 'imgur' in row.select('.title.may-blank')[0]['href']:
            likes = row.select('.score.likes')[0].text

            url = row.select('.title.may-blank')[0]['href']
            url = url.replace('http://imgur.com/', 'http://i.imgur.com/')
            if not url.endswith(".jpg"): url += '.jpg'

            return {
                'title': row.select('.title.may-blank')[0].text,
                'url': url,
                'likes': int(likes) if likes != u'\u2022' else 0
            }

    def _persist(self, data):
        with self.db_session.begin(subtransactions=True):
            for page in data:
                for line in page:
                    existing_record = self.db_session.query(Tweet).filter_by(url=line['url']).first()
                    if existing_record is None:
                        self.db_session.add(Tweet().fromdict(line))
                    elif existing_record.likes > line['likes']:
                        existing_record.likes = line['likes']
                        existing_record.title = line['title']

