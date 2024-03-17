from __future__ import annotations

from datetime import date, datetime
from math import ceil
from time import sleep
from typing import Dict, List, Tuple

import requests


class SFMArtist:
    @staticmethod
    def from_json(artist_json: Dict) -> SFMArtist:
        id = artist_json['mbid']
        name = artist_json['name']

        return SFMArtist(id, name)

    def __init__(self, artist_id: str, name: str):
        self.artist_id = artist_id
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.artist_id == other.artist_id

    def __hash__(self):
        return hash(self.artist_id)


class SFMVenue:
    @staticmethod
    def from_json(venue_json: Dict) -> SFMVenue:
        id = venue_json['id']
        name = venue_json.get('name')
        venue_city_json = venue_json['city']
        city = venue_city_json['name']
        country = venue_city_json['country']['name']

        return SFMVenue(id, name, city, country)

    def __init__(self, id: str, name: str | None, city: str, country: str):
        self.id = id
        self.name = name
        self.city = city
        self.country = country

    def __str__(self):
        return ", ".join([self.name, self.city, self.country])

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class SFMSong:
    @staticmethod
    def from_json(song_json: Dict) -> SFMSong | None:
        name = song_json['name']

        if not name:
            return None

        was_tape = song_json.get('tape') == 'true'

        if was_tape:
            return None

        raw_covered_artist = song_json.get('cover')
        covered_artist = SFMArtist.from_json(raw_covered_artist) if raw_covered_artist else None

        return SFMSong(name, covered_artist)

    def __init__(self, name: str, covered_artist: SFMArtist | None = None):
        self.name = name
        self.covered_artist = covered_artist

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name and self.covered_artist == other.covered_artist

    def __hash__(self):
        return hash((self.name, self.covered_artist))


class SFMSet:
    @staticmethod
    def from_json(set_json: Dict) -> SFMSet:
        songs = [SFMSong.from_json(song_json) for song_json in set_json['song']]
        songs = [song for song in songs if song is not None]
        return SFMSet(songs)

    def __init__(self, songs: List[SFMSong]):
        self.songs = songs

    def __str__(self):
        return str(self.songs)


class SFMSetlist:
    @staticmethod
    def from_json(setlist_json: Dict) -> SFMSetlist:
        id = setlist_json['id']
        date_string = setlist_json['eventDate']
        date = datetime.strptime(date_string, '%d-%m-%Y').date()

        artist = SFMArtist.from_json(setlist_json['artist'])
        venue = SFMVenue.from_json(setlist_json['venue'])
        sets = [SFMSet.from_json(set_json) for set_json in setlist_json['sets']['set']]

        return SFMSetlist(id, date, artist, venue, sets)

    def __init__(self, id: str, date: date, artist: SFMArtist, venue: SFMVenue, sets: List[SFMSet]):
        self.id = id
        self.date = date
        self.artist = artist
        self.venue = venue
        self.sets = sets

    def __str__(self):
        return f"{self.artist} @ {self.venue} on {self.date}"

    def songs(self):
        return [song for set in self.sets for song in set.songs]


class SetlistFMAPI:
    _max_requests_per_second = 16
    _request_cooldown_period_seconds = 1 / _max_requests_per_second
    _url_base = "https://api.setlist.fm/rest/1.0"

    def __init__(self, api_key: str):
        self.__headers = {'x-api-key': api_key, 'Accept': 'application/json'}

    def get_all_setlists_for_artist(self, artist_id: str) -> List[SFMSetlist]:
        return self.__get_all_setlists(endpoint_path=f"/artist/{artist_id}/setlists")

    def get_all_setlists_for_user(self, username: str) -> List[SFMSetlist]:
        return self.__get_all_setlists(endpoint_path=f"/user/{username}/attended")

    def __get_all_setlists(self, endpoint_path: str) -> List[SFMSetlist]:
        (result, setlists_per_page, total_setlists) = \
            self.__get_single_page_of_setlists(endpoint_path=endpoint_path, page=1)

        page_count = ceil(total_setlists / setlists_per_page)

        for page in range(2, page_count + 1):
            sleep(self._request_cooldown_period_seconds)
            (page_setlists, _, _) = \
                self.__get_single_page_of_setlists(endpoint_path=endpoint_path, page=page)

            result += page_setlists

        return result

    def __get_single_page_of_setlists(self, endpoint_path: str, page: int) -> Tuple[List[SFMSetlist], int, int]:
        url = f"{self._url_base}{endpoint_path}?p={page}"

        # todo: error handling
        json = requests.get(
            url=url,
            headers=self.__headers
        ).json()

        setlists_per_page = int(json['itemsPerPage'])
        total_setlists = int(json['total'])
        page_setlists = [SFMSetlist.from_json(setlist) for setlist in json['setlist']]

        return page_setlists, setlists_per_page, total_setlists
