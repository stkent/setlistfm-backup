# setlist.fm backup script

Note: I am not a Python developer, please forgive my syntactic sins.

## Setup

Install the appropriate version of Python using e.g. `asdf`:

```shell
asdf plugin-add python
asdf install python
```

Install Pipenv:

```shell
pip install --user pipenv
```

Install dependencies from the lockfile:

```shell
pipenv sync
```

## Usage

Execute:

```shell
pipenv run python back_up_user_data.py -k API_KEY -u USERNAME
```

where

* `API_KEY` can be applied for via https://www.setlist.fm/settings/apps, and
* `USERNAME` is your setlist.fm username.

This will create a CSV file named `USERNAME_setlist.csv` in the `outputs` directory.

## Sample CSV Output

```csv
Date,Artist,Venue,City,Country,Songs
2023-12-09,Dawes,The Bellwether,Los Angeles,United States,A Little Bit of Everything;From the Right Angle;This Christmas;Someone Else's Café/Doomscroller Tries to Relax;Paul McCarthy;Comes in Waves;How Could This Be Christmas?;When the Tequila Runs Out;Feeling California;Feed the Fire;Broken Harvest;Oh My Christmas Tree;Most People;Skeleton Is Walking;Lazy Daisy;Salute the Institution;Christmas in L.A.;All Your Favorite Bands
2021-12-04,Dawes,Vic Theatre,Chicago,United States,"Still Feel Like a Kid;Most People;Mistakes We Should Have Made;Now That It's Too Late, Maria;Roll With the Punches;Bear Witness;My Way Back Home;Comes in Waves;When My Time Comes;House Parties;Crack the Case;Things Happen;Didn't Fix Me;A Little Bit of Everything;From a Window Seat;All Your Favorite Bands;If I Wanted Someone"
```
