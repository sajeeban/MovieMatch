import requests
import urllib

CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'
INFO_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}?api_key={key}'
KEY = 'a6972bd924d0c12c4a9a01fc192a611c'


class MovieInfo(object):

    def __init__(self, movie_name):
        self.movie_name = movie_name
        self.ID = self.imdb_id_from_title(self.movie_name)

    def get_movie_info(self):
        return self.get_poster_urls(self.ID)

    def imdb_id_from_title(self, title):
        """ return IMDB id for search string
            Args::
                title (str): the movie title search string
            Returns:
                str. IMDB id, e.g., 'tt0095016'
                None. If no match was found
        """
        pattern = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q={movie_title}'
        url = pattern.format(movie_title=urllib.parse.quote(title))
        r = requests.get(url)
        res = r.json()
        # sections in descending order or preference
        for section in ['popular','exact','substring']:
            key = 'title_' + section
            if key in res:
                return res[key][0]['id']

    @staticmethod
    def _get_json(url):
        r = requests.get(url)
        return r.json()

    def get_poster_urls(self, imdbid):
        """ return image urls of posters for IMDB id
            returns all poster images from 'themoviedb.org'. Uses the
            maximum available size.
            Args:
                imdbid (str): IMDB id of the movie
            Returns:
                list: list of urls to the images
        """
        config = self._get_json(CONFIG_PATTERN.format(key=KEY))
        base_url = config['images']['base_url']
        sizes = config['images']['poster_sizes'][-4]

        backdrop_size = config['images']['backdrop_sizes'][-2]

        # posters = self._get_json(IMG_PATTERN.format(key=KEY,imdbid=imdbid))['posters']
        images = self._get_json(IMG_PATTERN.format(key=KEY,imdbid=imdbid))
        # Get poster url
        poster = images['posters']
        rel_path = poster[0]['file_path']
        poster_url = "{0}{1}{2}".format(base_url, sizes, rel_path)

        # Get backdrop url
        backdrop = images['backdrops']
        rel_path = backdrop[0]['file_path']
        backdrop_url = "{0}{1}{2}".format(base_url, backdrop_size, rel_path)

        # Get movie information
        info = self._get_json(INFO_PATTERN.format(key=KEY, imdbid=imdbid))

        overview = info['overview']
        revenue = info['revenue']
        title = info['title']
        tagline = info['tagline']
        revenue = format(revenue, ",d")

        movie_details = {
            'poster_url': poster_url,
            'backdrop_url': backdrop_url,
            'overview': overview,
            'revenue': revenue,
            'title': title,
            'tagline': tagline,
        }
        return movie_details
