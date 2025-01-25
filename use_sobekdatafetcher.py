from sobekdatafetcher import SobekDataFetcher
import resultsat

sbk_fetcher = SobekDataFetcher(
    dir_sobek='data_for_examples\\',
    project='PyTls.lit',
    case='Case 1 of dummy model for examples Python tools',
    name_hisfile=resultsat.RESULTS_AT_NODES
)

ids = sbk_fetcher.get_ids_list()
print('ids:', sbk_fetcher.get_ids_list())

parameter = 0
id_1 = ids[0]
id_2 = ids[1]
ids = [id_1, id_2]
results = sbk_fetcher.get_data(
    index_parameter_sobek_data=parameter,
    ids_sobek=ids
)

print('\nData gelezen uit hisfile:')
for id_ in ids:
    print(f"    node: {id_} | maximum waterpeil: {max(results.data[id_]):.3f} m NAP")

results.write_to_excel(
    path='n:/tmp/sbk_datafetcher_result.xlsx',
    sheet_name='Case 1',
    overwrite=True
)
