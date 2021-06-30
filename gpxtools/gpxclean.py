import argparse
import gpxpy.gpx as gpxpy
import gpxpy as gpx_parser
import glob
from . import common

from typing import *

def main() -> None:
    parser = argparse.ArgumentParser(description='Clean GPX tracks')
    parser.add_argument('-e', '--extensions', action='store_true', help='Remove extensions')
    parser.add_argument('-m', '--time', action='store_true', help='Remove time')
    parser.add_argument('-x', '--elevations', action='store_true', help='Remove extensions')
    parser.add_argument('-r', '--routes', action='store_true', help='Remove routes')
    parser.add_argument('-t', '--tracks', action='store_true', help='Remove tracks')
    parser.add_argument('-a', '--author', action='store_true', help='Remove author data')
    parser.add_argument('-w', '--waypoints', action='store_true', help='Remove waypoints')
    parser.add_argument('-o', '--output', type=str, help='Output GPX file')
    parser.add_argument('-f', '--folder', type=str, help='Folder containing files')
    parser.add_argument('-p', '--prefix', type=str, default = 'cleaned_', help='Prefix of output files')

    args, gpx_files = parser.parse_known_args()

    extensions: bool = args.extensions
    time: bool = args.time
    elevations: bool = args.elevations
    routes: bool = args.routes
    tracks: bool = args.tracks
    author: bool = args.author
    waypoints: bool = args.waypoints
    output = args.output
    folder = args.folder
    prefix = args.prefix

    if folder:
        filelist = glob.glob(folder + '*.gpx')
        gpx_files.extend(filelist)

    for gpx_file in gpx_files:
        with open(gpx_file, encoding='utf-8') as f:
            g = gpx_parser.parse(f)
        if extensions:
            common.clean_extensions(g)
        if time:
            g.time = None
            g.remove_time()
        if elevations:
            g.remove_elevation()
        if routes:
            g.routes = []
        if tracks:
            g.tracks = []
        if author:
            g.author_name = None
            g.author_email = None
            g.author_link = None
            g.author_link_text = None
            g.author_link_type = None
        if waypoints:
            g.waypoints = []

        if len(gpx_files) > 1 or (not output):
            out_gpx = common.prefix_filename(gpx_file, prefix)

        with open(out_gpx, "w", encoding='utf-8') as f:
            print(f'Cleaned {gpx_file} => {out_gpx}')
            f.write(g.to_xml())

