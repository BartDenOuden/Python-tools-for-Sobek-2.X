import sobekdatafetcher as sbk
import resultsat

sbk_fetcher = sbk.SobekDataFetcher(str_sob_dir='N:\\Sobek213\\',
                                   str_lit='LiebrMid.lit',
                                   str_case='Locatie 2; 6 Bos en Bijkerk = 5',
                                   results_at=resultsat.RESULTS_AT_NODES
                                   )

# sobek_data_server = sbk.SobekDataFetcher(str_sob_dir='N:\\Sobek213\\',
#                                              str_lit='2d.lit',
#                                              str_case='test korte tijdstap uitvoer data',
#                                              results_at=sbk.RESULTS_AT_NODES
#                                              )

sbk_fetcher.print_parameters()
#
ids = sbk_fetcher.get_ids_list()
print(sbk_fetcher.get_ids_list())
parameter = 2

data = sbk_fetcher.get_data(index_parameter_sobek_data=parameter,
                            list_str_ids_sobek_to_get_data_from=[ids[0], ids[1]]
                            )
print(f"\nnode: {ids[0]}\nmaximum '{sbk_fetcher.get_parameters_list_str()[parameter]}': {max(data['data'][ids[0]]):.3f} m NAP")
