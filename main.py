import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))

        self.setWindowIcon(QIcon("./img/icon.svg"))

        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        #Titulo
        self.setWindowTitle("Gallifrey")
        self.setGeometry(100, 100, 800, 600)

        #Barra de Navegação
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Botão Voltar
        voltar_botao = QAction('<', self)
        voltar_botao.triggered.connect(self.browser.back)
        navbar.addAction(voltar_botao)

        # Botão Recarregar
        recarregar_botao = QAction('R', self)
        recarregar_botao.triggered.connect(self.browser.reload)
        navbar.addAction(recarregar_botao)

        # Botão Home
        home_botao = QAction('H', self)
        home_botao.triggered.connect(self.load_home)
        navbar.addAction(home_botao)

        # Botão Avançar
        avancar_botao = QAction('>', self)
        avancar_botao.triggered.connect(self.browser.forward)
        navbar.addAction(avancar_botao)

        # Barra de pesquisa
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.go_url)
        navbar.addWidget(self.url_bar)
        #self.browser.urlChanged.connect(self.update_url)

        # Load home page on startup
        self.load_home()

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Loading progress
        self.browser.loadProgress.connect(self.update_loading_progress)

    def update_loading_progress(self, progress):
        if progress == 100:
            self.status_bar.showMessage("")
        else:
            self.status_bar.showMessage("Loading... {}%".format(progress))
    def go_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))
    def update_url(self, url):
        self.url_bar.setText(url.ToString)
    def load_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))




app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())