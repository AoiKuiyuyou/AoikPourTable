# coding: utf-8
#
from __future__ import absolute_import

from argparse import ArgumentParser
from argparse import ArgumentTypeError
from contextlib import contextmanager
from datetime import datetime
import sys
import traceback

from .aoikimportutil import load_obj
from .print_util import print_stderr


#
def int_gt0(text):
    """
    ArgumentParser's type function that converts "text" to an integer greater
    than 0.

    @param text: The text to convert to integer.

    @return: An integer greater than 0.
    """
    try:
        # Convert to int
        int_value = int(text)

        # Ensure greater than 0
        assert int_value > 0
    except Exception:
        # Raise an exception to notify ArgumentParser
        raise ArgumentTypeError(
            '"%s" is not an integer greater than 0.' % text)

    # Return the valid value
    return int_value


#
def int_ge0(text):
    """
    ArgumentParser's type function that converts "text" to an integer greater
    than or equal to 0.

    @param text: The text to convert to integer.

    @return: An integer greater than or equal to 0.
    """
    try:
        # Convert to int
        int_value = int(text)

        # Ensure greater than or equal to 0
        assert int_value >= 0
    except Exception:
        # Raise an exception to notify ArgumentParser
        raise ArgumentTypeError(
            '"%s" is not an integer greater than or equal to 0.' % text)

    # Return the valid value
    return int_value


#
def get_arg_parser():
    """
    Create an "ArgumentParser" instance for "main" function.

    @return: An "ArgumentParser" instance.
    """
    # Create an "ArgumentParser" instance
    arg_parser = ArgumentParser()

    # Specify arguments

    #
    arg_parser.add_argument(
        '--input',
        dest='input_uri',
        default='',
        metavar='URI',
        help='Set input URI to be passed to input factory.',
    )

    #
    arg_parser.add_argument(
        '--input-query',
        dest='input_query',
        default='',
        metavar='QUERY',
        help='Set input query to be passed to input factory.',
    )

    #
    arg_parser.add_argument(
        '--input-args',
        dest='input_args',
        default='',
        metavar='ARGS',
        help='Set input arguments to be passed to input factory.',
    )

    #
    arg_parser.add_argument(
        '--input-factory',
        dest='input_factory_uri',
        default='aoikpourtable.empty_io::input_factory',
        metavar='URI',
        help='Set input factory URI.',
    )

    #
    arg_parser.add_argument(
        '--output',
        dest='output_uri',
        default='',
        metavar='URI',
        help='Set output URI to be passed to output factory',
    )

    #
    arg_parser.add_argument(
        '--output-args',
        dest='output_args',
        default='',
        metavar='ARGS',
        help='Set output arguments to be passed to input factory.',
    )

    #
    arg_parser.add_argument(
        '--output-query',
        dest='output_query',
        default='',
        metavar='QUERY',
        help='Set output query to be passed to output factory.',
    )

    #
    arg_parser.add_argument(
        '--output-factory',
        dest='output_factory_uri',
        default='aoikpourtable.empty_io::output_factory',
        metavar='URI',
        help='Set output factory URI.',
    )

    #
    arg_parser.add_argument(
        '--count-args',
        dest='count_args',
        default='',
        metavar='ARGS',
        help='Set count arguments to be passed to count factory.',
    )

    #
    arg_parser.add_argument(
        '--count-factory',
        dest='count_factory_uri',
        default=None,
        metavar='URI',
        help='Set count factory URI or a fixed count value.',
    )

    #
    arg_parser.add_argument(
        '--only-columns',
        dest='only_columns_text',
        default=None,
        metavar='M,N,O',
        help='Only these input columns are fed to output. One-based.',
    )

    #
    arg_parser.add_argument(
        '--convert-args',
        dest='convert_args',
        default='',
        metavar='ARGS',
        help='Set convert arguments to be passed to convert factory.',
    )

    #
    arg_parser.add_argument(
        '--convert-factory',
        dest='convert_factory_uri',
        default='aoikpourtable.convert_io::convert_factory',
        metavar='URI',
        help=('Set convert factory URI. '
              'Default is "aoikpourtable.convert_io::convert_factory".'),
    )

    #
    arg_parser.add_argument(
        '--start-row',
        dest='start_row',
        type=int_ge0,
        default=None,
        metavar='N',
        help='Starting row index, zero-based, inclusive.',
    )

    #
    arg_parser.add_argument(
        '--end-row',
        dest='end_row',
        type=int_ge0,
        default=None,
        metavar='N',
        help='Ending row index, zero-based, exclusive.',
    )

    #
    arg_parser.add_argument(
        '--limit-rows',
        dest='limit_rows',
        type=int_ge0,
        default=None,
        metavar='N',
        help='Limit rows.',
    )

    #
    arg_parser.add_argument(
        '--batch-size',
        dest='batch_size',
        type=int_gt0,
        default=1000,
        metavar='N',
        help='Accumulate N rows for one batch of processing. Default is 1000.',
    )

    # Return an "ArgumentParser" instance
    return arg_parser


