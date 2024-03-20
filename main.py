from datetime import datetime
import sys

import PyQt5.uic.pyuic
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from componentes.BrowserMemory import BrowserMemory

# Uso do BrowserMemory
memoria_navegador = BrowserMemory()

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

        # Carrega o arquivo CSS e aplica o estilo
        with open("config/style.css", "r") as f:
            self.setStyleSheet(f.read())
        """
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Loading progress
        if(self.browser.loadProgress):
            self.browser.loadProgress.connect(self.update_loading_progress)"""

    def init_ui(self):
        # Create QTabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setTabsClosable(True)
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
        self.new_tab_button = QPushButton()
        self.new_tab_button.setObjectName("Adicionar_Tab")
        self.new_tab_button.setIcon(QIcon('./img/barra.svg'))
        self.new_tab_button.clicked.connect(lambda: self.add_new_tab("http://www.google.com"))
        self.new_tab_button.setToolTip("Adicionar Nova Aba")  # Definindo o texto da dica de ferramenta

        # Adicionar o botão de fechar da primeira aba
        self.tab_widget.setCornerWidget(self.new_tab_button, Qt.TopRightCorner)

        # Set the QTabWidget as the central widget of the QMainWindow
        self.setCentralWidget(self.tab_widget)
    def criar_barra_de_ferramentas(self):
        # Botão Voltar
        self.voltar_botao = QToolButton()
        self.voltar_botao.setText('<')
        self.voltar_botao.clicked.connect(self.navigate_back)
        self.voltar_botao.setToolTip("Voltar")
        self.voltar_botao.setObjectName("voltar_botao")  # Definindo um ID único para o botão
        self.barra_ferramentas.addWidget(self.voltar_botao)
        # Botão Recarregar
        self.recarregar_botao = QToolButton()
        self.recarregar_botao.setText('R')
        self.recarregar_botao.clicked.connect(self.navigate_reload)
        self.recarregar_botao.setToolTip("Recarregar")
        self.recarregar_botao.setObjectName("recarregar_botao")  # Definindo um ID único para o botão
        self.barra_ferramentas.addWidget(self.recarregar_botao)
        # Botão Home
        self.home_botao = QToolButton()
        self.home_botao.setText('H')
        self.home_botao.clicked.connect(self.load_home)
        self.home_botao.setToolTip("Botão de Home")
        self.home_botao.setObjectName("home_botao")  # Definindo um ID único para o botão
        self.barra_ferramentas.addWidget(self.home_botao)
        # Botão Avançar
        self.avancar_botao = QToolButton()
        self.avancar_botao.setText('>')
        self.avancar_botao.clicked.connect(self.navigate_forward)
        self.avancar_botao.setToolTip("Avançar")
        self.avancar_botao.setObjectName("avancar_botao")
        self.avancar_botao.setVisible(True)
        self.barra_ferramentas.addWidget(self.avancar_botao)
        # Barra de pesquisa
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        self.barra_ferramentas.addWidget(self.urlbar)

        self.favoritar = QToolButton()
        self.favoritar.setIcon(QIcon('./img/config.svg'))
        self.favoritar.setToolTip("Favoritar")
        self.favoritar.setCheckable(True)
        self.favoritar.clicked.connect(self.add_fav)
        self.barra_ferramentas.addWidget(self.favoritar)
        self.favoritar.setCursor(Qt.PointingHandCursor)

        self.abrir_barra_lateral = QToolButton()
        self.abrir_barra_lateral.setIcon(QIcon('./img/barra.svg'))
        self.abrir_barra_lateral.clicked.connect(self.mostrar_barra_lateral)
        self.abrir_barra_lateral.setCursor(Qt.PointingHandCursor)
        self.abrir_barra_lateral.setToolTip("Barra lateral")
        self.abrir_barra_lateral.setObjectName("abrir_barra_lateral")
        self.abrir_barra_lateral.setVisible(True)
        self.barra_ferramentas.addWidget(self.abrir_barra_lateral)

        # Configuração da barra lateral
        self.configuracaoBarra = QToolBar()
        self.addToolBar(Qt.RightToolBarArea, self.configuracaoBarra)
        self.configuracaoBarra.setCursor(Qt.PointingHandCursor)
        self.configuracaoBarra.setVisible(True)

        self.congiguracao_navegador = QToolButton()
        self.congiguracao_navegador.setIcon(QIcon('./img/config.svg'))
        self.congiguracao_navegador.setToolTip("Configuração")
        self.congiguracao_navegador.setCheckable(True)
        self.configuracaoBarra.addWidget(self.congiguracao_navegador)
        self.congiguracao_navegador.setCursor(Qt.PointingHandCursor)

        self.historico_botton = QToolButton()
        self.historico_botton.setIcon(QIcon('./img/config.svg'))
        self.historico_botton.setToolTip("Historico")
        self.historico_botton.setCheckable(True)
        self.configuracaoBarra.addWidget(self.historico_botton)
        self.historico_botton.setCursor(Qt.PointingHandCursor)

        self.configuracaoBarra.addSeparator()

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
        self.tab_index = self.tab_widget.currentIndex()
        for i, browser in enumerate(self.browser):
            browser.titleChanged.connect(lambda title, index=i: self.update_tab_title(index, title))
            # Atualizar a URL do QWebEngineView correspondente à aba selecionada
        try:
            q_url = self.browser[self.tab_index].url()
            self.update_urlbar(q_url)
            print(f"alterado {q_url.toString()}")
        except Exception as ex:
            print(f"Não consegui acessar a pagina {ex}")
    def tab_closed(self, index):
        print(index)
        self.tab_widget.removeTab(index)
        self.browser[index].close()
        del self.browser[index]
        self.reorganize_tabs()
    def reorganize_tabs(self):
        for i in range(len(self.browser)):
            self.tab_widget.setTabText(i, f'Tab {i+1}')
    def add_new_tab(self, link):
        # Aumentar o tamanho da lista para incluir um novo elemento
        self.browser.append(QWebEngineView())

        # Create a new QWebEngineView
        new_browser = self.browser[len(self.browser) - 1]
        new_browser.setUrl(QUrl(link))
        page_title = new_browser.page().title()

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

        self.tab_widget.tabCloseRequested.connect(self.tab_closed)
        # Add the new tab to the QTabWidget
        self.tab_widget.addTab(new_widget, 'Nova aba')

    def update_tab_title(self, index, title):
        if len(title) > 26:
            title = title[:26]
        self.tab_widget.setTabText(index, title)
        q_url = self.browser[self.tab_index].url()
        self.update_urlbar(q_url)
        self.update_title()

    def add_fav(self):
        self.tab_index = self.tab_widget.currentIndex()
        current_browser = self.browser[self.tab_index]

        # Obtém o ícone da página atual
        page_icon = current_browser.page().icon()
        page_title = current_browser.page().title()
        page_link = current_browser.page().url()
        print(f'fav {page_link.toString()}')
        # Verifica se o ícone é válido
        if not page_icon.isNull():
            # Cria um botão de ferramenta para o favorito
            self.favorito_site = QToolButton()
            self.favorito_site.setIcon(QIcon(page_icon))
            self.favorito_site.setToolTip(f"{page_title}")
            self.favorito_site.clicked.connect(lambda: self.add_new_tab(page_link))
            self.favorito_site.setCheckable(True)
            self.configuracaoBarra.addWidget(self.favorito_site)
            self.favorito_site.setCursor(Qt.PointingHandCursor)
        # Exemplo de como adicionar um favorito
        memoria_navegador.adicionar_favorito(page_link.toString())
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
        """
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
        print(q.toString())
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
    def load_home(self):
        self.tab_index = self.tab_widget.currentIndex()
        self.browser[self.tab_index].setUrl(QUrl("http://www.google.com"))
    def update_title(self):
        title = self.browser[self.tab_index].page().title()
        self.setWindowTitle(f"Gallifrey - {title}")
        # Adiciona ao historico de pesquisa
        q = QUrl(self.urlbar.text())
        h = self.historico
        data = datetime.now()
        pagina = [title, q.toString(), data.strftime("%d/%m/%Y")]
        if len(h) == 0 or h[-1] != pagina:
            h.append(pagina)
        #print(h)
    def load_memory(self):
        self.tab_index = self.tab_widget.currentIndex()
        current_browser = self.browser[self.tab_index]

        # Obtém o ícone da página atual
        page_icon = current_browser.page().icon()
        page_title = current_browser.page().title()
        page_link = current_browser.page().url()
        print(memoria_navegador)
        # Verifica se o ícone é válido
        if not page_icon.isNull():
            # Cria um botão de ferramenta para o favorito
            self.favorito_site = QToolButton()
            self.favorito_site.setIcon(QIcon(page_icon))
            self.favorito_site.setToolTip(f"{page_title}")
            self.favorito_site.clicked.connect(lambda: self.add_new_tab(page_link))
            self.favorito_site.setCheckable(True)
            self.configuracaoBarra.addWidget(self.favorito_site)
            self.favorito_site.setCursor(Qt.PointingHandCursor)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())