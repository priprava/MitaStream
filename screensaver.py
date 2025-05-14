
import screeninfo, main, os


import sys, main, random, glob, os, screensaver
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, QTimer, Qt
import logging



class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mita Stream")
        w, h = screensaver.get_size_monitor()
        self.resize(w, h)
        self.main = False

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)


        self.video_widget = QVideoWidget()
        self.setCentralWidget(self.video_widget)

        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0.1)

        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setAudioOutput(self.audio_output)

        self.media_player.mediaStatusChanged.connect(self.handle_media_status)

        self.play_stream()

    def play_stream(self):
        video_path = ""
        if main.stream_ready:
            video_path = os.path.abspath("temp/main_stream_subtitle.mp4")
            self.main = True
        else:
            videos = glob.glob(os.path.abspath("screensaver/*"))
            if videos:
                video_path = random.choice(videos)
                self.main = False

        if video_path:
            self.media_player.setSource(QUrl.fromLocalFile(video_path))
            self.media_player.play()

    def handle_media_status(self, status):
        # Когда видео закончилось, запускаем следующее
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            print(f"self.main {self.main}")
            if self.main == True:
                main.create_ready = True
                main.stream_ready = False
            QTimer.singleShot(1000, self.play_stream)  # Небольшая задержка перед следующим видео



def get_size_monitor():
    for monitor in screeninfo.get_monitors():
        return monitor.width, monitor.height

def scrnsvr_main():
    import os
    os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.*=false"
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    import os
    os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.*=false"
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())