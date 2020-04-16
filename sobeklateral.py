"""
This module contains functions to generate Sobek timeseries for lateral discharges from data in an Excel file.
Sobek is a program for making models of water systems.

REQUIRED FORMAT DATA IN SPREADSHEET
- date en time in first column as Excel date-type
- first row: header or first row of data (choose "headers = True"/ "headers = False" accordingly)

Run as file: fill out variables in this module under " VARIABLES...".

Required Python version: 3.6 or higher.
Required third party modules: see import statements.

Bart den Ouden Wateradvies, oktober 2019
bart@bartdenoudenwateradvies.nl
"""

# built in modules:
import re
import sys

# third party modules:
import xlrd

# TODO: make constants of all strings that represent parts of a Sobek LATERAL.DAT file and place them on top.
# TODO: write unit tests

__author__ = "Bart den Ouden, Bart den Ouden Wateradvies"


MIN_PYTHON = (3, 6)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


# CONSTANTS
LINEAR = 'linear'
BLOCK = 'block'
Q = 'q'
H = 'h'

def return_data_from_xls(xls_path, sheet_name, column_values, headers):

    COLUMN_DATETIME = 0

    column_values -= 1

    workbook = xlrd.open_workbook(filename=xls_path)
    sheet = workbook.sheet_by_name(sheet_name)
    first_row_values = 0
    if headers:
        first_row_values = 1
    last_row = sheet.nrows

    lst_datetime = sheet.col_values(COLUMN_DATETIME, start_rowx=first_row_values, end_rowx=last_row)
    lst_datetime = [xlrd.xldate_as_datetime(date_number, workbook.datemode) for date_number in lst_datetime]

    lst_values = sheet.col_values(column_values, start_rowx=first_row_values, end_rowx=last_row)

    return (lst_datetime, lst_values)


def _return_str_header_data_block(node_id, sobek_function_type):

    STR_FUNCTION_TYPE_LINEAR = "PDIN 0 0 '' pdin"
    STR_FUNCTION_TYPE_BLOCK = "PDIN 1 0 '' pdin"

    if sobek_function_type == LINEAR:
        str_function_type = STR_FUNCTION_TYPE_LINEAR
    else:
        str_function_type = STR_FUNCTION_TYPE_BLOCK

    return f"FLNO id '{node_id}' sc 0 lt 0 dc lt 1 0 0 {str_function_type}\nTBLE\n"


def _return_str_data_block(lst_datetime, lst_values):

    def _return_str_date_value(date, value):
        str_date_time = date.strftime("%Y/%m/%d;%H:%M:%S")
        return f"'{str_date_time}' {value} <"


    data_block = ""
    for date, value in zip(lst_datetime, lst_values):
        data_block += _return_str_date_value(date, value) + '\n'

    return data_block


def return_str_sobek_lateral_q_timeseries_from_excel(node_id,
                                                     sobek_function_type,
                                                     xls_path,
                                                     sheet_name,
                                                     column_values,
                                                     headers=True,
                                                     ):
    """Returns a Sobek boundary from a time series in an Excel file.

    REQUIRED FORMAT DATA IN SPREADSHEET
    - date en time in first column as Excel date-type
    - first row: header or first row of data (choose "headers=True"/ "headers=False" accordingly)

    Arguments:
        column_values: Number of the column containing Q or H values in the Excel sheet.
                       '1' equals the first column in the sheet!

    """

    lst_datetime, lst_values = return_data_from_xls(xls_path, sheet_name, column_values, headers)
    str_sobek_time_series_bnd = _return_str_header_data_block(node_id, sobek_function_type)
    str_sobek_time_series_bnd += _return_str_data_block(lst_datetime, lst_values)
    str_sobek_time_series_bnd += "tble flno\n"

    return str_sobek_time_series_bnd

def return_str_sobek_lateral_q_timeseries_from_lists(node_id,
                                                     sobek_function_type,
                                                     lst_datetime,
                                                     lst_values
                                                     ):
    """Returns a Sobek boundary from two lists.
    arguments:
    node_id: string id boundary node
    sobek_function_type: LINEAR ('linear') or BLOCK ('block')
    lst_datetime: list of datetime.datetime objects corresponding to the boundary values
    lst_values: boundary values as a list of floats
    """

    str_sobek_time_series_bnd = _return_str_header_data_block(node_id, sobek_function_type)
    str_sobek_time_series_bnd += _return_str_data_block(lst_datetime, lst_values)
    str_sobek_time_series_bnd += "tble flno\n"

    return str_sobek_time_series_bnd

def add_or_replace_timeseries_lateral_file(path_lat_file, str_sobek_lateral_q_timeseries):
    """Adds a time series to a BOUNDARY.DAT file, or replaces it if a boundary for the node already exists."""

    # Get part containing Sobek node id from string (data) that has to be added to BOUNDARY.DAT:
    pattern = r"(FLNO id '[^']*')"
    first_part_replace_pattern = re.match(pattern, str_sobek_lateral_q_timeseries).group()

    # New pattern for removing existing (if any) boundary data for Sobek node id in BOUNDARY.DAT:
    # (Operators are 'greedy'; they take as much text as possible. The ? after an operator makes it 'non-greedy'.)
    pattern = first_part_replace_pattern + r".*?flno\n"

    with open(path_lat_file, 'r') as f:
        str_data_bnd_file = f.read()
        # remove all boundary definitions for boundary node:
        str_data_bnd_file = re.sub(pattern, '', str_data_bnd_file, flags=re.DOTALL)
        str_data_bnd_file += str_sobek_lateral_q_timeseries

    with open(path_lat_file, 'w') as f:
        f.write(str_data_bnd_file)
