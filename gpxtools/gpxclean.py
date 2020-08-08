import argparse
import gpxpy.gpx as gpxpy
import gpxpy as gpx_parser

from . import common

from typing import *

def main() -> None:
    parser = argparse.ArgumentParser(description='Clean GPX tracks')
    parser.add_argument('-e', '--extensions', action='store_true', help='Remove extensions')
    parser.add_argument('-t', '--time', action='store_true', help='Remove time')
    parser.add_argument('-x', '--elevations', action='store_true', help='Remove extensions')
    parser.add_argument('-r', '--routes', action='store_true', help='Remove routes')
    parser.add_argument('-tr', '--tracks', action='store_true', help='Remove tracks')
    parser.add_argument('-a', '--author', action='store_true', help='Remove author data')
    parser.add_argument('-w', '--waypoints', action='store_true', help='Waypoints')
    parser.add_argument('-o', '--output', metavar='F', type=str, default='clean.gpx', help='Output GPX file')
    args, gpx_files = parser.parse_known_args()

    extensions: bool = args.extensions
    time: bool = args.time
    elevations: bool = args.elevations
    routes: bool = args.routes
    tracks: bool = args.tracks
    author: bool = args.author
    waypoints: bool = args.waypoints
    output = args.output

    for gpx_file in gpx_files:
        with open(gpx_file) as f:
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

    if not output:
        output = common.prefix_filename(gpx_file, "clean_")

    with open(output, "w") as f:
        f.write(g.to_xml())

