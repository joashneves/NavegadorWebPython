import sys

import PyQt5.uic.pyuic
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class MainWindow(QMainWindow):
    app = QCoreApplication.instance()
    print(f"PyQt5 version: {PyQt5.uic.pyuic.Version}")
    historico_de_pesquisa = []
    historico = []
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))

        #Titulo
        self.setGeometry(0,0,800,600)
        self.setWindowIcon(QIcon("./img/icon.svg"))

        self.guias_navegador = QToolBar()
        self.addToolBar(self.guias_navegador)
        self.guias_navegador.setFixedHeight(32)
        self.guias_navegador.setMovable(False)
        self.guias_navegador.addSeparator()


        criar_guia_navegador = QToolButton()
        criar_guia_navegador.setText('+')
        criar_guia_navegador.setObjectName("criar_guia_navegador")  # Definindo um ID único para o botão
        self.guias_navegador.addWidget(criar_guia_navegador)

        self.BrowserTab() # chama browser

        # Carrega o arquivo CSS e aplica o estilo
        with open("config/style.css", "r") as f:
            self.setStyleSheet(f.read())

        # Load home page on startup
        self.load_home()

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Loading progress
        if(self.browser.loadProgress):
            self.browser.loadProgress.connect(self.update_loading_progress)

    def BrowserTab(self):
        # Definindo as preferências do navegador
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)

        self.browser.urlChanged.connect(self.update_urlbar) # muda a url da barra
        self.browser.loadFinished.connect(self.update_title) # muda o nome do navegador

        # Evento para mostrar o QWebEngineView quando o mouse estiver próximo da barra de ferramentas
        self.guias_navegador.setMouseTracking(True)
        self.guias_navegador.installEventFilter(self)

        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(self.browser)
        # Evento para mostrar o QWebEngineView quando o mouse estiver próximo
        self.centralWidget().setMouseTracking(True)
        self.centralWidget().installEventFilter(self)

        self.guias_navegador.addSeparator() # Separador das guias para a ferramenta
        # Botão Voltar
        voltar_botao = QToolButton()
        voltar_botao.setText('<')
        voltar_botao.clicked.connect(self.browser.back)
        voltar_botao.setCursor(Qt.PointingHandCursor)
        voltar_botao.setObjectName("voltar_botao")  # Definindo um ID único para o botão
        self.guias_navegador.addWidget(voltar_botao)

        # Botão Recarregar
        recarregar_botao = QToolButton()
        recarregar_botao.setText('R')
        recarregar_botao.clicked.connect(self.browser.reload)
        recarregar_botao.setCursor(Qt.PointingHandCursor)
        recarregar_botao.setObjectName("recarregar_botao")  # Definindo um ID único para o botão
        self.guias_navegador.addWidget(recarregar_botao)

        # Botão Home
        home_botao = QToolButton()
        home_botao.setText('H')
        home_botao.clicked.connect(self.load_home)
        home_botao.setCursor(Qt.PointingHandCursor)
        home_botao.setObjectName("home_botao")  # Definindo um ID único para o botão
        self.guias_navegador.addWidget(home_botao)

        # Botão Avançar
        avancar_botao = QToolButton()
        avancar_botao.setText('>')
        avancar_botao.clicked.connect(self.browser.forward)
        avancar_botao.setCursor(Qt.PointingHandCursor)
        avancar_botao.setObjectName("avancar_botao")
        avancar_botao.setVisible(True)
        self.guias_navegador.addWidget(avancar_botao)

        # Barra de pesquisa
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        self.guias_navegador.addWidget(self.urlbar)

        # Adiciona um espaço vazio para posicionar a barra lateral no final da página
        layout.addStretch()

        # Configuração da barra lateral
        abrir_barra_lateral = QToolButton()
        abrir_barra_lateral.setIcon(QIcon('./img/settings.svg'))
        abrir_barra_lateral.clicked.connect(self.mostrar_barra_lateral)
        abrir_barra_lateral.setCursor(Qt.PointingHandCursor)
        abrir_barra_lateral.setObjectName("abrir_barra_lateral")
        abrir_barra_lateral.setVisible(True)
        self.guias_navegador.addWidget(abrir_barra_lateral)

        self.configuracaoBarra = QToolBar()
        self.configuracaoBarra.setIconSize(QSize(16, 16))
        self.addToolBar(Qt.RightToolBarArea, self.configuracaoBarra)
        self.configuracaoBarra.setVisible(False)

        button_action = QAction(QIcon("/img/settings.svg"), "Config's", self)
        button_action.setStatusTip("This is your button")
        button_action.setCheckable(True)
        self.configuracaoBarra.addAction(button_action)

        button_action2 = QAction(QIcon("/img/settings.svg"), "Fav's", self)
        button_action2.setStatusTip("This is your button2")

        button_action2.setCheckable(True)
        self.configuracaoBarra.addAction(button_action2)

        # Adiciona o navegador à janela central
        self.setCentralWidget(self.browser)

    def toggleMaximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mostrar_barra_lateral(self):
        if self.configuracaoBarra.isVisible():
            self.configuracaoBarra.setVisible(False)
        else:
            self.addToolBar(Qt.RightToolBarArea, self.configuracaoBarra)
            self.configuracaoBarra.setVisible(True)

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
        # Adiciona ao historico de pesquisa
        h = self.historico_de_pesquisa
        if len(h) == 0 or h[-1] != q.toString:
            h.append(q.toString())



    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def load_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(f"Gallifrey - {title}")

        # Adiciona ao historico de pesquisa
        q = QUrl(self.urlbar.text())
        h = self.historico
        if len(h) == 0 or h[-1] != q.toString():
            h.append(q.toString())
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())