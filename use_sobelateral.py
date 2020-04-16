import sobeklateral as sbklat

xls_path = r"N:\Sobek213\LiebrLnd.lit\OPBOUW MODEL\meetreeksen voor randvoorwaarden.xlsx XXX"
lateral_path = r"N:\Sobek213\LiebrLnd.lit\WORK\LATERAL.DAT XXX"

node = "Qlat_st_GA42st7"

# plaats debiet stuw GA42-st7 in knooppunt lateraal debiet:
str_time_series = sbklat.return_str_sobek_lateral_q_timeseries_from_excel(node_id=node,
                                                                          sobek_function_type=sbklat.LINEAR,
                                                                          xls_path=xls_path,
                                                                          sheet_name="0086 stuw GA42-st7",
                                                                          column_values=10,
                                                                          headers=True)
sbklat.add_or_replace_timeseries_lateral_file(lateral_path, str_time_series)
