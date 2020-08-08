# GPX commandline tools

* `gpxinfo`: General information about GPX file(s)
* `gpxclean`: Removeparts of GPX files (elevations, times, extensions, etc.)
* `gpxmerge`: Merge GPX files
* `gpxsimplify`: Simplify GPX files
* `gpxsplitter`: Split GPX files by time gaps

## gpxinfo

Example:

```
$ gpxinfo test_files/2014-with-wpts.gpx 
File: test_files/2014-with-wpts.gpx
    Waypoints: 2
    Routes: 0
    Length 2D: 4.451km
    Length 3D: 4.607km
    Moving time: 00:30:50
    Stopped time: n/a
    Max speed: 3.35m/s = 12.05km/h
    Avg speed: 2.49m/s = 8.97km/h
    Total uphill: 241.00m
    Total downhill: 258.00m
    Started: 2014-08-22 16:48:52+00:00
    Ended: 2014-08-22 17:19:42+00:00
    Points: 413
    Avg distance between points: 10.78m

    Track #0, Segment #0
        Length 2D: 4.451km
        Length 3D: 4.607km
        Moving time: 00:30:50
        Stopped time: n/a
        Max speed: 3.35m/s = 12.05km/h
        Avg speed: 2.49m/s = 8.97km/h
        Total uphill: 241.00m
        Total downhill: 258.00m
        Started: 2014-08-22 16:48:52+00:00
        Ended: 2014-08-22 17:19:42+00:00
        Points: 413
        Avg distance between points: 10.78m
```

For more options: `gpxinfo -h`

## gpxclean

```
$ gpxclean -h
usage: gpxclean [-h] [-e] [-t] [-x] [-r] [-tr] [-a] [-w] [-o F]

Clean GPX tracks

optional arguments:
  -h, --help        show this help message and exit
  -e, --extensions  Remove extensions
  -t, --time        Remove time
  -x, --elevations  Remove extensions
  -r, --routes      Remove routes
  -tr, --tracks     Remove tracks
  -a, --author      Remove author data
  -w, --waypoints   Waypoints
  -o F, --output F  Output GPX file
```

## gpxmerge

```
$ gpxmerge -h
usage: gpxmerge [-h] [-o F] [-t] [gpx [gpx ...]]

Merge GPX files

positional arguments:
  gpx               GPX file

optional arguments:
  -h, --help        show this help message and exit
  -o F, --output F  Output GPX file
  -t, --time        Sort by time
```

## gpxsimplify

```
$ gpxsimplify -h
usage: gpxsimplify [-h] [-d DISTANCE] gpx

Simplify tracks using the Ramer-Douglas-Peucker algorithm

positional arguments:
  gpx                   GPX file

optional arguments:
  -h, --help            show this help message and exit
  -d DISTANCE, --distance DISTANCE
                        Max distance
```

## gpxsplitter

```
$ gpxsplitter -h
usage: gpxsplitter [-h] [-d] [-t TIME] [gpx [gpx ...]]

Split GPX file

positional arguments:
  gpx                   GPX file

optional arguments:
  -h, --help            show this help message and exit
  -d, --days            Split multi-day track into single day tracks
  -t TIME, --time TIME  Split by time intervals (for exampe 1m, 2s, 3h)
```

## Installation

```
pip install gpx-cmd-tools
```

## See also

* <https://github.com/tkrajina/gpxpy>: Python library for GPX files
* <https://github.com/tkrajina/gpxgo>: Golang library for GPX files
* <https://github.com/tkrajina/gpxchart>: Golang tool for drawing SVG graphs from GPX files

## License

These tools are licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)