#
def get_progress_info(
        row_count,
        last_row_count,
        last_start_time,
        total_row_count,
        total_start_time):
    """
    Get progress info.

    @param row_count: Processed rows count.

    @param last_row_count: Last round processed rows count.

    @param last_start_time: Last round insert time.

    @param total_row_count: Total rows count.

    @param total_start_time: Total start time.

    @return A tuple of 4 elements: (row_count, now_time, total_rate, msg):
    "row_count": "last_row_count" of next call.
    "now_time": "last_start_time" of next call.
    "total_rate": Total processing rate.
    "msg": Output message.
    """
    # Get current time
    now_time = datetime.utcnow()

    # Calculate duration spent this round
    round_dura = (now_time - last_start_time).total_seconds()

    # Calculate rows inserted this round
    round_row_count = row_count - last_row_count

    # If round duration is not zero
    if round_dura:
        # Calculate round rate
        round_rate = round_row_count / round_dura
    else:
        # Set round rate to None
        round_rate = None

    # Calculate total duration
    total_dura = (now_time - total_start_time).total_seconds()

    # If total duration is not zero
    if total_dura:
        # Calculate total rate
        total_rate = row_count / total_dura
    else:
        # Set total rate to None
        total_rate = None

    # If total row count and total rate are not zero
    if total_row_count and total_rate:
        # Calculate need duration
        need_dura = \
            (total_row_count - row_count) / total_rate
    else:
        # Set need duration to None
        need_dura = None

    # Create message
    msg = '+{} ={}'.format(
        round_row_count,
        row_count,
        round_rate,
        total_rate)

    # If total rate is not None
    if total_rate is not None:
        # Add total rate to message
        msg += ' ={:.0f}/s'.format(total_rate)

    # If round rate is not None
    if round_rate is not None:
        # Add round rate to message
        msg += ' +{:.0f}/s'.format(round_rate)
    else:
        # Add round rate to message
        msg += ' +?/s'

    # Add total duration to message
    msg = '{}, past {:.0f}s'.format(msg, total_dura)

    # If need duration is not None
    if need_dura is not None:
        # Add need duration and total duration to message
        msg = '{}, need {:.0f}s, total {:.0f}s'.format(
            msg, need_dura, total_dura + need_dura)

    # Return information.
    # "row_count" is "last_row_count" of next call.
    # "now_time" is "last_start_time" of next call.
    return row_count, now_time, total_rate, msg


#
def decide_frac_len(value):
    """
    Decide a float value's fraction part's display width.

    @param value: The float value.

    @return: The float value's fraction part's display width.
    """
    # Decide fraction part's display width
    if value == 0:
        frac_len = 0
    elif value < 0.001:
        frac_len = 6
    elif value < 0.01:
        frac_len = 5
    elif value < 0.1:
        frac_len = 4
    elif value < 1:
        frac_len = 3
    elif value < 10:
        frac_len = 2
    else:
        frac_len = 0

    # Return fraction part's display width
    return frac_len


