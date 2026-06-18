import sys
import re
import yt_dlp
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QProgressBar, QLabel
from PyQt5.QtCore import QThread, pyqtSignal

class DownloadThread(QThread):
    progress_signal = pyqtSignal(float)
    status_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        def my_hook(d):
            if d['status'] == 'downloading':
                # 진행률 계산
                try:
                    total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                    downloaded_bytes = d.get('downloaded_bytes', 0)
                    
                    if total_bytes > 0:
                        percent = (downloaded_bytes / total_bytes) * 100
                        self.progress_signal.emit(percent)
                    elif '_percent_str' in d:
                        # ANSI escape 코드가 포함되어 있을 수 있으므로 제거
                        percent_str = d['_percent_str']
                        clean_str = re.sub(r'\x1b\[[0-9;]*m', '', percent_str).replace('%', '').strip()
                        if clean_str:
                            self.progress_signal.emit(float(clean_str))
                except Exception:
                    pass
                
                speed_str = d.get('_speed_str', 'N/A')
                clean_speed = re.sub(r'\x1b\[[0-9;]*m', '', speed_str).strip()
                eta_str = d.get('_eta_str', 'N/A')
                clean_eta = re.sub(r'\x1b\[[0-9;]*m', '', eta_str).strip()
                
                self.status_signal.emit(f"다운로드 중... (속도: {clean_speed}, 남은 시간: {clean_eta})")
                
            elif d['status'] == 'finished':
                self.progress_signal.emit(100.0)
                self.status_signal.emit("다운로드 완료! 파일 처리 중...")

        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [my_hook],
            'nocolor': True,  # 콘솔 색상 코드 비활성화
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.status_signal.emit("다운로드 준비 중...")
                ydl.download([self.url])
            self.status_signal.emit("모든 작업 완료!")
        except Exception as e:
            self.status_signal.emit(f"오류 발생: {str(e)}")
        finally:
            self.finished_signal.emit()

class DownloaderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('유튜브 다운로더')
        self.resize(600, 200)

        layout = QVBoxLayout()

        # URL 입력 영역
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('다운로드할 유튜브 URL을 입력하세요')
        self.download_btn = QPushButton('다운로드', self)
        self.download_btn.clicked.connect(self.start_download)
        
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.download_btn)

        layout.addLayout(url_layout)

        # 상태 표시 라벨
        self.status_label = QLabel('대기 중...', self)
        layout.addWidget(self.status_label)

        # 진행률 바
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%") # 퍼센트 포맷 지정
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            self.status_label.setText('URL을 입력해주세요.')
            return

        self.download_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_label.setText('다운로드 준비 중...')

        self.thread = DownloadThread(url)
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.status_signal.connect(self.update_status)
        self.thread.finished_signal.connect(self.download_finished)
        self.thread.start()

    def update_progress(self, percent):
        self.progress_bar.setValue(int(percent))

    def update_status(self, status):
        self.status_label.setText(status)

    def download_finished(self):
        self.download_btn.setEnabled(True)
        if "오류" not in self.status_label.text():
            self.status_label.setText('다운로드가 완료되었습니다.')
            self.progress_bar.setValue(100)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DownloaderGUI()
    ex.show()
    sys.exit(app.exec_())
