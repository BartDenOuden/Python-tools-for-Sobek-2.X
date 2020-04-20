"""This module contains a class to make graphs showing Sobek data.
Bart den Ouden, october 2019, april 2020
bart@bartdenoudenwateradvies.nl"""

__version__ = 1.0

import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from settings import *
import sobekdatafetcher


class _Title:

    _title = None

    def __init__(self, axes):
        self.axes = axes

    def set_title(self, title):
        self._title = title

    def _apply_settings(self):
        if self._title:
            self.axes.set_title(self._title)


class _Axis:

    _title = None
    _label = None
    _lim_low = None
    _lim_high = None
    _major_grid_visible = None
    _minor_grid_visible = None

    def __init__(self, axes):
        self.axes = axes

    def set_lower_limit(self, limit_datetime):
        self._lim_low = limit_datetime

    def set_upper_limit(self, limit_datetime):
        self._lim_high = limit_datetime

    def set_label(self, str_label):
        self._label = str_label

    def set_major_grid_visible(self, visible):
        self._major_grid_visible = visible

    def set_minor_grid_visible(self, visible):
        self._minor_grid_visible = visible

    def _set_visibility_grid(self, axis):
        if self._major_grid_visible == True:
            axis.grid(b=True, which="major", linewidth=LINEWIDTH_MAJOR_GRID)
        else:
            axis.grid(b=False, which="major")
        if self._minor_grid_visible == True:
            axis.grid(b=True, which="minor", linewidth=LINEWIDTH_MINOR_GRID)
        else:
            axis.grid(b=False, which="minor")


class _Xaxis(_Axis):

    def __init__(self, axes):
        super().__init__(axes)
        self._major_grid_visible = DEFAULT_MAJOR_GRID_X_AXIS_VISIBLE
        self._minor_grid_visible = DEFAULT_MINOR_GRID_X_AXIS_VISIBLE

    def _set_angle_tick_labels(self):
        for tick in self.axes.get_xticklabels():
            tick.set_rotation(ANGLE_TICK_LABELS_X_AXIS)

    def _get_locators_and_formatters(self,
                                     days_per_cm,
                                     locators_and_formatters=VALUES_AUTO_X_AXIS_FORMATTER):

        for lower_lim, dict_locators_and_formatters in locators_and_formatters:
            if days_per_cm > lower_lim:
                return dict_locators_and_formatters
        print(f"WARNING: locators and formatters could not be set according to scope. \nScope [days] = {days_per_cm}\n")
        return None

    def _set_locators_and_formatters(self):
        # LOCATORS determine the location of ticks
        # FORMATTERS determine the layout of ticks

        scope_days = self.axes.viewLim.width
        width_axes_inch = self.axes.get_window_extent().transformed(self.axes.figure.dpi_scale_trans.inverted()).width
        width_axes_cm = width_axes_inch * 2.54
        days_per_cm = scope_days / width_axes_cm
        # print(days_per_cm)

        locators_and_formatters = self._get_locators_and_formatters(days_per_cm)
        if locators_and_formatters:
            self.axes.xaxis.set_major_locator(locators_and_formatters['major_locator'])
            self.axes.xaxis.set_major_formatter(locators_and_formatters['major_formatter'])
            self.axes.xaxis.set_minor_locator(locators_and_formatters['minor_locator'])
            self.axes.xaxis.set_minor_formatter(locators_and_formatters['minor_formatter'])

    def _apply_settings(self):
        if self._lim_low:
            self.axes.set_xlim(left=self._lim_low)
        if self._lim_high:
            self.axes.set_xlim(right=self._lim_high)
        if self._label:
            self.axes.set_xlabel(self._label)
        self._set_locators_and_formatters()
        self._set_visibility_grid(self.axes.xaxis)
        self._set_angle_tick_labels()


