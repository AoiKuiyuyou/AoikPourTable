# coding: utf-8
#
from __future__ import absolute_import

from decimal import Decimal
import sys


#
IS_PY2 = (sys.version_info[0] == 2)


#
def convert_factory(args, cmd_args):
    """
    Convert factory that returns a list of field convert functions according to
    convert arguments string.

    @param args: Convert arguments string.

    @param cmd_args: Command arguments dict.

    @return: A list of field convert functions.
    """
    # Map convert argument to field convert function
    convert_arg_to_field_func = {
        '': None,
        's': None,
        'i': int,
        'f': float,
        'd': Decimal,
    }

    # Strip convert arguments string
    convert_args = args.strip()

    # If convert arguments string is empty
    if not convert_args:
        # Set field convert functions list to None
        field_func_s = None
    else:
        # Field convert functions list
        field_func_s = []

        # For each convert argument
        for convert_arg in convert_args.split(','):
            # Strip convert argument
            convert_arg = convert_arg.strip()

            # Get field function
            field_func = convert_arg_to_field_func.get(convert_arg, False)

            # If field function is not found
            if field_func is False:
                # Create a string encoding function,
                # using convert argument as encoding.
                def field_func(x, convert_encoding=convert_arg):
                    if IS_PY2:
                        return x
                    else:
                        return x.encode(convert_encoding)

            # Add field function to list
            field_func_s.append(field_func)

    # Return field convert functions list
    return field_func_s
