# coding: utf-8
#
from __future__ import absolute_import

from contextlib import contextmanager
import itertools

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import text

from .print_util import print_stderr
from .uri_util import uri_query_to_args


#
def make_table(
        table_name,
        column_name_s,
        schema_name=None,
        metadata=None):
    """
    Make a SQLAlchemy Table object.

    @param table_name: Table name.

    @param column_name_s: Column name list.

    @param schema_name: Schema name.

    @param metadata: Metadata object.

    @return: Table object.
    """
    # If metadata object is not given
    if not metadata:
        # Create one
        metadata = MetaData()

    # Create "Table" object
    table = Table(table_name, metadata, schema=schema_name)

    # For each column name
    for column_name in column_name_s:
        # Create "Column" object
        column = Column(column_name, String(), nullable=True)

        # Add "Column" object to "Table" object
        table.append_column(column)

    # Return "Table" object
    return table


#
def select_factory(uri, query, args, cmd_args):
    """
    Input factory that produces an infinite empty string generator.

    @param uri: Input URI.

    @param query: Input query.

    @param args: Input arguments string.

    @param cmd_args: Command arguments dict.

    @return: An infinite empty string generator.
    """
    # Print message
    print_stderr('{:20}'.format('Input:', uri))

    # Get engine
    engine = create_engine(uri)

    # Get arguments dict
    args_dict = uri_query_to_args(args, flatten=True)

    # Whether support range control
    support_range_control = False

    # If input query is specified
    if query:
        # Compile query to query object
        stmt_obj = text(query)

        # Query object made by "text" does not support "offset" and "limit"
        # methods.
        support_range_control = False
    else:
        # Get schema name
        schema_name = args_dict.pop('schema', None)

        # Get table name
        table_name = args_dict.pop('table', None)

        # If table name is not specified
        if not table_name:
            # Raise exception
            raise ValueError(
                '"table" argument is not specified in input arguments: {}'\
                .format(args))

        # Print message
        print_stderr('{:20}{}'.format('Schema:', schema_name))

        print_stderr('{:20}{}'.format('Table:', table_name))

        # Get MetaData object
        metadata = MetaData(engine)

        # Get columns argument
        dst_columns_text = args_dict.pop('columns', None)

        # If columns argument is not specified
        if not dst_columns_text:
            raise ValueError(
                '"columns" argument is not specified in input arguments: {}'\
                .format(args))

        # Split columns argument into column names
        dst_column_name_s = dst_columns_text.split(',')

        # Get table object
        table = make_table(
            table_name=table_name,
            column_name_s=dst_column_name_s,
            schema_name=schema_name,
            metadata=metadata,
        )

        # Get query object
        stmt_obj = table.select()

        # Get starting row index
        start_row_index = cmd_args['start_row_index']

        # Get starting ending row difference
        start_end_row_diff = cmd_args['start_end_row_diff']

        # If starting row index is specified
        if start_row_index is not None:
            # Add "offset" to statement
            stmt_obj = stmt_obj.offset(start_row_index)

        # If starting ending row difference is specified
        if start_end_row_diff is not None:
            # Add "limit" to statement
            stmt_obj = stmt_obj.limit(start_end_row_diff)

        # Tell program framework that range control has been done
        support_range_control = True

    # Print message
    print_stderr('{:20}{}'.format('Statement:', stmt_obj))

    # Open database connection
    connec = engine.connect()

    # Get repeat argument
    repeat_text = args_dict.pop('repeat', '1')

    # Get repeat int
    repeat_int = int(repeat_text)

    # Create generator factory
    def resultset_generator_factory():
        # Set initial repeat count to 0
        repeat_count = 0

        # If repeat int is -1 (meaning infinite),
        # or repeat count is LT repeat int
        while repeat_int == -1 or repeat_count < repeat_int:
            # Increment repeat count
            repeat_count += 1

            # Execute statement
            resultset = connec.execute(stmt_obj)

            # Yield result set
            yield resultset

    # Create generator
    resultset_generator = resultset_generator_factory()

    # Create context factory
    @contextmanager
    def input_context_factory():
        # Get row iterator
        row_iter = itertools.chain.from_iterable(resultset_generator)

        # Yield row iterator
        yield row_iter

        # Close database connection
        connec.close()

    # Create context object
    input_context = input_context_factory()

    # Get factory info dict
    factory_info = {
        'input_obj': input_context,
        'support_range_control': support_range_control,
    }

    # Return factory info dict
    return factory_info


#
def insert_factory(uri, query, args, cmd_args):
    """
    Output factory that produces an insert function context object.

    @param uri: Output URI.

    @param query: Output query.

    @param args: Output arguments string.

    @param cmd_args: Command arguments dict.

    @return: An insert function context object.
    """
    # Print message
    print_stderr('{:20}{}'.format('Output:', uri))

    # Get arguments dict
    args_dict = uri_query_to_args(args, flatten=True)

    # Get schema name
    schema_name = args_dict.pop('schema', None)

    # Get table name
    table_name = args_dict.pop('table', None)

    # If table name is not specified
    if not table_name:
        # Raise exception
        raise ValueError(
            '"table" argument is not specified in output arguments: {}'\
            .format(args))

    # Get columns argument
    dst_columns_text = args_dict.pop('columns', None)

    # If columns argument is not specified
    if not dst_columns_text:
        # Raise exception
        raise ValueError(
            '"columns" argument is not specified in output arguments: {}'\
            .format(args))

    # Split columns argument into column names
    dst_column_name_s = dst_columns_text.split(',')

    # Get engine
    engine = create_engine(uri)

    # Get MetaData object
    metadata = MetaData(engine)

    # Get table object
    table = make_table(
        table_name=table_name,
        column_name_s=dst_column_name_s,
        schema_name=schema_name,
        metadata=metadata,
    )

    # Print message
    print_stderr('{:20}{}'.format('Schema:', schema_name))

    print_stderr('{:20}{}'.format('Table:', table_name))

    # Get statement object
    insert_obj = table.insert()

    # Print message
    print_stderr('{:20}{}'.format('Statement:', insert_obj))

    # Open database connection
    connec = engine.connect()

    # Create output function
    def insert_func(rows):
        # Begin transaction
        transac = connec.begin()

        # Execute statement
        connec.execute(insert_obj.values(rows))

        # Commit transaction
        transac.commit()

    # Create context factory
    @contextmanager
    def output_context_factory():
        # Yield insert function
        yield insert_func

        # Close database connection
        connec.close()

    # Create context object
    output_context = output_context_factory()

    # Return context object
    return output_context
