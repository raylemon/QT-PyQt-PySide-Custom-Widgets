try:
    from PySide6 import QtWidgets, QtCore
    from PySide6.QtCore import Qt, QSize
    from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPaintEvent, QFont
except ModuleNotFoundError:
    print("Please install any suitable version of PySide 6")


class SpiralProgressBar(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(SpiralProgressBar, self).__init__(parent)

        self.position_x = 0
        self.position_y = 0
        self.spb_size = 0
        self.pos_factor = 0
        self.size_factor = 0

        self.spb_maxim_size = (0, 0)
        self.spb_minim_size = (0, 0)

        self.spb_dynamic_min = True
        self.spb_dynamic_max = True

        self.no_prog_bar = 3

        self.spb_value = [-48 * 16, -24 * 16, -12 * 16]
        self.spb_minim_value = [0, 0, 0]
        self.spb_maxim_value = [100, 100, 100]
        self.spb_start_pos = [self.StartPosFlags.North] * 3
        self.spb_direction = [self.RotationFlags.Clockwise] * 3

        self.line_width = 5
        self.line_color = [[0, 159, 227]] * 3
        self.line_style = [self.LineStyleFlags.SolidLine] * 3
        self.line_cap = [self.LineCapFlags.RoundCap] * 3
        self.var_width = False
        self.width_incr = 1

        self.path_width = 5
        self.path_color = [[179, 241, 215]] * 3
        self.path_present = True
        self.path_style = [self.LineStyleFlags.SolidLine] * 3
        self.path_independ = False

        self.spb_gap = self.line_width * 2  # GAP BETWEEN THE ROUNDPROGRESS BAR MAKING A SPIRAL PROGRESS BAR.
        self.gap_cngd = False
        self.spb_cng_size = 1

    # ------------------------------------------------------CLASS ENUMERATORS
    class LineStyleFlags:
        SolidLine = Qt.SolidLine
        DotLine = Qt.DotLine
        DashLine = Qt.DashLine

    class LineCapFlags:
        SquareCap = Qt.SquareCap
        RoundCap = Qt.RoundCap

    class RotationFlags:
        Clockwise = -1
        AntiClockwise = 1

    class StartPosFlags:
        North = 90 * 16
        South = -90 * 16
        East = 0 * 16
        West = 180 * 16


    def spb_setMinimumSize(self, width, height):

        self.spb_dynamic_min = False
        self.setMinimumSize(width, height)
        self.spb_minim_size = (width, height)
        self.update()

    def spb_setMaximumSize(self, width, height):

        self.spb_dynamic_max = False
        self.setMaximumSize(width, height)
        self.spb_maxim_size = (width, height)
        self.update()

    def spb_setNoProgressBar(self, num):

        if type(num) != type(5):  # MAKING SURE THAT THE ENTERED IS A NUMBER AND NOT A STRING OR OTHERS
            raise Exception("Supported Format: int and not: " + str(type(num)))
        if 6 >= num >= 2:
            self.no_prog_bar = num
            self.spb_value = []
            self.spb_maxim_value = []
            self.spb_minim_value = []
            self.spb_start_pos = []
            self.spb_direction = []
            self.line_color = []
            self.line_style = []
            self.line_cap = []
            for each in range(0, self.no_prog_bar, 1):
                self.spb_value.append(-12 * self.no_prog_bar * 16 / (each + 1))
                self.spb_maxim_value.append(100)
                self.spb_minim_value.append(0)
                self.spb_start_pos.append(self.StartPosFlags.North)
                self.spb_direction.append(self.RotationFlags.Clockwise)
                self.line_color.append([0, 159, 227])
                self.line_style.append(self.LineStyleFlags.SolidLine)
                self.line_cap.append(self.LineCapFlags.RoundCap)
                self.path_color.append([179, 241, 215])
                self.path_style.append(self.LineStyleFlags.SolidLine)
            self.update()

    def spb_setValue(self, value):  # value: TUPLE OF (value1, value2, value3)

        if type(value) != type(()):  # IF INPUT IS NOT A TUPLE
            raise Exception("Value should be a Tuple and not " + str(type(value)))
        elif len(value) > self.no_prog_bar:  # IF TUPLE LENGTH IS MORE THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length more than number of Progress Bars")
        elif len(value) < self.no_prog_bar:  # IF INPUT TUPLE LENGTH IS LESS THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length less than the number of Progress Bars")
        elif self.spb_value != value:  # IF EVERY THING GOES RIGHT
            for each in range(0, self.no_prog_bar, 1):
                if value[each] != 'nc':  # nc: NOC CHANGE STRING FOR ELEIMINATING THE NO CHANGE PROGRESS VALUES
                    if value[each] < self.spb_minim_value[each]:
                        SpiralProgressBar.convValue(self, self.spb_minim_value[each], each)
                    elif value[each] > self.spb_maxim_value[each]:
                        SpiralProgressBar.convValue(self, self.spb_maxim_value[each], each)
                    else:
                        SpiralProgressBar.convValue(self, value[each], each)
            self.update()

    def spb_setMaximum(self, max_val):

        if type(max_val) != type(()):  # IF INPUT IS NOT A TUPLE
            raise Exception("The Max. for should be in form of a Tuple and not: " + str(type(max_val)))
        elif len(max_val) > self.no_prog_bar:  # IF TUPLE LENGTH IS MORE THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length more than number of Progress Bars")
        elif len(max_val) < self.no_prog_bar:  # IF INPUT TUPLE LENGTH IS LESS THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length less than the number of Progress Bars")
        elif self.spb_maxim_value != max_val:
            for each in range(0, self.no_prog_bar, 1):  # TO AVOID FUTURE DIVISION BY ZERO ERROR
                if max_val[each] == self.spb_minim_value[each]:
                    raise ValueError("Maximum and Minimum Value Cannot be the Same")
            self.spb_maxim_value = list(max_val)
            self.update()

    def spb_setMinimum(self, min_val):

        if type(min_val) != type(()):  # IF INPUT IS NOT A TUPLE
            raise Exception("The Min. for should be in form of a Tuple and not: " + str(type(min_val)))
        elif len(min_val) > self.no_prog_bar:  # IF TUPLE LENGTH IS MORE THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length more than number of Progress Bars")
        elif len(min_val) < self.no_prog_bar:  # IF INPUT TUPLE LENGTH IS LESS THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length less than the number of Progress Bars")
        elif self.spb_minim_value != min_val:
            for each in range(0, self.no_prog_bar, 1):  # TO AVOID FUTURE DIVISION BY ZERO ERROR
                if min_val[each] == self.spb_maxim_value[each]:
                    raise ValueError("Maximum and Minimum Value Cannot be the Same")
            self.spb_minim_value = list(min_val)
            self.update()

    def spb_setRange(self, min_tuple, max_tuple):

        if type(min_tuple) != type(()) or type(max_tuple) != type(()):
            raise Exception("The Minimum and Maximum should be a Tuple")
        elif len(min_tuple) > self.no_prog_bar or len(max_tuple) > self.no_prog_bar:
            raise ValueError("Minimum/Maximum Tuple length exceeds the number of Progress Bar")
        elif len(min_tuple) < self.no_prog_bar or len(max_tuple) < self.no_prog_bar:
            raise ValueError("Minimum/Maximum Tuple length is less than the number of Progress Bar")
        for each in range(0, self.no_prog_bar, 1):
            if min_tuple[each] == max_tuple[each]:
                raise ValueError("Minimum and Maximum cannot be the Same")
        self.spb_minim_value = min_tuple
        self.spb_maxim_value = max_tuple
        self.update()

    def spb_setGap(self, gap):

        if type(gap) != type(5):
            raise ValueError("Gap should be an integer and not: " + str(type(gap)))
        else:
            self.spb_gap = gap
            self.gap_cngd = True
            self.update()

    def spb_setInitialPos(self, position):


        if type(position) != type(()):  # IF INPUT IS NOT A TUPLE
            raise Exception("Position should be a Tuple and not " + str(type(position)))
        elif len(position) > self.no_prog_bar:  # IF TUPLE LENGTH IS MORE THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length more than number of Progress Bars")
        elif len(position) < self.no_prog_bar:  # IF INPUT TUPLE LENGTH IS LESS THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length less than the number of Progress Bars")
        else:
            for each in range(0, self.no_prog_bar, 1):
                if type(position[each]) != type("string"):
                    raise Exception("Position Tuple elements should be String and not: " + str(type(position[each])))
                elif position[each] == 'North':
                    self.spb_start_pos[each] = self.StartPosFlags.North
                elif position[each] == 'South':
                    self.spb_start_pos[each] = self.StartPosFlags.South
                elif position[each] == 'East':
                    self.spb_start_pos[each] = self.StartPosFlags.East
                elif position[each] == 'West':
                    self.spb_start_pos[each] = self.StartPosFlags.West
                else:
                    raise Exception(
                        "Position can hold Property: 'North', 'South', 'East' and 'West' and not: " + position[each])
            self.update()

    def spb_reset(self):


        for each in range(0, self.no_prog_bar, 1):
            SpiralProgressBar.convValue(self, self.spb_minim_value[each], each)
        self.update()

    def spb_setGeometry(self, pos_x, pos_y):


        if type(pos_x) != type(5) or type(pos_y) != type(5):
            raise Exception("Position should be a int and not: X" + str(type(pos_x))) + ", Y: " + str(type(pos_y))
        if self.position_x != pos_x:
            self.position_x = pos_x
        if self.position_y != pos_y:
            self.position_y = pos_y
        self.update()

    def spb_setDirection(self, direction):


        if type(direction) != type(()):  # IF INPUT IS NOT A TUPLE
            raise Exception("Direction should be a Tuple and not " + str(type(direction)))
        elif len(direction) > self.no_prog_bar:  # IF TUPLE LENGTH IS MORE THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length more than number of Progress Bars")
        elif len(direction) < self.no_prog_bar:  # IF INPUT TUPLE LENGTH IS LESS THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length less than the number of Progress Bars")
        else:
            for each in range(0, self.no_prog_bar, 1):
                if type(direction[each]) != type("String"):
                    raise Exception("Direction Tuple elements should be String and not: " + str(type(direction[each])))
                elif direction[each] == 'Clockwise':
                    self.spb_direction[each] = self.RotationFlags.Clockwise
                elif direction[each] == 'AntiClockwise':
                    self.spb_direction[each] = self.RotationFlags.AntiClockwise
                else:
                    raise Exception("Direction can hold Property: 'Clockwise'/'AntiClockwise' and not: " + str(
                        type(direction[each])))
            self.update()

    def variableWidth(self, inp):

        if type(inp) != type(True):
            raise Exception("Variable Width should be a Bool and not " + str(type(inp)))
        else:
            self.var_width = inp
            self.update()

    def spb_widthIncrement(self, increm):

        if type(increm) != type(5):
            raise Exception("Increment should be an integer and not " + str(type(increm)))
        else:
            self.width_incr = increm
            self.update()

    def spb_lineWidth(self, width):

        if type(width) != type(5):
            raise Exception("Width should be an Integer and not " + str(type(width)))
        else:
            self.line_width = width
            if not self.gap_cngd:
                self.spb_gap = self.line_width * 2
            self.update()

    def spb_lineColor(self, color):

        if type(color) != type(()):
            raise Exception("Color should be a Tuple and not " + str(type(Color)))
        elif type(color[0]) != type(()):
            raise Exception("Color should be in Format: ((R, G, B), (R, G, B), (R, G, B)) and not any other")
        elif len(color) > self.no_prog_bar:
            raise ValueError("Tuple length more than number of Progress Bars")
        elif len(color) < self.no_prog_bar:  # IF INPUT TUPLE LENGTH IS LESS THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length less than the number of Progress Bars")
        else:
            for each in range(0, self.no_prog_bar, 1):
                if len(color[each]) != 3:
                    raise Exception('Color should be in format (R, G, B)')
                elif self.line_color[each] != color[each]:
                    self.line_color[each] = color[each]
            self.update()

    def spb_lineStyle(self, style):

        if type(style) != type(()):
            raise Exception("Style should be a tuple and not: " + str(type(style)))
        elif len(style) > self.no_prog_bar:  # IF TUPLE LENGTH IS MORE THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length more than number of Progress Bars")
        elif len(style) < self.no_prog_bar:  # IF INPUT TUPLE LENGTH IS LESS THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length less than the number of Progress Bars")
        else:
            for each in range(0, self.no_prog_bar, 1):
                if type(style[each]) != type("String"):
                    raise Exception("Style Tuple element should be a String and not: " + str(type(style[each])))
                elif style[each] == 'SolidLine':
                    self.line_style[each] = self.LineStyleFlags.SolidLine
                elif style[each] == 'DotLine':
                    self.line_style[each] = self.LineStyleFlags.DotLine
                elif style[each] == 'DashLine':
                    self.line_style[each] = self.LineStyleFlags.DashLine
                else:
                    raise Exception("Style can hold 'SolidLine', DotLine' and 'DashLine' only.")
            self.update()

    def spb_lineCap(self, cap):

        if type(cap) != type(()):
            raise Exception("Cap should be a tuple and not: " + str(type(cap)))
        elif len(cap) > self.no_prog_bar:  # IF TUPLE LENGTH IS MORE THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length more than number of Progress Bars")
        elif len(cap) < self.no_prog_bar:  # IF INPUT TUPLE LENGTH IS LESS THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length less than the number of Progress Bars")
        else:
            for each in range(0, self.no_prog_bar, 1):
                if type(cap[each]) != type("String"):
                    raise Exception('Cap Tuple element should be a String and not a: ' + str(type(cap[each])))
                elif cap[each] == 'SquareCap':
                    self.line_cap[each] = self.LineCapFlags.SquareCap
                elif cap[each] == 'RoundCap':
                    self.line_cap[each] = self.LineCapFlags.RoundCap
                else:
                    raise Exception("Cap can hold 'SquareCap' and 'RoundCap' only")
            self.update()

    def spb_setPathHidden(self, hide):

        if type(hide) != type(True):
            raise Exception("Hidden accept a bool and not: " + str(type(hide)))
        self.path_present = not hide

    def spb_pathColor(self, color):

        if type(color) != type(()):
            raise Exception("Color should be a Tuple and not " + str(type(Color)))
        elif type(color[0]) != type(()):
            raise Exception("Color should be in Format: ((R, G, B), (R, G, B), (R, G, B)) and not any other")
        elif len(color) > self.no_prog_bar:
            raise ValueError("Tuple length more than number of Progress Bars")
        elif len(color) < self.no_prog_bar:  # IF INPUT TUPLE LENGTH IS LESS THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length less than the number of Progress Bars")
        else:
            for each in range(0, self.no_prog_bar, 1):
                if len(color[each]) != 3:
                    raise Exception('Color should be in format (R, G, B)')
                elif self.path_color[each] != color[each]:
                    self.path_color[each] = color[each]
            self.update()


    def spb_MinimumSize(self, dynMax, minim, maxim):
        spb_height = self.height()
        spb_width = self.width()

        if dynMax:
            if spb_width >= spb_height >= minim[1]:
                self.spb_size = spb_height
            elif spb_height > spb_width >= minim[0]:
                self.spb_size = spb_width
        else:
            if spb_width >= spb_height and spb_height <= maxim[1]:
                self.spb_size = spb_height
            elif spb_width < spb_height and spb_width <= maxim[0]:
                self.spb_size = spb_width

    def geometricFactor(self):

        self.pos_factor = self.line_width / 2 + 1
        self.size_factor = self.line_width + 1

    def convValue(self, value, pos):

        self.spb_value[pos] = ((value - self.spb_minim_value[pos]) / (
                self.spb_maxim_value[pos] - self.spb_minim_value[pos])) * 360 * 16
        self.spb_value[pos] = self.spb_direction[pos] * self.spb_value[pos]

    def paintEvent(self, event: QPaintEvent):

        if self.spb_dynamic_min:
            self.setMinimumSize(QSize(self.line_width * 6 + self.path_width * 6, self.line_width * 6 + self.path_width * 6))

        SpiralProgressBar.spb_MinimumSize(self, self.spb_dynamic_max, self.spb_minim_size, self.spb_maxim_size)
        SpiralProgressBar.geometricFactor(self)
        spiral_increm = 0
        spiral_increm2 = 0

        if not self.path_independ:
            self.path_width = self.line_width
        self.tempWidth = self.path_width
        if self.path_present:
            for path in range(0, self.no_prog_bar, 1):
                if self.var_width:  # CREAETS A INCREASING OR DECREASING TYPE OF WITH
                    self.tempWidth = self.tempWidth + self.width_incr
                    if not self.gap_cngd:
                        self.spb_gap = self.tempWidth * 2
                path_painter = QPainter(self)
                path_painter.setRenderHint(QPainter.Antialiasing)
                pen_path = QPen()
                pen_path.setStyle(self.path_style[path])
                pen_path.setWidth(self.tempWidth)
                pen_path.setBrush(QColor(self.path_color[path][0], self.path_color[path][1], self.path_color[path][2]))
                path_painter.setPen(pen_path)
                path_painter.drawArc(self.position_x + self.pos_factor + self.spb_cng_size * spiral_increm2,
                                         self.position_y + self.pos_factor + self.spb_cng_size * spiral_increm2,
                                         self.spb_size - self.size_factor - 2 * self.spb_cng_size * spiral_increm2,
                                         self.spb_size - self.size_factor - 2 * self.spb_cng_size * spiral_increm2,
                                         self.spb_start_pos[path], 360 * 16)
                path_painter.end()
                spiral_increm2 = spiral_increm2 + self.spb_gap

        temp_width = self.line_width  # TEMPWIDTH TEMPORARLY STORES THE LINEWIDTH, USEFUL IN VARIABLE WIDTH OPTION.
        for bar in range(0, self.no_prog_bar, 1):
            if self.var_width:  # CREAETS A INCREASING OR DECREASING TYPE OF WITH
                temp_width = temp_width + self.width_incr
                if not self.gap_cngd:
                    self.spb_gap = self.tempWidth * 2
            line_painter = QPainter(self)
            line_painter.setRenderHint(QPainter.Antialiasing)
            pen_line = QPen()
            pen_line.setStyle(self.line_style[bar])
            pen_line.setWidth(self.tempWidth)
            pen_line.setCapStyle(self.line_cap[bar])
            pen_line.setBrush(QColor(self.line_color[bar][0], self.line_color[bar][1], self.line_color[bar][2]))
            line_painter.setPen(pen_line)
            line_painter.drawArc(self.position_x + self.pos_factor + self.spb_cng_size * spiral_increm,
                                     self.position_y + self.pos_factor + self.spb_cng_size * spiral_increm,
                                     self.spb_size - self.size_factor - 2 * self.spb_cng_size * spiral_increm,
                                     self.spb_size - self.size_factor - 2 * self.spb_cng_size * spiral_increm,
                                     self.spb_start_pos[bar], self.spb_value[bar])
            line_painter.end()
            spiral_increm = spiral_increm + self.spb_gap
