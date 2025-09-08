""" 
Código para limpeza automática de pastas com base em uma lista de diretórios e um limite de dias.
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importação de bibliotecas necessárias
#   asyncio: Biblioteca para programação assíncrona.
#   os: Biblioteca para interações com o sistema operacional.
#   datetime, timedelta: Bibliotecas para manipulação de datas e tempos.
#   GenericDBOperations, SettingsDB: Classes para operações de banco de dados.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import asyncio
import os
from datetime import datetime, timedelta
from app.database.operationDBs import GenericDBOperations
from app.database.settingsDB import SettingsDB
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Classe FolderCleaner
#   Responsável por limpar pastas automaticamente com base em um limite de dias.
#   A classe utiliza uma instância de manipulador para realizar operações de exclusão.
#   A limpeza é realizada diariamente em um loop assíncrono.
#   Métodos:
#       __init__: Inicializa a classe com o manipulador e o limite de dias.
#       _daily_loop: Loop assíncrono que executa a limpeza diariamente.
#       clean_if_old: Verifica e limpa arquivos/pastas mais antigos que o limite de dias.
#       start: Inicia o loop de limpeza.
#       stop: Para o loop de limpeza.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class FolderCleaner:
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método construtor que inicializa a classe FolderCleaner.
#   Parâmetros:
#       manipulador_instance: Instância do manipulador para operações de arquivo.
#       days_threshold: Limite de dias para considerar arquivos/pastas como antigos (padrão: 30).
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self, manipulador_instance, days_threshold=30):
        self.days_threshold = days_threshold
        self.manipulador = manipulador_instance
        self._running = False
        self._task = None
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método _daily_loop
#   Loop assíncrono que executa a limpeza diariamente.
#   Lê as pastas a serem limpas do banco de dados e chama o método clean_if_old para cada pasta.
#   Aguarda 24 horas entre cada execução.
#   Utiliza asyncio.gather para executar a limpeza de múltiplas pastas simultaneamente.
#   Parâmetros:
#       Nenhum.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    async def _daily_loop(self):
        # Inicializa a conexão com o banco de dados
        self.db_settings = GenericDBOperations(SettingsDB, "sqlite:///C:/Terminator/Database/executerDB.db")

        # Loop principal que roda enquanto a limpeza estiver ativa
        while self._running:
            # Lê as pastas a serem limpas do banco de dados
            self.list_folders_delete = []

            # Lê as configurações do banco de dados
            for setting in self.db_settings.get_all():
                # Extrai a lista de pastas do campo paths_delete
                raw_string = setting['paths_delete'].strip("[]").replace("'", "")
                # Divide a string em uma lista de caminhos, removendo virgulas e espaços extras
                self.list_folders_delete = [path.strip() for path in raw_string.split(",")]

            # Executa a limpeza para cada pasta na lista
            # Cria uma lista de tarefas para limpar cada pasta
            tasks = [self.clean_if_old(folder) for folder in self.list_folders_delete]
            # Executa todas as tarefas simultaneamente
            await asyncio.gather(*tasks)
            # Aguarda 24 horas antes da próxima execução
            await asyncio.sleep(86400) 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que verifica e limpa arquivos/pastas mais antigos que o limite de dias.
#   Parâmetros:
#       path_folder: Caminho da pasta a ser limpa.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    async def clean_if_old(self, path_folder):
        # Verifica se a pasta existe
        if not os.path.exists(path_folder):
            return
        
        # Itera sobre os itens na pasta
        for item in os.listdir(path_folder):
            # Constrói o caminho completo do item
            item_path = os.path.join(path_folder, item)
            try:
                # Obtém a data de criação do item
                item_time = datetime.fromtimestamp(os.path.getctime(item_path))
                # Verifica se o item é mais antigo que o limite de dias
                if datetime.now() - item_time > timedelta(days=self.days_threshold):
                    # Remove o item (arquivo ou link simbólico ou pasta)
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        self.manipulador.dell_item(item_path)
                    elif os.path.isdir(item_path):
                        self.manipulador.dell_folder(item_path)
            except Exception as e:
                print(f"Error checking item {item_path}:\n {e}")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que inicia o loop de limpeza diária.
#   Parâmetros:
#       Nenhum.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def start(self):
        # Inicia o loop de limpeza se não estiver rodando ou se a tarefa atual estiver concluída
        if not self._running or self._task is None or self._task.done():
            self._running = True
            # Obtém o loop de eventos atual e cria a tarefa assíncrona
            loop = asyncio.get_event_loop()
            # Inicia a tarefa de limpeza diária
            self._task = loop.create_task(self._daily_loop())
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que para o loop de limpeza diária.
#   Parâmetros:
#       Nenhum.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def stop(self):
        # Para o loop de limpeza se estiver rodando
        if self._running:
            self._running = False
            if self._task:
                # Cancela a tarefa assíncrona
                self._task.cancel()