#
def main_core(args=None, step_info_set_func=None):
    """
    The main function that implements the core functionality.

    @param args: Command arguments list.

    @param step_info_set_func: A function to set step information for the upper
    context.

    @return: Exit code.
    """
    # Ensure this argument is given
    assert step_info_set_func is not None

    # Set step info
    step_info_set_func(title='Parse arguments')

    # Get arguments parser
    arg_parser = get_arg_parser()

    # Parse arguments
    args = arg_parser.parse_args(args)

    # Set step info
    step_info_set_func(title='Get starting row index')

    # Get starting row index, zero-based, inclusive
    start_row_index = args.start_row

    # Get starting row ordinal, one-based.
    # The reason to use one-based ordinal is at "5LUCR" we can write
    # "if start_row_ordinal", which handles index zero well.

    # Set step info
    step_info_set_func(title='Get starting row ordinal')

    # If starting row index is specified
    if start_row_index is not None:
        # Set starting row ordinal
        start_row_ordinal = start_row_index + 1
    else:
        # Set starting row ordinal to None
        start_row_ordinal = None

    # Set step info
    step_info_set_func(title='Get ending row index')

    # Get ending row index, zero-based, exclusive
    end_row_index = args.end_row

    # Set step info
    step_info_set_func(title='Get limit rows')

    # Get limit rows
    limit_rows = args.limit_rows

    # Set step info
    step_info_set_func(title='Get ending row index limit')

    # If limit rows is specified
    if limit_rows is not None:
        # If starting row index is specified
        if start_row_index is not None:
            # Use starting row index plus limit rows as ending row index limit
            end_row_index_limit = start_row_index + limit_rows
        else:
            # Use limit rows as ending row index limit
            end_row_index_limit = limit_rows

        # If ending row index is specified
        if end_row_index is not None:
            # If ending row index is greater than ending row index limit
            if end_row_index > end_row_index_limit:
                # Use ending row index limit as ending row index
                end_row_index = end_row_index_limit
        else:
            # Use ending row index limit as ending row index
            end_row_index = end_row_index_limit

    # Get ending row ordinal, one-based.
    # The reason to use one-based ordinal is at "76TUC" we can write
    # "if end_row_ordinal", which handles index zero well.

    # Set step info
    step_info_set_func(title='Get ending row ordinal')

    # If ending row index is specified
    if end_row_index is not None:
        # Set ending row ordinal
        end_row_ordinal = end_row_index + 1
    else:
        # Set ending row ordinal to None
        end_row_ordinal = None

    # Set step info
    step_info_set_func(title='Get starting ending row index difference')

    # The starting ending row index difference
    start_end_row_diff = None

    # If ending row index is specified
    if end_row_index is not None:
        # Use it as starting ending row index difference
        start_end_row_diff = end_row_index

        # If starting row index is specified
        if start_row_index is not None:
            # Deduct it from from the difference
            start_end_row_diff -= start_row_index

        # Ensure starting ending row index difference is >= 0
        assert start_end_row_diff >= 0, start_end_row_diff

    # Set step info
    step_info_set_func(title='Get batch size')

    # Get batch size
    batch_size = args.batch_size

    assert batch_size > 0

    # Set step info
    step_info_set_func(title='Get command arguments to be passed to factory')

    # Get command arguments to be passed to factory
    cmd_args = {
        'start_row_index': start_row_index,
        'start_row_ordinal': start_row_ordinal,
        'end_row_index': end_row_index,
        'end_row_ordinal': end_row_ordinal,
        'start_end_row_diff': start_end_row_diff,
        'batch_size': batch_size,
    }

    # Set step info
    step_info_set_func(title='Get only columns')

    # Get only-column argument text
    only_columns_text = args.only_columns_text

    # If only-column argument is not specified
    if not only_columns_text:
        # Set only-column indices to None
        only_column_index_s = None
    else:
        # The only-column indices list
        only_column_index_s = []

        # Split only-column argument into index texts
        only_column_index_text_s = only_columns_text.strip().split(',')

        # For each index text
        for only_column_index_text in only_column_index_text_s:
            # Convert to int
            only_column_index = int(only_column_index_text)

            # Convert from 1-based to 0-based
            only_column_index -= 1

            # Add to list
            only_column_index_s.append(only_column_index)

    # Set step info
    step_info_set_func(title='Get convert factory')

    # Get convert arguments
    convert_args = args.convert_args

    # Get convert factory URI
    convert_factory_uri = args.convert_factory_uri

    # Get convert factory
    convert_mod, convert_factory = load_obj(
        convert_factory_uri, mod_name='aoikpourtable._convert', retn_mod=True)

    # Set step info
    step_info_set_func(title='Get convert function')

    # Get convert function
    convert_func = convert_factory(args=convert_args, cmd_args=cmd_args)

    # Flag to say the convert function is a list
    convert_func_is_list = False

    # Flag to say the convert function is a function
    convert_func_is_func = False

    # If the convert function is a list or tuple instance
    if isinstance(convert_func, (list, tuple)):
        # Set the flag to say the convert function is a list
        convert_func_is_list = True

    # If the convert function is not None
    elif convert_func is not None:
        # Set the flag to say the convert function is a function
        convert_func_is_func = True

    # If the convert function is None
    else:
        pass

    # Set step info
    step_info_set_func(title='Get input factory')

    # Get input URI
    input_uri = args.input_uri

    # Get input factory URI
    input_factory_uri = args.input_factory_uri

    # Get input factory
    input_mod, input_factory = load_obj(
        input_factory_uri, mod_name='aoikpourtable._input', retn_mod=True)

    # Get input arguments
    input_args = args.input_args

    # Get input query
    input_query = args.input_query

    # Set step info
    step_info_set_func(title='Get input object')

    # Call input factory
    input_obj = input_factory(
        input_uri, input_query, args=input_args, cmd_args=cmd_args)

    # Whether range control is enabled at 3NWP4.
    enable_range_control = True

    # If input object is a dict instance
    if isinstance(input_obj, dict):
        # Get the info dict
        input_factory_info = input_obj

        # Get the input object
        input_obj = input_factory_info['input_obj']

        # If the input factory not supports range control,
        # Enable range control at 3NWP4.
        enable_range_control = not input_factory_info.get(
            'support_range_control', False)

    # Set step info
    step_info_set_func(title='Get input context')

    # If input object is a context object
    if hasattr(input_obj, '__enter__') \
            and hasattr(input_obj, '__exit__'):
        # Use it as input context
        input_ctx = input_obj

    # If input object is not a context object
    else:
        # Create a context factory
        @contextmanager
        def input_context_manager():
            # Yield the input object as the input iterator
            yield input_obj

        # Use the context factory to create an input context
        input_ctx = input_context_manager()

    # Set step info
    step_info_set_func(title='Get count factory')

    # Get count factory URI
    count_factory_uri = args.count_factory_uri

    # If count factory URI is not specified
    if count_factory_uri is None:
        # Set total row count to None
        total_row_count = None

    # If count factory URI is an integer
    elif count_factory_uri.isdigit():
        # The total row count is given, use it directly,
        # do not do the actual counting.
        total_row_count_text = count_factory_uri

        # Parse text to int
        total_row_count = int(total_row_count_text)

        # Ensure it is > 0
        assert total_row_count > 0

    else:
        # Get count arguments
        count_args = args.count_args

        # Get count factory
        count_mod, count_factory = load_obj(
            count_factory_uri, mod_name='aoikpourtable._count', retn_mod=True)

        # Get count function
        count_func = count_factory(
            input_uri,
            input_query,
            args=count_args,
            cmd_args=cmd_args)

        # If the count function is a dict
        if isinstance(count_func, dict):
            # Use as count info
            count_info = count_func

        # If the count function is a function
        else:
            # Call the count function to get count info
            count_info = count_func(
                input_uri,
                args=count_args,
                cmd_args=cmd_args)

        # Get total row count
        total_row_count = count_info['count']

        # Get count duration
        count_rows_dura = count_info['duration'] or 0.0

        # Get count rate
        count_rows_rate = count_info['rate'] or None

        #
        if total_row_count is not None:
            # Get message format
            msg_fmt = '{} row{}, {:.%sf}s' \
                % (decide_frac_len(count_rows_dura), )

            # Get message
            msg = msg_fmt.format(
                total_row_count,
                '' if total_row_count <= 1 else 's',
                count_rows_dura)

            # If counting rate is not None
            if count_rows_rate is not None:
                # Add counting rate to message
                msg = '{:20}{}, {:.0f} rows/s'.format(
                    'Count:', msg, count_rows_rate)
            else:
                msg = '{:20}{}, ? rows/s'.format(
                    'Count:', msg)

            # Print message
            print_stderr(msg)

    # Set step info
    step_info_set_func(title='Limit total row count')

    # Ensure starting row ordinal and ending row ordinal are valid
    if start_row_ordinal and end_row_ordinal:
        assert start_row_ordinal <= end_row_ordinal, \
            (start_row_ordinal, end_row_ordinal)

    # If ending row ordinal is not None
    if end_row_ordinal:
        # If total row count is None
        if total_row_count is None:
            # Use ending row ordinal as total row count
            total_row_count = end_row_ordinal
        # If total row count is not None
        else:
            # If total row count overflows ending row ordinal
            if total_row_count > end_row_ordinal:
                # Limit total row count to ending row ordinal
                total_row_count = end_row_ordinal

    # If total row count is not None or zero
    if total_row_count:
        # Ensure total row count is > 0
        assert total_row_count > 0, total_row_count

    # Set step info
    step_info_set_func(title='Get output factory')

    # Get output factory URI
    output_factory_uri = args.output_factory_uri

    # Get output factory
    output_mod, output_factory = load_obj(
        output_factory_uri, mod_name='aoikpourtable._output', retn_mod=True)

    # Get output arguments
    output_args = args.output_args

    # Get output query
    output_query = args.output_query

    # Set step info
    step_info_set_func(title='Get output object')

    # Get output object
    output_object = output_factory(
        args.output_uri, output_query, args=output_args, cmd_args=cmd_args)

    # Set step info
    step_info_set_func(title='Get output context')

    # If output object is a context object
    if hasattr(output_object, '__enter__') \
            and hasattr(output_object, '__exit__'):
        # Use it as output context
        output_ctx = output_object

    # If output object is not a context object
    else:
        # Create a context factory
        @contextmanager
        def output_context_manager():
            # Yield the output object as the output function
            yield output_object

        # Use the context factory to create an output context
        output_ctx = output_context_manager()

    # Set step info
    step_info_set_func(title='Process data')

    # Current row ordinal
    row_ordinal = 0

    # Processed row count
    row_count = 0

    # Last batch processed row count
    last_row_count = 0

    # Starting time
    total_start_time = datetime.utcnow()

    # Last batch starting time
    last_start_time = total_start_time

    # Total processing rate
    total_rate = None

    # Input object returns None to mean "ignore current row".
    IGNORE_OBJ = None

    # Input object returns None.__class__ to mean "stop processing"
    STOP_OBJ = None.__class__

    #
    with input_ctx as input_iter, output_ctx as output_func:
        # Rows accumulated for one batch
        row_s = []

        # For each row in the input iterator
        for row in input_iter:
            # Get the current row ordinal
            row_ordinal += 1

            # 3NWP4
            # If range control is enabled
            if enable_range_control:
                # 5LUCR
                # If the current row ordinal is smaller than starting row
                # ordinal.
                if start_row_ordinal and row_ordinal < start_row_ordinal:
                    # Ignore the current row
                    continue

                # 76TUC
                # If the current row ordinal is greater than or equal to
                # ending row ordinal.
                if end_row_ordinal and row_ordinal >= end_row_ordinal:
                    # Stop processing
                    break

            # Increment batch row count
            row_count += 1

            # If only-column indices are specified
            if only_column_index_s:
                # The new row
                new_row = []

                # Extract columns from the old row
                for only_column_index in only_column_index_s:
                    new_row.append(row[only_column_index])

                # Override the old row
                row = new_row

            # If convert function is a list
            if convert_func_is_list:
                # The new row
                new_row = []

                # For each field in the row
                for field_index, field in enumerate(row):
                    # Get field convert function
                    filed_func = convert_func[field_index]

                    # If field convert function is None
                    if not filed_func:
                        # Add the field to new row
                        new_row.append(field)
                    # If field convert function is not None
                    else:
                        # Convert the field
                        new_field = filed_func(field)

                        # Add the field to new row
                        new_row.append(new_field)

                # Override the old row
                row = new_row

            # If convert function is a function
            elif convert_func_is_func:
                # Convert the row
                row = convert_func(row)

            # If the current row should be ignored
            if row is IGNORE_OBJ:
                # Ignore
                continue

            # If the processing should be stopped
            elif row is STOP_OBJ:
                # Stop
                break

            # Add the row to rows accumulated for one batch
            row_s.append(row)

            # If batch size is met
            if row_count % batch_size == 0:
                # Output the rows
                output_func(row_s)

                # Empty the accumulated list of rows
                row_s[:] = []

                # Update progress info
                last_row_count, last_start_time, total_rate, msg = \
                    get_progress_info(
                        row_count=row_count,
                        last_row_count=last_row_count,
                        last_start_time=last_start_time,
                        total_row_count=total_row_count,
                        total_start_time=total_start_time)

                # Print message
                print_stderr(msg)

        # If there are rows left after the loop above
        if row_count > last_row_count:
            # Output the rows
            output_func(row_s)

            # Empty the accumulated list of rows
            row_s[:] = []

            # Update progress info
            last_row_count, last_start_time, total_rate, msg = \
                get_progress_info(
                    row_count=row_count,
                    last_row_count=last_row_count,
                    last_start_time=last_start_time,
                    total_row_count=total_row_count,
                    total_start_time=total_start_time)

            # Print message
            print_stderr(msg)

        # Get ending time
        total_end_time = datetime.utcnow()

        # Get past duration
        past_dura = (total_end_time - total_start_time).total_seconds()

        # Get past duration fraction width
        past_dura_frac_len = decide_frac_len(past_dura)

        # Get message format
        msg_fmt = 'Total: {} row{}, {:.%sf}s' % (past_dura_frac_len, )

        # Get message
        msg = msg_fmt.format(
            row_count,
            '' if row_count <= 1 else 's',
            past_dura)

        # If total rate is not None
        if total_rate is not None:
            # Add total rate to message
            msg += ', {:.0f} rows/s'.format(total_rate)
        else:
            # Add total rate to message
            msg += ', ? rows/s'

        # Print message
        print_stderr(msg)

    # Return without error
    return 0


