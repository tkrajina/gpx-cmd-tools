import argparse
import gpxpy.gpx as gpxpy
import gpxpy as gpx_parser
import datetime
import sys

from . import common

from typing import *

DATE_FORMAT = "%Y-%m-%d"
LONG_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
TIME_FORMAT = '%Y%m%d%H%M%S'

def need_split_by_days(t1: datetime.datetime, t2: datetime.datetime, seconds: int) -> bool:
    return t1.strftime(DATE_FORMAT) != t2.strftime(DATE_FORMAT)

def need_split_by_time_interval(t1: datetime.datetime, t2: datetime.datetime, seconds: int) -> bool:
    return abs((t2 - t1).total_seconds()) > seconds

def save_gpx(gpg: gpxpy.GPX) -> None:
    pass

def process(gpx_file: str, split_by_days: bool, time_interval: str) -> None:
    print(f"Opening {gpx_file}")
    with open(gpx_file) as f:
        gpx = gpx_parser.parse(f)

    split_func: Callable[[datetime.datetime, datetime.datetime, int], bool]
    interval = 0
    if split_by_days:
        split_func = need_split_by_days
    elif time_interval:
        split_func = need_split_by_time_interval
        interval = common.parse_duration(time_interval)
    else:
        print("Specify way to split GPX file")
        sys.exit(1)

    times: List[datetime.datetime] = []

    for track in gpx.tracks:
        for segment in track.segments:
            for pt in segment.points:
                if pt.time:
                    times.append(pt.time)

    if not times:
        print("No times in track")
        sys.exit(0)

    times.sort()
    
    split_times: List[datetime.datetime] = [times[0] - datetime.timedelta(seconds=1)]
    for n, time in enumerate(times):
        if n > 0:
            prev_time = times[n-1]
            if split_func(prev_time, time, interval):
                split_times.append(time)
    split_times.append(times[-1] + datetime.timedelta(seconds = 1))

    #print(f"Split times: {split_times}")
    for n, time in enumerate(split_times):
        if n > 0:
            gpx_interval = gpx.clone()
            time_from = split_times[n-1]
            time_to = time
            print(f"Interval time {time_from.strftime(LONG_TIME_FORMAT)} - {time_to.strftime(LONG_TIME_FORMAT)}")
            for track in gpx_interval.tracks:
                for segment in track.segments:
                    def fltr(pt: gpxpy.GPXTrackPoint) -> bool:
                        return bool(pt.time and time_from <= pt.time and pt.time < time_to)
                    segment.points = list(filter(fltr, segment.points))
            gpx_interval.remove_empty()
            gpx_interval.remove_empty()
            gpx_interval.remove_empty()

            fn = common.prefix_filename(gpx_file, time_from.strftime(TIME_FORMAT))
            with open(fn, "w") as f:
                f.write(gpx_interval.to_xml())
                print(f"Saved {fn}")

def main() -> None:
    parser = argparse.ArgumentParser(description='Split GPX file')
    parser.add_argument('-d', '--days', action='store_true', default=False, help='How many days')
    parser.add_argument('-t', '--time', type=str, default="", help='Split by time intervals (for exampe 1m, 2s, 3h)')
    parser.add_argument('gpx_files', metavar='gpx', type=str, default='', nargs='*', help='GPX file')
    args = parser.parse_args()

    gpx_files = args.gpx_files
    split_by_days = args.days
    time_interval = args.time

    for gpx_file in gpx_files:
        process(gpx_file, split_by_days = split_by_days, time_interval=time_interval)