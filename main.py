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

        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(self.browser)
        # Evento para mostrar o QWebEngineView quando o mouse estiver próximo
        self.centralWidget().setMouseTracking(True)
        self.centralWidget().installEventFilter(self)

        #Titulo
        self.setWindowTitle("Gallifrey")
        self.setGeometry(0,0,800,600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        #Barra de Navegação
        navbar = QToolBar()
        navbar.setMouseTracking(True)
        navbar.setVisible(True)
        navbar.installEventFilter(self)
        # Conectar os eventos enterEvent e leaveEvent aos métodos correspondentes

        self.addToolBar(navbar) # Add nav bar


        # Evento para mostrar o QWebEngineView quando o mouse estiver próximo da barra de ferramentas
        navbar.setMouseTracking(True)
        navbar.installEventFilter(self)

        # Botão Voltar
        voltar_botao = QToolButton()
        voltar_botao.setText('<')
        voltar_botao.clicked.connect(self.browser.back)
        voltar_botao.setCursor(Qt.PointingHandCursor)
        voltar_botao.setObjectName("voltar_botao")  # Definindo um ID único para o botão
        navbar.addWidget(voltar_botao)

        # Botão Recarregar
        recarregar_botao = QToolButton()
        recarregar_botao.setText('R')
        recarregar_botao.clicked.connect(self.browser.reload)
        recarregar_botao.setCursor(Qt.PointingHandCursor)
        recarregar_botao.setObjectName("recarregar_botao")  # Definindo um ID único para o botão
        navbar.addWidget(recarregar_botao)

        # Botão Home
        home_botao = QToolButton()
        home_botao.setText('H')
        home_botao.clicked.connect(self.load_home)
        home_botao.setCursor(Qt.PointingHandCursor)
        home_botao.setObjectName("home_botao")  # Definindo um ID único para o botão
        navbar.addWidget(home_botao)

        # Botão Avançar
        avancar_botao = QToolButton()
        avancar_botao.setText('>')
        avancar_botao.clicked.connect(self.browser.forward)
        avancar_botao.setCursor(Qt.PointingHandCursor)
        avancar_botao.setObjectName("avancar_botao")  # Definindo um ID único para o botão
        navbar.addWidget(avancar_botao)

        # Barra de pesquisa
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.urlbar)

        #Adicionando Menu
        menuBox = QComboBox()
        menuBox.addItems(['...','Opções', 'Histórico'])
        # Definir ícone apenas para o primeiro item
        menuBox.setItemIcon(0, QIcon('img/settings.svg'))  # Ícone para 'Opções'
        menuBox.currentIndexChanged.connect(self.opcao_selecionada)

        # Add the dropdown button to the navigation bar
        navbar.addWidget(menuBox)

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

    def opcao_selecionada(self, index):
        opcao_selecionada = self.combobox.itemText(index)
        print(f"Opção selecionada: {opcao_selecionada}")

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