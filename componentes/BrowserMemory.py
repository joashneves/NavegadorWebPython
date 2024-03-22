import json

class BrowserMemory:
    def __init__(self):
        self.favoritos = []
        self.historico = []
        self.tabs = []
        self.carregar_memoria()

    def listar_favorito(self):
        return self.favoritos

    def adicionar_favorito(self, url):
        if url not in self.favoritos:
            self.favoritos.append(url)
            #self._salvar_memoria()

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
        try:
            favorito = self.favoritos
            with open("favorito.json", "w") as file:
                json.dump(favorito, file)
            print('Dados Salvos Favoritos com sucesso')
        except Exception as ex:
            print(f'não foi possivel salvar dados: {ex}')
        try:
            historico = self.historico
            with open("favorito.json", "w") as file:
                json.dump(historico, file)
            print('Dados Salvos Historico com sucesso')
        except Exception as ex:
            print(f'não foi possivel salvar dados: {ex}')
        try:
            tabs = self.tabs
            with open("favorito.json", "w") as file:
                json.dump(tabs, file)
            print('Dados Salvos Historico com sucesso')
        except Exception as ex:
            print(f'não foi possivel salvar dados: {ex}')


    def carregar_memoria(self):
        try:
            with open("memoria.json", "r") as file:
                try:
                    memoria = json.load(file)
                    self.favoritos = memoria.get("favoritos", [])
                    self.historico = memoria.get("historico", [])
                    self.tabs = memoria.get("tabs", [])
                except json.decoder.JSONDecodeError as ex:
                    # Se o JSON estiver vazio ou não for válido, simplesmente ignore
                    print(f"JSON arquivo esta vazio: {ex}")
        except FileNotFoundError:
            # Se o arquivo não existe, cria um novo
            self._salvar_memoria()


