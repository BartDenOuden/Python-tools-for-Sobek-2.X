from unittest import TestCase

import matplotlib

import sobekgraph

xls_path = r"testdata\test.xlsx"

class Test_Xaxis(TestCase):
    def test__set_locators_and_formatters(self):

        graph = sobekgraph.SobekGraph()

        graph.add_excel_data(xls_path,
                          str_sheet_name='long time series',
                          index_column_data=0,
                          index_start=None,
                          str_label_legend='data Excel')
        graph.x_axis._set_locators_and_formatters()

        self.assertIsInstance(graph.axes.xaxis.major.formatter, matplotlib.dates.DateFormatter)
