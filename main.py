from datetime import datetime
import sys
import os

import requests
from PyQt5.uic.properties import QtGui
from bs4 import BeautifulSoup

import PyQt5.uic.pyuic
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QCursor
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

        self.favoritos_sites_salvos = memoria_navegador.listar_favorito()
        self.load_favoritos()  # Carrega os favoritados anteriores

        # Carrega o arquivo CSS e aplica o estilo
        with open("config/style.css", "r") as f:
            self.setStyleSheet(f.read())

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
        self.historico_botton.setContextMenuPolicy(Qt.CustomContextMenu)
        abrir_menu = self.criar_funcao_abrir_menu_historico(self.historico_botton)
        self.historico_botton.customContextMenuRequested.connect(abrir_menu)
        self.configuracaoBarra.addWidget(self.historico_botton)
        self.historico_botton.setCursor(Qt.PointingHandCursor)

        self.configuracaoBarra.addSeparator()
    def criar_funcao_abrir_menu_historico(self, objeto):
        def show_custom_context_menu_historico(pos):
            try:
                # Aqui você pode usar o objeto do botão, pois ele foi capturado pela função de encerramento
                print(f'Botão associado: {objeto}')
                menu = QMenu()
                historico_menu = menu.addMenu("Histórico")
                historico_list = memoria_navegador.listar_historico()
                for item in historico_list:
                    sub_action = QAction(item['titulo'], self)
                    sub_action.triggered.connect(lambda checked, link=item['link']: self.browser[self.tab_index].setUrl(QUrl(link)))
                    historico_menu.addAction(sub_action)
                # Adicionar Apagar
                apagar_action = QAction("Apagar",self)
                apagar_action.triggered.connect(memoria_navegador.deletar_historico)
                menu.addAction(apagar_action)

                menu.exec_(QCursor.pos())  # Exibir o menu na posição do cursor
            except Exception as e:
                # Escrever mensagem de erro no console
                sys.stderr.write(f'Ocorreu um erro: {e}\n')

        return show_custom_context_menu_historico

    def mouseEnterEvent(self, event):
        show_menu_function = self.criar_funcao_abrir_menu_historico(self.sender())
        show_menu_function(event)

    def mouseLeaveEvent(self, event):
        if self.menu_historico:
            self.menu_historico.close()

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
            sys.stderr.write(f"Não consegui acessar a pagina {ex}")
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
        print(f'fav {current_browser}')
        # Verifica se o ícone é válido
        if not page_icon.isNull():
            # Cria um botão de ferramenta para o favorito
            favorito_site = QToolButton()
            favorito_site.setIcon(QIcon(page_icon))
            favorito_site.setToolTip(page_title)
            abrir_tab = self.criar_funcao_abrir_tab(page_link)
            favorito_site.clicked.connect(abrir_tab)
            favorito_site.setCheckable(True)
            favorito_site.setCursor(Qt.PointingHandCursor)
            favorito_site.setContextMenuPolicy(Qt.CustomContextMenu)
            abrir_menu = self.criar_funcao_abrir_menu(favorito_site)
            favorito_site.customContextMenuRequested.connect(abrir_menu)
            self.configuracaoBarra.addWidget(favorito_site)
            # Adiciona nos favoritos
            memoria_navegador.adicionar_favorito(current_browser)
    def mostrar_barra_lateral(self):
        if self.configuracaoBarra.isVisible():
            self.configuracaoBarra.setVisible(False)
        else:
            self.addToolBar(Qt.RightToolBarArea, self.configuracaoBarra)
            self.configuracaoBarra.setVisible(True)
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
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
    def load_home(self):
        self.tab_index = self.tab_widget.currentIndex()
        self.browser[self.tab_index].setUrl(QUrl("http://www.google.com"))
    def update_title(self):
        title = self.browser[self.tab_index].page().title()
        self.setWindowTitle(f"Gallifrey - {title}")
        # Adiciona ao historico de pesquisa
        current_browser = self.browser[self.tab_index]
        memoria_navegador.adicionar_historico(current_browser)
    def load_favoritos(self):
        # Verificar se a pasta temporária existe e, se não, criá-la
        temp_folder = "temp/icons"
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        for favorito in self.favoritos_sites_salvos:
            try:
                icon_path = favorito.get("icon_path")
                if icon_path:
                    # Verifica se o ícone já foi baixado
                    if not os.path.exists(icon_path):
                        # Baixar o ícone se ainda não estiver presente
                        with open(icon_path, 'wb') as f:
                            icon_response = requests.get(favorito["link"])
                            f.write(icon_response.content)

                    # Cria um botão de ferramenta para o favorito
                    favorito_site = QToolButton()
                    favorito_site.setIcon(QIcon(icon_path))
                    favorito_site.setToolTip(favorito["title"])
                    abrir_tab = self.criar_funcao_abrir_tab(favorito["link"])
                    favorito_site.clicked.connect(abrir_tab)
                    favorito_site.setCheckable(True)
                    favorito_site.setCursor(Qt.PointingHandCursor)
                    favorito_site.setContextMenuPolicy(Qt.CustomContextMenu)
                    abrir_menu = self.criar_funcao_abrir_menu(favorito_site)
                    favorito_site.customContextMenuRequested.connect(abrir_menu)
                    self.configuracaoBarra.addWidget(favorito_site)

                else:
                    sys.stderr.write("Ícone da página não encontrado para:", favorito["title"])
            except Exception as ex:
                sys.stderr.write(f"Erro ao carregar o ícone da página:{ex}")
    def deletar_button(self, objeto):
        objeto.deleteLater()
        print(f'nome {objeto.toolTip()}')
        memoria_navegador.remover_favorito(objeto.toolTip())
        print(f'deletado o botão {objeto}')
    def criar_funcao_abrir_menu(self, objeto):
        def show_custom_context_menu_fav(pos):
            # Aqui você pode usar o objeto do botão, pois ele foi capturado pela função de encerramento
            print(f'Botão associado: {objeto}')
            menu = QMenu()
            deletar = menu.addAction("Deletar")
            # Conectar a ação do menu a uma função para deletar o botão
            deletar.triggered.connect(lambda: self.deletar_button(objeto))
            menu.exec_(QCursor.pos())  # Exibir o menu na posição do cursor

        return show_custom_context_menu_fav

    def criar_funcao_abrir_tab(self, url):
        def abrir_tab():
            self.add_new_tab(url)
        return abrir_tab
    def criar_funcao_remover_fav(self, pos, fav):
        def remove_fav():
            self.mostrar_menu_contexto(pos, fav)
        return remove_fav
    def show_custom_context_menu_fav(self,event):
        print(f' criado mas chamado {event}')


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())