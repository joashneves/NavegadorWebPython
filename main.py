
import sys
import os
from itertools import islice

import requests
from PyQt5.uic.properties import QtGui

import PyQt5.uic.pyuic
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from componentes.BrowserMemory import BrowserMemory
from componentes.Inspetor import ElementInspector  # Importa a Inspecionar elementos

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
        self.browser = []

        # Set URLs for the QWebEngineView widgets
        self.init_ui()
        # Titulo
        self.setGeometry(0, 0, 800, 600)
        self.setWindowIcon(QIcon("./img/icon.svg"))

        self.favoritos_sites_salvos = memoria_navegador.listar_favorito()
        self.load_favoritos()  # Carrega os favoritados anteriores

        # Initialize ElementInspector for context menus
        self.element_inspector = ElementInspector(self, self.browser)

        # Carrega o arquivo CSS e aplica o estilo
        with open("config/style.css", "r") as f:
            self.setStyleSheet(f.read())

    def init_ui(self):
        # Create QTabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setTabsClosable(True)
        self.setCentralWidget(self.tab_widget)

        self.dock_widget = None  # Variável para armazenar o QDockWidget

        self.barra_ferramentas = QToolBar()
        self.addToolBar(self.barra_ferramentas)
        self.barra_ferramentas.setObjectName("barraFerramenta")

        self.tab_widget.currentChanged.connect(self.tab_changed)
        self.tab_index = self.tab_widget.currentIndex()

        self.criar_barra_de_ferramentas() # Cria barra de ferramentas

        # verifica aonde esta o     tab selecionado
        self.tab_index = self.tab_widget.currentIndex()
        print(f"Selected tab index: {self.tab_index}")

        # Add a button to create a new tab
        self.new_tab_button = QPushButton()
        self.new_tab_button.setObjectName("Adicionar_Tab")
        self.new_tab_button.setIcon(QIcon('./img/add.svg'))
        self.new_tab_button.clicked.connect(lambda: self.add_new_tab("http://www.google.com"))
        self.new_tab_button.setToolTip("Adicionar Nova Aba")  # Definindo o texto da dica de ferramenta

        # Adicionar o botão de fechar da primeira aba
        self.tab_widget.setCornerWidget(self.new_tab_button, Qt.TopRightCorner)

        # Set the QTabWidget as the central widget of the QMainWindow
        self.setCentralWidget(self.tab_widget)

        # Inicializa a primeira aba
        self.add_new_tab("http://www.google.com")

    def criar_barra_de_ferramentas(self):
        # Botão Voltar
        self.voltar_botao = QToolButton()
        self.voltar_botao.setIcon(QIcon('./img/left.svg'))
        self.voltar_botao.clicked.connect(self.navigate_back)
        self.voltar_botao.setToolTip("Voltar")
        self.voltar_botao.setObjectName("voltar_botao")  # Definindo um ID único para o botão
        self.voltar_botao.setCursor(Qt.PointingHandCursor)
        self.barra_ferramentas.addWidget(self.voltar_botao)
        # Botão Recarregar
        self.recarregar_botao = QToolButton()
        self.recarregar_botao.setIcon(QIcon('./img/refresh.svg'))
        self.recarregar_botao.clicked.connect(self.navigate_reload)
        self.recarregar_botao.setToolTip("Recarregar")
        self.recarregar_botao.setObjectName("recarregar_botao")  # Definindo um ID único para o botão
        self.recarregar_botao.setCursor(Qt.PointingHandCursor)
        self.barra_ferramentas.addWidget(self.recarregar_botao)
        # Botão Home
        self.home_botao = QToolButton()
        self.home_botao.setIcon(QIcon('./img/home.svg'))
        self.home_botao.clicked.connect(self.load_home)
        self.home_botao.setToolTip("Botão de Home")
        self.home_botao.setObjectName("home_botao")  # Definindo um ID único para o botão
        self.home_botao.setCursor(Qt.PointingHandCursor)
        self.barra_ferramentas.addWidget(self.home_botao)
        # Botão Avançar
        self.avancar_botao = QToolButton()
        self.avancar_botao.setIcon(QIcon('./img/right.svg'))
        self.avancar_botao.clicked.connect(self.navigate_forward)
        self.avancar_botao.setToolTip("Avançar")
        self.avancar_botao.setObjectName("avancar_botao")
        self.avancar_botao.setCursor(Qt.PointingHandCursor)
        self.avancar_botao.setVisible(True)
        self.barra_ferramentas.addWidget(self.avancar_botao)
        # Barra de pesquisa
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        self.urlbar.focusInEvent = self.urlbar_focus_in
        self.urlbar.focusOutEvent = self.urlbar_focus_out
        self.urlbar.setCursor(Qt.PointingHandCursor)
        self.urlbar.textChanged.connect(self.text_changed_event)  # Conectar o evento de mudança de texto
        self.barra_ferramentas.addWidget(self.urlbar)

        self.favoritar = QToolButton()
        self.favoritar.setIcon(QIcon('./img/fav.svg'))
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
        self.historico_botton.setIcon(QIcon('./img/historic.svg'))
        self.historico_botton.setToolTip("Historico")
        self.historico_botton.setCheckable(True)
        self.historico_botton.clicked.connect(self.criar_barra_de_historico)
        self.historico_botton.setContextMenuPolicy(Qt.CustomContextMenu)
        abrir_menu = self.criar_funcao_abrir_menu_historico(self.historico_botton)
        self.historico_botton.customContextMenuRequested.connect(abrir_menu)
        self.configuracaoBarra.addWidget(self.historico_botton)
        self.historico_botton.setCursor(Qt.PointingHandCursor)

    def urlbar_focus_in(self, event):
        self.urlbar.setStyleSheet("QLineEdit { background: white; }")
        QLineEdit.focusInEvent(self.urlbar, event)
        QTimer.singleShot(0, self.urlbar.selectAll)

    def urlbar_focus_out(self, event):
        self.urlbar.setStyleSheet("")
        QLineEdit.focusOutEvent(self.urlbar, event)
    def criar_barra_de_historico(self):
        try:
            if self.dock_widget and self.dock_widget.isVisible():
                self.dock_widget.hide()  # Se sim, esconda-o
            else:
                # Segunda barra de ferramentas
                self.historicoBarra = QVBoxLayout()

                historico_list = memoria_navegador.listar_historico()
                historico_list_last = historico_list[-1:];

                # Crie um QDockWidget
                self.dock_widget = QDockWidget()
                self.dock_widget.setWindowTitle("Historico")
                self.dock_widget.setObjectName("historicoTitulo")  # Defina o nome do objeto para aplicar estilo
                # Defina o QDockWidget como estático e bloqueado
                self.dock_widget.setFeatures(QDockWidget.NoDockWidgetFeatures)

                page1 = QWidget()
                page1.setObjectName("historicoWidget")  # Defina o nome do objeto para aplicar estilo
                exibir = QVBoxLayout()
                for item in historico_list:
                    link = QPushButton(f"{item['titulo']}"  if len(item['titulo']) <= 40 else item['titulo'][:37] + '...')
                    link.clicked.connect(lambda checked, link=item['link']: self.browser[self.tab_index].setUrl(QUrl(link)))
                    link.setObjectName("historicoBotao")  # Defina o nome do objeto para aplicar estilo
                    exibir.addWidget(link)
                page1.setLayout(exibir)

                # Defina o widget como o widget do dock
                self.dock_widget.setWidget(page1)

                # Defina o QToolBox como widget do QDockWidget
                self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

                self.scroll = QScrollArea()

                # Scroll Area Properties
                self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
                self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.scroll.setWidgetResizable(True)
                self.scroll.setWidget(page1)

                self.dock_widget.setWidget(self.scroll)
                # Adicione o QDockWidget à janela principal
                self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        except Exception as e:
            # Escrever mensagem de erro no console
            sys.stderr.write(f'Ocorreu um erro: {e}\n')

    def criar_funcao_abrir_menu_historico(self, objeto):
        def show_custom_context_menu_historico(pos):
            try:
                # Aqui você pode usar o objeto do botão, pois ele foi capturado pela função de encerramento
                print(f'Botão associado: {objeto}')
                menu = QMenu()
                historico_menu = menu.addMenu("Histórico")
                historico_list = memoria_navegador.listar_historico()
                # Percorra somente os 8 primeiros itens da lista
                for item in islice(historico_list, 8):
                    titulo_truncado = item['titulo'] if len(item['titulo']) <= 30 else item['titulo'][:27] + '...'
                    sub_action = QAction(titulo_truncado, self)
                    sub_action.triggered.connect(
                        lambda checked, link=item['link']: self.browser[self.tab_index].setUrl(QUrl(link)))
                    historico_menu.addAction(sub_action)
                # Adicionar Apagar
                apagar_action = QAction("Apagar", self)
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
        if index == 0:
            sys.exit()
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
        # Inicializa o inspetor de elementos

        # Configure context menu for the new browser
        new_browser.setContextMenuPolicy(Qt.CustomContextMenu)
        new_browser.customContextMenuRequested.connect(self.show_context_menu)

    def update_tab_title(self, index, title):
        if len(title) > 26:
            title = title[:26]
        self.tab_widget.setTabText(index, title)
        q_url = self.browser[self.tab_index].url()
        self.update_urlbar(q_url)
        print(f'{index} == {self.tab_index}')
        if index == self.tab_index:
            self.update_title()

    def add_fav(self):
        # Obtém o índice da aba atual
        self.tab_index = self.tab_widget.currentIndex()
        current_browser = self.browser[self.tab_index]

        # Obtém o ícone, título e URL da página atual
        page_icon = current_browser.page().icon()
        page_title = current_browser.page().title()
        page_link = current_browser.page().url().toString()

        # Verifica se o ícone é válido
        if not page_icon.isNull():
            print(f'Fav: {page_title} : {page_link}')
        else:
            page_icon = QIcon("/img/notFound.svg")  # Define um ícone padrão caso o ícone da página seja nulo

        # Verifica se o favorito já existe na memória
        for favorito_site in self.configuracaoBarra.findChildren(QToolButton):
            print(self.configuracaoBarra.findChildren(QToolButton))
            if favorito_site.toolTip() == page_title:
                self.deletar_button(favorito_site)
                break

        # Cria um botão de ferramenta para o favorito
        favorito_site = QToolButton()
        favorito_site.setIcon(page_icon)
        favorito_site.setToolTip(page_title)
        favorito_site.clicked.connect(lambda: self.browser[self.tab_index].setUrl(QUrl(page_link)))
        favorito_site.setCheckable(True)
        favorito_site.setCursor(Qt.PointingHandCursor)
        favorito_site.setContextMenuPolicy(Qt.CustomContextMenu)
        abrir_menu = self.criar_funcao_abrir_menu(favorito_site, QUrl(page_link))
        favorito_site.customContextMenuRequested.connect(abrir_menu)

        # Adiciona o botão de favorito à barra de configuração
        self.configuracaoBarra.addWidget(favorito_site)
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
    def text_changed_event(self, text):
        print(f'Texto alterado: {text}')


    def load_home(self):
        self.tab_index = self.tab_widget.currentIndex()
        self.browser[self.tab_index].setUrl(QUrl("http://www.google.com"))
    def update_title(self):
        title = self.browser[self.tab_index].page().title()
        self.setWindowTitle(f"Gallifrey - {title}")
        current_browser = self.browser[self.tab_index]
        memoria_navegador.adicionar_historico(current_browser)
    def load_favoritos(self):
        # Verificar se a pasta temporária existe e, se não, criá-la
        temp_folder = "temp/icons"
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        # Caminho para o ícone padrão
        default_icon_path = "img/notFound.svg"

        def adicionar_botao(icon):
            # Adicionar o botão de favorito com o ícone padrão em caso de erro
            favorito_site = QToolButton()
            favorito_site.setIcon(QIcon(icon))
            favorito_site.setToolTip(favorito["title"])
            favorito_site.clicked.connect(lambda: self.browser[self.tab_index].setUrl(QUrl(favorito["link"])))
            favorito_site.setCheckable(True)
            favorito_site.setCursor(Qt.PointingHandCursor)
            favorito_site.setContextMenuPolicy(Qt.CustomContextMenu)
            abrir_menu = self.criar_funcao_abrir_menu(favorito_site, favorito["link"])
            favorito_site.customContextMenuRequested.connect(abrir_menu)
            self.configuracaoBarra.addWidget(favorito_site)

        for favorito in self.favoritos_sites_salvos:
            try:
                icon_path = favorito.get("icon_path")
                if icon_path:
                    # Verifica se o ícone já foi baixado
                    if not os.path.exists(icon_path):
                        try:
                            # Baixar o ícone se ainda não estiver presente
                            with open(icon_path, 'wb') as f:
                                icon_response = requests.get(favorito["link"])
                                f.write(icon_response.content)
                        except Exception as download_ex:
                            sys.stderr.write(f"Erro ao baixar o ícone: {download_ex}\n")
                            icon_path = default_icon_path  # Use ícone padrão em caso de falha

                    # Cria um botão de ferramenta para o favorito
                    adicionar_botao(icon_path)

                else:
                    sys.stderr.write(f"Ícone da página não encontrado para: {favorito['title']}\n")
            except Exception as ex:
                sys.stderr.write(f"Erro ao carregar o ícone da página: {ex}\n")
                # Cria um botão de ferramenta para o favorito
                adicionar_botao(default_icon_path)
    def deletar_button(self, objeto):
        objeto.deleteLater()
        print(f'nome {objeto.toolTip()}')
        memoria_navegador.remover_favorito(objeto.toolTip())
        print(f'deletado o botão {objeto}')
    def criar_funcao_abrir_menu(self, objeto, link):
        def show_custom_context_menu_fav(pos):
            # Aqui você pode usar o objeto do botão, pois ele foi capturado pela função de encerramento
            print(f'Botão associado: {objeto}')
            menu = QMenu()
            deletar = menu.addAction("Deletar")
            new_aba_fav = menu.addAction("Abrir nova Aba")
            # Conectar a ação do menu a uma função para deletar o botão
            deletar.triggered.connect(lambda: self.deletar_button(objeto))
            new_aba_fav.triggered.connect( self.criar_funcao_abrir_tab(link))
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
    def show_context_menu(self, position):
        context_menu = QMenu()

        # Adicionar ação para voltar
        back_action = QAction("Voltar", self)
        back_action.triggered.connect(self.navigate_back)
        context_menu.addAction(back_action)

        # Adicionar ação para avançar
        reload_action = QAction("Recarregar", self)
        reload_action.triggered.connect(self.navigate_reload)
        context_menu.addAction(reload_action)

        # Adicionar ação para avançar
        forward_action = QAction("Avançar", self)
        forward_action.triggered.connect(self.navigate_forward)
        context_menu.addAction(forward_action)

        # Adicionar separador
        context_menu.addSeparator()

        # Adicionar ação para inspecionar elemento
        inspect_action = QAction("Inspecionar", self)
        inspect_action.triggered.connect(lambda: self.element_inspector.inspect_element(position))
        context_menu.addAction(inspect_action)

        view_source_action = QAction("Exibir código", self)
        view_source_action.triggered.connect(lambda: self.element_inspector.view_page_source())
        context_menu.addAction(view_source_action)

        context_menu.exec_(self.browser[self.tab_index].mapToGlobal(position))


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())