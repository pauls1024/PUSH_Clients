#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Checks any files on your computer to see if they are
older than a specified age. The check will fail if
the file is too old or if the file goes missing.
"""

import os
import time
from . import _utils


########################## USER DEFINED VARIABLES #############################

# Each key is the path to the file and its name, then each value is another
# dictionary with days, hours, and minutes old you expect the file to be.

filenames = {
    "/path/to/file1": {"days": 0, "hours": 0, "minutes": 0},
    "/path/to/file2": {"days": 0, "hours": 0, "minutes": 0}
}

###############################################################################


def get_file_status(files):
    """
    """

    all_status = {}

    now = time.time()

    for f, times in files.items():
        day_to_sec = times['days'] * 86400
        hr_to_sec = times['hours'] * 3600
        min_to_sec = times['minutes'] * 60
        total_sec = day_to_sec + hr_to_sec + min_to_sec

        file_exists = os.path.isfile(f)

        if file_exists:
            st = os.stat(f)
            mtime = st.st_mtime

            file_age = now - mtime

            if file_age > total_sec:
                all_status.update({f: 0})
            else:
                all_status.update({f: 1})
        else:
            all_status.update({f: 0})

    return all_status


def main(system, logger):
    """
    Returns a 1 or 0 for each file in the user-defined
    list that passes or fails.
    """

    files_status = get_file_status(filenames)

    return _utils.report(files_status)
