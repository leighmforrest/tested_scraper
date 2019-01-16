import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, site):
        self.site = site

    def get_soup(self):
        self.html = requests.get(self.site).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        return self.soup

    def get_text(self, element):
        """Strip out text from ResultSet"""
        for wrapper in element:
            return wrapper.text.strip().lower()


class Chart(Scraper):
    def get_date(self):
        """Get a date string. Returned string does not conform to Python's formatting."""
        self.get_soup()
        date = self.soup.findAll("button", {"class": "chart-detail-header__date-selector-button"})
        date = self.get_text(date).title().split()
        date_number = int(date[1][:-1])
        if date_number < 10:
            date[1] = f'0{date_number},'
        return ' '.join(date)

    def get_next_weeks_link(self):
        """Get the link for the following week."""
        self.get_soup()
        next_week = None
        dropdowns = self.soup.findAll("li", {"class": "dropdown__date-selector-option"})
        for links in dropdowns:
            for link in links.find_all('a'):
                if link.find('span', {"class": "fa-chevron-right"}):
                    print(link)
                    next_week = 'https://www.billboard.com' + link['href']
        return next_week

    def get_chart_topper(self):
        """Get the number one song."""
        title = self.soup.findAll("div", {"class": "chart-number-one__title"})
        title = self.get_text(title)
        artist = self.soup.findAll("div", {"class": "chart-number-one__artist"})
        artist = self.get_text(artist)
        return {'rank': 1, 'artist': artist, 'title': title}

    def get_songs(self):
        """Get all 100 songs in the chart."""
        rankings = [self.get_chart_topper()]

        songs = self.soup.findAll("div", {"class": "chart-list-item"})
        for song in songs:
            rank = artist = int(song.attrs['data-rank'])
            artist = song.attrs['data-artist'].strip().lower()
            title = song.attrs['data-title'].strip().lower()
            ranking = {
                'rank': rank,
                'artist': artist,
                'title': title
            }
            rankings.append(ranking)

        return rankings
