# coding: utf-8
#
from __future__ import absolute_import

from datetime import datetime
import sys

from .uri_util import uri_get_path
from .uri_util import uri_query_to_args


#
IS_PY2 = (sys.version_info[0] == 2)


#
def count_lines(uri, query, args, cmd_args):
    """
    Count factory that counts lines of a file.

    @param uri: Input URI.

    @param query: Input query.

    @param args: Input arguments string.

    @param cmd_args: Command arguments dict.

    @return: Count info dict, in the format:
    {
        'count': ...,
        'duration': ...,
        'rate': ...,
    }
    """
    # Get starting row ordinal
    start_row_ordinal = cmd_args['start_row_ordinal']

    # Get ending row ordinal
    end_row_ordinal = cmd_args['end_row_ordinal']

    # Parse query to arguments dict
    args_dict = uri_query_to_args(args, flatten=True)

    # Get input file encoding
    encoding = args_dict.pop('encoding', 'utf-8')

    # If input URI is "-"
    if uri == '-':
        # Use stdin as input file
        input_file = sys.stdin
    else:
        # Get input file path from input URI
        input_file_path = uri_get_path(uri)

        # Open input file
        if IS_PY2:
            input_file = open(input_file_path, mode='r')
        else:
            input_file = open(input_file_path, mode='r', encoding=encoding)

    # Count duration
    count_dura = None

    # Count rate
    count_rate = None

    # If input file is stdin
    if input_file is sys.stdin:
        # Stdin data can only be read once.
        # We can not count in this case.
        # Set count to None.
        count = None

    # If input file is not stdin
    else:
        # Get starting time
        count_start_time = datetime.utcnow()

        # Count value
        count = 0

        # Get ending row ordinal inclusive
        if end_row_ordinal:
            end_row_ordinal_inclusive = end_row_ordinal - 1
        else:
            end_row_ordinal_inclusive = None

        # For each line in input file
        for line in input_file:
            # Increment count
            count += 1

            # If count reaches ending row ordinal
            if end_row_ordinal_inclusive \
                    and count >= end_row_ordinal_inclusive:
                # Stop counting
                break

        # Set seek pointer to file beginning
        input_file.seek(0)

        # Get ending time
        count_end_time = datetime.utcnow()

        # Get duration
        count_dura = \
            (count_end_time - count_start_time).total_seconds()

        # If duration is not zero
        if count_dura:
            # Get rate
            count_rate = count / count_dura
        else:
            # Set rate to None
            count_rate = None

    # If staring row ordinal is not None
    if start_row_ordinal:
        # If count is not None
        if count is not None:
            # Deduct from count
            count -= start_row_ordinal - 1

            # If count is LT 0
            if count < 0:
                # Set count to 0
                count = 0

    # Return count info dict
    return {
        'count': count,
        'duration': count_dura,
        'rate': count_rate,
    }
