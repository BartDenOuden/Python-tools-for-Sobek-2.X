"""Class for reading resultaten_laatste_tijdstap from Sobek HIS files

Bart den Ouden Wateradvies,
4 january 2014
8 juni 2019: omgezet naar Python 3, verbeterd en uitgebreid
januari 2025: refactoring, verbeteringen
"""

# TODO: pad valideren

from dataclasses import dataclass
import datetime
import os
from pathlib import Path
import re
import struct
import sys
from typing import Optional

from openpyxl import Workbook, load_workbook
import xlsxwriter

import resultsat

# Format HIS-file:
# 1. Header string 160 tekens
# 2. aantal parameters, integer 4 bytes
# 3. aantal locaties, integer 4 bytes
# 4. locaties [volgnummer en string Id, integer 4 bytes gevolgd door string 20 tekens, ... aantal locaties]
# 5. tijdstap en berekeningsresultaten, integer 4 bytes aantal tijdstappen, floats 4 bytes, gegroepeerd per locaties (node1par1, node1par2, node1par3, node2par1, node2par2, node2par3, ...)


MAX_COLUMNS_EXCEL = 16_384
MAX_ROWS_EXCEL = 1_048_576
DATA_START_ROW_EXCEL = 2  # First row is headers

NM_CASELIST = 'CASELIST.CMT'

MAXBYTES = 20_000_000    # maximum number of bytes that is read form HIS file at once

POS_N_PAR = 160
POS_N_ID = 164
POS_STR_PAR = 168
POS_STR_DATE = 124
POS_STR_TIME = 135

# lengtes van delen van een HIS-file voor het instellen van het leespunt van het bestand
LEN_HEADER = 160
LEN_N_PAR_N_ID = 8
LEN_STR_PAR = 20
LEN_ID = 24
LEN_VALUE = 4
LEN_STR_DATE = 10
LEN_STR_TIME = 8
LEN_STR_DATE_TIME_TIMESTEP = 36


def _convert_bytestring_to_float(bytestring) -> float:
    [flt] = struct.unpack('f', bytestring)
    return flt


