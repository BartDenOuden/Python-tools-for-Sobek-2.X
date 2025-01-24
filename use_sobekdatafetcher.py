from sobekdatafetcher import SobekDataFetcher
import resultsat

sbk_fetcher = SobekDataFetcher(
    dir_sobek='data_for_examples\\',
    lit='PyTls.lit',
    case='Case 1 of dummy model for examples Python tools',
    name_hisfile=resultsat.RESULTS_AT_NODES
)

ids = sbk_fetcher.get_ids_list()
print(sbk_fetcher.get_ids_list())
parameter = 0

data = sbk_fetcher.get_data(index_parameter_sobek_data=parameter,
                            ids_sobek=[ids[0], ids[1]]
                            )
print(f"\nnode: {ids[0]}\nmaximum '{sbk_fetcher.get_parameters_list_str()[parameter]}': {max(data['data'][ids[0]]):.3f} m NAP")
