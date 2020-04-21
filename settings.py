import matplotlib.ticker as ticker
import matplotlib.dates as dates

# ___________________
# SETTINGS SOBEKGRAPH

DEFAULT_WIDTH_FIGURE_CM = 14
DEFAULT_HEIGHT_FIGURE_CM = 12

DEFAULT_MAJOR_GRID_X_AXIS_VISIBLE = True
DEFAULT_MINOR_GRID_X_AXIS_VISIBLE = False
DEFAULT_MAJOR_GRID_Y_AXIS_VISIBLE = True
DEFAULT_MINOR_GRID_Y_AXIS_VISIBLE = False

LINEWIDTH_MAJOR_GRID = 1.5
LINEWIDTH_MINOR_GRID = 0.5

ANGLE_TICK_LABELS_X_AXIS = 90

# These are te possible units for the ticks of the y-axis (* 10 ** x).
# - first unit must be 1
# - last unit must be 10
# - units have to be sorted ascending
UNITS_AUTO_Y_AXIS_FORMATTER = [1, 2.5, 5, 10]
DESIRED_WIDTH_TICKS_Y_AXIS_CM = 1.7

# the numbers represent the lower boundary of the classes
# unit numbers: [days / cm]
# numbers have to be sorted descending
# THE LAST UNIT NUMBER MUST BE ZERO (VALUES_AUTO_X_AXIS_FORMATTER[-1][0] == 0).
VALUES_AUTO_X_AXIS_FORMATTER = ((75,
                                 {
                                     'major_locator': dates.YearLocator(),
                                     'major_formatter': dates.DateFormatter('%Y'),
                                     'minor_locator': dates.MonthLocator(interval=3),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (38,
                                 {
                                     'major_locator': dates.MonthLocator(bymonth=[1,4,7,10]),
                                     'major_formatter': dates.DateFormatter('%b %Y'),
                                     'minor_locator': dates.MonthLocator(interval=1),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (5,
                                 {
                                     'major_locator': dates.MonthLocator(),
                                     'major_formatter': dates.DateFormatter('%b %Y'),
                                     'minor_locator': dates.WeekdayLocator(),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (0.7,
                                 {
                                     'major_locator': dates.WeekdayLocator(),
                                     'major_formatter': dates.DateFormatter('%d-%m-%Y'),
                                     'minor_locator': dates.DayLocator(),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (0.2,
                                 {
                                     'major_locator': dates.DayLocator(),
                                     'major_formatter': dates.DateFormatter('%d-%m-%Y'),
                                     'minor_locator': dates.HourLocator(byhour=range(0, 24, 6)),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (0.07,
                                 {
                                     'major_locator': dates.HourLocator(byhour=range(0, 24, 6)),
                                     'major_formatter': dates.DateFormatter('%d-%m-%y  %H:%M'),
                                     'minor_locator': dates.HourLocator(byhour=range(0, 24, 1)),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (0.028,
                                 {
                                     'major_locator': dates.HourLocator(byhour=range(0, 24, 3)),
                                     'major_formatter': dates.DateFormatter('%d-%m-%y  %H:%M'),
                                     'minor_locator': dates.HourLocator(byhour=range(0, 24, 1)),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (0.01,
                                 {
                                     'major_locator': dates.HourLocator(byhour=range(0, 24, 1)),
                                     'major_formatter': dates.DateFormatter('%d-%m-%y  %H:%M'),
                                     'minor_locator': dates.MinuteLocator(interval=15),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (0.005,
                                 {
                                     'major_locator': dates.MinuteLocator(interval=15),
                                     'major_formatter': dates.DateFormatter('%d-%m-%y  %H:%M'),
                                     'minor_locator': dates.MinuteLocator(interval=5),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (0,
                                 {
                                     'major_locator': dates.MinuteLocator(interval=5),
                                     'major_formatter': dates.DateFormatter('%d-%m-%y  %H:%M'),
                                     'minor_locator': dates.MinuteLocator(interval=1),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                )
