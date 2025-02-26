"""
Voorbeelden van het gebruik van de SobekDataFetcher class voor het lezen van Sobek-berekeningsresultaten en het
schrijven daarvan naar een excelbestand.

Bart den Ouden, 26 februari 2025
"""

from sobekdatafetcher import SobekDataFetcher
import resultsat


DIR_SOBEK = 'D:/Migratie/Sobek213/'
SOBEK_PROJECT = '3108KD.lit'
CASE = 'HK T10'
NAAM_HISFILE = resultsat.RESULTS_AT_NODES

# Creëer SobekDataFetcher-object. Hierbij wordt metadata uit het desbetreffende HIS-bestand in het object opgeslagen.
sbk_fetcher = SobekDataFetcher(
    dir_sobek=DIR_SOBEK,
    project=SOBEK_PROJECT,
    case=CASE,
    name_hisfile=NAAM_HISFILE
)

# Een HIS-file kan verschillende typen data bevatten. Kies de index voor de gewenste parameter. Zie hiervoor de
# informatie die het SobekDataFetcher-object naar de console print.
PARAMETER = 0
# Het opgeven van id's is optioneel. Als je geen id's opgeeft krijg je de Sobekresultaten van alle locaties in het model.
IDS = ["CONN1", 'CONN35']
# Ook het opgeven van een periode is optioneel. In dit voorbeeld lezen we de laatste tijdstap uit de metadata in het
# SobekDataFetcher-object, en gebruiken die om de in te lezen periode op te geven.
laatste_tijdstap = sbk_fetcher.timestamps[-1]

results = sbk_fetcher.get_data(
    index_parameter_sobek_data=PARAMETER,
    ids_sobek=IDS,
    start=laatste_tijdstap,
    end=laatste_tijdstap,
)

# Deze methode kan alle regels en kolommen als die al bestaan overschrijven als je 'overwrite=True' opgeeft!
results.write_to_excel(
    path='n:/tmp/sbk_datafetcher_result_xlsxwriter.xlsx',
    sheet_name='Resultaten T=10 oid',
    overwrite=True
)
