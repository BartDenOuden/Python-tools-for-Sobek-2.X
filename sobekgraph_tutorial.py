"""Tutorial/ examples sobekgraph.py"""

import sobekgraph
import resultsat


# VARIABLES:
xls_path = r"data_for_examples\Excel\bnd.xlsx"
# Path of directory that contains Sobek models:
sobek_dir = r"data_for_examples"
# Name of Sobek model:
sobek_lit = 'PyTls.lit'
# Names of Sobek cases:
case_1 ='Case 1 of dummy model for examples Python tools'
case_2 ='Case 2 of dummy model for examples Python tools'


# ------------
# DEPENDENCIES
# ------------

# Python version: 3.6 or later.

# sobekgraph.py needs the following libraries:
# numpy
# pandas
# matplotlib

# Installing just pandas should be enough as it depends on both numpy and matplotlib.
# To install libraries you can use pip or conda:
# https://docs.python.org/3/installing/index.html
# https://docs.conda.io/en/latest/miniconda.html

# sobekgraph.py depends on the following other files that are part of python tools for Sobek:
# sobekdatafetcher.py
# settings.py
# resultsat.py

# Make sure these files are placed in the same directory as this file and sobekgraph.py.


# ------------
# QUICK START:
# ------------

# 0. Make sure you are using Python 3.6 or later and you have the libraries needed installed (see dependencies).

# 1. Make a SobekGraph-object:
first_sbkgraph = sobekgraph.SobekGraph()

# 2. Add data to this object:
first_sbkgraph.add_sobek_data(str_sob_dir=sobek_dir,
                              str_lit=sobek_lit,
                              str_case=case_1,
                              results_at=resultsat.RESULTS_AT_NODES,
                              index_parameter_sobek_data=0,
                              list_str_ids_sobek_to_get_data_from=['1_15']
                              )

# 3. Show the graph,
first_sbkgraph.show()
# or export it as a file:
first_sbkgraph.save_as_png_file("image_files/first_sbkgraph", dpi=150)


# ------------------------
# FEATURES OF SOBEKGRAPH
# ------------------------

# Sobekgraph uses the matplotlib library to make graphs of Sobek data.

# - Easy viewing of Sobek data from different cases and data from Excel in one graph.
# - Smart scaling and formatting of axis labels (which can be configured in settings.py).


# ---------------------------------
# OVERVIEW ELEMENTS OF A SOBEKGRAPH
# ---------------------------------

# A SobekGraph object has the following (public) objects:
# - .x_axis and .y_axis, with which you can set  lower_limit, upper_limit, label and grid visibility of these axis;
# - .title, which you can set the title with;
# - .figure, which you can access the matplotlib figure with that contains the graph (= axes);
# - .axes, which you can access the matplotlib axes (= the graph) with.


# -------------
# DOCUMENTATION
# -------------

# Most of the methods of SobekGraph are self explanatory. For more complex methods like '.add_sobek_data()'
# please refer to the docstring. In Pycharm for example, you can view the docstring by selecting the method and
# pressing Ctrl+q


# ---------------------------------
# MORE ABOUT ADDING DATA TO A GRAPH
# ---------------------------------

# At the moment (april 2020) two types of data can be added to the graph:
# - Sobek data (data in His-files)
# - Excel data (time series); The data must be a table with a one row header. The first column must be Excel dates.

# We make a new SobekGraph object and set the title:
sbkgraph_1 = sobekgraph.SobekGraph(width_cm=14, height_cm=16)
sbkgraph_1.title.set_title("Example adding data")

# To get an overview of the Sobek data in an Hisfile you can use:
sbkgraph_1.print_info_about_sobek_data_file(str_sob_dir=sobek_dir,
                                            str_lit=sobek_lit,
                                            str_case=case_1,
                                            results_at=resultsat.RESULTS_AT_REACHSEGMENTS)

# In the information printed you can see this his-file has two parameters:
# 0: discharge
# 1: velocity

# When you add Sobek data to a graph you have to let the method 'add_sobek_data()' know
# the parameter of the Sobek His file, bij assigning it to 'index_parameter_sobek_data'.

# We add time series of discharges of two reach segments, '1_13' and '1_15', to the graph:
sbkgraph_1.add_sobek_data(str_sob_dir=sobek_dir,
                          str_lit=sobek_lit,
                          str_case=case_1,
                          results_at=resultsat.RESULTS_AT_REACHSEGMENTS,
                          index_parameter_sobek_data=0,
                          list_str_ids_sobek_to_get_data_from=['1_1','1_15'],
                          list_str_labels_legend=['Case 1, rs 1_1', 'Case 1, rs 1_15']
                          )

