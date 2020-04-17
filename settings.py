import matplotlib.ticker as ticker
import matplotlib.dates as dates

# settings SobekGraph
DEFAULT_MAJOR_GRID_X_AXIS_VISIBLE = True
DEFAULT_MINOR_GRID_X_AXIS_VISIBLE = False
DEFAULT_MAJOR_GRID_Y_AXIS_VISIBLE = True
DEFAULT_MINOR_GRID_Y_AXIS_VISIBLE = False

LINEWIDTH_MAJOR_GRID = 1.5
LINEWIDTH_MINOR_GRID = 0.5

ANGLE_TICK_LABELS_X_AXIS = 90

# unit numbers: [days / cm]
VALUES_AUTO_X_AXIS_FORMATTER = ((50,
                                 {
                                     'major_locator': dates.YearLocator(),
                                     'major_formatter': dates.DateFormatter('A %Y'),
                                     'minor_locator': dates.MonthLocator(interval=3),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (4.70968,
                                 {
                                     'major_locator': dates.MonthLocator(),
                                     'major_formatter': dates.DateFormatter('B %b %Y'),
                                     'minor_locator': dates.WeekdayLocator(),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (0.94194,
                                 {
                                     'major_locator': dates.WeekdayLocator(),
                                     'major_formatter': dates.DateFormatter('C %d-%m-%Y'),
                                     'minor_locator': dates.DayLocator(),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (0.18839,
                                 {
                                     'major_locator': dates.DayLocator(),
                                     'major_formatter': dates.DateFormatter('D %d-%m-%Y'),
                                     'minor_locator': dates.HourLocator(byhour=range(0, 24, 6)),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (0.037677,
                                 {
                                     'major_locator': dates.HourLocator(byhour=range(0, 24, 6)),
                                     'major_formatter': dates.DateFormatter('E %d-%m-%y  %H:%M'),
                                     'minor_locator': dates.HourLocator(byhour=range(0, 24, 1)),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (0.0075355,
                                 {
                                     'major_locator': dates.HourLocator(byhour=range(0, 24, 3)),
                                     'major_formatter': dates.DateFormatter('6 %d-%m-%y  %H:%M'),
                                     'minor_locator': dates.HourLocator(byhour=range(0, 24, 1)),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                (0.0,
                                 {
                                     'major_locator': dates.MinuteLocator(interval=5),
                                     'major_formatter': dates.DateFormatter('7 %d-%m-%y  %H:%M'),
                                     'minor_locator': dates.MinuteLocator(interval=1),
                                     'minor_formatter': ticker.NullFormatter()
                                 }),
                                )
