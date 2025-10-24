""" 
Codigo para manipulação de arquivos e pastas do sistema operacional
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importação de bibliotecas
#   os: para manipulação de arquivos e pastas do sistema operacional
#   sys: para manipulação de variáveis e funções do sistema
#   json: para manipulação de arquivos JSON
#   pathlib.Path: para manipulação de caminhos de arquivos e pastas
#   shutil: para operações de alto nível em arquivos e pastas
#   Hash: para hash e verificação de senhas
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import os
import sys
import json
from pathlib import Path
import shutil
from app.security.password_hash import Hash
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Classe para manipulação de arquivos e pastas do sistema operacional
#   Métodos:
#       __init__: inicializa a classe e define os caminhos das pastas e arquivos
#       dell_item: apaga um arquivo
#       dell_folder: apaga uma pasta e todo o seu conteúdo
#       create_folders: cria uma pasta
#       clean_folder: limpa o conteúdo de uma pasta
#       create_txt: cria um arquivo .txt
#       write_txt: escreve em um arquivo .txt
#       create_connection_file: cria um arquivo de conexão JSON
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class manipulador:
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Construtor para inicializar a classe e definir os caminhos das pastas e arquivos
#   Parâmetros: nenhum
#   root: caminho raiz do programa
#   maestro_folder: pasta raiz do programa
#   database_folder: pasta para armazenar o banco de dados
#   master_folder: pasta para armazenar os arquivos mestre
#   logs_folder: pasta para armazenar os arquivos de log
#   executed_txt: arquivo .txt para armazenar os programas executados
#   programs_txt: arquivo .txt para armazenar os programas registrados
#   users_txt: arquivo .txt para armazenar os usuários registrados
#   settings_txt: arquivo .txt para armazenar as configurações registradas
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#    
    def __init__(self):
        if getattr(sys, 'frozen', False):
            self.root = Path(sys._MEIPASS)
            self.root = os.path.dirname(os.path.dirname(self.root))
        else: 
            self.root = Path(__file__).parent
            self.root = os.path.dirname(os.path.dirname(self.root))
        
        # Criação de pastas para armezenar os aruquivos
        self.maestro_folder = r"C:\Terminator"
        self.database_folder = os.path.join(self.maestro_folder, "Database")
        self.master_folder = os.path.join(self.maestro_folder, "Master Files")
        self.logs_folder = os.path.join(self.maestro_folder, "Logs")
        self.image_folder = os.path.join(self.maestro_folder, "Images")

        # Criação dos .txt para armazenar todas as modificações das tabelas dos bancos de dados
        self.executed_txt = os.path.join(self.logs_folder, "executed.txt")
        self.programs_txt = os.path.join(self.logs_folder, "programs.txt")
        self.users_txt = os.path.join(self.logs_folder, "users.txt")
        self.settings_txt = os.path.join(self.logs_folder, "settings.txt")

        # Caminho ícone imagem
        self.icon_terminator = os.path.join(self.image_folder, "icon_terminator.ico")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para apagar um arquivo ou pasta
#   Parâmetros: 1. caminho do arquivo ou pasta
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def dell_item(self, item_path):
        try: 
            # Verifica se o item é um arquivo ou link simbólico e apaga
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
        except Exception as e:
            print(f"Error to delete file {item_path}. Check the error:\n{e}")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#  Método para apagar uma pasta e todo o seu conteúdo
#  Parâmetros: 1. caminho da pasta
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------# 
    def dell_folder(self, path_folder):
        try:
            # Verifica se o item é uma pasta e apaga todo o seu conteúdo
            if os.path.isdir(path_folder):
                shutil.rmtree(path_folder)
        except Exception as e:
            print(f"Error to delete folder {path_folder}. Check the error:\n{e}")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para criar uma pasta
#   Parâmetros: 1. nome da pasta
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#     
    def create_folders(self, name_folder):
        # Cria a pasta se não existir
        if not os.path.exists(name_folder):
            os.makedirs(name_folder)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para limpar o conteúdo de uma pasta
#   Parâmetros: 1. caminho da pasta
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def clean_folder(self, path_folder):
        # Verifica se a pasta existe
        if not os.path.exists(path_folder):
            return
        
        # Para cada item na pasta, apaga o item
        for item in os.listdir(path_folder):
            path_item = os.path.join(path_folder, path_item)
            try:
                # Verifica se o item é um arquivo ou link e apaga
                if os.path.isfile(path_item) or os.path.islink(path_item):
                    self.dell_item(path_item)
                # Verifica se o item é uma pasta e apaga todo o seu conteúdo
                if os.path.isdir(path_item):
                    self.dell_folder(path_item)
            except Exception as e:
                print(f"Error to remove the {path_item}: \n{e}")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para criar um arquivo .txt
#   Parâmetros: 1. caminho do arquivo .txt
#               2. conteúdo a ser escrito
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def create_txt(self, path_txt, content):
        # Verifica se o arquivo já existe
        if os.path.exists(path_txt):
            return 
        # Cria o arquivo .txt e escreve o conteúdo inicial
        with open(path_txt, 'w', encoding='utf-8') as file:
            file.write(content)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para escrever em um arquivo .txt
#   Parâmetros: 1. caminho do arquivo .txt
#               2. conteúdo a ser escrito   
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def write_txt(self, path_txt, new_content):
        # Verifica se o arquivo existe
        if not os.path.exists(path_txt):
            print(f"The '{path_txt}' does not exist:")
        # Abre o arquivo .txt e escreve o novo conteúdo no final do arquivo
        with open(path_txt, 'a', encoding='utf-8') as file:
            file.write(f"\n{new_content}")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para criar um arquivo de conexão JSON para usar no PREP
#   Parâmetros: 1. nome do arquivo JSON
#               2. output_list - lista de conexões de saída
#               3. input_list - lista de conexões de entrada
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def create_connection_file(self, file_name, output_list, input_list):
        # Dados a serem escritos no arquivo JSON
        out_data = []
        for data_out in output_list:
            out_data.append({
                "serverUrl": data_out["ServerURLOut"],
                "contentUrl": data_out["ContentURLOut"],
                "username": data_out["UsernameOut"],
                "password": Hash().restore_password(data_out["PasswordOut"])
            })
        in_data = []
        for data_in in input_list:
            in_data.append({
                "username": data_in["UsernameIn"],
                "hostname": data_in["HostnameIn"],
                "contentUrl": data_in["ContentURLIn"],
                "password": Hash().restore_password(data_in["PasswordIn"])
            })

        data = {
            "outputConnections": 
                out_data
            ,
            "inputConnections": 
                in_data
        }
        # Escreve os dados no arquivo JSON
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)