# We add Sobek data from another case:
sbkgraph_1.add_sobek_data(str_sob_dir=sobek_dir,
                          str_lit=sobek_lit,
                          str_case=case_2,
                          results_at=resultsat.RESULTS_AT_REACHSEGMENTS,
                          index_parameter_sobek_data=0,
                          list_str_ids_sobek_to_get_data_from=['1_15'],
                          list_str_labels_legend=['Case 2, rs 1_15']
                          )

# And we add data from an Excel file:
sbkgraph_1.add_excel_data(xls_path,
                          str_sheet_name='blad_bnd',
                          index_column_data=0,
                          index_start=None,
                          str_label_legend='data Excel')

# NOTA BENE:
# As you can see 'index_column_data' is 0.
# The first column in the Excel table next to the dates has index 0.
# Typically this will be the second column in the Excel sheet.

# The data in the Excel file can have a time step that differs from the time step of the Sobek data.

# Finally we add a label to the y-axis and show the graph:
sbkgraph_1.y_axis.set_label('Q [m$^3$/s]')
sbkgraph_1.show()


# --------------------------
# ADJUST SCOPE X- AND Y-AXIS
# --------------------------

sbkgraph_2 = sobekgraph.SobekGraph()
sbkgraph_2.title.set_title('Example adjusting scope of axis')

sbkgraph_2.add_sobek_data(str_sob_dir=sobek_dir,
                          str_lit=sobek_lit,
                          str_case=case_1,
                          results_at=resultsat.RESULTS_AT_REACHSEGMENTS,
                          index_parameter_sobek_data=0,
                          list_str_ids_sobek_to_get_data_from=['1_1','1_15'],
                          list_str_labels_legend=['Case 1, rs 1_1', 'Case 1, rs 1_15'])

# To adjust the scope of the x-axis use a datetime object from the standard python library 'datetime':
import datetime
start_date = datetime.datetime(2020,4,15,18)
sbkgraph_2.x_axis.set_lower_limit(limit_datetime=start_date)
end_date = datetime.datetime(2020,4,16)
sbkgraph_2.x_axis.set_upper_limit(limit_datetime=end_date)

# Adjust y-axis:
sbkgraph_2.y_axis.set_upper_limit(.4)

sbkgraph_2.show()


# -----------------------
# SETTING GRID VISIBILITY
# -----------------------

sbkgraph_3 = sobekgraph.SobekGraph()
sbkgraph_3.title.set_title("Example grid visibility")

sbkgraph_3.add_sobek_data(str_sob_dir=sobek_dir,
                          str_lit=sobek_lit,
                          str_case=case_1,
                          results_at=resultsat.RESULTS_AT_REACHSEGMENTS,
                          index_parameter_sobek_data=0,
                          list_str_ids_sobek_to_get_data_from=['1_1','1_15'],
                          list_str_labels_legend=['Case 1, rs 1_1', 'Case 1, rs 1_15'])

sbkgraph_3.y_axis.set_major_grid_visible(False)
sbkgraph_3.x_axis.set_minor_grid_visible(True)

sbkgraph_3.show()
# Smart scaling and formatting of the minor grid of the y-axis is not yet implemented (sobekgraph.py version 1.0).


# ---------------------------
# DIRECT ACCESS TO MATPLOTLIB
# ---------------------------

# When you want to change something to the graph that is not possible using the methods of SobekGraph you
# can directly use the axes and figure objects of Matplotlib.
# https://matplotlib.org/


# Preparation:
sbkgraph_4 = sobekgraph.SobekGraph()
sbkgraph_4.add_sobek_data(str_sob_dir=sobek_dir,
                          str_lit=sobek_lit,
                          str_case=case_1,
                          results_at=resultsat.RESULTS_AT_REACHSEGMENTS,
                          index_parameter_sobek_data=0,
                          list_str_ids_sobek_to_get_data_from=['1_1','1_15'],
                          list_str_labels_legend=['Case 1, rs 1_1', 'Case 1, rs 1_15'])

# Set .sbkgraph_4.only_use_figure_and_axes_to_make_settings to True:
sbkgraph_4.only_use_figure_and_axes_to_make_settings = True
# This turns of the applying of settings to the graph by SobekGraph.

# An example of direct adjustment to the graph:
import matplotlib.dates as dates

sbkgraph_4.axes.xaxis.set_major_locator(dates.DayLocator())
sbkgraph_4.axes.xaxis.set_major_formatter(dates.DateFormatter('%d-%m-%Y'))
for tick in sbkgraph_4.axes.get_xticklabels():
    tick.set_rotation(270)

sbkgraph_4.axes.set_title('Example direct manipulation of Matplotlib axes')

sbkgraph_4.show()
