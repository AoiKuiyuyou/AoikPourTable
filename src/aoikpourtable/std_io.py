# coding: utf-8
#
from __future__ import absolute_import

import sys


#
def stdin_factory(uri, query, args, cmd_args):
    """
    Input factory that produces "sys.stdin" object.

    @param uri: Input URI.

    @param query: Input query.

    @param args: Input arguments string.

    @param cmd_args: Command arguments dict.

    @return: "sys.stdin" object.
    """
    # Return "sys.stdin" object
    return sys.stdin


#
def stdout_factory(uri, query, args, cmd_args):
    """
    Output factory that produces an output function that writes to
    "sys.stdout".

    @param uri: Output URI.

    @param query: Output query.

    @param args: Output arguments string.

    @param cmd_args: Command arguments dict.

    @return: An output function that writes to "sys.stdout".
    """
    # Create output function
    def output_func(rows):
        # For each row
        for row in rows:
            # Get row string
            row_str = repr(row)

            # Write row string
            sys.stdout.write(row_str)

            # If row string is not empty and last character is not newline
            if row_str and row_str[-1] != '\n':
                # Write newline
                sys.stdout.write('\n')

    # Return output function
    return output_func
