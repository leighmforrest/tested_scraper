from datetime import datetime
import pytest
import requests
from unittest import mock


from scraper.scraper import Scraper


def test_existence(scraper):
    assert scraper is not None


def test_has_site_url(scraper):
    assert scraper.site == 'https://www.billboard.com/'


def test_get_soup(scraper, webpage):
    with mock.patch('requests.get') as m:
        m.return_value.text = webpage
        soup = scraper.get_soup()
        assert soup.find('a') is not None


def test_chart_existence(chart):
    assert chart is not None


def test_chart_has_site_url(chart):
    assert chart.site == 'https://www.billboard.com/'


def test_chart_get_soup(chart, webpage):
    with mock.patch('requests.get') as m:
        m.return_value.text = webpage
        soup = chart.get_soup()
        assert soup.find('a') is not None


def test_chart_date(chart, webpage):
    """Billboard has the date as 'January 19, 2019' '%B %-d, %Y'"""
    with mock.patch('requests.get') as m:
        m.return_value.text = webpage
        date = chart.get_date()
        assert date == 'January 19, 2019'


def test_current_weeks_chart_has_no_next_week(chart, webpage):
    with mock.patch('requests.get') as m:
        m.return_value.text = webpage
        next_week = chart.get_next_weeks_link()
        assert next_week is None


def test_get_chart_topper(chart, webpage):
    with mock.patch('requests.get') as m:
        m.return_value.text = webpage
        topper = chart.get_chart_topper()
        assert 'post malone' in topper['artist']
        assert 'sunflower (spider-man: into the spider-verse)' == topper['title']
        assert 1 == topper['rank']


def test_previous_chart_date(chart, previous_webpage):
    """Billboard has the date as 'January 05, 2019''"""
    with mock.patch('requests.get') as m:
        m.return_value.text = previous_webpage
        date = chart.get_date()
        assert date == 'January 05, 2019'


def test_previous_weeks_chart_has_next_week(chart, previous_webpage):
    with mock.patch('requests.get') as m:
        m.return_value.text = previous_webpage
        next_week = chart.get_next_weeks_link()
        assert next_week == 'https://www.billboard.com/charts/hot-100/2019-01-12'


def test_get_previous_chart_topper(chart, previous_webpage):
    with mock.patch('requests.get') as m:
        m.return_value.text = previous_webpage
        topper = chart.get_chart_topper()
        assert 'ariana grande' in topper['artist']
        assert 'thank u, next' == topper['title']
        assert 1 == topper['rank']


def test_get_chart_songs_is_100(chart, webpage):
    with mock.patch('requests.get') as m:
        m.return_value.text = webpage
        songs = chart.get_songs()
        assert len(songs) == 100


def test_get_chart_songs_correct_format(chart, webpage):
    with mock.patch('requests.get') as m:
        m.return_value.text = webpage
        songs = chart.get_songs()
        for song in songs:
            assert len(song['title']) > 0
            assert len(song['artist']) > 0
            assert song['rank'] > 0 and song['rank'] <= 100
