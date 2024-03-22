import json
import os

import requests
from PyQt5.QtGui import QIcon, QCursor

class BrowserMemory:
    def __init__(self):
        self.favoritos = []
        self.historico = []
        self.tabs = []
        self.carregar_memoria()

    def listar_favorito(self):
        return self.favoritos

    def baixar_icon(self, icon_url):
        try:
            # Verifica se a pasta temporária existe e, se não, cria-a
            temp_folder = "temp/icons"
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)

            # Baixa o ícone da página
            icon_filename = os.path.basename(QIcon(icon_url))
            icon_path = os.path.join(temp_folder, icon_filename)
            if not os.path.exists(icon_path):  # Verifica se o ícone já foi baixado
                with open(icon_path, 'wb') as f:
                    icon_response = requests.get(icon_url)
                    f.write(icon_response.content)

            return icon_path
        except Exception as ex:
            print(f'Não foi possível baixar o ícone: {ex}')
            return None

    def adicionar_favorito(self, current_browser):
        try:
            # Obtém o ícone da página atual
            page_icon = current_browser.page().icon()
            page_title = current_browser.page().title()
            page_link = current_browser.page().url().toString()

            # Salvar o ícone em um arquivo local
            icon_filename = f"{page_title.replace(' ', '_')}.png"  # Nome do arquivo com base no título da página
            icon_path = os.path.join("temp\\icons", icon_filename)  # Caminho completo para o arquivo

            # Salvar o ícone em um arquivo local
            page_icon.pixmap(page_icon.availableSizes()[0]).save(icon_path)

            # Informações do favorito com o caminho do ícone
            favorito_info = {'icon_path': icon_path, 'title': page_title, 'link': page_link}
            print(f'adicionado favorito {favorito_info}')

            # Adiciona o favorito à lista de favoritos
            self.favoritos.append(favorito_info)

            # Salvar a memória
            self._salvar_memoria()

        except Exception as ex:
            print(f'não foi possível adicionar favorito: {ex}')

    def remover_favorito(self, title):
        for favorito in self.favoritos:
            if favorito['title'] == title:
                self.favoritos.remove(favorito)
                self._salvar_memoria()
                print(f'Favorito removido: {favorito}')
                return  # Removido apenas um favorito, então podemos sair da função após a remoção
        print(f'Nenhum favorito encontrado para a URL: {title}')

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
            arquivo_favorito = os.path.join("memoria", "favorito.json")
            favorito = self.favoritos
            with open(arquivo_favorito, "w") as file:
                json.dump(favorito, file)
                print(f'Dados Salvos Favoritos com sucesso {favorito}:{file}')
        except Exception as ex:
            print(f'não foi possivel salvar dados: {ex}')
        try:
            arquivo_historico = os.path.join("memoria", "historico.json")
            historico = self.historico
            with open(arquivo_historico, "w") as file:
                json.dump(historico, file)
                print(f'Dados Salvos Historico com sucesso {historico}:{file}')
        except Exception as ex:
            print(f'não foi possivel salvar dados: {ex}')
        try:
            arquivo_tabs = os.path.join("memoria", "tabs.json")
            tabs = self.tabs
            with open(arquivo_tabs, "w") as file:
                json.dump(tabs, file)
                print(f'Dados Salvos Historico com sucesso {tabs}:{file}')
        except Exception as ex:
            print(f'não foi possivel salvar dados: {ex}')

    def carregar_memoria(self):
        try:
            try:
                arquivo_favorito = os.path.join("memoria", "favorito.json")

                with open(arquivo_favorito, "r") as file:
                    fav = json.load(file)
                    print(fav)
                    self.favoritos = fav
            except json.decoder.JSONDecodeError as ex:
                # Se o JSON estiver vazio ou não for válido, simplesmente ignore
                print(f"JSON de favoritos está vazio: {ex}")

            try:
                arquivo_historico = os.path.join("memoria", "historico.json")
                with open(arquivo_historico, "r") as file:
                    historico = json.load(file)
                    print(historico)
            except json.decoder.JSONDecodeError as ex:
                # Se o JSON estiver vazio ou não for válido, simplesmente ignore
                print(f"JSON de histórico está vazio: {ex}")

            try:
                arquivo_tabs = os.path.join("memoria", "tabs.json")
                with open(arquivo_tabs, "r") as file:
                    tabs = json.load(file)
                    print(tabs)
            except json.decoder.JSONDecodeError as ex:
                # Se o JSON estiver vazio ou não for válido, simplesmente ignore
                print(f"JSON de abas está vazio: {ex}")

        except FileNotFoundError:
            # Se o arquivo não existe, cria um novo
            self._salvar_memoria()


