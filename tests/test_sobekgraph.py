from unittest import TestCase

import matplotlib
from matplotlib import dates, ticker

import sobekgraph
import settings

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

    def test__get_locators_and_formatters_choose_dict_in_first_item_of_locators_and_formatters(self):
        graph = sobekgraph.SobekGraph()

        locators_and_formatters = ((10,
                                 {
                                     'major_locator': dates.YearLocator(),
                                     'major_formatter': dates.DateFormatter('%Y'),
                                     'minor_locator': dates.MonthLocator(interval=3),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (5,
                                 {
                                     'major_locator': dates.MonthLocator(bymonth=[1,4,7,10]),
                                     'major_formatter': dates.DateFormatter('%b %Y'),
                                     'minor_locator': dates.MonthLocator(interval=1),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (0,
                                 {
                                     'major_locator': dates.MonthLocator(),
                                     'major_formatter': dates.DateFormatter('%b %Y'),
                                     'minor_locator': dates.WeekdayLocator(),
                                     'minor_formatter': ticker.NullFormatter()
                                 })
                                )

        days_per_cm = 11

        locator_and_formatter = graph.x_axis._get_locators_and_formatters(days_per_cm=days_per_cm,
                                                                          locators_and_formatters=locators_and_formatters)

        self.assertEqual(locators_and_formatters[0][1], locator_and_formatter)

    def test__get_locators_and_formatters_choose_dict_in_last_item_of_locators_and_formatters(self):
        graph = sobekgraph.SobekGraph()

        locators_and_formatters = ((10,
                                 {
                                     'major_locator': dates.YearLocator(),
                                     'major_formatter': dates.DateFormatter('%Y'),
                                     'minor_locator': dates.MonthLocator(interval=3),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (5,
                                 {
                                     'major_locator': dates.MonthLocator(bymonth=[1,4,7,10]),
                                     'major_formatter': dates.DateFormatter('%b %Y'),
                                     'minor_locator': dates.MonthLocator(interval=1),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (0,
                                 {
                                     'major_locator': dates.MonthLocator(),
                                     'major_formatter': dates.DateFormatter('%b %Y'),
                                     'minor_locator': dates.WeekdayLocator(),
                                     'minor_formatter': ticker.NullFormatter()
                                 })
                                )

        days_per_cm = 0.000000000001

        locator_and_formatter = graph.x_axis._get_locators_and_formatters(days_per_cm=days_per_cm,
                                                                          locators_and_formatters=locators_and_formatters)

        self.assertEqual(locators_and_formatters[-1][1], locator_and_formatter)

    def test__get_locators_and_formatters_choose_dict_in_middle_item_of_locators_and_formatters(self):
        graph = sobekgraph.SobekGraph()

        locators_and_formatters = ((10,
                                 {
                                     'major_locator': dates.YearLocator(),
                                     'major_formatter': dates.DateFormatter('%Y'),
                                     'minor_locator': dates.MonthLocator(interval=3),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (5,
                                 {
                                     'major_locator': dates.MonthLocator(bymonth=[1,4,7,10]),
                                     'major_formatter': dates.DateFormatter('%b %Y'),
                                     'minor_locator': dates.MonthLocator(interval=1),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (0,
                                 {
                                     'major_locator': dates.MonthLocator(),
                                     'major_formatter': dates.DateFormatter('%b %Y'),
                                     'minor_locator': dates.WeekdayLocator(),
                                     'minor_formatter': ticker.NullFormatter()
                                 })
                                )

        days_per_cm = 10

        locator_and_formatter = graph.x_axis._get_locators_and_formatters(days_per_cm=days_per_cm,
                                                                          locators_and_formatters=locators_and_formatters)

        self.assertEqual(locators_and_formatters[1][1], locator_and_formatter)
class Test_Yaxis(TestCase):

    def test__e_power_should_be_0(self):
        graph = sobekgraph.SobekGraph()

        x = 7.4
        power_should_be_0 = graph.y_axis._e_power(x)
        self.assertEqual(0, power_should_be_0)

    def test__e_power_should_be_minus1(self):
        graph = sobekgraph.SobekGraph()

        x = 0.74
        power_should_be_minus1 = graph.y_axis._e_power(x)
        self.assertEqual(-1, power_should_be_minus1)

    def test__e_power_should_be_3(self):
        graph = sobekgraph.SobekGraph()

        x = 9999.99
        power_should_be_3 = graph.y_axis._e_power(x)
        self.assertEqual(3, power_should_be_3)

    def test__multiple_for_locator_1_in_1_out(self):
        graph = sobekgraph.SobekGraph()

        target_values = [1, 2.5, 5, 10]

        units_per_major_tick = 1
        multiple_should_be_1 = graph.y_axis._multiple_for_locator(units_per_major_tick=units_per_major_tick,
                                                                  target_values=target_values)

        self.assertEqual(1, multiple_should_be_1)

    def test__multiple_for_locator_1point8_in_2point5_out(self):
        graph = sobekgraph.SobekGraph()

        target_values = [1, 2.5, 5, 10]

        units_per_major_tick = 1.8
        multiple_should_be_2point5 = graph.y_axis._multiple_for_locator(units_per_major_tick=units_per_major_tick,
                                                                        target_values=target_values)

        self.assertEqual(2.5, multiple_should_be_2point5)

    def test__multiple_for_locator_3point7_in_2point5_out(self):
        graph = sobekgraph.SobekGraph()

        target_values = [1, 2.5, 5, 10]

        units_per_major_tick = 3.7
        multiple_should_be_2point5 = graph.y_axis._multiple_for_locator(units_per_major_tick=units_per_major_tick,
                                                                        target_values=target_values)

        self.assertEqual(2.5, multiple_should_be_2point5)

    def test__multiple_for_locator_7point4_in_5_out(self):
        graph = sobekgraph.SobekGraph()

        target_values = [1, 2.5, 5, 10]

        units_per_major_tick = 7.4
        multiple_should_be_5 = graph.y_axis._multiple_for_locator(units_per_major_tick=units_per_major_tick,
                                                                  target_values=target_values)

        self.assertEqual(5, multiple_should_be_5)

    def test__multiple_for_locator_7point5_in_10_out(self):
        graph = sobekgraph.SobekGraph()

        target_values = [1, 2.5, 5, 10]

        units_per_major_tick = 7.5
        multiple_should_be_10 = graph.y_axis._multiple_for_locator(units_per_major_tick=units_per_major_tick,
                                                                   target_values=target_values)

        self.assertEqual(10, multiple_should_be_10)

    def test__multiple_for_locator_37_in_25_out(self):
        graph = sobekgraph.SobekGraph()

        target_values = [1, 2.5, 5, 10]

        units_per_major_tick = 37
        multiple_should_be_25 = graph.y_axis._multiple_for_locator(units_per_major_tick=units_per_major_tick,
                                                                   target_values=target_values)

        self.assertEqual(25, multiple_should_be_25)

    def test__multiple_for_locator_0point037_in_0point025_out(self):
        graph = sobekgraph.SobekGraph()

        target_values = [1, 2.5, 5, 10]

        units_per_major_tick = 0.037
        multiple_should_be_0point025 = graph.y_axis._multiple_for_locator(units_per_major_tick=units_per_major_tick,
                                                                          target_values=target_values)

        self.assertEqual(0.025, multiple_should_be_0point025)

    def test__units_per_major_tick_simple_input(self):
        graph = sobekgraph.SobekGraph()

        scope = 10
        height_axes_inch = 10 / 2.54  # Height = 10 cm
        desired_width_ticks_y_axis_cm = 1

        units_per_major_tick = graph.y_axis._units_per_major_tick(scope=scope,
                                                                  height_axes_inch=height_axes_inch,
                                                                  desired_width_ticks_y_axis_cm=desired_width_ticks_y_axis_cm)

        self.assertEqual(1, units_per_major_tick)

    def test__units_per_major_tick_input_double_desired_width_ticks(self):
        graph = sobekgraph.SobekGraph()
        # graph.add_excel_data(xls_path,
        #                      str_sheet_name='scope is 10',
        #                      index_column_data=0,
        #                      index_start=None,
        #                      str_label_legend='data Excel')

        scope = 10
        height_axes_inch = 10 / 2.54  # Height = 10 cm
        desired_width_ticks_y_axis_cm = 2

        units_per_major_tick = graph.y_axis._units_per_major_tick(scope=scope,
                                                                  height_axes_inch=height_axes_inch,
                                                                  desired_width_ticks_y_axis_cm=desired_width_ticks_y_axis_cm)
        # graph.show()
        self.assertEqual(2.0, units_per_major_tick)

    def test__units_per_major_tick_input_half_scope(self):
        graph = sobekgraph.SobekGraph()
        # graph.add_excel_data(xls_path,
        #                      str_sheet_name='scope is 10',
        #                      index_column_data=0,
        #                      index_start=None,
        #                      str_label_legend='data Excel')

        scope = 5
        height_axes_inch = 10 / 2.54  # Height = 10 cm
        desired_width_ticks_y_axis_cm = 1

        units_per_major_tick = graph.y_axis._units_per_major_tick(scope=scope,
                                                                  height_axes_inch=height_axes_inch,
                                                                  desired_width_ticks_y_axis_cm=desired_width_ticks_y_axis_cm)
        # graph.show()
        self.assertEqual(0.5, units_per_major_tick)

    def test__units_per_major_tick_half_height_axes(self):
        graph = sobekgraph.SobekGraph()

        scope = 10
        height_axes_inch = 5 / 2.54  # Height = 10 cm
        desired_width_ticks_y_axis_cm = 1

        units_per_major_tick = graph.y_axis._units_per_major_tick(scope=scope,
                                                                  height_axes_inch=height_axes_inch,
                                                                  desired_width_ticks_y_axis_cm=desired_width_ticks_y_axis_cm)

        self.assertEqual(2.0, units_per_major_tick)