class _Yaxis(_Axis):

    def __init__(self, axes):
        super().__init__(axes)
        self._major_grid_visible = DEFAULT_MAJOR_GRID_Y_AXIS_VISIBLE
        self._minor_grid_visible = DEFAULT_MINOR_GRID_Y_AXIS_VISIBLE

    @staticmethod
    def _e_power(x):
        return math.floor(math.log(abs(x), 10))

    def _multiple_for_locator(self,
                              units_per_major_tick,
                              target_values=UNITS_AUTO_Y_AXIS_FORMATTER):

        power = self._e_power(units_per_major_tick)
        multiple = units_per_major_tick * 10 ** -power

        target_values = np.array(target_values)
        borders = (target_values[1:] + target_values[:-1]) / 2

        for border, target_value in zip(borders, target_values):
            if multiple < border:
                multiple = target_value
                return multiple * 10 ** power
        return target_values[-1] * 10 ** power

    def _units_per_major_tick(self,
                              scope,
                              height_axes_inch,
                              desired_width_ticks_y_axis_cm=DESIRED_WIDTH_TICKS_Y_AXIS_CM):

        height_axes_cm = height_axes_inch * 2.54
        units_per_cm = scope / height_axes_cm
        units_per_major_tick = units_per_cm * desired_width_ticks_y_axis_cm
        return units_per_major_tick

    def _set_locators_and_formatters(self):
        # LOCATORS in a matplotlib graph (axes) determine the location of ticks
        # FORMATTERS determine the layout of ticks
        scope = self.axes.viewLim.height
        height_axes_inch = self.axes.get_window_extent().transformed(self.axes.figure.dpi_scale_trans.inverted()).height
        units_per_major_tick = self._units_per_major_tick(scope=scope, height_axes_inch=height_axes_inch)
        multiple = self._multiple_for_locator(units_per_major_tick)
        self.axes.yaxis.set_major_locator(ticker.MultipleLocator(multiple))

    def _apply_settings(self):
        if self._lim_low:
            self.axes.set_ylim(bottom=self._lim_low)
        if self._lim_high:
            self.axes.set_ylim(top=self._lim_high)
        if self._label:
            self.axes.set_ylabel(self._label)
        self._set_locators_and_formatters()
        self._set_visibility_grid(self.axes.yaxis)


