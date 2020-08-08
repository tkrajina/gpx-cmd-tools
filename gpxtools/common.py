import gpxpy.gpx as gpx
import os.path as path
import re

from typing import *

def parse_duration(s: str) -> int:
    all = re.findall("(\d+)(\w+)", s)
    if not all:
        return -1
    i = int(all[0][0])
    unit = all[0][1]
    if unit == "s":
        return i
    elif unit == "m":
        return i * 60 * 1000
    elif unit == "h":
        return i * 60 * 60 * 1000
    else:
        return -1

def clean_extensions(g: gpx.GPX) -> None:
    g.extensions = []
    for rte in g.routes:
        rte.extensions = []
        for pt in rte.points:
            pt.extensions = []
    for t in g.tracks:
        t.extensions = []
        for s in t.segments:
            s.extensions = []
            for p in s.points:
                p.extensions = []

def prefix_filename(fn: str, prefix: str) -> str:
    dir, fn = path.split(fn)
    return path.join(dir, prefix + fn)