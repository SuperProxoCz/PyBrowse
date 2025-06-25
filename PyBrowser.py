import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineProfile
from PyQt5.QtCore import QUrl

class Interceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        if url.startswith("file:") or url.startswith("blob:") or url.startswith("data:"):
            info.block(True)

class PyBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.webview = QWebEngineView()
        interceptor = Interceptor()
        QWebEngineProfile.defaultProfile().setRequestInterceptor(interceptor)
        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.load_url)
        layout = QVBoxLayout()
        layout.addWidget(self.address_bar)
        layout.addWidget(self.webview)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_url(self):
        url = self.address_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.webview.setUrl(QUrl(url))

app = QApplication(sys.argv)
window = PyBrowser()
window.show()
sys.exit(app.exec_())
