import datetime

import sobekgraph
import resultsat


xls_path = r"tests\testdata\test.xlsx"

sbkgraph = sobekgraph.SobekGraph(height_cm=13, width_cm=30)
sbkgraph.x_axis.set_major_grid_visible(True)
sbkgraph.x_axis.set_minor_grid_visible(True)

sbkgraph.add_excel_data(xls_path,
                          str_sheet_name='long time series',
                          index_column_data=0,
                          index_start=None,
                          str_label_legend='data Excel')

sbkgraph.x_axis.set_lower_limit(datetime.datetime(2010, 1, 1))

sbkgraph.show()
sbkgraph.x_axis.set_upper_limit(datetime.datetime(2011, 1, 2))
sbkgraph.show()
sbkgraph.x_axis.set_upper_limit(datetime.datetime(2010, 12, 31))
sbkgraph.show()
# sbkgraph.x_axis.set_upper_limit(datetime.datetime(2010, 1, 7))
# sbkgraph.show()
# sbkgraph.x_axis.set_upper_limit(datetime.datetime(2010, 1, 2))
# sbkgraph.show()
# sbkgraph.x_axis.set_upper_limit(datetime.datetime(2010, 1, 1, 12))
# sbkgraph.show()
# sbkgraph.x_axis.set_upper_limit(datetime.datetime(2010, 1, 1, 1))
# sbkgraph.show()
# sbkgraph.x_axis.set_upper_limit(datetime.datetime(2010, 1, 1, 0, 30))
# sbkgraph.show()
