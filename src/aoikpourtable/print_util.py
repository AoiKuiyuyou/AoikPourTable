# coding: utf-8
#
from __future__ import absolute_import

import sys


#
def print_stderr(msg):
    # Write message
    sys.stderr.write(msg)

    # Write newline
    sys.stderr.write('\n')
