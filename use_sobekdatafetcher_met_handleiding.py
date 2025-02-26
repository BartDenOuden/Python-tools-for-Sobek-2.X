"""
Voorbeelden van het gebruik van de SobekDataFetcher class voor het lezen van Sobek-berekeningsresultaten en het
schrijven daarvan naar een excelbestand.

Bart den Ouden, 26 februari 2025
"""

from sobekdatafetcher import SobekDataFetcher
import resultsat
from datetime import datetime


# ----------------------------------------------------------------------------------------------------------------------
# 1: OPGEVEN PARAMETERWAARDEN VOOR CREËREN SobekDataFetcher-OBJECT:

# Dit betreft parameterwaarden die bepalen welk HIS-bestand wordt gelezen.
# Welke data uit dit HIS-bestand wordt gelezen bepaal je met de parameters in stap 3.

DIR_SOBEK = 'D:/Migratie/Sobek213/'
SOBEK_PROJECT = '3108KD.lit'
CASE = 'HK T10'
NAAM_HISFILE = resultsat.RESULTS_AT_NODES


# ----------------------------------------------------------------------------------------------------------------------
# 2: CREËREN SobekDataFetcher-OBJECT:

# Het SobekDataFetcher-object krijgt in dit geval de naam 'sbk_fetcher'.
sbk_fetcher = SobekDataFetcher(
    dir_sobek=DIR_SOBEK,
    project=SOBEK_PROJECT,
    case=CASE,
    name_hisfile=NAAM_HISFILE
)
# Dit SobekDataFetcher-object bevat meta-data van het Sobek-HIS-bestand die je kunt opvragen met onder andere:
# sbk_fetcher.timestamps
# sbk_fetcher.t0
# sbk_fetcher.IDS


# ----------------------------------------------------------------------------------------------------------------------
# 3: KIEZEN PARAMETERWAARDEN VOOR LEZEN SOBEK-RESULTATEN:

# Een HIS-bestand kan verschillende typen data bevatten, die Sobek 'parameters' noemt.
# Het HIS-bestand 'CALCPNT.HIS' kan bijvoorbeeld al naar gelang de settings in Sobek bevatten:
# Waterlevel, Waterdepth, Free board.
# Bij het aanmaken van een SobekDataFetcher-object worden de parameters naar de console geprint.
# Dat ziet er bijvoorbeeld zo uit:
# ----------------------------------------------------------------------------------------------------
#  Parameters in CALCPNT.HIS:
#                 Index | Description
#                     0 | Waterlevel  (m AD)
#                     1 | Waterdepth  (m)
#                     2 | Free board (m)
# ----------------------------------------------------------------------------------------------------
# Je kunt hiervoor ook opdracht geven met:
# sbk_fetcher.print_parameters()
# of:
# parameters: list = sbk_fetcher.get_parameters()

# Je kiest een index door de corresponderende index te kiezen.
PARAMETER = 0

# Het opgeven van id's is optioneel. Als je geen id's opgeeft krijg je de Sobekresultaten van alle locaties in het model.
id_1 = sbk_fetcher.ids[0]
id_2 = sbk_fetcher.ids[1]
ids = ["CONN1", 'CONN35']

# Ook het opgeven van een periode is optioneel. Als je niets opgeeft, worden alle tijdstappen ingelezen.
# Je kunt de periode met de parameters 'start' en 'end' de methode '.get_data'. Zie hieronder.
# Je kunt hierbij indices opgeven (volgnummers die beginnen bij 0) en datetime.datetime-objecten. Een voorbeeld van
# het aanmaken van een datetime.datetime-object:
einddatum = datetime(year=2000, month=1, day=21, hour=1)
# Je kunt ook een datetime.datetime-object kiezen uit de metadata van het SobekDataFetcher-object:
eerste_tijdstap = sbk_fetcher.timestamps[0]
tweede_tijdstap = sbk_fetcher.timestamps[1]
laatste_tijdstap = sbk_fetcher.timestamps[-1]

# ----------------------------------------------------------------------------------------------------------------------
# 4: LEZEN DATA:
resultaten_laatste_tijdstap_voor_alle_locaties = sbk_fetcher.get_data(
    index_parameter_sobek_data=PARAMETER,
    start=laatste_tijdstap,
    end=laatste_tijdstap,
)
resultaten_alle_tijdstappen_voor_twee_locaties = sbk_fetcher.get_data(
    index_parameter_sobek_data=PARAMETER,
    ids_sobek=ids
)
resultaten_eerste_twee_tijdstappen_voor_twee_locaties = sbk_fetcher.get_data(
    index_parameter_sobek_data=PARAMETER,
    ids_sobek=ids,
    start=eerste_tijdstap,
    end=tweede_tijdstap
)

# ----------------------------------------------------------------------------------------------------------------------
# 5: SCHRIJVEN DATA NAAR EXCEL-BESTAND:
resultaten_alle_tijdstappen_voor_twee_locaties.write_to_excel(
    path='n:/tmp/sbk_datafetcher_result_xlsxwriter.xlsx',
    sheet_name='alle tijdstappen',
    overwrite=True
)
resultaten_laatste_tijdstap_voor_alle_locaties.write_to_excel(
    path='n:/tmp/sbk_datafetcher_result_xlsxwriter.xlsx',
    sheet_name='alle locaties',
    overwrite=True
)
resultaten_eerste_twee_tijdstappen_voor_twee_locaties.write_to_excel(
    path='n:/tmp/sbk_datafetcher_result_xlsxwriter.xlsx',
    sheet_name='2x2',
    overwrite=True
)
