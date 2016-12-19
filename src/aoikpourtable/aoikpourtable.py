# coding: utf-8
from __future__ import absolute_import

import os.path
import sys


#
def pythonpath_init():
    """
    Prepare "sys.path" for import resolution.
    """
    # Get this file's directory path
    my_dir = os.path.dirname(os.path.abspath(__file__))

    # Remove some paths from "sys.path" to avoid unexpected import resolution.

    # For each path in the list
    for path in ['', '.', my_dir]:
        # If the path is in "sys.path"
        if path in sys.path:
            # Remove the path from "sys.path"
            sys.path.remove(path)

    # Add "src" directory to "sys.path".
    # This is the import resolution we want.

    # Get "src" directory path
    src_dir = os.path.dirname(my_dir)

    # If "src" directory path is not in "sys.path"
    if src_dir not in sys.path:
        # Add "src" directory to "sys.path"
        sys.path.insert(0, src_dir)


#
def main(args=None):
    """
    Program entry function.
    Call "pythonpath_init" to prepare "sys.path" for import resolution.
    Then call "main_wrap" to implement functionality.

    @param args: Command arguments list.

    @return: Exit code.
    """
    # Prepare "sys.path" for import resolution
    pythonpath_init()

    # Import "main_wrap" function
    from aoikpourtable.main import main_wrap

    # Call "main_wrap" function
    return main_wrap(args=args)


# If this module is the main module
if __name__ == '__main__':
    # Call "main" function
    sys.exit(main())
