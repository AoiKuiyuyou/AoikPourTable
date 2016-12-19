# coding: utf-8
#
from __future__ import absolute_import

import csv
import sys

from .print_util import print_stderr
from .uri_util import uri_query_to_args


#
IS_PY2 = (sys.version_info[0] == 2)


# Map quoting mode names to int values
_quoting_map = {
    'QUOTE_ALL': csv.QUOTE_ALL,
    'QUOTE_MINIMAL': csv.QUOTE_MINIMAL,
    'QUOTE_NONNUMERIC': csv.QUOTE_NONNUMERIC,
    'QUOTE_NONE': csv.QUOTE_NONE,
}


#
def csv_input_factory(uri, query, args, cmd_args):
    """
    Input factory that produces a CSV reader.

    @param uri: Input URI.

    @param query: Input query.

    @param args: Input arguments string.

    @param cmd_args: Command arguments dict.

    @return: A CSV reader.
    """
    # Print message
    print_stderr('{:20}{}'.format('Input:', uri))

    # Get arguments dict
    args_dict = uri_query_to_args(args, flatten=True)

    # Get encoding
    encoding = args_dict.pop('encoding', 'utf-8')

    # Print message
    print_stderr('{:20}{}'.format('encoding:', encoding))

    # Get line terminator
    lineterminator = args_dict.pop('lineterminator', '\n')

    # Print message
    print_stderr('{:20}{}'.format('lineterminator:', repr(lineterminator)))

    # Get delimiter
    delimiter = args_dict.pop('delimiter', ',')

    # Print message
    print_stderr('{:20}{}'.format('delimiter:', repr(delimiter)))

    # Get quote character
    quotechar = args_dict.pop('quotechar', '"')

    # Print message
    print_stderr('{:20}{}'.format('quotechar', repr(quotechar)))

    # Get quoting mode
    quoting = args_dict.pop('quoting', 'QUOTE_ALL')

    # Print message
    print_stderr('{:20}{}'.format('quoting', quoting))

    # Get quoting mode int
    quoting_int = _quoting_map[quoting]

    # Open input file
    if IS_PY2:
        input_file = open(uri, mode='r')
    else:
        input_file = open(uri, mode='r', encoding=encoding)

    # Get CSV reader
    csv_reader = csv.reader(
        input_file,
        lineterminator=lineterminator,
        delimiter=delimiter,
        quotechar=quotechar,
        quoting=quoting_int)

    # Return CSV reader
    return csv_reader


#
def csv_output_factory(uri, query, args, cmd_args):
    """
    Output factory that produces an output function that writes to a file.

    @param uri: Output URI.

    @param query: Output query.

    @param args: Output arguments string.

    @param cmd_args: Command arguments dict.

    @return: An output function that writes to a file.
    """
    # Print message
    print_stderr('{:20}{}'.format('Output', uri))

    # Get arguments dict
    args_dict = uri_query_to_args(args, flatten=True)

    # Get encoding
    encoding = args_dict.pop('encoding', 'utf-8')

    # Print message
    print_stderr('{:20}{}'.format('encoding:', encoding))

    # Get line terminator
    lineterminator = args_dict.pop('lineterminator', '\n')

    # Print message
    print_stderr('{:20}{}'.format('lineterminator:', repr(lineterminator)))

    # Get delimiter
    delimiter = args_dict.pop('delimiter', ',')

    # Print message
    print_stderr('{:20}{}'.format('delimiter:', repr(delimiter)))

    # Get quote character
    quotechar = args_dict.pop('quotechar', '"')

    # Print message
    print_stderr('{:20}{}'.format('quotechar', repr(quotechar)))

    # Get quoting mode
    quoting = args_dict.pop('quoting', 'QUOTE_ALL')

    # Print message
    print_stderr('{:20}{}'.format('quoting', quoting))

    # Get quoting mode int
    quoting_int = _quoting_map[quoting]

    # Open output file
    if IS_PY2:
        output_file = open(uri, mode='w')
    else:
        output_file = open(uri, mode='w', encoding=encoding)

    # Get CSV writer
    csv_writer = csv.writer(
        output_file,
        lineterminator=lineterminator,
        delimiter=delimiter,
        quotechar=quotechar,
        quoting=quoting_int)

    # Create output function
    def output_func(rows):
        csv_writer.writerows(rows)

    # Return output function
    return output_func
