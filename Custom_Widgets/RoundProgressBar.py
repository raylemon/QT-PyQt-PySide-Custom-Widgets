try:
    from PySide6 import QtWidgets, QtCore
    from PySide6.QtCore import Qt, QSize
    from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPaintEvent, QFont
except ModuleNotFoundError:
    print("Please install any suitable version of PySide 6")

class RoundProgressBar(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(RoundProgressBar, self).__init__(parent)

        self.position_x = 0
        self.position_y = 0
        self.pos_factor = 0

        self.rpb_minimum_size = (0, 0)
        self.rpb_maximum_size = (0, 0)
        self.rpb_dynamic_min = True
        self.rpb_dynamic_max = True
        self.rpb_size = 0
        self.size_factor = 0

        self.rpb_maximum = 100
        self.rpb_minimum = 0

        self.rpb_type = self.BarStyleFlags.Donut
        self.start_position = self.StartPosFlags.North
        self.rpb_direction = self.RotationFlags.Clockwise

        self.rpb_text_type = self.TextFlags.Percentage
        self.rpb_text_color = (0, 159, 227)
        self.rpb_text_width = self.rpb_size / 8
        self.rpb_text_font = 'Segoe UI'
        self.rpb_text_value = '12%'
        self.rpb_text_ratio = 8
        self.text_factor_x = 0
        self.text_factor_y = 0
        self.dynamic_text = True
        self.rpb_text_active = True

        self.line_width = 5
        self.path_width = 5
        self.rpb_line_style = self.LineStyleFlags.SolidLine
        self.rpb_line_cap = self.LineCapFlags.SquareCap
        self.line_color = (0, 159, 227)
        self.path_color = (218, 218, 218)

        self.rpb_circle_color = (218, 218, 218)
        self.rpb_circle_ratio = 0.8
        self.rpb_circle_pos_x = 0
        self.rpb_circle_pos_y = 0

        self.rpb_pie_color = (200, 200, 200)
        self.rpb_pie_ratio = 1
        self.rpb_pie_pos_x = 0
        self.rpb_pie_pos_y = 0

        self.rpb_value = -45 * 16

        if self.rpb_dynamic_min:
            self.setMinimumSize(QSize(self.line_width * 6 + self.path_width * 6, self.line_width * 6 + self.path_width * 6))

    # ------------------------------------------------------CLASS ENUMERATORS
    class LineStyleFlags:
        SolidLine = Qt.SolidLine
        DotLine = Qt.DotLine
        DashLine = Qt.DashLine

    class LineCapFlags:
        SquareCap = Qt.SquareCap
        RoundCap = Qt.RoundCap

    class BarStyleFlags:
        Donut = 0
        Line = 1
        Pie = 2
        Pizza = 3
        Hybrid1 = 4
        Hybrid2 = 5

    class RotationFlags:
        Clockwise = -1
        AntiClockwise = 1

    class TextFlags:
        Value = 0
        Percentage = 1

    class StartPosFlags:
        North = 90 * 16
        South = -90 * 16
        East = 0 * 16
        West = 180 * 16

    # ------------------------------------------------------METHODS FOR CHANGING THE PROPERTY OF THE ROUNDPROGRESSBAR :SOLTS

    def rpb_setMinimumSize(self, width, height):

        if type(width) != type(5) or type(height) != type(5):
            raise Exception('Sorry Width/Height should be an int')
        self.rpb_dynamic_min = False
        self.setMinimumSize(width, height)
        self.rpb_minimum_size = (width, height)
        self.update()

    def rpb_setMaximumSize(self, width, height):
        if type(width) != type(5) or type(height) != type(5):
            raise Exception('Sorry Width/Height should be an int')
        self.rpb_dynamic_max = False
        self.setMaximumSize(width, height)
        self.rpb_maximum_size = (width, height)
        self.update()

    def rpb_setMaximum(self, maximum):

        if self.rpb_minimum == maximum:  # FOR AVOIDING DIVISION BY ZERO ERROR IN FUTURE
            raise Exception("Maximum and Minimum cannot be the Same")
        if self.rpb_maximum != maximum:
            self.rpb_maximum = maximum
            self.update()

    def rpb_setMinimum(self, minimum):

        if self.rpb_minimum == minimum:  # FOR AVOIDING DIVISION BY ZERO ERROR IN FUTURE
            raise Exception("Maximum and Minimum cannot be the Same")
        if self.rpb_minimum != minimum:
            self.rpb_minimum = minimum
            self.update()

    def rpb_setRange(self, maximum, minimum):

        if minimum > maximum:
            maximum, minimum = minimum, maximum
        if self.rpb_maximum != maximum:
            self.rpb_maximum = maximum
        if self.rpb_minimum != minimum:
            self.rpb_minimum = minimum
        self.update()

    def rpb_setInitialPos(self, pos):

        if pos == 'North':
            self.start_position = self.StartPosFlags.North
        elif pos == 'South':
            self.start_position = self.StartPosFlags.South
        elif pos == 'East':
            self.start_position = self.StartPosFlags.East
        elif pos == 'West':
            self.start_position = self.StartPosFlags.West
        else:
            raise Exception("Initial Position String can be: 'South', 'North'")

    def rpb_setValue(self, value):

        if self.rpb_value != value:
            if value >= self.rpb_maximum:
                RoundProgressBar.convertInputValue(self, self.rpb_maximum)
            elif value < self.rpb_minimum:
                RoundProgressBar.convertInputValue(self, self.rpb_minimum)
            else:
                RoundProgressBar.convertInputValue(self, value)
            self.update()

    def rpb_reset(self):

        RoundProgressBar.convertInputValue(self, self.rpb_minimum)
        self.update()

    def rpb_setGeometry(self, pos_x, pos_y):

        if self.position_x != pos_x:
            self.position_x = pos_x
        if self.position_y != pos_y:
            self.position_y = pos_y
        self.update()

    def rpb_setLineWidth(self, width):

        if type(width) != type(5):
            raise Exception('Line Width should be in int')
        if self.line_width != width:
            self.line_width = width
            self.update()

    def rpb_setLineColor(self, rgb):

        if type(rgb) != type(()):
            raise Exception("Line Color accepts a tuple: (R, G, B).")
        if self.line_color != rgb:
            self.line_color = rgb
            self.update()

    def rpb_setPathColor(self, rgb):

        if type(rgb) != type(()):
            raise Exception("Path Color accepts a tuple: (R, G, B).")
        if self.path_color != rgb:
            self.path_color = rgb
            self.update()

    def rpb_setPathWidth(self, width):

        if type(width) != type(5):
            raise Exception('Path Width should be in int')
        if self.path_width != width:
            self.path_width = width
            self.update()

    def rpb_setDirection(self, direction):

        if direction == 'Clockwise' or direction == -1:
            self.rpb_direction = self.RotationFlags.Clockwise
        elif direction == 'AntiClockwise' or direction == 1:
            self.rpb_direction = self.RotationFlags.AntiClockwise
        else:
            raise Exception("Direction can only be: 'Clockwise' and 'AntiClockwise' and Not: " + str(direction))
        self.update()

    def rpb_setBarStyle(self, style):

        if style == 'Donut':
            self.rpb_type = self.BarStyleFlags.Donut
        elif style == 'Line':
            self.rpb_type = self.BarStyleFlags.Line
        elif style == 'Pie':
            self.rpb_type = self.BarStyleFlags.Pie
        elif style == 'Pizza':
            self.rpb_type = self.BarStyleFlags.Pizza
        elif style == 'Hybrid1':
            self.rpb_type = self.BarStyleFlags.Hybrid1
        elif style == 'Hybrid2':
            self.rpb_type = self.BarStyleFlags.Hybrid2
        else:
            raise Exception(
                "Round Progress Bar has only the following styles: 'Line', 'Donet', 'Hybrid1', 'Pizza', 'Pie' and 'Hybrid2'")
        self.update()

    def rpb_setLineStyle(self, style):

        if style == 'SolidLine':
            self.rpb_line_style = self.LineStyleFlags.SolidLine
        elif style == 'DotLine':
            self.rpb_line_style = self.LineStyleFlags.DotLine
        elif style == 'DashLine':
            self.rpb_line_style = self.LineStyleFlags.DashLine
        else:
            self.rpb_line_style = self.LineStyleFlags.SolidLine

    def rpb_setLineCap(self, cap):

        if cap == 'SquareCap':
            self.rpb_line_cap = self.LineCapFlags.SquareCap
        elif cap == 'RoundCap':
            self.rpb_line_cap = self.LineCapFlags.RoundCap

    def rpb_setTextColor(self, rgb):

        if self.rpb_text_color != rgb:
            self.rpb_text_color = rgb
            self.update()

    def rpb_setTextFont(self, font):
        if self.rpb_text_font != font:
            self.rpb_text_font = font
            self.update()

    def rpb_setTextFormat(self, textTyp):

        if textTyp == 'Value':
            self.rpb_text_type = self.TextFlags.Value
        elif textTyp == 'Percentage':
            self.rpb_text_type = self.TextFlags.Percentage
        else:
            self.rpb_text_type = self.TextFlags.Percentage

    def rpb_setTextRatio(self, ratio):

        if self.rpb_text_ratio != ratio:
            if ratio < 3:
                ratio = 3
            elif ratio > 50:
                ratio = 50
            self.rpb_text_ratio = ratio
            self.update()

    def rpb_setTextWidth(self, width):

        self.dynamic_text = False
        if width > 0:
            self.rpb_text_width = width
            self.update()

    def rpb_setCircleColor(self, rgb):

        if self.rpb_circle_color != rgb:
            self.rpb_circle_color = rgb
            self.update()

    def rpb_setCircleRatio(self, ratio):

        if self.rpb_circle_ratio != ratio:
            self.rpb_circle_ratio = ratio
            self.update()

    def rpb_setPieColor(self, rgb):

        if self.rpb_pie_color != rgb:
            self.rpb_pie_color = rgb
            self.update()

    def rpb_setPieRatio(self, ratio):

        if self.rpb_pie_ratio != ratio:
            self.rpb_pie_ratio = ratio
            self.update()

    def rpb_enableText(self, enable):
      self.rpb_text_active = enable

      self.update()


    def rpb_getSize(self):
       return self.rpb_size

    def rpb_getValue(self):
       return self.rpb_value / 16

    def rpb_getRange(self):
        return self.rpb_minimum, self.rpb_maximum

    def rpb_getTextWidth(self):

        return self.rpb_text_width

    def rpb_MinimumSize(self, dynamic_max, minimum, maximum):

        rpb_height = self.height()
        rpb_width = self.width()
        if dynamic_max:
            if rpb_width >= rpb_height >= minimum[1]:
                self.rpb_size = rpb_height
            elif rpb_height > rpb_width >= minimum[0]:
                self.rpb_size = rpb_width
        else:
            if rpb_width >= rpb_height and rpb_height <= maximum[1]:
                self.rpb_size = rpb_height
            elif rpb_width < rpb_height and rpb_width <= maximum[0]:
                self.rpb_size = rpb_width

    def convertInputValue(self, value):

        self.rpb_value = ((value - self.rpb_minimum) / (self.rpb_maximum - self.rpb_minimum)) * 360 * 16
        self.rpb_value = self.rpb_direction * self.rpb_value
        if self.rpb_text_type == RoundProgressBar.TextFlags.Percentage:
            self.rpb_text_value = str(
                round(((value - self.rpb_minimum) / (self.rpb_maximum - self.rpb_minimum)) * 100)) + "%"
        else:
            self.rpb_text_value = str(value)

    def geometryFactor(self):
        if self.line_width > self.path_width:
            self.pos_factor = self.line_width / 2 + 1
            self.size_factor = self.line_width + 1
        else:
            self.pos_factor = self.path_width / 2 + 1
            self.size_factor = self.path_width + 1

    def rpb_textFactor(self):
        if self.dynamic_text:
            self.rpb_text_width = self.rpb_size / self.rpb_text_ratio
        self.text_factor_x = self.pos_factor + (self.rpb_size - self.size_factor) / 2 - self.rpb_text_width * 0.75 * (
                len(self.rpb_text_value) / 2)
        self.text_factor_y = self.rpb_text_width / 2 + self.rpb_size / 2

    def rpb_circleFactor(self):
        self.rpb_circle_pos_x = self.position_x + self.pos_factor + (self.rpb_size * (1 - self.rpb_circle_ratio)) / 2
        self.rpb_circle_pos_y = self.position_y + self.pos_factor + (self.rpb_size * (1 - self.rpb_circle_ratio)) / 2

    def rpb_pieFactor(self):
        self.rpb_pie_pos_x = self.position_x + self.pos_factor + (self.rpb_size * (1 - self.rpb_pie_ratio)) / 2
        self.rpb_pie_pos_y = self.position_y + self.pos_factor + (self.rpb_size * (1 - self.rpb_pie_ratio)) / 2

    def paintEvent(self, event: QPaintEvent):

        if self.rpb_dynamic_min:
            self.setMinimumSize(QSize(self.line_width * 6 + self.path_width * 6, self.line_width * 6 + self.path_width * 6))

        RoundProgressBar.rpb_MinimumSize(self, self.rpb_dynamic_max, self.rpb_minimum_size, self.rpb_maximum_size)
        RoundProgressBar.geometryFactor(self)
        RoundProgressBar.rpb_textFactor(self)
        RoundProgressBar.rpb_circleFactor(self)
        RoundProgressBar.rpb_pieFactor(self)

        if self.rpb_type == 0:  # DONUT TYPE
            RoundProgressBar.pathComponent(self)
            RoundProgressBar.lineComponent(self)
            RoundProgressBar.textComponent(self)
        elif self.rpb_type == 1:  # LINE TYPE
            RoundProgressBar.lineComponent(self)
            RoundProgressBar.textComponent(self)
        elif self.rpb_type == 2:  # Pie
            RoundProgressBar.pieComponent(self)
            RoundProgressBar.textComponent(self)
        elif self.rpb_type == 3:  # PIZZA
            RoundProgressBar.circleComponent(self)
            RoundProgressBar.lineComponent(self)
            RoundProgressBar.textComponent(self)
        elif self.rpb_type == 4:  # HYBRID1
            RoundProgressBar.circleComponent(self)
            RoundProgressBar.pathComponent(self)
            RoundProgressBar.lineComponent(self)
            RoundProgressBar.textComponent(self)
        elif self.rpb_type == 5:  # HYBRID2
            RoundProgressBar.pieComponent(self)
            RoundProgressBar.lineComponent(self)
            RoundProgressBar.textComponent(self)

    def lineComponent(self):
        line_painter = QPainter(self)
        line_painter.setRenderHint(QPainter.Antialiasing)
        pen_line = QPen()
        pen_line.setStyle(self.rpb_line_style)
        pen_line.setWidth(self.line_width)
        pen_line.setBrush(QColor(self.line_color[0], self.line_color[1], self.line_color[2]))
        pen_line.setCapStyle(self.rpb_line_cap)
        pen_line.setJoinStyle(Qt.RoundJoin)
        line_painter.setPen(pen_line)
        line_painter.drawArc(self.position_x + self.pos_factor, self.position_y + self.pos_factor,
                            self.rpb_size - self.size_factor, self.rpb_size - self.size_factor, self.start_position,
                            self.rpb_value)
        line_painter.end()

    def pathComponent(self):
        path_painter = QPainter(self)
        path_painter.setRenderHint(QPainter.Antialiasing)
        pen_path = QPen()
        pen_path.setStyle(Qt.SolidLine)
        pen_path.setWidth(self.path_width)
        pen_path.setBrush(QColor(self.path_color[0], self.path_color[1], self.path_color[2]))
        pen_path.setCapStyle(Qt.RoundCap)
        pen_path.setJoinStyle(Qt.RoundJoin)
        path_painter.setPen(pen_path)
        path_painter.drawArc(self.position_x + self.pos_factor, self.position_y + self.pos_factor,
                            self.rpb_size - self.size_factor, self.rpb_size - self.size_factor, 0, 360 * 16)
        path_painter.end()

    def textComponent(self):
        if self.rpb_text_active:
            text_painter = QPainter(self)
            pen_text = QPen()
            pen_text.setColor(QColor(self.rpb_text_color[0], self.rpb_text_color[1], self.rpb_text_color[2]))
            text_painter.setPen(pen_text)
            font_text = QFont()
            font_text.setFamily(self.rpb_text_font)
            font_text.setPointSize(self.rpb_text_width)
            text_painter.setFont(font_text)
            text_painter.drawText(self.position_x + self.text_factor_x, self.position_y + self.text_factor_y,
                                 self.rpb_text_value)
            text_painter.end()

    def circleComponent(self):
        circle_painter = QPainter(self)
        pen_circle = QPen()
        pen_circle.setWidth(0)
        pen_circle.setColor(QColor(self.rpb_circle_color[0], self.rpb_circle_color[1], self.rpb_circle_color[2]))
        circle_painter.setRenderHint(QPainter.Antialiasing)
        circle_painter.setPen(pen_circle)
        circle_painter.setBrush(QColor(self.rpb_circle_color[0], self.rpb_circle_color[1], self.rpb_circle_color[2]))
        circle_painter.drawEllipse(self.rpb_circle_pos_x, self.rpb_circle_pos_y,
                                  int((self.rpb_size - self.size_factor) * self.rpb_circle_ratio),
                                  int((self.rpb_size - self.size_factor) * self.rpb_circle_ratio))

    def pieComponent(self):
        pie_painter = QPainter(self)
        pen_pie = QPen()
        pen_pie.setWidth(0)
        pen_pie.setColor(QColor(self.rpb_pie_color[0], self.rpb_pie_color[1], self.rpb_pie_color[2]))
        pie_painter.setRenderHint(QPainter.Antialiasing)
        pie_painter.setPen(pen_pie)
        pie_painter.setBrush(QColor(self.rpb_pie_color[0], self.rpb_pie_color[1], self.rpb_pie_color[2]))
        pie_painter.drawPie(self.rpb_pie_pos_x, self.rpb_pie_pos_y, (self.rpb_size - self.size_factor) * self.rpb_pie_ratio,
                           (self.rpb_size - self.size_factor) * self.rpb_pie_ratio, self.start_position, self.rpb_value)
