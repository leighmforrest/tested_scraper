import pytest

from ..scraper import Scraper, Chart


@pytest.fixture(scope="module")
def webpage():
    with open('tests/chart.txt') as f:
        return f.read()

@pytest.fixture(scope="module")
def previous_webpage():
    with open('tests/previous.txt') as f:
        return f.read()


@pytest.fixture(scope="module")
def scraper():
    return Chart('https://www.billboard.com/')


@pytest.fixture(scope="module")
def chart():
    return Chart('https://www.billboard.com/')


if __name__ == '__main__':
    x = webpage()
    print(x)
