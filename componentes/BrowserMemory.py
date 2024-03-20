import json

class BrowserMemory:
    def __init__(self):
        self.favoritos = []
        self.historico = []
        self.tabs = []

    def adicionar_favorito(self, url):
        if url not in self.favoritos:
            self.favoritos.append(url)
            self._salvar_memoria()

    def remover_favorito(self, url):
        if url in self.favoritos:
            self.favoritos.remove(url)
            self._salvar_memoria()

    def adicionar_historico(self, url):
        self.historico.append(url)
        self._salvar_memoria()

    def adicionar_tab(self, url):
        self.tabs.append(url)
        self._salvar_memoria()

    def remover_tab(self, url):
        if url in self.tabs:
            self.tabs.remove(url)
            self._salvar_memoria()

    def _salvar_memoria(self):
        memoria = {
            "favoritos": self.favoritos,
            "historico": self.historico,
            "tabs": self.tabs
        }
        with open("memoria.json", "w") as file:
            json.dump(memoria, file)


    def carregar_memoria(self):
        try:
            with open("memoria.json", "r") as file:
                memoria = json.load(file)
                self.favoritos = memoria.get("favoritos", [])
                self.historico = memoria.get("historico", [])
                self.tabs = memoria.get("tabs", [])
        except FileNotFoundError:
            # Se o arquivo não existe, cria um novo
            self._salvar_memoria()


