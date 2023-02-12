import sys
from PyQt5.QtCore import Qt, QThread
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from form_alarm import Ui_MainWindow
from datetime import datetime
from playsound import *


class Work(QThread):
    finish_signal = QtCore.pyqtSignal()  # сигнал для завершения потока

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.disable_sound = True
        self.start_alarm = False

    def run(self):
        """Запускает проверку времени в отдельном потоке"""
        hour = self.main_window.ui.hour.value()
        minutes = self.main_window.ui.minutes.value()
        seconds = self.main_window.ui.seconds.value()
        print(hour, minutes, seconds)
        while self.start_alarm:
            now = datetime.now()
            get_hour = now.hour
            get_minutes = now.minute
            get_seconds = now.second
            if hour == get_hour and minutes == get_minutes and seconds == get_seconds:
                self.finish_signal.emit()
                while self.disable_sound:
                    playsound('melodiya.mp3')
                break


class MyAlarm(QWidget):
    def __init__(self):
        super(MyAlarm, self).__init__(parent=None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # скрывает кнопку "развернуть на весь экран"
        # скрывает кнопку "закрыть"
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.ui.run_alarm_btn.clicked.connect(self.starting_a_thread)
        self.ProgressThread_instance = Work(main_window=self)
        self.ProgressThread_instance.finish_signal.connect(self.my_message_box)
        self.ui.disable_btn.clicked.connect(QApplication.quit)  # закрывает приложение

    def my_message_box(self):
        """Выводит сообщение о том что будильник сработал"""
        self.ui.run_alarm_btn.show()
        result = QMessageBox.information(self, "Будильник!", "DISABLE - Закрывает приложение")
        # При нажатии кнопки Ok в модальном окне прерывает цикл воспроизведения звука
        if result == QMessageBox.Ok:
            self.ProgressThread_instance.disable_sound = False

    def starting_a_thread(self):
        """Запускает отдельный поток"""
        self.ProgressThread_instance.terminate()
        self.ProgressThread_instance.start()
        self.ProgressThread_instance.disable_sound = True
        self.ProgressThread_instance.start_alarm = True


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создаем приложение
    main_prog = MyAlarm()  # Создаем главное окно на которое будет помещаться все о стольные виджеты
    main_prog.show()  # Показываем главное окно
    sys.exit(app.exec_())  # Запускаем приложение(запускает цикл, некие обработчики)
