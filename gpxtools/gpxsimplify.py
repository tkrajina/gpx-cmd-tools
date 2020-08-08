"""
Command line utility to extract basic statistics from gpx file(s)
"""

import sys as mod_sys
import logging as mod_logging
import math as mod_math
import argparse as mod_argparse
from . import common

import gpxpy as mod_gpxpy
import gpxpy.gpx as mod_gpx

from typing import *

def main() -> None:
    parser = mod_argparse.ArgumentParser(description='Simplify tracks using the Ramer-Douglas-Peucker algorithm')
    parser.add_argument('-d', '--distance', type=float, default=10, help='Max distance')
    parser.add_argument('gpx_files', metavar='gpx', type=str, default='', nargs=1, help='GPX file')

    args = parser.parse_args()
    gpx_file = args.gpx_files[0]
    distance = args.distance

    with open(gpx_file) as f:
        g = mod_gpxpy.parse(f)
    
    g.simplify(max_distance=distance)

    with open(common.prefix_filename(gpx_file, "_simplified"), "w") as f:
        f.write(g.to_xml())