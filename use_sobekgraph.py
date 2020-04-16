import datetime

import sobekgraph
import resultsat

# VARIABELEN:

xls_path = r"data_for_examples\Excel\bnd.xlsx"

# Pad directory die Sobekmodellen bevat:
SOBDIR = r"data_for_examples"
# Naam Sobekmodel:
SOBLIT = 'PyTls.lit'

case_1 ='Dummymodel voor voorbeelden Python tools voor Sobek'
case_2 ='Dummymodel voor voorbeelden Python tools voor Sobek 2'


# WERKEN MET SOBEKGRAPH:

# Je begint met het aanmaken van een grafiek-object:
sbkgraph_1 = sobekgraph.SobekGraph(title="Voorbeeld 1: peilen op twee nodes")

# De methodes van SobekGraph zijn gedocumenteerd in de docstrings.
# In bijvoorbeeld Pycharm en Jupyter Notebook/ Lab kun je die laten weergeven.

# VOORBEELD 0: print info Sobek-His-file naar console:
print("\nOUTPUT SOBEK GRAPH:")
sbkgraph_1.print_info_about_sobek_data_file(SOBDIR, SOBLIT, case_1, resultsat.RESULTS_AT_REACHSEGMENTS)

# VOORBEELD 1: drie nodes in dezelfde case:
sbkgraph_1.add_sobek_data(str_sob_dir=SOBDIR,
                          str_lit=SOBLIT,
                          str_case=case_1,
                          results_at=resultsat.RESULTS_AT_NODES,
                          index_parameter_sobek_data=0,
                          list_str_ids_sobek_to_get_data_from=['1_15', '1_22'])

# TODO: nagaan wat er gebeurd als je commando .show() in een terminal geeft.
sbkgraph_1.show()


# VOORBEELD 2: Hetzelfde reachsegment in twee cases:
sbkgraph_2 = sobekgraph.SobekGraph(title="Voorbeeld 2: één reachsegment in twee cases",
                                   ylabel='Q [m3/s]',
                                   height_cm=10)
sbkgraph_2.add_sobek_data(SOBDIR, SOBLIT, case_1, resultsat.RESULTS_AT_REACHSEGMENTS, 0, ['1_13'], ['case 1'])
sbkgraph_2.add_sobek_data(SOBDIR, SOBLIT, case_2, resultsat.RESULTS_AT_REACHSEGMENTS, 0, ['1_13'], ['case 2'])

sbkgraph_2.show()

# VOORBEELD 3: Toevoegen van data uit Excel.
sbkgraph_3 = sobekgraph.SobekGraph(title="Voorbeeld 3: data uit Sobek en Excel",
                                   ylabel='Q [m3/s]',
                                   height_cm=10)
sbkgraph_3.add_sobek_data(SOBDIR, SOBLIT, case_1, resultsat.RESULTS_AT_REACHSEGMENTS, 0, ['1_22'], ['data Sobek'])

# Tijdreeks uit Excel toegevoegen:
sbkgraph_3.add_excel_data(xls_path,
                          str_sheet_name='blad_bnd',
                          index_column_data=0,
                          index_start=None,
                          str_label_legend='data Excel')
sbkgraph_3.show()

# TODO: voorbeeld weergeven deel van de tijd.
# TODO: voorbeeld aanpassen y-as.

# TODO: consequent Engels gebruiken.
# TODO: index kolom data Excel is zero based. Dit leidt makkelijk tot verwarring bij gebruiker. Oplossing?