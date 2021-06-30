"""
Command line utility to extract basic statistics from gpx file(s)
"""

import sys as mod_sys
import logging as mod_logging
import math as mod_math
import argparse as mod_argparse

import gpxpy.gpx as gpxpy
import gpxpy as gpx_parser
import glob

from typing import *

KM_TO_MILES = 0.621371
M_TO_FEET = 3.28084


def format_time(time_s: float, seconds: bool) -> str:
    if not time_s:
        return 'n/a'
    elif seconds:
        return str(int(time_s))
    else:
        minutes = mod_math.floor(time_s / 60.)
        hours = mod_math.floor(minutes / 60.)
        return '%s:%s:%s' % (str(int(hours)).zfill(2), str(int(minutes % 60)).zfill(2), str(int(time_s % 60)).zfill(2))


def format_long_length(length: float, miles: bool) -> str:
    if miles:
        return '{:.3f}miles'.format(length / 1000. * KM_TO_MILES)
    else:
        return '{:.3f}km'.format(length / 1000.)


def format_short_length(length: float, miles: bool) -> str:
    if miles:
        return '{:.2f}ft'.format(length * M_TO_FEET)
    else:
        return '{:.2f}m'.format(length)


def format_speed(speed: float, miles: bool) -> str:
    if not speed:
        speed = 0
    if miles:
        return '{:.2f}mph'.format(speed * KM_TO_MILES * 3600. / 1000.)
    else:
        return '{:.2f}m/s = {:.2f}km/h'.format(speed, speed * 3600. / 1000.)


def print_gpx_part_info(gpx_part: Union[gpxpy.GPX, gpxpy.GPXTrack, gpxpy.GPXTrackSegment], indentation: str='    ', miles: bool = False, seconds: bool = False) -> None:
    """
    gpx_part may be a track or segment.
    """
    length_2d = gpx_part.length_2d()
    length_3d = gpx_part.length_3d()
    print('%sLength 2D: %s' % (indentation, format_long_length(length_2d or 0, miles)))
    print('%sLength 3D: %s' % (indentation, format_long_length(length_3d, miles)))

    moving_data = gpx_part.get_moving_data()
    if moving_data:
        print('%sMoving time: %s' % (indentation, format_time(moving_data.moving_time, seconds)))
        print('%sStopped time: %s' % (indentation, format_time(moving_data.stopped_time, seconds)))
        #print('%sStopped distance: %s' % (indentation, format_short_length(stopped_distance)))
        print('%sMax speed: %s' % (indentation, format_speed(moving_data.max_speed, miles)))
        print('%sAvg speed: %s' % (indentation, format_speed(moving_data.moving_distance / moving_data.moving_time, miles) if moving_data.moving_time > 0 else "?"))

    uphill, downhill = gpx_part.get_uphill_downhill()
    print('%sTotal uphill: %s' % (indentation, format_short_length(uphill, miles)))
    print('%sTotal downhill: %s' % (indentation, format_short_length(downhill, miles)))

    start_time, end_time = gpx_part.get_time_bounds()
    print('%sStarted: %s' % (indentation, start_time))
    print('%sEnded: %s' % (indentation, end_time))

    points_no = len(list(gpx_part.walk(only_points=True)))
    print('%sPoints: %s' % (indentation, points_no))

    if points_no > 0:
        distances: List[float] = []
        previous_point = None
        for point in gpx_part.walk(only_points=True):
            if previous_point:
                distance = point.distance_2d(previous_point)
                distances.append(distance)
            previous_point = point
        print('%sAvg distance between points: %s' % (indentation, format_short_length(sum(distances) / len(list(gpx_part.walk())), miles)))

    print('')


def print_gpx_info(gpx: gpxpy.GPX, gpx_file: str, miles: bool, seconds: bool, only_track: bool) -> None:
    print('File: %s' % gpx_file)

    if gpx.name:
        print('  GPX name: %s' % gpx.name)
    if gpx.description:
        print('  GPX description: %s' % gpx.description)
    if gpx.author_name:
        print('  Author: %s' % gpx.author_name)
    if gpx.author_email:
        print('  Email: %s' % gpx.author_email)
    print(f'    Waypoints: {len(gpx.waypoints)}')
    print(f'    Routes: {len(gpx.routes)}')

    print_gpx_part_info(gpx, miles=miles, seconds=seconds)

    if only_track:
        return

    for track_no, track in enumerate(gpx.tracks):
        for segment_no, segment in enumerate(track.segments):
            print('    Track #%s, Segment #%s' % (track_no, segment_no))
            print_gpx_part_info(segment, indentation='        ', miles=miles, seconds=seconds)


def run(gpx_files: List[str], miles: bool, seconds: bool, only_track: bool) -> None:
    if not gpx_files:
        print('No GPX files given')
        mod_sys.exit(1)

    for gpx_file in gpx_files:
        try:
            gpx = gpx_parser.parse(open(gpx_file, encoding='utf-8'))
            print_gpx_info(gpx, gpx_file, miles, seconds, only_track)
        except Exception as e:
            mod_logging.exception(e)
            print('Error processing %s' % gpx_file)
            mod_sys.exit(1)


def main() -> None:
    parser = mod_argparse.ArgumentParser(usage='%(prog)s [-s] [-m] [-d] [file ...]',
        description='Command line utility to extract basic statistics from gpx file(s)')
    parser.add_argument('-t', '--track', action='store_true', help='Only root track')
    parser.add_argument('-s', '--seconds', action='store_true', help='print times as N seconds, rather than HH:MM:SS')
    parser.add_argument('-m', '--miles', action='store_true', help='print distances and speeds using miles and feet')
    parser.add_argument('-d', '--debug', action='store_true', help='show detailed logging')
    parser.add_argument('-f', '--folder', type=str, help='Folder containing files')
    
    args, gpx_files = parser.parse_known_args()
    seconds = args.seconds
    miles = args.miles
    debug = args.debug
    only_track = args.track
    folder: bool = args.folder

    if folder:
        filelist = glob.glob(folder + '*.gpx')
        gpx_files.extend(filelist)

    if debug:
        mod_logging.basicConfig(level=mod_logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    run(gpx_files=gpx_files, miles=miles, seconds=seconds, only_track=only_track)