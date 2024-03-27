import json
import os
import sys
from datetime import datetime
import re

import requests
from PyQt5.QtGui import QIcon, QCursor

hora = datetime

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
            sys.stderr.write(f'Não foi possível baixar o ícone: {ex}')
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
            sys.stderr.write(f'não foi possível adicionar favorito: {ex}')

    def remover_favorito(self, title):
        for favorito in self.favoritos:
            if favorito['title'] == title:
                self.favoritos.remove(favorito)
                self._salvar_memoria()
                print(f'Favorito removido: {favorito}')
                return  # Removido apenas um favorito, então podemos sair da função após a remoção
        sys.stderr.write(f'Nenhum favorito encontrado para a URL: {title}')

    def adicionar_historico(self, current_browser):
        try:
            page_title = current_browser.page().title()
            page_link = current_browser.page().url().toString()
            hora_atual = datetime.now()
            # Verifica se o page_title não está vazio e não parece ser um link
            if page_title.strip() and not re.match(r'^https?://', page_title):
                dia = {
                    "dia": hora_atual.strftime("%d-%m-%Y"),
                    "hora": hora_atual.strftime("%H:%M:%S"),
                    "titulo": page_title,
                    "link": page_link
                }
                print(f'Enviado historico {dia["dia"]}, {dia["hora"]}, {dia["titulo"]}, {dia["link"]}')
                if dia["link"] == "https://www.google.com/":
                    print(f'Home não adicionada {dia["link"]}')
                else:
                    self.historico.append(dia)
                    self._salvar_memoria()
        except Exception as ex:
            sys.stderr.write(f'não foi possível adicionar ao historico: {ex}')
    def listar_historico(self):
        self.carregar_memoria()
        historico_lista_reversa = list(reversed(self.historico))
        print(f'Lista atual {historico_lista_reversa}')
        return historico_lista_reversa
    def deletar_historico(self):
        # Limpar a lista de histórico
        self.historico = []
        # Remover o arquivo JSON do histórico
        arquivo_historico = os.path.join("memoria", "historico.json")
        try:
            os.remove(arquivo_historico)
            print("Arquivo de histórico removido com sucesso.")
        except FileNotFoundError:
            sys.stderr.write("Arquivo de histórico não encontrado.")
        except Exception as e:
            sys.stderr.write(f"Ocorreu um erro ao tentar remover o arquivo de histórico: {e}")

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
            sys.stderr.write(f'não foi possivel salvar dados: {ex}')
        try:
            arquivo_historico = os.path.join("memoria", "historico.json")
            historico = self.historico
            with open(arquivo_historico, "w") as file:
                json.dump(historico, file)
                print(f'Dados Salvos Historico com sucesso {historico}:{file}')
        except Exception as ex:
            sys.stderr.write(f'não foi possivel salvar dados: {ex}')
        try:
            arquivo_tabs = os.path.join("memoria", "tabs.json")
            tabs = self.tabs
            with open(arquivo_tabs, "w") as file:
                json.dump(tabs, file)
                print(f'Dados Salvos Historico com sucesso {tabs}:{file}')
        except Exception as ex:
            sys.stderr.write(f'não foi possivel salvar dados: {ex}')

    def carregar_memoria(self):
        try:
            try:
                arquivo_favorito = os.path.join("memoria", "favorito.json")

                with open(arquivo_favorito, "r") as file:
                    fav = json.load(file)
                    self.favoritos = fav
                    print(f'Favoritos carregado : {self.favoritos}')
            except json.decoder.JSONDecodeError as ex:
                # Se o JSON estiver vazio ou não for válido, simplesmente ignore
                sys.stderr.write(f"JSON de favoritos está vazio: {ex}")

            try:
                arquivo_historico = os.path.join("memoria", "historico.json")
                with open(arquivo_historico, "r") as file:
                    self.historico = json.load(file)
                    print(f'Historicos carregado : {self.historico}')
            except json.decoder.JSONDecodeError as ex:
                # Se o JSON estiver vazio ou não for válido, simplesmente ignore
                sys.stderr.write(f"JSON de histórico está vazio: {ex}")

            try:
                arquivo_tabs = os.path.join("memoria", "tabs.json")
                with open(arquivo_tabs, "r") as file:
                    self.tabs = json.load(file)
                    print(f'Tabs carregado : {self.tabs}')
            except json.decoder.JSONDecodeError as ex:
                # Se o JSON estiver vazio ou não for válido, simplesmente ignore
                sys.stderr.write(f"JSON de abas está vazio: {ex}")

        except FileNotFoundError:
            # Se o arquivo não existe, cria um novo
            self._salvar_memoria()