class SobekGraph:

    # Names in Matplotlib:
    # figure = figure that can contain multiple graphs
    # axes = a graph
    # axis = axis of a graph

    def __init__(self,
                 width_cm=DEFAULT_WIDTH_FIGURE_CM,
                 height_cm=DEFAULT_HEIGHT_FIGURE_CM):

        self.width_cm = DEFAULT_WIDTH_FIGURE_CM
        self.height_cm = DEFAULT_HEIGHT_FIGURE_CM

        self.only_use_figure_and_axes_to_make_settings = False

        self.figure = plt.figure(figsize=(self._cm_to_inch(width_cm), self._cm_to_inch(height_cm)))
        self.axes = self.figure.add_subplot(111)

        self.title = _Title(self.axes)

        self.x_axis = _Xaxis(self.axes)
        self.y_axis = _Yaxis(self.axes)

        self.labels_legend = []

        self.tests()


    def tests(self):
        if not VALUES_AUTO_X_AXIS_FORMATTER[-1][0] == 0:
            print(f"WARNING: The last unit number  of settings.VALUES_AUTO_X_AXIS_FORMATTER must be zero \n(VALUES_AUTO_X_AXIS_FORMATTER[-1][0] == 0)\nThe value now is: {VALUES_AUTO_X_AXIS_FORMATTER[-1][0]}")
            print("Please change this value to 0 and start again. ")

    @staticmethod
    def print_info_about_sobek_data_file(str_sob_dir,
                                         str_lit,
                                         str_case,
                                         results_at):
        print(sobekdatafetcher.SobekDataFetcher(str_sob_dir, str_lit, str_case, results_at).__str__())

    def add_sobek_data(self,
                       str_sob_dir,
                       str_lit,
                       str_case,
                       results_at,
                       index_parameter_sobek_data,
                       list_str_ids_sobek_to_get_data_from,
                       list_str_labels_legend=None,
                       index_start=0,
                       index_end=None
                       ):
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
        :param index_parameter_sobek_data:
            Integer, zero based. A Sobek HIS-files can contain different parameters. To get an overview of the
            available parameters and corresponding indexes, use "SobekGraph.print_info_about_sobek_data_file()"
        :param list_str_ids_sobek_to_get_data_from:
            List of ids of Sobekmodel elements (nodes, reaches, reachsegments). Example: []
        :param list_str_labels_legend:
            Optional. Number of strings must be equal to number of ids Sobek to get data from.
            When this param is not given param "list_str_ids_sobek_to_get_data_from" will be used for legend labels.
        :param index_start:
            Optional. Integer.
            To get an overview of the available timesteps use "SobekGraph.print_info_about_sobek_data_file()"
        :param index_end:
            Optional. Integer.
            To get an overview of the available timesteps use "SobekGraph.print_info_about_sobek_data_file()"
        """

        sbkfetcher = sobekdatafetcher.SobekDataFetcher(str_sob_dir, str_lit, str_case, results_at)
        sbkdata = sbkfetcher.get_data(index_parameter_sobek_data,
                                      list_str_ids_sobek_to_get_data_from,
                                      index_start,
                                      index_end)

        # Convert dates, so they are easier to layout:
        lst_dates = self._convert_lst_datetime_to_dates(sbkdata['timestamps'])
        # plot (add) data:
        for id, data in sbkdata['data'].items():
            self.figure.axes[0].plot_date(lst_dates, data, marker=None, linestyle='solid')
            if not list_str_labels_legend:
                self.labels_legend.append(id)

        if list_str_labels_legend:
            self.labels_legend.extend(list_str_labels_legend)

    def add_excel_data(self,
                       str_path_xl_file,
                       str_sheet_name,
                       index_column_data,
                       index_start=0,
                       index_end=None,
                       str_label_legend=None
                       ):
        """
        Format Excel file:
            Date and time in first column; the format must be excel date.
            A header is required, and must be the first row of the sheet only.
        :param str_path_xl_file:
            Path of the excel file. Example: "C:\\data\\river.xls"".
        :param str_sheet_name:
            Name of the sheet name. Example: "measure point 13".
        :param index_column_data:
            INDEX FIRST DATA COLUMN (=second column of the sheet) = 0
        :param index_start:
            Zero indexed.
        :param index_end:
            Zero indexed.
            Given row is not included in data shown in graph.
        :param str_label_legend:
            Optional.
            When this param is not given param "list_str_ids_sobek_to_get_data_from" will be used for legend labels.
        """
        df = pd.read_excel(str_path_xl_file, sheet_name=str_sheet_name, index_col=0)
        if index_end is None:
            self.figure.axes[0].plot_date(df.index[index_start:],
                                          df.iloc[index_start:, index_column_data],
                                          marker=None,
                                          linestyle='solid')
        else:
            self.figure.axes[0].plot_date(df.index[index_start:index_end],
                                          df.iloc[index_start:index_end, index_column_data],
                                          marker=None,
                                          linestyle='solid')

        if not str_label_legend:
            self.labels_legend.append(df.columns[index_column_data])
        else:
            self.labels_legend.append(str_label_legend)

    @staticmethod
    def _cm_to_inch(cm):
        return cm / 2.54

    @staticmethod
    def _convert_lst_datetime_to_dates(lst_datetime):
        return [dates.date2num(datetm) for datetm in lst_datetime]

    def _apply_settings_to_graph(self):
        if not self.only_use_figure_and_axes_to_make_settings:
            self.title._apply_settings()
            self.x_axis._apply_settings()
            self.y_axis._apply_settings()
            self.axes.legend(self.labels_legend)
            self.figure.tight_layout()

    def show(self):
        self._apply_settings_to_graph()
        self.figure.show()

    def save_as_png_file(self, path, dpi=200):
        "Outputs a png image file to given path. "
        self._apply_settings_to_graph()
        self.figure.savefig(path, dpi=dpi)

    # TODO: change unit y-axis, for example meter to milimeter. Actual data stays the same; just the ticklabels change.
