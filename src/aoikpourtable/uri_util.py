# coding: utf-8
#
from __future__ import absolute_import

try:
    # Python 3
    from urllib import parse as _urlparser
except ImportError:
    # Python 2
    import urlparse as _urlparser


#
def uri_query_to_args(query, flatten=False):
    """
    Parse query string to arguments dict.

    @param query: A query string.

    @param flatten: Flatten each argument value from a list to a single value.

    @return: An arguments dict.
    """
    # Parse query to arguments dict
    args_dict = _urlparser.parse_qs(query)

    # If flatten is True
    if flatten:
        # For each key
        for key in args_dict.keys():
            # Use the first value in the value list as the flat value
            args_dict[key] = args_dict[key][0]

    # Return arguments dict
    return args_dict


#
def uri_get_path(uri):
    """
    Get path part from a URI.

    @param uri: A URI.

    @return: Path part of the URI.
    """
    # Split the URI into parts
    url_part_s = _urlparser.urlsplit(uri)

    # Return the path part
    return url_part_s[2]