@dataclass
class SobekResults:
    """
    Dataclass for containing data read from Sobek .his-files.
    """
    timestamps: list[datetime.datetime]
    data: dict[str, list[float]]

    def write_to_excel(
            self,
            path: str | Path,
            sheet_name: str,
            overwrite: bool
    ) -> None:
        """
        Writes the data in this class to an excelfile. The first column contains the timestamps, the following columns
        the data for every id.

        Args:
            path (str or pathlib.Path): path Excelfile
            sheet_name (str): name of the sheet to write to
            overwrite (bool): if true: removes the sheet with the given name if it already exists

        Returns:
            None

        Raises:
            TODO
        """

        if isinstance(path, str):
            path = Path(path)

        # Validate; path:
        if not path.parent.exists():
            raise ValueError(f'Directory does not exist ({path.parent.resolve()})')
        # Validate; length sheetname:
        if len(sheet_name) > 31:  # Excel's limit
            raise ValueError("Sheet name cannot exceed 31 characters")
        # Validate; check if sheet can accommodate all IDs (plus timestamp column):
        if len(self.data) + 1 >= MAX_COLUMNS_EXCEL:
            raise ValueError(f'Too many IDs ({len(self.data)}) to fit in Excel sheet (max columns: {MAX_COLUMNS_EXCEL})')
        # Validate; number of rows (accounting for header row):
        if len(self.timestamps) + DATA_START_ROW_EXCEL - 1 > MAX_ROWS_EXCEL:
            raise ValueError(
                f'Too many timestamps ({len(self.timestamps)}) to fit in Excel sheet. '
                f'Maximum allowed: {MAX_ROWS_EXCEL - DATA_START_ROW_EXCEL + 1}'
            )

        if path.exists():
            # Load existing workbook:
            wb = load_workbook(path)
        else:
            # Create new workbook:
            wb = Workbook()
            # Remove default sheet:
            default_sheet = wb.active
            wb.remove(default_sheet)

        if sheet_name in wb.sheetnames:
            if overwrite:
                # Remove existing sheet:
                del wb[sheet_name]
            else:
                raise PermissionError(f'Cannot write resultaten_laatste_tijdstap to excelfile: sheet "{sheet_name}" allready exists and "overwrite" = {overwrite}. ')
        ws = wb.create_sheet(sheet_name)

        # Write timestamps in first column:
        ws.cell(row=1, column=1, value='Timestamp')  # header
        for row, timestamp in enumerate(self.timestamps, start=DATA_START_ROW_EXCEL):
            ws.cell(row=row, column=1, value=timestamp)

        # Write data to columns:
        for col, (id_, values) in enumerate(self.data.items(), start=DATA_START_ROW_EXCEL):
            # Write header (Sobek id):
            ws.cell(row=1, column=col, value=id_)
            # Write values:
            for row, value in enumerate(values, start=DATA_START_ROW_EXCEL):
                ws.cell(row=row, column=col, value=value)

        # Save the workbook:
        wb.save(path)

    def write_to_excel_xlsxwriter(
            self,
            path: str | Path,
            sheet_name: str
    ) -> None:
        """
        Faster alternative to the method write_to_excel(). It is about three times faster.

        NB: This method has the limitation that it cannot write to an existing excelfile!

        Writes the data in this class to an Excel file using XlsxWriter. The first column contains
        the timestamps, the following columns contain the data for every id.

        Args:
            path (str or pathlib.Path): path to Excel file (will be created/overwritten)
            sheet_name (str): name of the sheet to write to

        Returns:
            None

        Raises:
            ValueError: If directory doesn't exist, sheet name too long, or data exceeds Excel limits
        """
        if isinstance(path, str):
            path = Path(path)

        # Validate path:
        if not path.parent.exists():
            raise ValueError(f'Directory does not exist ({path.parent.resolve()})')

        # Validate length of sheet name:
        if len(sheet_name) > 31:  # Excel's limit
            raise ValueError("Sheet name cannot exceed 31 characters")

        # Validate number of columns:
        if len(self.data) + 1 >= MAX_COLUMNS_EXCEL:
            raise ValueError(
                f'Too many IDs ({len(self.data)}) to fit in Excel sheet '
                f'(max columns: {MAX_COLUMNS_EXCEL})'
            )

        # Validate number of rows:
        if len(self.timestamps) + DATA_START_ROW_EXCEL - 1 > MAX_ROWS_EXCEL:
            raise ValueError(
                f'Too many timestamps ({len(self.timestamps)}) to fit in Excel sheet. '
                f'Maximum allowed: {MAX_ROWS_EXCEL - DATA_START_ROW_EXCEL + 1}'
            )

        # Create workbook and worksheet:
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet(sheet_name)

        # Create datetime format
        datetime_format = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss'})

        # Write timestamps in first column:
        worksheet.write(0, 0, 'Timestamp')  # header
        for row, timestamp in enumerate(self.timestamps, start=DATA_START_ROW_EXCEL - 1):
            worksheet.write(row, 0, timestamp, datetime_format)

        # Write data to columns:
        for col, (id_, values) in enumerate(self.data.items(), start=1):
            # Write header (Sobek id):
            worksheet.write(0, col, id_)
            # Write values:
            for row, value in enumerate(values, start=DATA_START_ROW_EXCEL - 1):
                worksheet.write(row, col, value)

        workbook.close()


