"""Class for reading data from Sobek HIS files

Bart den Ouden Wateradvies,
4 january 2014
8 juni 2019 (omgezet naar Python 3, verbeterd en uitgebreid)"""

import os
import sys
import re
import struct
import datetime

import resultsat

# Format HIS-file:
# 1. Header string 160 tekens
# 2. aantal parameters, integer 4 bytes
# 3. aantal locaties, integer 4 bytes
# 4. locaties [volgnummer en string Id, integer 4 bytes gevolgd door string 20 tekens, ... aantal locaties]
# 5. tijdstap en berekeningsresultaten, integer 4 bytes aantal tijdstappen, floats 4 bytes, gegroepeerd per locaties (node1par1, node1par2, node1par3, node2par1, node2par2, node2par3, ...)


class SobekDataFetcher(object):
    """
    Class for reading Sobek data from his files.
    """

    NM_CASELIST = 'CASELIST.CMT'

    MAXBYTES = 20000000    # maximum number of bytes that is read form HIS file at once

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

    def __init__(self, str_sob_dir, str_lit, str_case, results_at):
        """
        :param str_sob_dir:
            path of the Sobek dir. Example: "C:\\Sobek213\\"".
        :param str_lit:
            name of the directory of the Sobek project. Example: "Rijn.lit".
        :param str_case:
            name of the Sobek case. Example: "case 13: BB=23, weir 3 raised"
        :param results_at:
            name of the Sobek HIS-file. Example: 'CALCPNT.HIS'. The module resultsat.py contains constants for
            convenience.
        """
        self.str_sob_dir = str_sob_dir
        self.str_lit = str_lit
        self.str_case = str_case
        self.str_results_at = results_at

    def __str__(self):
        timestamps = self.get_timestamps_list_datetime()

        report = "\n________________________________________________________\n" + \
                 " Overview Sobek data fetcher / his file\n" + \
                 "________________________________________________________\n" + \
                 "\n" + \
                 f"         Sobek Project: {self.str_lit}\n" + \
                 f"                  Case: {self.str_case}\n" + \
                 f"            Results at: {self._get_results_at_str()}\n" + \
                 "\n" + \
                 f"  Number of timestamps: {len(self.get_timestamps_dict())}\n" + \
                 f"       First timestamp: {timestamps[0]}\n" + \
                 f"        Last timestamp: {timestamps[-1]}\n" + \
                 "\n" + \
                 f"  Timestep calculation: {self.get_timestep_computation_sec()} sec\n" + \
                 f"         Timestep data: {self.get_timestep_data_sec()} sec\n" + \
                 "\n" + \
                 f"   Number of locations: {self.count_ids()}\n" + \
                 self._get_parameter_report_str()

        return report

    def _get_results_at_str(self):
        res_at_dict = {resultsat.RESULTS_AT_NODES: 'nodes',
                       resultsat.RESULTS_AT_STRUCTURES: 'structures',
                       resultsat.RESULTS_AT_REACHSEGMENTS: 'reach segments'}
        if self.str_results_at in res_at_dict.keys():
            return res_at_dict[self.str_results_at]
        else:
            return self.str_results_at

    def _get_parameter_report_str(self):
        parameters = self.get_parameters_list_str()
        parameter_table = ''
        for i, param in enumerate(parameters):
            parameter_table += (f"{i :>21} | {param}\n")

        report = "________________________________________________________\n" + \
                 " Parameters (Type of data in his file. Zero indexed!)\n" + \
                 "                Index | Description\n" + \
                 parameter_table  + \
                 "________________________________________________________\n"

        return report

    def _get_path_his_file(self):
        path_caselist = os.path.join(self.str_sob_dir, self.str_lit, self.NM_CASELIST)
        with open(path_caselist) as caselist:
            str_caselist = caselist.read()
            pattern = r"([0-9]*) '(.*)'"
            match = re.findall(pattern, str_caselist)
            case_dict = {case_name: case_dir for case_dir, case_name in match}
            case_dir = case_dict[self.str_case]
            return os.path.join(self.str_sob_dir, self.str_lit, case_dir, self.str_results_at)

    def _get_his_file(self):
        """ returns a file object to the HIS file """
        path = self._get_path_his_file()
        try:
            return open(path, 'rb')                 #Attention! 'b' signifies reading 'binary'; 'newlines' will be ignored.
        except IOError:
            raise Exception('\nCould not find or open his file: ' + path + '\n')

    def _print_header_his_file(self):
        hisfile = self._get_his_file()
        hisfile.seek(0)                  # stelt leespositie in op punt waar een integer van 4 bytes staat
        first_thousend_characters = hisfile.read(2000).decode('latin-1', errors='ignore')
        print(first_thousend_characters)
        hisfile.close()

    def print_overview(self):
        print(self.__str__())

    def count_ids(self):
        hisfile = self._get_his_file()
        hisfile.seek(self.POS_N_ID)                  # stelt leespositie in op punt waar een integer van 4 bytes staat
        nr_ids = int.from_bytes(hisfile.read(4), byteorder=sys.byteorder)
        hisfile.close()
        return nr_ids

    def count_par(self):
        hisfile = self._get_his_file()
        hisfile.seek(self.POS_N_PAR)
        nr_par = int.from_bytes(hisfile.read(4), byteorder=sys.byteorder)
        hisfile.close()
        return nr_par

    def count_timestamps(self):
        n_ids = self.count_ids()
        n_par = self.count_par()

        hisfile = self._get_his_file()
        hisfile.seek(0, os.SEEK_END)
        size_timesteps = int(hisfile.tell())         #aantal bytes in bestand
        size_timesteps = size_timesteps - (self.LEN_HEADER + self.LEN_N_PAR_N_ID + self.LEN_STR_PAR * n_par + self.LEN_ID * n_ids) # aantal bytes bestand minus bytes voor header en ids = bytes voor waarden parameters
        size_timestep = n_par * n_ids * 4 + 4          #aantal bytes per tijdstap = aantal parameters * aantal Ids (nodes) * 4 bytes + tijd (4 bytes)
        hisfile.close()

        return size_timesteps // size_timestep         #aantal tijdstappen
        
    def get_t0_datetime(self):
        """ returns a time and date object containing the start date and time of the HIS file """
        hisfile = self._get_his_file()
        hisfile.seek(self.POS_STR_DATE)
        str_date = hisfile.read(self.LEN_STR_DATE).decode("latin-1")
        lst_date = str_date.split(sep=".")

        hisfile.seek(self.POS_STR_TIME)
        str_time = hisfile.read(self.LEN_STR_TIME).decode("latin-1")
        lst_time = str_time.split(sep=':')

        start_date_and_time = datetime.datetime(int(lst_date[0]),
                                                int(lst_date[1]),
                                                int(lst_date[2]),
                                                int(lst_time[0]),
                                                int(lst_time[1]),
                                                int(lst_time[2]))
        hisfile.close()

        return start_date_and_time

    def get_timestep_computation_sec(self):
        hisfile = self._get_his_file()
        hisfile.seek(self.POS_STR_DATE)
        str_date = hisfile.read(self.LEN_STR_DATE_TIME_TIMESTEP).decode("latin-1")
        pattern = r"([0-9]+)s\)"
        timestep = int(re.findall(pattern, str_date)[0])
        hisfile.close()

        return timestep

    def get_timestep_data_sec(self):
        timestamps = self.get_timestamps_list_datetime()
        if len(timestamps)>1:
            timestep = timestamps[1] - timestamps[0]
            return timestep.seconds
        else:
            return -999

    def get_timestamps_list_datetime(self):
        n_ids = self.count_ids()
        n_par = self.count_par()
        t0 = self.get_t0_datetime()  # = time and date object
        timestep_sec = self.get_timestep_computation_sec()
        n_timesteps = self.count_timestamps()

        hisfile = self._get_his_file()

        pos_start_data = self.LEN_HEADER + self.LEN_N_PAR_N_ID + self.LEN_STR_PAR * n_par + self.LEN_ID * n_ids  # aantal bytes bestand minus bytes voor header en ids = bytes voor waarden parameters
        bytes_per_timestep = n_ids * n_par * self.LEN_VALUE + self.LEN_VALUE
        lst_timestamps = []

        # read timesteps from HIS file and write to list
        for timestep_int in range(n_timesteps):
            pos = pos_start_data + timestep_int * bytes_per_timestep
            hisfile.seek(pos)
            nr_of_timesteps = int.from_bytes(hisfile.read(4), byteorder='little')
            seconds = nr_of_timesteps * timestep_sec
            timestamp = t0 + datetime.timedelta(seconds=seconds)
            lst_timestamps.append(timestamp)

        hisfile.close()

        return lst_timestamps

    def get_timestamps_dict(self):
        lst_timestamps = self.get_timestamps_list_datetime()
        dict_timestamps = {date: index for index, date in enumerate(lst_timestamps)}
        return dict_timestamps

    def get_ids_list(self):
        n_ids = self.count_ids()
        n_par = self.count_par()

        # read string from HIS-file with all id's
        his_file = self._get_his_file()

        pos = self.LEN_HEADER + self.LEN_N_PAR_N_ID + self.LEN_STR_PAR * n_par
        length = n_ids * 24
        his_file.seek(pos)
        bytes_ids = his_file.read(length)            # reeks van Ids; 4 bytes integer gevolgd door string van 20 tekens
        his_file.close()
        # read id's from string and write them to list (leaves out the 4 byte integers!)
        lst_str_ids = []
        for i in range(n_ids):
            lst_str_ids.append(bytes_ids[i * 24 + 4 : i * 24 + 24].rstrip().decode("latin-1"))

        his_file.close()

        return lst_str_ids

    def get_ids_dict(self):
        n_ids = self.count_ids()
        n_par = self.count_par()

        # read string from HIS-file with all id's
        his_file = self._get_his_file()

        pos = self.LEN_HEADER + self.LEN_N_PAR_N_ID + self.LEN_STR_PAR * n_par
        length = n_ids * 24
        his_file.seek(pos)
        bytes_ids = his_file.read(length)  # reeks van Ids; 4 bytes integer gevolgd door string van 20 tekens
        his_file.close()
        # read id's from string and write them to list (leaves out the 4 byte integers!)
        lst_str_ids = []
        for i in range(n_ids):
            lst_str_ids.append(bytes_ids[i * 24 + 4: i * 24 + 24].rstrip().decode("latin-1"))
        dict_ids = {id:index for index, id in enumerate(lst_str_ids)}

        his_file.close()

        return dict_ids

    def print_parameters(self):
        print(self._get_parameter_report_str())

    def get_parameters_list_str(self):
        n_par =  self.count_par()

        his_file = self._get_his_file()
        his_file.seek(self.POS_STR_PAR)
        list_par = []
        for i in range(n_par):
            list_par.append(his_file.read(self.LEN_STR_PAR).decode('latin-1'))

        his_file.close()

        return list_par

    def _convert_bytestring_to_float(self, bytestring):
        [flt] = struct.unpack('f', bytestring)
        return flt

    def get_data(self, index_parameter_sobek_data, list_str_ids_sobek_to_get_data_from, index_start=0, index_end=None):
        """
        :param index_parameter_sobek_data:
            Integer, zero based. A Sobek HIS-files can contain different parameters. To get an overview of the
            available parameters and corresponding indexes, use "print_parameters(self)"
        :param list_str_ids_sobek_to_get_data_from:
            List of ids of Sobekmodel elements (nodes, reaches, reachsegments). Example: []
        :param list_str_labels_legend:
            Optional. Number of values must be equal to number of number of ids Sobek to get data from.
            When this param is not given param "list_str_ids_sobek_to_get_data_from" will be used for legend labels.
        :param index_start:
            Optional. Integer. To get an overview of the available timesteps use "print_overview(self)"
        :param index_end:
            Optional. Integer. To get an overview of the available timesteps use "print_overview(self)"
        :return: {'timestamps':[datetime.datetime()..], 'data':{'id1':[float, ..], 'id2'[float, ..], ..}}.
        """

        data_sobek_to_return = {'timestamps':None, 'data':{}}

        ids_dict = self.get_ids_dict()

        ids_not_in_his_file = []
        for id_sobek_node in list_str_ids_sobek_to_get_data_from:
            if id_sobek_node not in ids_dict: ids_not_in_his_file.append(id_sobek_node)
        if len(ids_not_in_his_file) > 0:
            message = ''
            for id in ids_not_in_his_file:
                message = message + id + ', '
            message = "Id's not existing in HIS file: " + message
            raise Exception(message)

        n_ids = self.count_ids()
        n_par = self.count_par()
        n_timesteps = self.count_timestamps()

        if not index_end: index_end = n_timesteps - 1

        if index_start > n_timesteps - 1:
            message = "Given index_start exceeds number of timesteps in his file. "
            raise Exception(message)
        if index_end > n_timesteps - 1:
            message = "Given index_end exceeds number of timesteps in his file. "
            raise Exception(message)
        if index_end <= index_start:
            message = "'index_end' must be larger than 'index_start'. "
            raise Exception(message)

        # read data from Sobek his file and add to result:
        hisfile = self._get_his_file()

        pos_start_data = self.LEN_HEADER + self.LEN_N_PAR_N_ID + self.LEN_STR_PAR * n_par + self.LEN_ID * n_ids  + index_parameter_sobek_data * self.LEN_VALUE  # aantal bytes bestand minus bytes voor header en ids = bytes voor waarden parameters
        for id_sobek_node in list_str_ids_sobek_to_get_data_from:
            lst_data_values_for_sobek_id = []
            id_index = ids_dict[id_sobek_node]
            for index_timestep in range(index_start, index_end):
                pos =((index_timestep * (n_ids * n_par + 1)) + 1 + id_index * n_par) * self.LEN_VALUE
                hisfile.seek(pos_start_data + pos)
                data_value = self._convert_bytestring_to_float(hisfile.read(self.LEN_VALUE))
                lst_data_values_for_sobek_id.append(data_value)
            data_sobek_to_return['data'][id_sobek_node] = lst_data_values_for_sobek_id

        hisfile.close()

        # add timestamps to result:
        timestamps = self.get_timestamps_list_datetime()[index_start:index_end]
        data_sobek_to_return['timestamps'] = timestamps

        return data_sobek_to_return
