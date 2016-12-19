# coding: utf-8
#
from __future__ import absolute_import


#
def input_factory(uri, query, args, cmd_args):
    """
    Input factory that produces an infinite empty string generator.

    @param uri: Input URI.

    @param query: Input query.

    @param args: Input arguments string.

    @param cmd_args: Command arguments dict.

    @return: An infinite empty string generator.
    """
    # Create generator factory
    def empty_generator_factory():
        while True:
            yield ''

    # Create generator
    empty_generator = empty_generator_factory()

    # Return generator
    return empty_generator


#
def output_factory(uri, query, args, cmd_args):
    """
    Output factory that produces a do-nothing output function.

    @param uri: Output URI.

    @param query: Output query.

    @param args: Output arguments string.

    @param cmd_args: Command arguments dict.

    @return: A do-nothing output function.
    """
    # Create output function
    def output_func(rows):
        pass

    # Return output function
    return output_func
