from __future__ import annotations

import csv
import os
from argparse import ArgumentParser
from typing import List
from datetime import datetime

from setlist_fm_api import SetlistFMAPI, SFMSetlist


def __write_user_data_csv(username: str, setlists: List[SFMSetlist]):
    titles = ["Date", "Artist", "Venue", "City", "Country", "Songs"]
    rows = [
        [
            datetime.strftime(setlist.date, '%Y-%m-%d'),
            setlist.artist.name,
            setlist.venue.name or "Unknown venue",
            setlist.venue.city,
            setlist.venue.country,
            ";".join([song.name for song in setlist.songs()])
        ] for setlist in setlists
    ]

    __write_csv(titles, rows, filename=f"{username}_setlists")


def __write_csv(titles: List[str], rows: List[List[str]], filename: str):
    output_filename = f"outputs/{filename}.csv"
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    with open(output_filename, mode='w') as output_file:
        output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        output_writer.writerow(titles)

        for row in rows:
            output_writer.writerow(row)


if __name__ == "__main__":
    argParser = ArgumentParser()
    argParser.add_argument('-k', '--api-key', help='setlist.fm API key', required=True)
    argParser.add_argument('-u', '--username', help='setlist.fm username', required=True)
    args = argParser.parse_args()

    username = args.username
    setlist_fm_api = SetlistFMAPI(api_key=args.api_key)
    setlists = setlist_fm_api.get_all_setlists_for_user(username=username)

    __write_user_data_csv(username, setlists)