#
def main_wrap(args=None):
    """
    The main function that provides exception handling.
    Call "main_core" to implement the core functionality.

    @param args: Command arguments list.

    @return: Exit code.
    """
    # A dict that contains step info
    step_info = {
        'title': '',
        'exit_code': 0
    }

    # A function that updates step info
    def step_info_set_func(title=None, exit_code=None):
        # If title is not None
        if title is not None:
            # Update title
            step_info['title'] = title

        # If exit code is not None
        if exit_code is not None:
            # Update exit code
            step_info['exit_code'] = exit_code

    #
    try:
        # Call "main_core" to implement the core functionality
        return main_core(args=args, step_info_set_func=step_info_set_func)
    # Catch keyboard interrupt
    except KeyboardInterrupt:
        # Return without error
        return 0
    # Catch other exceptions
    except Exception:
        # Get step title
        step_title = step_info.get('title', '')

        # Get traceback
        traceback_msg = ''.join(traceback.format_exception(*sys.exc_info()))

        # If step title is not empty
        if step_title:
            # Get message
            msg = '# Error: {}\n---\n{}---\n'.format(step_title, traceback_msg)
        else:
            # Get message
            msg = '# Error\n---\n{}---\n'.format(traceback_msg)

        # Output message
        sys.stderr.write(msg)

        # Get exit code
        exit_code = step_info.get('exit_code', 1)

        # Exit
        return exit_code
