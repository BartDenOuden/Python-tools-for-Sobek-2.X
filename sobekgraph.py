"""This module contains a class to make graphs showing Sobek data.
Bart den Ouden, october 2019
bart@bartdenoudenwateradvies.nl"""

import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import matplotlib.pyplot as plt

import sobekdatafetcher


class SobekGraph:

    PAD = 1.2

    def __init__(self,
                 ylabel = None,
                 xlabel = None,
                 width_cm = 14.0,
                 height_cm = 9.0,
                 title = None,
                 xlim_left = None,
                 xlim_right = None,
                 ylim_bottom = None,
                 ylim_top = None,
                 angle_labels_xaxis = 90):

        # TODO: docstring
        # TODO: add unit to xlim_left and xlim_right
        self.figure = self._make_figure_timeseries(ylabel=ylabel,
                                                   xlabel=xlabel,
                                                   width_cm=width_cm,
                                                   height_cm=height_cm,
                                                   title=title,
                                                   xlim_left=xlim_left,
                                                   xlim_right=xlim_right,
                                                   ylim_bottom=ylim_bottom,
                                                   ylim_top=ylim_top,
                                                   angle_labels_xaxis=angle_labels_xaxis)
        self.labels_legend = []


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

    def _make_figure_timeseries(self,
                                ylabel,
                                xlabel,
                                width_cm,
                                height_cm,
                                title,
                                xlim_left,
                                xlim_right,
                                ylim_bottom,
                                ylim_top,
                                angle_labels_xaxis):

        # HELP:
        # figure = figure that can contain multiple graphs
        # axes = a graph
        # axis = axis of a graph

        # LOCATORS determine the location of ticks (x and y axis)
        # FORMATTERS determine the layout of ticks (x and y axis)

        width = self._cm_to_inch(width_cm)
        height = self._cm_to_inch(height_cm)

        figure = plt.figure(figsize=(width, height))
        axes = figure.add_subplot(111)

        # show range x axis:
        if xlim_right and not xlim_left:
            axes.set_xlim(right=xlim_right)
        if not xlim_right and xlim_left:
            axes.set_xlim(left=xlim_left)
        if xlim_right and xlim_left:
            axes.set_xlim(right=xlim_right, left=xlim_left)

        # show range y axis:
        if ylim_top and not ylim_bottom:
            axes.set_ylim(top=ylim_top)
        if not ylim_top and ylim_bottom:
            axes.set_ylim(bottom=ylim_bottom)
        if ylim_top and ylim_bottom:
            axes.set_ylim(top=ylim_top, bottom=ylim_bottom)

        # title:
        if title: axes.set_title(title)

        # labels x and y axis:
        if xlabel: axes.set_xlabel(xlabel)
        if ylabel: axes.set_ylabel(ylabel)

        # LAYOUT X-AS
        # LOCATORS determine the location of ticks
        # TODO: determine interval on the basis of the scope
        for tick in axes.get_xticklabels():
            tick.set_rotation(angle_labels_xaxis)
        axes.xaxis.set_major_locator(dates.DayLocator(bymonthday=range(1, 32), interval=1))
        axes.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
        axes.xaxis.set_minor_locator(dates.HourLocator(byhour=range(0, 24, 6)))
        # ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
        axes.xaxis.grid(which="major", linewidth=1.5)
        axes.xaxis.grid(which="minor")

        # LAYOUT Y-AS
        axes.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
        axes.yaxis.grid(True, which="major", linewidth=1)

        # Further layout:
        figure.tight_layout(pad=self.PAD)

        # Finish:
        return figure

    def show(self):
        self.figure.axes[0].legend(self.labels_legend)
        self.figure.show()

    def save_as_image_file(self, filename, dpi=200):
        # TODO: docstring, output format
        self.figure.savefig(filename, dpi=dpi)
