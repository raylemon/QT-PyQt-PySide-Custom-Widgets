import math
import os

try:
    from PySide6.QtWidgets import QMainWindow, QWidget, QApplication
    from PySide6.QtGui import QPolygon, QPolygonF, QColor, QPen, QFont, QPainter, QFontMetrics, QConicalGradient, \
        QRadialGradient, QFontDatabase
    from PySide6.QtCore import Qt, QTime, QTimer, QPoint, QPointF, QRect, QSize, QObject
    from PySide6.QtCore import Signal
except ModuleNotFoundError:
    print("Please install any suitable version of Pyside 6")


class AnalogGaugeWidget(QWidget):
    """Fetches rows from a Bigtable.
    """
    valueChanged = Signal(int)

    def __init__(self, parent=None):
        super(AnalogGaugeWidget, self).__init__(parent)

        self.scala_count = None
        self.enable_filled_polygon = None
        self.enable_bar_graph = None
        self.enable_scale_text = None
        self.center_point_color = None
        self.display_value_color = None
        self.scale_value_color = None
        self.needle_color_drag = None
        self.needle_color = None
        self.widget_diameter = None
        self.needle_center_bg = None
        self.outer_circle_bg = None
        self.show_custom_widgets_logs = True
        self.use_timer_event = False

        self.setNeedleColor(0, 0, 0, 255)

        self.needle_color_released = self.needle_color

        self.setNeedleColorOnDrag(255, 0, 00, 255)

        self.setScaleValueColor(0, 0, 0, 255)

        self.setDisplayValueColor(0, 0, 0, 255)

        self.set_CenterPointColor(0, 0, 0, 255)

        self.value_needle_count = 1

        self.value_needle = QObject

        self.min_value = 0
        self.max_value = 1000
        self.value = self.min_value

        self.value_offset = 0

        self.value_needle_snapzone = 0.05
        self.last_value = 0

        self.gauge_color_outer_radius_factor = 1
        self.gauge_color_inner_radius_factor = 0.9

        self.center_horizontal_value = 0
        self.center_vertical_value = 0

        self.scale_angle_start_value = 135
        self.scale_angle_size = 270

        self.angle_offset = 0

        self.setScalaCount(10)
        self.scala_subdiv_count = 5

        self.pen = QPen(QColor(0, 0, 0))

        QFontDatabase.addApplicationFont(
            os.path.join(os.path.dirname(__file__), 'fonts/Orbitron/Orbitron-VariableFont_wght.ttf'))

        self.scale_polygon_colors = []

        self.big_scale_marker = Qt.black

        self.fine_scale_marker = Qt.black

        self.setEnableScaleText(True)
        self.scale_fontname = "Orbitron"
        self.initial_scale_fontsize = 14
        self.scale_fontsize = self.initial_scale_fontsize

        self.enable_value_text = True
        self.value_fontname = "Orbitron"
        self.initial_value_fontsize = 40
        self.value_fontsize = self.initial_value_fontsize
        self.text_radius_factor = 0.5

        self.setEnableBarGraph(True)
        self.setEnableScalePolygon(True)
        self.enable_center_point = True
        self.enable_fine_scaled_marker = True
        self.enable_big_scaled_marker = True

        self.needle_scale_factor = 0.8
        self.enable_Needle_Polygon = True

        self.setMouseTracking(True)

        self.units = "℃"

        if self.use_timer_event:
            timer = QTimer(self)
            timer.timeout.connect(self.update)
            timer.start(10)
        else:
            self.update()

        self.setGaugeTheme(0)

        self.rescale_method()

    def setScaleFontFamily(self, font):
        self.scale_fontname = str(font)

    def setValueFontFamily(self, font):
        self.value_fontname = str(font)

    def setBigScaleColor(self, color):
        self.big_scale_marker = QColor(color)

    def setFineScaleColor(self, color):
        self.fine_scale_marker = QColor(color)

    def setGaugeTheme(self, theme=1):
        match theme:
            case 0, None:
                self.set_scale_polygon_colors([[.00, Qt.red],
                                               [.1, Qt.yellow],
                                               [.15, Qt.green],
                                               [1, Qt.transparent]])

                self.needle_center_bg = [
                    [0, QColor(35, 40, 3, 255)],
                    [0.16, QColor(30, 36, 45, 255)],
                    [0.225, QColor(36, 42, 54, 255)],
                    [0.423963, QColor(19, 23, 29, 255)],
                    [0.580645, QColor(45, 53, 68, 255)],
                    [0.792627, QColor(59, 70, 88, 255)],
                    [0.935, QColor(30, 35, 45, 255)],
                    [1, QColor(35, 40, 3, 255)]
                ]

                self.outer_circle_bg = [
                    [0.0645161, QColor(30, 35, 45, 255)],
                    [0.37788, QColor(57, 67, 86, 255)],
                    [1, QColor(30, 36, 45, 255)]
                ]

            case 1:
                self.set_scale_polygon_colors([[.75, Qt.red],
                                               [.5, Qt.yellow],
                                               [.25, Qt.green]])

                self.needle_center_bg = [
                    [0, QColor(35, 40, 3, 255)],
                    [0.16, QColor(30, 36, 45, 255)],
                    [0.225, QColor(36, 42, 54, 255)],
                    [0.423963, QColor(19, 23, 29, 255)],
                    [0.580645, QColor(45, 53, 68, 255)],
                    [0.792627, QColor(59, 70, 88, 255)],
                    [0.935, QColor(30, 35, 45, 255)],
                    [1, QColor(35, 40, 3, 255)]
                ]

                self.outer_circle_bg = [
                    [0.0645161, QColor(30, 35, 45, 255)],
                    [0.37788, QColor(57, 67, 86, 255)],
                    [1, QColor(30, 36, 45, 255)]
                ]

            case 2:
                self.set_scale_polygon_colors([[.25, Qt.red],
                                               [.5, Qt.yellow],
                                               [.75, Qt.green]])

                self.needle_center_bg = [
                    [0, QColor(35, 40, 3, 255)],
                    [0.16, QColor(30, 36, 45, 255)],
                    [0.225, QColor(36, 42, 54, 255)],
                    [0.423963, QColor(19, 23, 29, 255)],
                    [0.580645, QColor(45, 53, 68, 255)],
                    [0.792627, QColor(59, 70, 88, 255)],
                    [0.935, QColor(30, 35, 45, 255)],
                    [1, QColor(35, 40, 3, 255)]
                ]

                self.outer_circle_bg = [
                    [0.0645161, QColor(30, 35, 45, 255)],
                    [0.37788, QColor(57, 67, 86, 255)],
                    [1, QColor(30, 36, 45, 255)]
                ]

            case 3:
                self.set_scale_polygon_colors([[.00, Qt.white]])

                self.needle_center_bg = [
                    [0, Qt.white],
                ]

                self.outer_circle_bg = [
                    [0, Qt.white],
                ]

                self.big_scale_marker = Qt.black
                self.fine_scale_marker = Qt.black

            case 4:
                self.set_scale_polygon_colors([[1, Qt.black]])

                self.needle_center_bg = [
                    [0, Qt.black],
                ]

                self.outer_circle_bg = [
                    [0, Qt.black],
                ]

                self.big_scale_marker = Qt.white
                self.fine_scale_marker = Qt.white

            case 5:
                self.set_scale_polygon_colors([[1, QColor("#029CDE")]])

                self.needle_center_bg = [
                    [0, QColor("#029CDE")],
                ]

                self.outer_circle_bg = [
                    [0, QColor("#029CDE")],
                ]

            case 6:
                self.set_scale_polygon_colors([[.75, QColor("#01ADEF")],
                                               [.5, QColor("#0086BF")],
                                               [.25, QColor("#005275")]])

                self.needle_center_bg = [
                    [0, QColor(0, 46, 61, 255)],
                    [0.322581, QColor(1, 173, 239, 255)],
                    [0.571429, QColor(0, 73, 99, 255)],
                    [1, QColor(0, 46, 61, 255)]
                ]

                self.outer_circle_bg = [
                    [0.0645161, QColor(0, 85, 116, 255)],
                    [0.37788, QColor(1, 173, 239, 255)],
                    [1, QColor(0, 69, 94, 255)]
                ]

                self.big_scale_marker = Qt.black
                self.fine_scale_marker = Qt.black

            case 7:
                self.set_scale_polygon_colors([[.25, QColor("#01ADEF")],
                                               [.5, QColor("#0086BF")],
                                               [.75, QColor("#005275")]])

                self.needle_center_bg = [
                    [0, QColor(0, 46, 61, 255)],
                    [0.322581, QColor(1, 173, 239, 255)],
                    [0.571429, QColor(0, 73, 99, 255)],
                    [1, QColor(0, 46, 61, 255)]
                ]

                self.outer_circle_bg = [
                    [0.0645161, QColor(0, 85, 116, 255)],
                    [0.37788, QColor(1, 173, 239, 255)],
                    [1, QColor(0, 69, 94, 255)]
                ]

                self.big_scale_marker = Qt.black
                self.fine_scale_marker = Qt.black

            case 8:
                self.setCustomGaugeTheme(
                    color1="#ffaa00",
                    color2="#7d5300",
                    color3="#3e2900"
                )

                self.big_scale_marker = Qt.black
                self.fine_scale_marker = Qt.black

            case 9:
                self.setCustomGaugeTheme(
                    color1="#3e2900",
                    color2="#7d5300",
                    color3="#ffaa00"
                )

                self.big_scale_marker = Qt.white
                self.fine_scale_marker = Qt.white

            case 10:
                self.setCustomGaugeTheme(
                    color1="#ff007f",
                    color2="#aa0055",
                    color3="#830042"
                )

                self.big_scale_marker = Qt.black
                self.fine_scale_marker = Qt.black

            case 11:
                self.setCustomGaugeTheme(
                    color1="#830042",
                    color2="#aa0055",
                    color3="#ff007f"
                )

                self.big_scale_marker = Qt.white
                self.fine_scale_marker = Qt.white

            case 12:
                self.setCustomGaugeTheme(
                    color1="#ffe75d",
                    color2="#896c1a",
                    color3="#232803"
                )

                self.big_scale_marker = Qt.black
                self.fine_scale_marker = Qt.black

            case 13:
                self.setCustomGaugeTheme(
                    color1="#ffe75d",
                    color2="#896c1a",
                    color3="#232803"
                )

                self.big_scale_marker = Qt.black
                self.fine_scale_marker = Qt.black

            case 14:
                self.setCustomGaugeTheme(
                    color1="#232803",
                    color2="#821600",
                    color3="#ffe75d"
                )

                self.big_scale_marker = Qt.white
                self.fine_scale_marker = Qt.white

            case 15:
                self.setCustomGaugeTheme(
                    color1="#00FF11",
                    color2="#00990A",
                    color3="#002603"
                )

                self.big_scale_marker = Qt.black
                self.fine_scale_marker = Qt.black

            case 16:
                self.setCustomGaugeTheme(
                    color1="#002603",
                    color2="#00990A",
                    color3="#00FF11"
                )

                self.big_scale_marker = Qt.white
                self.fine_scale_marker = Qt.white

            case 17:
                self.setCustomGaugeTheme(
                    color1="#00FFCC",
                    color2="#00876C",
                    color3="#00211B"
                )

                self.big_scale_marker = Qt.black
                self.fine_scale_marker = Qt.black

            case 18:
                self.setCustomGaugeTheme(
                    color1="#00211B",
                    color2="#00876C",
                    color3="#00FFCC"
                )

                self.big_scale_marker = Qt.white
                self.fine_scale_marker = Qt.white

            case 19:
                self.setCustomGaugeTheme(
                    color1="#001EFF",
                    color2="#001299",
                    color3="#000426"
                )

                self.big_scale_marker = Qt.black
                self.fine_scale_marker = Qt.black

            case 20:
                self.setCustomGaugeTheme(
                    color1="#000426",
                    color2="#001299",
                    color3="#001EFF"
                )

                self.big_scale_marker = Qt.white
                self.fine_scale_marker = Qt.white

            case 21:
                self.setCustomGaugeTheme(
                    color1="#F200FF",
                    color2="#85008C",
                    color3="#240026"
                )

                self.big_scale_marker = Qt.black
                self.fine_scale_marker = Qt.black

            case 22:
                self.setCustomGaugeTheme(
                    color1="#240026",
                    color2="#85008C",
                    color3="#F200FF"
                )

                self.big_scale_marker = Qt.white
                self.fine_scale_marker = Qt.white

            case 23:
                self.setCustomGaugeTheme(
                    color1="#FF0022",
                    color2="#080001",
                    color3="#009991"
                )

                self.big_scale_marker = Qt.white
                self.fine_scale_marker = Qt.white

            case 24:
                self.setCustomGaugeTheme(
                    color1="#009991",
                    color2="#080001",
                    color3="#FF0022"
                )

                self.big_scale_marker = Qt.white
                self.fine_scale_marker = Qt.white

    def setCustomGaugeTheme(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                                   [.5, QColor(str(colors['color2']))],
                                                   [.75, QColor(str(colors['color3']))]])

                    self.needle_center_bg = [
                        [0, QColor(str(colors['color3']))],
                        [0.322581, QColor(str(colors['color1']))],
                        [0.571429, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color3']))]
                    ]

                    self.outer_circle_bg = [
                        [0.0645161, QColor(str(colors['color3']))],
                        [0.36, QColor(str(colors['color1']))],
                        [1, QColor(str(colors['color2']))]
                    ]

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                                   [1, QColor(str(colors['color2']))]])

                    self.needle_center_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color1']))]
                    ]

                    self.outer_circle_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color2']))]
                    ]

            else:

                self.set_scale_polygon_colors([[1, QColor(str(colors['color1']))]])

                self.needle_center_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

                self.outer_circle_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

        else:
            self.setGaugeTheme(0)
            if self.show_custom_widgets_logs:
                print("Custom Gauge Theme: color1 is not defined")

    def setScalePolygonColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                                   [.5, QColor(str(colors['color2']))],
                                                   [.75, QColor(str(colors['color3']))]])

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                                   [1, QColor(str(colors['color2']))]])

            else:

                self.set_scale_polygon_colors([[1, QColor(str(colors['color1']))]])

        else:
            if self.show_custom_widgets_logs:
                print("Custom Gauge Theme: color1 is not defined")

    def setNeedleCenterColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.needle_center_bg = [
                        [0, QColor(str(colors['color3']))],
                        [0.322581, QColor(str(colors['color1']))],
                        [0.571429, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color3']))]
                    ]

                else:

                    self.needle_center_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color1']))]
                    ]

            else:

                self.needle_center_bg = [
                    [1, QColor(str(colors['color1']))]
                ]
        else:
            if self.show_custom_widgets_logs:
                print("Custom Gauge Theme: color1 is not defined")

    def setOuterCircleColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.outer_circle_bg = [
                        [0.0645161, QColor(str(colors['color3']))],
                        [0.37788, QColor(str(colors['color1']))],
                        [1, QColor(str(colors['color2']))]
                    ]

                else:

                    self.outer_circle_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color2']))]
                    ]

            else:

                self.outer_circle_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

        else:
            if self.show_custom_widgets_logs:
                print("Custom Gauge Theme: color1 is not defined")

    def rescale_method(self):
        if self.width() <= self.height():
            self.widget_diameter = self.width()
        else:
            self.widget_diameter = self.height()

        self.change_value_needle_style([QPolygon([
            QPoint(4, 30),
            QPoint(-4, 30),
            QPoint(-2, - int(self.widget_diameter / 2 * self.needle_scale_factor)),
            QPoint(0, - int(self.widget_diameter / 2 * self.needle_scale_factor - 6)),
            QPoint(2, - int(self.widget_diameter / 2 * self.needle_scale_factor))
        ])])

        self.scale_fontsize = self.initial_scale_fontsize * self.widget_diameter / 400
        self.value_fontsize = self.initial_value_fontsize * self.widget_diameter / 400

    def change_value_needle_style(self, design):
        # prepared for multiple needle instrument
        self.value_needle = []
        for i in design:
            self.value_needle.append(i)
        if not self.use_timer_event:
            self.update()

    def updateValue(self, value):

        if value <= self.min_value:
            self.value = self.min_value
        elif value >= self.max_value:
            self.value = self.max_value
        else:
            self.value = value

        self.valueChanged.emit(int(value))

        if not self.use_timer_event:
            self.update()

    def updateAngleOffset(self, offset):
        self.angle_offset = offset
        if not self.use_timer_event:
            self.update()

    def center_horizontal(self, value):
        self.center_horizontal_value = value

    def center_vertical(self, value):
        self.center_vertical_value = value

    def setNeedleColor(self, r=50, g=50, b=50, transparency=255):
        self.needle_color = QColor(r, g, b, transparency)
        self.needle_color_released = self.needle_color

        if not self.use_timer_event:
            self.update()

    def setNeedleColorOnDrag(self, r=50, g=50, b=50, transparency=255):
        self.needle_color_drag = QColor(r, g, b, transparency)

        if not self.use_timer_event:
            self.update()

    def setScaleValueColor(self, r=50, g=50, b=50,transparency=255):
        self.scale_value_color = QColor(r, g, b, transparency)

        if not self.use_timer_event:
            self.update()

    def setDisplayValueColor(self, r=50, g=50, b=50,transparency=255):
        self.display_value_color = QColor(r, g, b, transparency)

        if not self.use_timer_event:
            self.update()

    def set_CenterPointColor(self, r=50, g=50, b=50, transparency=255):
        self.center_point_color = QColor(r, g, b, transparency)

        if not self.use_timer_event:
            self.update()

    def setEnableNeedlePolygon(self, enable=True):
        self.enable_Needle_Polygon = enable

        if not self.use_timer_event:
            self.update()

    def setEnableScaleText(self, enable=True):
        self.enable_scale_text = enable

        if not self.use_timer_event:
            self.update()

    def setEnableBarGraph(self, enable=True):
        self.enable_bar_graph = enable

        if not self.use_timer_event:
            self.update()

    def setEnableValueText(self, enable=True):
        self.enable_value_text = enable

        if not self.use_timer_event:
            self.update()

    def setEnableCenterPoint(self, enable=True):
        self.enable_center_point = enable

        if not self.use_timer_event:
            self.update()

    def setEnableScalePolygon(self, enable=True):
        self.enable_filled_polygon = enable

        if not self.use_timer_event:
            self.update()

    def setEnableBigScaleGrid(self, enable=True):
        self.enable_big_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    def setEnableFineScaleGrid(self, enable=True):
        self.enable_fine_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    def setScalaCount(self, count):
        if count < 1:
            count = 1
        self.scala_count = count

        if not self.use_timer_event:
            self.update()

    def setMinValue(self, minimum):
        if self.value < minimum:
            self.value = minimum
        if minimum >= self.max_value:
            self.min_value = self.max_value - 1
        else:
            self.min_value = minimum

        if not self.use_timer_event:
            self.update()

    def setMaxValue(self, maximum):
        if self.value > maximum:
            self.value = maximum
        if maximum <= self.min_value:
            self.max_value = self.min_value + 1
        else:
            self.max_value = maximum

        if not self.use_timer_event:
            self.update()

    def setScaleStartAngle(self, value):
        # Value range in DEG: 0 - 360
        self.scale_angle_start_value = value

        if not self.use_timer_event:
            self.update()

    def setTotalScaleAngleSize(self, value):
        self.scale_angle_size = value

        if not self.use_timer_event:
            self.update()

    def setGaugeColorOuterRadiusFactor(self, value):
        self.gauge_color_outer_radius_factor = float(value) / 1000

        if not self.use_timer_event:
            self.update()

    def setGaugeColorInnerRadiusFactor(self, value):
        self.gauge_color_inner_radius_factor = float(value) / 1000

        if not self.use_timer_event:
            self.update()

    def set_scale_polygon_colors(self, color_array):
        if 'list' in str(type(color_array)):
            self.scale_polygon_colors = color_array
        elif color_array is None:
            self.scale_polygon_colors = [[.0, Qt.transparent]]
        else:
            self.scale_polygon_colors = [[.0, Qt.transparent]]

        if not self.use_timer_event:
            self.update()

    def get_value_max(self):
        return self.max_value

    def create_polygon_pie(self, outer_radius, inner_raduis, start, lenght, bar_graph=True):
        polygon_pie = QPolygonF()

        n = 360  # angle steps size for full circle

        w = 360 / n  # angle per step

        x = 0
        y = 0

        if not self.enable_bar_graph and bar_graph:
            lenght = int(round((lenght / (self.max_value - self.min_value)) * (self.value - self.min_value)))

        for i in range(lenght + 1):  # add the points of polygon
            t = w * i + start - self.angle_offset
            x = outer_radius * math.cos(math.radians(t))
            y = outer_radius * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))
        # create inner circle line from "start + lenght"-angle to "start"-angle
        for i in range(lenght + 1):  # add the points of polygon
            t = w * (lenght - i) + start - self.angle_offset
            x = inner_raduis * math.cos(math.radians(t))
            y = inner_raduis * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))

        # close outer line
        polygon_pie.append(QPointF(x, y))
        return polygon_pie

    def draw_filled_polygon(self, outline_pen_with=0):
        if not self.scale_polygon_colors is None:
            painter_filled_polygon = QPainter(self)
            painter_filled_polygon.setRenderHint(QPainter.Antialiasing)
            painter_filled_polygon.translate(self.width() / 2, self.height() / 2)

            painter_filled_polygon.setPen(Qt.NoPen)

            self.pen.setWidth(outline_pen_with)
            if outline_pen_with > 0:
                painter_filled_polygon.setPen(self.pen)

            colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 2) - (self.pen.width() / 2)) * self.gauge_color_outer_radius_factor,
                (((self.widget_diameter / 2) - (self.pen.width() / 2)) * self.gauge_color_inner_radius_factor),
                self.scale_angle_start_value, self.scale_angle_size)

            grad = QConicalGradient(QPointF(0, 0), - self.scale_angle_size - self.scale_angle_start_value +
                                    self.angle_offset - 1)

            for eachcolor in self.scale_polygon_colors:
                grad.setColorAt(eachcolor[0], eachcolor[1])
            painter_filled_polygon.setBrush(grad)

            painter_filled_polygon.drawPolygon(colored_scale_polygon)

    def draw_icon_image(self):
        pass

    def draw_big_scaled_marker(self):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        my_painter.translate(self.width() / 2, self.height() / 2)

        self.pen = QPen(self.big_scale_marker)
        self.pen.setWidth(2)
        my_painter.setPen(self.pen)

        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) / float(self.scala_count))
        scale_line_outer_start = self.widget_diameter / 2
        scale_line_lenght = (self.widget_diameter / 2) - (self.widget_diameter / 20)
        for i in range(self.scala_count + 1):
            my_painter.drawLine(scale_line_lenght, 0, scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_scale_marker_values_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.scale_fontname, self.scale_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.scale_value_color)
        painter.setPen(pen_shadow)

        text_radius_factor = 0.8
        text_radius = self.widget_diameter / 2 * text_radius_factor

        scale_per_div = int((self.max_value - self.min_value) / self.scala_count)

        angle_distance = (float(self.scale_angle_size) / float(self.scala_count))
        for i in range(self.scala_count + 1):
            text = str(int(self.min_value + scale_per_div * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(QFont(self.scale_fontname, self.scale_fontsize, QFont.Bold))
            angle = angle_distance * i + float(self.scale_angle_start_value - self.angle_offset)
            x = text_radius * math.cos(math.radians(angle))
            y = text_radius * math.sin(math.radians(angle))

            text = [x - int(w / 2), y - int(h / 2), int(w), int(h), Qt.AlignCenter, text]
            painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])

    def create_fine_scaled_marker(self):

        my_painter = QPainter(self)

        my_painter.setRenderHint(QPainter.Antialiasing)

        my_painter.translate(self.width() / 2, self.height() / 2)

        my_painter.setPen(self.fine_scale_marker)
        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) / float(self.scala_count * self.scala_subdiv_count))
        scale_line_outer_start = self.widget_diameter / 2
        scale_line_lenght = (self.widget_diameter / 2) - (self.widget_diameter / 40)
        for i in range((self.scala_count * self.scala_subdiv_count) + 1):
            my_painter.drawLine(scale_line_lenght, 0, scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_values_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, self.value_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.display_value_color)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor

        text = str(int(self.value))
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname, self.value_fontsize, QFont.Bold))

        angle_end = float(self.scale_angle_start_value + self.scale_angle_size - 360)
        angle = (angle_end - self.scale_angle_start_value) / 2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        text = [x - int(w / 2), y - int(h / 2), int(w), int(h), Qt.AlignCenter, text]
        painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])

    def create_units_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, int(self.value_fontsize / 2.5), QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.display_value_color)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor

        text = str(self.units)
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname, int(self.value_fontsize / 2.5), QFont.Bold))

        angle_end = float(self.scale_angle_start_value + self.scale_angle_size + 180)
        angle = (angle_end - self.scale_angle_start_value) / 2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        text = [x - int(w / 2), y - int(h / 2), int(w), int(h), Qt.AlignCenter, text]
        painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])

    def draw_big_needle_center_point(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 8) - (self.pen.width() / 2)),
            0,
            self.scale_angle_start_value, 360, False)

        grad = QConicalGradient(QPointF(0, 0), 0)

        for eachcolor in self.needle_center_bg:
            grad.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(grad)

        painter.drawPolygon(colored_scale_polygon)

    def draw_outer_circle(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 2) - (self.pen.width())),
            (self.widget_diameter / 6),
            self.scale_angle_start_value / 10, 360, False)

        radial_gradient = QRadialGradient(QPointF(0, 0), self.width())

        for eachcolor in self.outer_circle_bg:
            radial_gradient.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(radial_gradient)

        painter.drawPolygon(colored_scale_polygon)

    def draw_needle(self):
        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.needle_color)
        painter.rotate(((self.value - self.value_offset - self.min_value) * self.scale_angle_size /
                        (self.max_value - self.min_value)) + 90 + self.scale_angle_start_value)

        painter.drawConvexPolygon(self.value_needle[0])

    def resizeEvent(self, event):

        self.rescale_method()

    def paintEvent(self, event):

        self.draw_outer_circle()
        self.draw_icon_image()

        if self.enable_filled_polygon:
            self.draw_filled_polygon()

        if self.enable_fine_scaled_marker:
            self.create_fine_scaled_marker()
        if self.enable_big_scaled_marker:
            self.draw_big_scaled_marker()

        if self.enable_scale_text:
            self.create_scale_marker_values_text()

        if self.enable_value_text:
            self.create_values_text()
            self.create_units_text()

        if self.enable_Needle_Polygon:
            self.draw_needle()

        if self.enable_center_point:
            self.draw_big_needle_center_point()

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QObject):
                try:
                    child.setMouseTracking(flag)
                except Exception:
                    pass
                recursive_set(child)

        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def mouseReleaseEvent(self, QMouseEvent):
        self.needle_color = self.needle_color_released

        if not self.use_timer_event:
            self.update()
        pass

    def leaveEvent(self, event):
        self.needle_color = self.needle_color_released
        self.update()

    def mouseMoveEvent(self, event):
        x, y = event.x() - (self.width() / 2), event.y() - (self.height() / 2)
        if not x == 0:
            angle = math.atan2(y, x) / math.pi * 180

            value = (float(math.fmod(angle - self.scale_angle_start_value + 720, 360)) / \
                     (float(self.scale_angle_size) / float(self.max_value - self.min_value))) + self.min_value

            if (self.value - (self.max_value - self.min_value) * self.value_needle_snapzone) <= \
                    value <= \
                    (self.value + (self.max_value - self.min_value) * self.value_needle_snapzone):
                self.needle_color = self.needle_color_drag

                if value >= self.max_value and self.last_value < (self.max_value - self.min_value) / 2:
                    value = self.max_value
                    self.last_value = self.min_value
                    self.valueChanged.emit(int(value))

                elif value >= self.max_value >= self.last_value:
                    value = self.max_value
                    self.last_value = self.max_value
                    self.valueChanged.emit(int(value))


                else:
                    self.last_value = value
                    self.valueChanged.emit(int(value))

                self.updateValue(value)
