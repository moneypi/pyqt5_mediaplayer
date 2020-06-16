import os
import time
import sys
import cv2

FileName = os.path.basename(sys.argv[0])
FilePath = sys.argv[0].replace(FileName, "")

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *


class TestSlider(QSlider):
    def __init__(self, *__args):
        super(TestSlider, self).__init__(*__args)

    def keyPressEvent(self, event):
        QCoreApplication.sendEvent(self.parentWidget(), event)


class m_window(QWidget):
    def __init__(self):
        super(m_window, self).__init__()

        self.media_path = ""
        self.timeLabelWidth = 120
        self.shape = (360, 480)
        self.volume = 50
        self.Slider = TestSlider(Qt.Horizontal, self)
        self.ProgressBarInit()
        self.mplayer = QMediaPlayer(self)
        self.mVideoWin = QVideoWidget(self)
        self.mVideoWin.setGeometry(0, 0, self.shape[1], self.shape[0])
        self.mplayer.setVideoOutput(self.mVideoWin)
        self.mplayer.positionChanged.connect(self.PlaySlide)
        self.mplayer.durationChanged.connect(self.MediaTime)
        # self.SetPlayMedia()
        self.mplayer.setVolume(self.volume)
        self.Slider.setGeometry(self.timeLabelWidth, self.shape[0], self.shape[1] - self.timeLabelWidth, 20)
        self.setWindowTitle("pyqt5Player")
        self.scale = 1.0
        # self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.setFixedSize(int(self.shape[1] * self.scale), int(self.shape[0] * self.scale) + 20)
        self.timeLabel = QLabel(self)
        self.timeLabel.setGeometry(0, self.shape[0], self.timeLabelWidth, 20)
        self.time = 0
        self.timeLabel.setText("0:0:0/0:0:0")
        self.volumeLabel = QLabel(self)
        self.volumeSlider = QSlider(Qt.Vertical, self)
        self.volumeLabel.setGeometry(100, 100, 25, 25)
        self.volumeSlider.setGeometry(100, 125, 25, 100)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.hide()
        self.volumeLabel.hide()
        self.volumeLabel.setAlignment(Qt.AlignCenter)

    def ProgressBarInit(self):
        # self.Slider.setRange(0, 100)
        self.Slider.show()
        self.Slider.sliderMoved.connect(self.valChange)

    def MediaTime(self, time):
        self.Slider.setValue(0)
        self.time = self.mplayer.duration()
        self.Slider.setRange(0, int(self.time))

    def PlaySlide(self, val):
        self.Slider.setValue(int(val))
        current_seconds = int(val / 1000)
        current_hours = int(current_seconds / 3600)
        current_seconds = current_seconds % 3600
        current_minutes = int(current_seconds / 60)
        current_seconds = current_seconds % 60

        total_seconds = int(self.time / 1000)
        total_hours = int(total_seconds / 3600)
        total_seconds = total_seconds % 3600
        total_minutes = int(total_seconds / 60)
        total_seconds = total_seconds % 60

        label_text = str(current_hours) + ":" + str(current_minutes) + ":" + str(current_seconds) + "/" \
                     + str(total_hours) + ":" + str(total_minutes) + ":" + str(total_seconds)
        self.timeLabel.setText(label_text)
        self.volumeSlider.hide()
        self.volumeLabel.hide()

    def SetPlayMedia(self):
        self.media_path = QFileDialog.getOpenFileUrl()[0].toString()[7:]
        print(self.media_path)
        cap = cv2.VideoCapture(self.media_path)
        if cap.isOpened():
            rval, frame = cap.read()
        else:
            return

        cap.release()

        if frame is None:
            return

        self.shape = frame.shape
        self.mVideoWin.setGeometry(0, 0, self.shape[1], self.shape[0])
        self.Slider.setGeometry(self.timeLabelWidth, self.shape[0], self.shape[1] - self.timeLabelWidth, 20)
        self.timeLabel.setGeometry(0, self.shape[0], self.shape[1], 20)
        self.mplayer.stop()
        self.mplayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.media_path)))
        self.mplayer.play()
        self.setWindowTitle(self.media_path)

    def keyPressEvent(self, event):
        # print("event.key")
        if event.key() == Qt.Key_Up:
            print("key up")
            self.volumeSlider.hide()
            self.volumeLabel.hide()
            if self.volume <= 95:
                self.volume += 5
                self.mplayer.setVolume(self.volume)
            self.volumeLabel.setText(str(self.volume))
            self.volumeSlider.setValue(self.volume)
            self.volumeLabel.show()
            self.volumeSlider.show()
            print(self.volume)
        if event.key() == Qt.Key_Down:
            print("key down")
            self.volumeSlider.hide()
            self.volumeLabel.hide()
            if self.volume >= 5:
                self.volume -= 5
                self.mplayer.setVolume(self.volume)
            self.volumeLabel.setText(str(self.volume))
            self.volumeSlider.setValue(self.volume)
            self.volumeLabel.show()
            self.volumeSlider.show()
            print(self.volume)
        if event.key() == Qt.Key_Right:
            print("right")
            self.mplayer.setPosition(self.mplayer.position() + 10 * 1000)
        if event.key() == Qt.Key_Left:
            print("left")
            self.mplayer.setPosition(self.mplayer.position() - 5 * 1000)
        if event.key() == Qt.Key_Space:
            print("space")
            if self.mplayer.state() == QMediaPlayer.PlayingState:
                self.mplayer.pause()
            elif self.mplayer.state() == QMediaPlayer.PausedState:
                self.mplayer.play()
            elif self.mplayer.state() == QMediaPlayer.StoppedState:
                self.SetPlayMedia()
        if event.key() == Qt.Key_Escape:
            quit()

        if event.key() == Qt.Key_0:
            self.scale = 0.5
        if event.key() == Qt.Key_1:
            self.scale = 1.0
        if event.key() == Qt.Key_2:
            self.scale = 1.5
        if event.key() == Qt.Key_3:
            self.scale = 2.0
        if event.key() == Qt.Key_4:
            self.scale = 2.5
        if event.key() == Qt.Key_5:
            self.scale = 3.0
        if event.key() == Qt.Key_6:
            self.scale = 4.0

        self.mVideoWin.resize(int(self.shape[1] * self.scale), int(self.shape[0] * self.scale))
        self.Slider.setGeometry(self.timeLabelWidth, int(self.shape[0] * self.scale),
                                int(self.shape[1] * self.scale) - self.timeLabelWidth, 20)
        self.timeLabel.setGeometry(0, int(self.shape[0] * self.scale), int(self.shape[1] * self.scale), 20)
        self.setFixedSize(int(self.shape[1] * self.scale), int(self.shape[0] * self.scale) + 20)

    def valChange(self):
        print(self.Slider.value())
        self.mplayer.setPosition(int(self.Slider.value()))


app = QApplication(sys.argv)
window = m_window()
window.show()
sys.exit(app.exec_())
