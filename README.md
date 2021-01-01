# tastybrianz
playing around with musicbrainz


# Running as script

brainz_series.py
* Get a series from musicbrainz.
* Downloaded data is saved to a cache directory.
* Optionally add additional lists as difference columns.
* Optionally sort the data.
* Format data as a tabulate table and print.

```
 usage: brainz_series.py [-h] [-s SORT] [--style STYLE] [-t TRUNCATE] [{rs2012,rs2020,guardian100,jaguaro}] [compare_ids ...]

positional arguments:
  {rs2012,rs2020,guardian100,jaguaro}
                        id of series to show
  compare_ids           ids of series to compare against

optional arguments:
  -h, --help            show this help message and exit
  -s SORT, --sort SORT  sort by column
  --style STYLE         tabulate style
  -t TRUNCATE, --truncate TRUNCATE
                        truncate entries
```

## Example
```
brainz_series.py -t 30 rs2020 rs2012
```

```
Rolling Stone: 500 Greatest Albums of All Time: 2020 edition
| num    | title                          | artist                         | year   | rs2012   |
|--------+--------------------------------+--------------------------------+--------+----------|
| 1      | What’s Going On                | Marvin Gaye                    | 1971   | ^5       |
| 2      | Pet Sounds                     | The Beach Boys                 | 1966   | -        |
| 3      | Blue                           | Joni Mitchell                  | 1971   | ^27      |
| 4      | Songs in the Key of Life       | Stevie Wonder                  | 1976   | ^53      |
| 5      | Abbey Road                     | The Beatles                    | 1969   | ^9       |
| 6      | Nevermind                      | Nirvana                        | 1991   | ^11      |
| 7      | Rumours                        | Fleetwood Mac                  | 1977   | ^19      |
| 8      | Purple Rain                    | Prince and The Revolution      | 1984   | ^68      |
etc...
```

```
brainz_series.py -t 30 --sort year --style plain guardian100
```

```
The Guardian 100 Best Albums Ever
  num  title                           artist                            year
   94  Songs for Swingin’ Lovers!      Frank Sinatra                     1956
   14  Kind of Blue                    Miles Davis                       1959
   11  Highway 61 Revisited            Bob Dylan                         1965
   45  A Love Supreme                  John Coltrane                     1965
    2  Revolver                        The Beatles                       1966
    6  Pet Sounds                      The Beach Boys                    1966
   24  Blonde on Blonde                Bob Dylan                         1966
    8  The Velvet Underground & Nico   The Velvet Underground & Nico     1967
etc...
```

# Using as module

```
import brainz_series
t=brainz_series.generate_table("rs2020",["rs2012"],30)
t.sort_by_column("year")
print(t.tabulate("simple"))
```
