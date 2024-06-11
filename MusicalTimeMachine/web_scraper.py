from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup
import requests

URL = "https://www.billboard.com/charts/hot-100/"


class WebScraper:

    def __init__(self):
        """Scraping Billboard 100"""
        self.date = str(date.today() - timedelta(days=1))
        self.thumbnail = None

    def get_songs(self):
        """Returns Billboard 100 songs and artists names in list"""
        response = requests.get(URL + self.date)
        soup = BeautifulSoup(response.text, "html.parser")

        song_contents = soup.select(selector="li h3[id='title-of-a-story']")
        artist_contents = soup.select(selector="li span[class='c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only'], li span[class='c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only u-font-size-20@tablet']")
        date_str = soup.select_one(selector="p[class='c-tagline a-font-primary-medium-xs u-font-size-11@mobile-max u-letter-spacing-0106 u-letter-spacing-0089@mobile-max lrv-u-line-height-copy lrv-u-text-transform-uppercase lrv-u-margin-a-00 lrv-u-padding-l-075 lrv-u-padding-l-00@mobile-max']")

        music_list = [{"song": song.text.strip(), "artist": artist.text.strip()} for artist, song in
                      zip(artist_contents, song_contents)]

        if not music_list:
            print("Billboard 100 doesn't exist for this date.")
            return exit()

        self.date = datetime.strptime(date_str.text[8:], "%B %d, %Y").strftime("%Y-%m-%d")
        self.thumbnail = soup.select_one(selector="li div div img").get("data-lazy-src")

        return music_list
