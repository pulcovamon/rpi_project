from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QGridLayout,
    QWidget,
    QDialog,
    QLabel
)
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import Qt, QPointF
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot, AxisItem
from PyQt6.QtGui import QPainter
import sys
from datetime import datetime
import temperature_sensor as sensor

class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Weather station')
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setGeometry(0, 0, 480, 320)

        self.tempout_list = []
        self.tempin_list = []
        self.hour_list = []
        self.time_list = []
        self.previous_time = int(datetime.now().strftime("%S"))

        self.tempout_graph = PlotWidget()
        self.tempout_graph.setBackground(None)
        self.tempout_graph.showGrid(x=True, y=True)
        self.data_out = self.tempout_graph.plot(
                    self.hour_list, self.tempout_list)

        self.tempin_graph = PlotWidget()
        self.tempin_graph.setBackground(None)
        self.tempin_graph.showGrid(x=True, y=True)
        self.data_in = self.tempin_graph.plot(
                    self.hour_list, self.tempin_list)

        self.date = QLabel('')
        self.time = QLabel('')
        self.time.setProperty('class', 'time')
    
        self.tempin_label = QLabel('Vnitřní teplota')
        self.tempin = QLabel('')
        self.tempin.setProperty('class', 'temp')
        self.tempout_label = QLabel('Venkovní teplota')
        self.tempout = QLabel('')
        self.tempout.setProperty('class', 'temp')

        self.humiin_label = QLabel('Vnitřní vlhkost')
        self.humiin = QLabel('')
        self.humiin.setProperty('class', 'value')
        self.humiout_label = QLabel('Venkovní vlhkost')
        self.humiout = QLabel('')
        self.humiout.setProperty('class', 'value')

        self.pressout_label = QLabel('Atmosférický tlak')
        self.pressout = QLabel('')
        self.pressout.setProperty('class', 'value')

        self.tempout_plot_label = QLabel('Venkovní teplota')
        self.tempin_plot_label = QLabel('Vnitřní teplota')

        self.layout.addWidget(self.tempin_label, 0, 10, 1, 4)
        self.layout.addWidget(self.tempout_label, 4, 10, 1, 4)
        self.layout.addWidget(self.tempin, 1, 10, 3, 4)
        self.layout.addWidget(self.tempout, 5, 10, 3, 4)

        self.layout.addWidget(self.humiin_label, 8, 10, 1, 4)
        self.layout.addWidget(self.humiout_label, 11, 10, 1, 4)
        self.layout.addWidget(self.humiin, 9, 10, 2, 4)
        self.layout.addWidget(self.humiout, 12, 10, 2, 4)

        self.layout.addWidget(self.pressout_label, 14, 10, 1, 4)
        self.layout.addWidget(self.pressout, 15, 10, 2, 4)

        self.layout.addWidget(self.time, 0, 3, 3, 5,
                                Qt.AlignmentFlag.AlignTop.AlignHCenter)
        self.layout.addWidget(self.date, 0, 0, 1, 3)

        self.layout.addWidget(self.tempin_plot_label, 4, 4, 1, 2,
                                        Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.tempout_plot_label, 10, 4, 1, 2,
                                        Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.tempin_graph, 5, 0, 5, 10)
        self.layout.addWidget(self.tempout_graph, 11, 0, 5, 10)

        self.timer = QTimer()
        self.timer.timeout.connect(self.time_number)
        self.timer.start(1000)
        self.time_number()


    def time_number(self):
        time = datetime.now()
        formatted_time = time.strftime("%H:%M:%S")
        date = time.strftime("%d. %m. %Y")


        self.time.setText(formatted_time)
        self.date.setText(date)

        temperature_in, humidity_in = sensor.inside_values()
        temperature_out, humidity_out, pressure = sensor.outside_values()
        self.tempin.setText(str(temperature_in)+'˚C')
        self.humiin.setText(str(humidity_in)+' %')
        self.tempout.setText(str(temperature_out)+'˚C')
        self.humiout.setText(str(humidity_out)+' %')
        self.pressout.setText(str(pressure)+' kPa')

        current_time = int(datetime.now().strftime("%S"))
        
        if current_time != self.previous_time:
            stamp = datetime.timestamp(time)
            self.previous_time = current_time
            self.tempout_list.append(temperature_out)
            self.tempin_list.append(temperature_in)
            self.hour_list.append(stamp)
            self.time_list.append(current_time)
            if len(self.tempin_list) > 24:
                self.tempout_list.pop(0)
                self.tempin_list.pop(0)
                self.hour_list.pop(0)
                self.time_list.pop(0)

            labels_x = [tuple([self.hour_list[i], str(self.time_list[i])]) for i in range(len(self.tempin_list)) if i%5 == 0]
    
            self.data_in.setData(
                    self.hour_list,
                    self.tempin_list, labels=labels_x)
            self.data_out.setData(
                    self.hour_list,
                    self.tempout_list, labels=labels_x)

            ax_in = self.tempin_graph.getAxis('bottom')
            ax_out = self.tempout_graph.getAxis('bottom')

            ax_in.setTicks([labels_x])
            ax_out.setTicks([labels_x])



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()

    with open('stylesheet.css', 'r') as styles:
        app.setStyleSheet(styles.read())

    window.show()
    sys-exit(app.exec())