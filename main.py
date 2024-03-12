from datetime import datetime
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

        # Create list of QWebEngineView widgets
        self.browser = [QWebEngineView() for _ in range(2)]

        # Set URLs for the QWebEngineView widgets
        for i, browser in enumerate(self.browser):
            browser.setUrl(QUrl("http://www.google.com"))

        self.init_ui()
        # Titulo
        self.setGeometry(0, 0, 800, 600)
        self.setWindowIcon(QIcon("./img/icon.svg"))
        """
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
            self.browser.loadProgress.connect(self.update_loading_progress)"""

    def init_ui(self):
        # Create QTabWidget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.barra_ferramentas = QToolBar()
        self.addToolBar(self.barra_ferramentas)

        self.tab_widget.currentChanged.connect(self.tab_changed)
        self.tab_index = self.tab_widget.currentIndex()

        # Create QWidget for the first tab
        self.widget_1 = QWidget()
        self.layout_1 = QVBoxLayout(self.widget_1)

        self.layout_1.addWidget(self.browser[0])

        # Add the first widget to the QTabWidget
        self.tab_widget.addTab(self.widget_1, 'Tab 1')

        # Create QWidget for the second tab
        self.widget_2 = QWidget()
        self.layout_2 = QVBoxLayout(self.widget_2)

        self.layout_2.addWidget(self.browser[1])

        # Add the second widget to the QTabWidget
        self.tab_widget.addTab(self.widget_2, 'Tab 2')

        self.criar_barra_de_ferramentas() # Cria barra de ferramentas

        # verifica aonde esta o     tab selecionado
        self.tab_index = self.tab_widget.currentIndex()
        print(f"Selected tab index: {self.tab_index}")

        # Add a button to create a new tab
        self.new_tab_button = QPushButton('New Tab')
        self.new_tab_button.clicked.connect(self.add_new_tab)

        # Adicionar o botão de fechar da primeira aba
        self.tab_widget.setCornerWidget(self.new_tab_button, Qt.TopRightCorner)

        # Set the QTabWidget as the central widget of the QMainWindow
        self.setCentralWidget(self.tab_widget)

    def criar_barra_de_ferramentas(self):
        # Botão Voltar
        self.voltar_botao = QToolButton()
        self.voltar_botao.setText('<')
        self.voltar_botao.clicked.connect(self.navigate_back)
        self.voltar_botao.setObjectName("voltar_botao")  # Definindo um ID único para o botão
        self.barra_ferramentas.addWidget(self.voltar_botao)
        # Botão Recarregar
        self.recarregar_botao = QToolButton()
        self.recarregar_botao.setText('R')
        self.recarregar_botao.clicked.connect(self.navigate_reload)
        self.recarregar_botao.setObjectName("recarregar_botao")  # Definindo um ID único para o botão
        self.barra_ferramentas.addWidget(self.recarregar_botao)
        # Botão Home
        self.home_botao = QToolButton()
        self.home_botao.setText('H')
        self.home_botao.clicked.connect(self.load_home)
        self.home_botao.setObjectName("home_botao")  # Definindo um ID único para o botão
        self.barra_ferramentas.addWidget(self.home_botao)
        # Botão Avançar
        self.avancar_botao = QToolButton()
        self.avancar_botao.setText('>')
        self.avancar_botao.clicked.connect(self.navigate_forward)
        self.avancar_botao.setObjectName("avancar_botao")
        self.avancar_botao.setVisible(True)
        self.barra_ferramentas.addWidget(self.avancar_botao)
        # Barra de pesquisa
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        self.barra_ferramentas.addWidget(self.urlbar)
    def navigate_reload(self):
        self.tab_index = self.tab_widget.currentIndex()
        self.browser[self.tab_index].reload()
    def navigate_back(self):
        self.tab_index = self.tab_widget.currentIndex()
        self.browser[self.tab_index].back()

    def navigate_forward(self):
        self.tab_index = self.tab_widget.currentIndex()
        self.browser[self.tab_index].forward()

    def tab_changed(self):
        for i, browser in enumerate(self.browser):
            browser.titleChanged.connect(lambda title, index=i: self.update_tab_title(index, title))

    def update_tab_title(self, index, title):
        if len(title) > 5:
            title = title[:5]
        self.tab_widget.setTabText(index, title)

    def add_new_tab(self):
        # Aumentar o tamanho da lista para incluir um novo elemento
        self.browser.append(QWebEngineView())

        # Create a new QWebEngineView
        new_browser = self.browser[len(self.browser) - 1]
        new_browser.setUrl(QUrl("http://www.google.com"))

        print(len(self.browser))

        # Definindo as preferências do navegador
        settings = new_browser.settings()
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard,  True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)

        # Create a new QWidget for the new tab
        new_widget = QWidget()
        new_layout = QVBoxLayout(new_widget)
        new_layout.addWidget(new_browser)

        close_button = QToolButton()
        close_button.setText('X')
        close_button.setStyleSheet('QToolButton { border: none; }')
        close_button.clicked.connect(new_widget.close)
        self.barra_ferramentas.addWidget(close_button)

        # Create a horizontal layout for the new widget and close button
        self.layout = QHBoxLayout()
        self.layout.addWidget(new_widget)
        self.layout.addWidget(close_button)

        # Add the new tab to the QTabWidget
        self.tab_widget.addTab(QWidget(), 'Nova tab')
        self.tab_widget.widget(self.tab_widget.count() - 1).setLayout(self.layout)

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

        self.barra_ferramentas = QDockWidget("barra_ferramentas")
        self.layout_1.addWidget(self.barra_ferramentas)

        # Evento para mostrar o QWebEngineView quando o mouse estiver próximo da barra de ferramentas
        self.barra_ferramentas.setMouseTracking(True)
        self.barra_ferramentas.installEventFilter(self)

        self.setCentralWidget(self.browser)
        # Evento para mostrar o QWebEngineView quando o mouse estiver próximo
        self.centralWidget().setMouseTracking(True)
        self.centralWidget().installEventFilter(self)

        """        # Configuração da barra lateral
        abrir_barra_lateral = QToolButton()
        abrir_barra_lateral.setIcon(QIcon('./img/settings.svg'))
        abrir_barra_lateral.clicked.connect(self.mostrar_barra_lateral)
        abrir_barra_lateral.setCursor(Qt.PointingHandCursor)
        abrir_barra_lateral.setObjectName("abrir_barra_lateral")
        abrir_barra_lateral.setVisible(True)
        self.barra_ferramentas.addWidget(abrir_barra_lateral)

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
        self.configuracaoBarra.addAction(button_action2)"""
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
        self.tab_index = self.tab_widget.currentIndex()
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            search_query = q.toString().replace(" ", "+")
            url = f"https://www.google.com/search?q={search_query}"
            self.browser[self.tab_index].setUrl(QUrl(url))
        else:
            self.browser[self.tab_index].setUrl(q)
        # Adiciona ao historico de pesquisa
        h = self.historico_de_pesquisa
        if len(h) == 0 or h[-1] != q.toString:
            h.append(q.toString())
    def update_urlbar(self, q):
        self.tab_index = self.tab_widget.currentIndex()
        self.urlbar[self.tab_index].setText(q.toString())
        self.urlbar[self.tab_index].setCursorPosition(0)
    def load_home(self):
        self.tab_index = self.tab_widget.currentIndex()
        self.browser[self.tab_index].setUrl(QUrl("http://www.google.com"))
    def update_title(self):
        title = self.browser[self.tab_index].page().title()
        self.setWindowTitle(f"Gallifrey - {title}")

        # Adiciona ao historico de pesquisa
        q = QUrl(self.urlbar[0].text())
        h = self.historico
        data = datetime.now()
        pagina = [title, q.toString(), data.strftime("%d/%m/%Y")]
        if len(h) == 0 or h[-1] != pagina:
            h.append(pagina)
        print(h)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())