class SobekDataFetcher:
    """
    Class for reading Sobek resultaten_laatste_tijdstap from his files.
    """

    def __init__(
            self,
            dir_sobek: str | Path,
            project: str,
            case: str,
            name_hisfile: str,
            report: bool = True
    ):
        """
        Args:
            dir_sobek:
                path of the Sobek dir. Example: "C:\\Sobek213\\"".
            project:
                name of the directory of the Sobek project. Example: "Rijn.lit".
            case:
                name of the Sobek case. Example: "case 13: BB=23, weir 3 raised"
            name_hisfile:
                name of the Sobek HIS-file. Example: 'CALCPNT.HIS'. The module resultsat.py contains constants for
                convenience.
            report:
                if true this method prints an overview of the .his-file.
        """

        if isinstance(dir_sobek, str):
            dir_sobek = Path(dir_sobek)

        # Validate:
        if not dir_sobek.exists():
            raise ValueError(f"Sobek directory not found. Path: {dir_sobek}")
        dir_project = dir_sobek / project
        if not dir_project.exists():
            raise ValueError(f"Project directory not found. Path: {dir_project}")

        self.dir_sobek = dir_sobek
        self.project = project
        self.case = case
        self.name_hisfile = name_hisfile

        # The order of creating the self variables below is critical!
        self.path_hisfile = self._get_path_his_file()  # path is validated by method

        self.id_count = self._get_id_count()
        self.parameter_count = self._get_parameter_count()
        self.timestamp_count = self._count_timestamps()

        self.ids = self._get_ids_list()
        self.ids_dict = self._get_ids_dict()

        self.t0 = self._get_t0_datetime()
        self.timestep_computation_sec = self._get_timestep_computation_sec()
        self.timestamps = self._get_timestamps_list_datetime()
        self.timestep_data_sec = self._get_timestep_data_sec()

        if report: self.print_overview_of_hisfile()

    def __str__(self):

        report = "\n----------------------------------------------------------------------------------------------------\n" + \
                 " Overview his file (file containing Sobek resultaten_laatste_tijdstap)\n" + \
                 "----------------------------------------------------------------------------------------------------\n" + \
                 f"         Sobek Project: {self.project}\n" + \
                 f"                  Case: {self.case}\n" + \
                 f"            Results at: {self._get_results_at_str()} ({self.name_hisfile})\n" + \
                 "\n" + \
                 f"  Number of timestamps: {self.timestamp_count}\n" + \
                 f"       First timestamp: {self.timestamps[0]}\n" + \
                 f"        Last timestamp: {self.timestamps[-1]}\n" + \
                 "\n" + \
                 f"  Timestep calculation: {self.timestep_computation_sec} sec\n" + \
                 f"      Timestep resultaten_laatste_tijdstap: {self.timestep_data_sec} sec\n" + \
                 "\n" + \
                 f"   Number of locations: {self.id_count}\n" + \
                 self._get_parameter_report_str()

        return report

    def _get_results_at_str(self):
        res_at_dict = {
            resultsat.RESULTS_AT_NODES: 'nodes',
            resultsat.RESULTS_AT_STRUCTURES: 'structures',
            resultsat.RESULTS_AT_REACHSEGMENTS: 'reach segments'
        }
        if self.name_hisfile in res_at_dict.keys():
            return res_at_dict[self.name_hisfile]
        else:
            return self.name_hisfile

    def _get_parameter_report_str(self):
        parameters = self.get_parameters()
        parameter_table = ''
        for i, param in enumerate(parameters):
            parameter_table += f"{i :>21} | {param}\n"

        report = "----------------------------------------------------------------------------------------------------\n" + \
                 f" Parameters in {self.name_hisfile}:\n" + \
                 "                Index | Description\n" + \
                 parameter_table + \
                 "----------------------------------------------------------------------------------------------------\n"

        return report

    def _get_dict_sobek_cases(self) -> dict[str, str]:
        path_caselist = self.dir_sobek / self.project / NM_CASELIST
        if not path_caselist.exists():
            raise FileExistsError(f"File Sobek CASELIST not found. Path: {path_caselist}")
        with open(path_caselist) as caselist:
            str_caselist = caselist.read()

        pattern = r"([0-9]*) '(.*)'"
        match = re.findall(pattern, str_caselist)
        case_dict = {case_name: case_dir for case_dir, case_name in match}

        return case_dict

    def _get_path_his_file(self) -> Path:
        case_dict = self._get_dict_sobek_cases()
        if self.case not in case_dict.keys():
            raise ValueError(f"Sobek Case '{self.case}' not present in CASELIST. ")
        case_dir = case_dict[self.case]
        path_his_file = self.dir_sobek / self.project / case_dir / self.name_hisfile

        if not path_his_file.exists():
            raise FileExistsError(f".his-file not found (file containing Sobek calculation resultaten_laatste_tijdstap). Path: {path_his_file}")

        return path_his_file

    def _print_header_his_file(self):
        with open(self.path_hisfile, 'rb') as hisfile:
            hisfile.seek(0)  # stelt leespositie in
            first_thousend_characters = hisfile.read(2000).decode('latin-1', errors='ignore')
        print(first_thousend_characters)

    def print_overview_of_hisfile(self):
        print(self.__str__())

    def _get_id_count(self):
        with open(self.path_hisfile, 'rb') as hisfile:
            hisfile.seek(POS_N_ID)  # stelt leespositie in op punt waar een integer van 4 bytes staat
            nr_ids = int.from_bytes(hisfile.read(LEN_VALUE), byteorder=sys.byteorder)
        return nr_ids

    def _get_parameter_count(self):
        with open(self.path_hisfile, 'rb') as hisfile:
            hisfile.seek(POS_N_PAR)
            parameter_count = int.from_bytes(hisfile.read(LEN_VALUE), byteorder=sys.byteorder)
        return parameter_count

    def _count_timestamps(self):

        with open(self.path_hisfile, 'rb') as hisfile:
            hisfile.seek(0, os.SEEK_END)
            size_timesteps = int(hisfile.tell())         #aantal bytes in bestand
            size_timesteps = size_timesteps - (LEN_HEADER + LEN_N_PAR_N_ID + LEN_STR_PAR * self.parameter_count + LEN_ID * self.id_count) # aantal bytes bestand minus bytes voor header en IDS = bytes voor waarden parameters
            size_timestep = self.parameter_count * self.id_count * LEN_VALUE + LEN_VALUE          #aantal bytes per tijdstap = aantal parameters * aantal Ids (nodes) * 4 bytes + tijd (4 bytes)

        return size_timesteps // size_timestep         #aantal tijdstappen
        
    def _get_t0_datetime(self):
        """ returns a time and date object containing the start date and time of the HIS file """
        with open(self.path_hisfile, 'rb') as hisfile:
            hisfile.seek(POS_STR_DATE)
            str_date = hisfile.read(LEN_STR_DATE).decode("latin-1")

            hisfile.seek(POS_STR_TIME)
            str_time = hisfile.read(LEN_STR_TIME).decode("latin-1")

        lst_date = str_date.split(sep=".")
        lst_time = str_time.split(sep=':')

        start_date_and_time = datetime.datetime(
            int(lst_date[0]),
            int(lst_date[1]),
            int(lst_date[2]),
            int(lst_time[0]),
            int(lst_time[1]),
            int(lst_time[2])
        )

        return start_date_and_time

    def _get_timestep_computation_sec(self):

        with open(self.path_hisfile, 'rb') as hisfile:
            hisfile.seek(POS_STR_DATE)
            str_date = hisfile.read(LEN_STR_DATE_TIME_TIMESTEP).decode("latin-1")

        pattern = r"([0-9]+)s\)"
        timestep = int(re.findall(pattern, str_date)[0])

        return timestep

    def _get_timestep_data_sec(self):
        if len(self.timestamps)>1:
            timestep = self.timestamps[1] - self.timestamps[0]
            return timestep.seconds
        else:
            return -999

    def _get_timestamps_list_datetime(self) -> list[datetime.datetime]:

        pos_start_data = LEN_HEADER + LEN_N_PAR_N_ID + LEN_STR_PAR * self.parameter_count + LEN_ID * self.id_count  # aantal bytes bestand minus bytes voor header en IDS = bytes voor waarden parameters
        bytes_per_timestep = self.id_count * self.parameter_count * LEN_VALUE + LEN_VALUE

        # read timesteps from HIS file and write to list
        lst_timestamps = []
        with open(self.path_hisfile, 'rb') as hisfile:
            for timestep_int in range(self.timestamp_count):
                pos = pos_start_data + timestep_int * bytes_per_timestep
                hisfile.seek(pos)
                nr_of_timesteps = int.from_bytes(hisfile.read(LEN_VALUE), byteorder='little')
                seconds = nr_of_timesteps * self.timestep_computation_sec
                timestamp = self.t0 + datetime.timedelta(seconds=seconds)
                lst_timestamps.append(timestamp)

        return lst_timestamps

    def get_timestamps_dict(self):
        dict_timestamps = {date: index for index, date in enumerate(self.timestamps)}
        return dict_timestamps

    def _get_ids_as_bytes(self) -> bytes:

        pos = LEN_HEADER + LEN_N_PAR_N_ID + LEN_STR_PAR * self.parameter_count
        length = self.id_count * LEN_ID
        with open(self.path_hisfile, 'rb') as hisfile:
            hisfile.seek(pos)
            bytes_ids = hisfile.read(length)  # reeks van Ids; 4 bytes integer gevolgd door string van 20 tekens
        return bytes_ids

    def _get_ids_list(self) -> list[str]:
        bytes_ids = self._get_ids_as_bytes()

        # read id's from string and write them to list (leaves out the 4 byte integers!)
        lst_str_ids = []
        for i in range(self.id_count):
            lst_str_ids.append(bytes_ids[i * LEN_ID + LEN_VALUE : i * LEN_ID + LEN_ID].rstrip().decode("latin-1"))

        return lst_str_ids

    def _get_ids_dict(self) -> dict[str, int] :
        bytes_ids = self._get_ids_as_bytes()

        # read id's from string and write them to list (leaves out the 4 byte integers!)
        lst_str_ids = []
        for i in range(self.id_count):
            lst_str_ids.append(bytes_ids[i * LEN_ID + LEN_VALUE: i * LEN_ID + LEN_ID].rstrip().decode("latin-1"))
        dict_ids = {id_:index for index, id_ in enumerate(lst_str_ids)}

        return dict_ids

    def print_parameters(self):
        print(self._get_parameter_report_str())

    def get_parameters(self) -> list[str]:

        with open(self.path_hisfile, 'rb') as hisfile:
            hisfile.seek(POS_STR_PAR)
            list_par = []
            for i in range(self.parameter_count):
                list_par.append(hisfile.read(LEN_STR_PAR).decode('latin-1'))

        return list_par

    def get_data(
            self,
            index_parameter_sobek_data: int,
            ids_sobek: Optional[list[str]] = None,
            start: Optional[int | datetime.datetime] = None,
            end: Optional[int | datetime.datetime] = None
    ) -> SobekResults:
        """
        Retrieves data from the Sobek HIS file for the specified PARAMETER, IDs, and time range.

        Only the PARAMETER index_parameter_sobek_data is mandatory; when PARAMETER values are ommited the
        maximum amount of data is returned.

        Args:
            index_parameter_sobek_data (int):
                Index of the PARAMETER to retrieve from the Sobek data.
                Use print_parameters() for a description of the parameters present in the .his-file and their indices.
            ids_sobek (Optional[list[str]], optional):
                List of Sobek IDs to retrieve data for.
                Defaults to None. If None, retrieves data for all IDs in the .his-file.
            start (Optional[int | datetime.datetime], optional):
                End of the timeperiod to be retrieved.
                Can be either an index or a datetime object.
                Defaults to None. If None, start is the first timestamp in the .his-file.
            end (Optional[int | datetime.datetime], optional):
                End of the timeperiod to be retrieved. This end timestamp is INCLUDED in the resultaten_laatste_tijdstap.
                Can be either an index or a datetime object.
                Defaults to None. If None, ends at the last timestamp in the .his-file.

        Returns:
            SobekResults: A dataclass containing:
                - timestamps: List of datetime objects for the retrieved period
                - data: Dictionary mapping Sobek IDs to lists of float values

        Raises:
            ValueError: If any specified IDs don't exist in the HIS file
            ValueError: If start or end index exceeds the number of timesteps
            ValueError: If end index is not larger than start index
            ValueError: If provided datetime for start/end doesn't match any timestamp
            TypeError: If start/end arguments are neither datetime nor int
        """

        # Determine ids_sobek:
        if ids_sobek is None: ids_sobek = self.ids
        # Validation ids_sobek:
        ids_not_in_his_file = []
        for id_ in ids_sobek:
            if id_ not in self.ids_dict: ids_not_in_his_file.append(id_)
        if len(ids_not_in_his_file) > 0:
            message = ''
            for id_ in ids_not_in_his_file:
                message = message + id_ + ', '
            message = "Id's not existing in HIS file: " + message
            raise Exception(message)

        # Determine index_start:
        if start is None:
            index_start = 0
        elif isinstance(start, datetime.datetime):
            try:
                index_start = self.timestamps.index(start)
            except ValueError:
                raise ValueError(f'Given start {start} is not present in timestamps hisfile. ')
        elif isinstance(start, int):
            index_start = start
        else:
            raise TypeError(f'Value for PARAMETER start must be datetime.datetime or int. Given: {type(start)}')

        # Determine index_end:
        if end is None:
            index_end = self.timestamp_count - 1
        elif isinstance(end, datetime.datetime):
            try:
                index_end = self.timestamps.index(end)
            except ValueError:
                raise ValueError(f'Given end {end} is not present in timestamps hisfile. ')
        elif isinstance(end, int):
            index_end = end
        else:
            raise TypeError(f'Value for PARAMETER end must be datetime.datetime or int. Given: {type(end)}')

        # Validate index_start and index_end:
        if index_start > self.timestamp_count - 1:
            raise ValueError(f"Given index_start ({index_start}) exceeds number of timesteps in his file ({self.timestamp_count}). ")
        if index_end > self.timestamp_count - 1:
            raise ValueError(f"Given index_end ({index_end}) exceeds number of timesteps in his file ({self.timestamp_count}). ")
        if index_end < index_start:
            raise ValueError(f"'index_end' ({index_end}) must be larger than 'index_start' ({index_start}). ")

        # Read data from Sobek .his-file:
        data = {}
        pos_start_data = LEN_HEADER + LEN_N_PAR_N_ID + LEN_STR_PAR * self.parameter_count + LEN_ID * self.id_count + index_parameter_sobek_data * LEN_VALUE  # aantal bytes bestand minus bytes voor header en IDS = bytes voor waarden parameters
        with open(self.path_hisfile, 'rb') as hisfile:
            for id_ in ids_sobek:
                lst_data_values_for_sobek_id = []
                id_index = self.ids_dict[id_]
                for index_timestep in range(index_start, index_end + 1):
                    pos =((index_timestep * (self.id_count * self.parameter_count + 1)) + 1 + id_index * self.parameter_count) * LEN_VALUE
                    hisfile.seek(pos_start_data + pos)
                    data_value = _convert_bytestring_to_float(hisfile.read(LEN_VALUE))
                    lst_data_values_for_sobek_id.append(data_value)
                data[id_] = lst_data_values_for_sobek_id

        results = SobekResults(
            timestamps=self.timestamps[index_start: index_end + 1],
            data=data
        )

        return results
