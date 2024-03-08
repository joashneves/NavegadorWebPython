import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class MainWindow(QMainWindow):
    app = QCoreApplication.instance()
    print("PyQt5 version:", QCoreApplication.applicationVersion())
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))

        self.setWindowIcon(QIcon("./img/icon.svg"))

        self.browser.urlChanged.connect(self.update_urlbar) # muda a url da barra
        self.browser.loadFinished.connect(self.update_title) # muda o nome do navegador

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
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.urlbar)
        # Estilo da Barra de pesquisa
        self.urlbar.setStyleSheet("""
          padding: 4px; 
          border: 2px solid black;
          border-radius: 12px;
          """)

        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading current page")

        stop_btn.triggered.connect(self.browser.stop)
        navbar.addAction(stop_btn)

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

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            search_query = q.toString().replace(" ", "+")
            url = f"https://www.google.com/search?q={search_query}"
            self.browser.setUrl(QUrl(url))
        else:
            self.browser.setUrl(q)


    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def load_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(f"Gallifrey - {title}")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())