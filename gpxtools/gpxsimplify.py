"""
Command line utility to extract basic statistics from gpx file(s)
"""

import sys as mod_sys
import logging as mod_logging
import math as mod_math
import argparse as mod_argparse
from . import common
# import gpxpy.gpx as gpxpy
import gpxpy as gpx_parser
import glob

from typing import *

def main() -> None:
    parser = mod_argparse.ArgumentParser(description='Simplify tracks using the Ramer-Douglas-Peucker algorithm')
    parser.add_argument('-d', '--distance', type=float, default=10, help='Max distance')
    # parser.add_argument('gpx_files', metavar='gpx', type=str, default='', nargs=1, help='GPX file')
    parser.add_argument('-o', '--output', type=str, help='Output GPX file')
    parser.add_argument('-f', '--folder', type=str, help='Folder containing files')
    parser.add_argument('-p', '--prefix', type=str, default = 'simplified_', help='Prefix of output files')

    args, gpx_files = parser.parse_known_args()
    distance = args.distance
    folder = args.folder
    output = args.output
    prefix = args.prefix

    if folder:
        filelist = glob.glob(folder + '*.gpx')
        gpx_files.extend(filelist)
    
    for gpx_file in gpx_files:

        with open(gpx_file, encoding='utf-8') as f:
            g = gpx_parser.parse(f)
                
            g.simplify(max_distance=distance)

            if len(gpx_files) > 1 or (not output):
                out_gpx = common.prefix_filename(gpx_file, prefix)

            with open(out_gpx, "w", encoding='utf-8') as f:
                f.write(g.to_xml())

                print(f'Simplified {gpx_file} => {out_gpx}')

