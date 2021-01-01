# tastybrianz
playing around with musicbrainz


# Running as script

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
etc....
```