import PyQt5.uic.pyuic
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
class ElementInspector:
    def __init__(self, parent, browsers):
        self.parent = parent
        self.browsers = browsers
        self.dock_widget = None  # Variável para armazenar o QDockWidget

        # Configurar menu de contexto para cada navegador
        for browser in self.browsers:
            browser.setContextMenuPolicy(Qt.CustomContextMenu)
            browser.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        context_menu = QMenu()

        inspect_action = QAction("Inspecionar", self.parent)
        inspect_action.triggered.connect(lambda: self.inspect_element(position))
        context_menu.addAction(inspect_action)

        context_menu.exec_(self.browsers[self.parent.tab_index].mapToGlobal(position))

    def inspect_element(self, position):
        js_code = """
            document.addEventListener('click', function(event) {
                event.preventDefault();
                event.stopPropagation();
                const element = event.target;
                const element_info = `
                    Tag: ${element.tagName}
                    ID: ${element.id}
                    Class: ${element.className}
                    HTML: ${element.outerHTML}
                `;
                console.log(element_info);
                element.style.outline = '2px solid red';  // Destacar o elemento
                element_info;
            }, { once: true });
        """
        self.browsers[self.parent.tab_index].page().runJavaScript(js_code, self.display_inspection)

    def display_inspection(self, element_info):
        # Aqui você pode exibir as informações do elemento em um QDockWidget
        if not self.dock_widget:
            self.dock_widget = QDockWidget("Inspetor", self.parent)
            self.inspector_text = QTextEdit()
            self.dock_widget.setWidget(self.inspector_text)
            self.parent.addDockWidget(Qt.BottomDockWidgetArea, self.dock_widget)
        self.inspector_text.setText(element_info)
        self.dock_widget.setVisible(True)

    def add_browser(self, browser):
        self.browsers.append(browser)
        self.configure_browsers([browser])