import requests
from bs4 import BeautifulSoup
import textwrap
import argparse


def scrape(url):
    """Scraper for washingtonpost articles
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="lxml")
    title = soup.find('h1', attrs={'class': "font--headline"}).text
    authors = "By: " + ", ".join([x.text for x in soup.find_all(
                        'div', class_='author-name')])
    date = soup.find('div', class_="display-date").text
    div_text = soup.find_all('p', class_='font--body')
    keep_text = [x for x in div_text
                 if 'hide-for-print' not in x.attrs.get('class')]
    # textwrap used to keep line widths no more than 70
    join_text = "\n\n".join([textwrap.fill(x.text) for x in keep_text])
    return title + "\n" + authors + "\n" + date + "\n\n" + join_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url of article to read")
    parser.add_argument("-v", "--verbosity", default=0,
                        help="Print article to terminal")
    parser.add_argument("-o", "--output", default="article.txt",
                        help="Output text file name")
    args = parser.parse_args()
    url = args.url

    article_string = scrape(url)
    if args.verbosity:
        print(article_string)

    # save to file
    file_path = args.output
    with open(file_path, 'w') as f:
        f.write(article_string)
        f.close()


if __name__ == '__main__':
    main()
