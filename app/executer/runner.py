""" 
Código para execução de programas de forma assíncrona, incluindo manipulação de parâmetros e atualização de status da janela principal.
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importações necessárias para a execução do Runner
#   re - Biblioteca para expressões regulares, usada para manipulação de strings.
#   ast - Biblioteca para manipulação de estruturas de dados em Python.
#   asyncio - Biblioteca para programação assíncrona, permitindo a execução de tarefas sem bloquear o fluxo principal.
#   datetime - Biblioteca para manipulação de datas e horas.
#   Applications internas:
#       password_hash - Classe para hash e verificação de senhas.
#       manipulator - Classe para manipulação de arquivos e diretórios.
#       settingsDB - Classe para configuração do banco de dados.
#       operationDBs - Classe para operações genéricas no banco de dados.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import re
import ast
import asyncio
from datetime import datetime
from app.security.password_hash import Hash
from app.adm_files.manipulator import manipulador, shutil, os
from app.database.settingsDB import SettingsDB
from app.database.operationDBs import GenericDBOperations

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Classe Runner
#   Responsável por gerenciar a execução de programas de forma assíncrona, incluindo manipulação de parâmetros e atualização de status.
#   A classe utiliza a biblioteca asyncio para permitir a execução de múltiplas tarefas sem bloquear o fluxo principal do programa.
#   A classe também interage com o banco de dados para obter configurações e registrar o status das execuções.
#   Métodos:
#       __init__: Inicializa a classe, configurando o hash de senhas, manipulador de arquivos, listas de tarefas e conexão com o banco de dados.
#       tasks_ondemmand: Executa uma tarefa sob demanda, atualizando o status e registrando a saída.
#       safe_decode: Decodifica bytes de saída de processos, tentando múltiplas codificações para evitar erros.
#       get_parameters: Extrai e processa parâmetros de uma string, incluindo a restauração de senhas criptografadas.
#       update_execute_list: Atualiza o status de uma tarefa na lista de execuções e chama o callback de atualização, se fornecido.                 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class Runner:
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método __init__
#   Inicializa a classe Runner, configurando o hash de senhas, manipulador de arquivos, listas de tarefas e conexão com o banco de dados.
#   Parâmetros:
#       update_callback: Função de callback opcional para atualizar a interface do usuário.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self, update_callback=None):
        # Inicializa o hash de senhas, manipulador de arquivos e listas de tarefas
        self.hash = Hash()
        
        self.manipulador = manipulador()
        self.master_files = self.manipulador.master_folder
        
        self.automatic_tasks = []
        self.ondemmand_tasks_list = []
        
        self.db_settings = GenericDBOperations(SettingsDB, "sqlite:///C:/Terminator/Database/executerDB.db")

        self.execute_list = []

        # Callback para atualizar a interface do usuário, se fornecido
        self.update_callback = update_callback
        
        # Declaro a variável para o caminho do json aqui para conseguir acessar a varíavel em qualquer lugar
        # Fiz isso para evitar o erro de acesso à variável quando tento apagar o arquivo do prep
        # A ideia é que sempre tente apagar o arquivo, mesmo não sendo "PREP" 
        # Logo se não é PREP a variável não é assesível e retorna erro, por isso essa declaração
        self.path_json = ""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método tasks_ondemmand
#   Executa uma tarefa sob demanda, atualizando o status e registrando a saída.
#   Parâmetros:
#       type_run: Tipo de execução (e.g., "On Demand").
#       id: ID do programa a ser executado.
#       name: Nome do programa a ser executado.     
#       type_program: Tipo do programa (e.g., "Executable", "Python", "Prep").
#       path: Caminho do programa a ser executado.
#       parameters: Parâmetros para a execução do programa. 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    async def tasks_ondemmand(self, type_run, id, name, type_program, path, parameters):
        try:
            # Obtém os parâmetros processados
            parameters = self.get_parameters(parameters)
            # Adiciona a tarefa à lista de execuções e atualiza a interface
            self.execute_list.insert(0, (f"{id}",f"{name}",f"{datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}","-","On Going", type_run))
            
            # Chama o callback de atualização, se fornecido
            if self.update_callback:
                self.update_callback()

            # Verifica se o caminho do programa existe
            if not os.path.exists(path):
                self.update_execute_list(id, "Path Not Found")
            # Se o caminho não existe, atualiza o status e registra a saída
            else:
                # Executa o programa com base no tipo especificado
                # Se o tipo do programa for "Executable", executa diretamente
                if type_program == "Executable":
                    # Executa o programa diretamente no sistema operacional
                    process = await asyncio.create_subprocess_exec(
                        path, *parameters,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                # Se o tipo do programa for "Python", usa o interpretador Python para rodar o script
                elif type_program == "Python":
                    # Usa o Python real do sistema, não o sys.executable
                    python_path = shutil.which("python") or shutil.which("python3")
                    process = await asyncio.create_subprocess_exec(
                        python_path, path, *parameters,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                # Se o tipo do programa for "Prep", executa o comando específico para Prep
                elif type_program == "Prep":
                    # Obtém o caminho do prep_cli a partir das configurações do banco de dados
                    prep_cli_path = self.db_settings.get_by_column("id", 1)["tableau_bat"]
                    # Garante que o caminho do prep_cli existe
                    self.path_json = os.path.join(self.master_files, f"{name}.json")

                    if parameters == []:
                        # Espera-se que 'parameters' contenha o caminho para o JSON de configuração
                        process = await asyncio.create_subprocess_exec(
                            prep_cli_path, "run", "-t", path,
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )
                    else:
                        # Separando os dados em litas de output e input
                        outputs = []
                        inputs = []
                        for item in parameters:
                            parsed = ast.literal_eval(item)
                            if any(key.endswith('Out') for key in parsed.keys()):
                                outputs.append(parsed)
                            elif any(key.endswith('In') for key in parsed.keys()):
                                inputs.append(parsed)

                        # Cria o arquivo de configuração JSON necessário para o Prep
                        self.manipulador.create_connection_file(self.path_json, outputs, inputs)
                        # Espera o arquivo ser criado
                        while not os.path.exists(self.path_json):
                            await asyncio.sleep(1)
                        # Espera-se que 'parameters' contenha o caminho para o JSON de configuração
                        process = await asyncio.create_subprocess_exec(
                            prep_cli_path, "run", "-t", path, "-c", self.path_json,
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )
                        
                # Associa o processo à tarefa atual para permitir o cancelamento
                current_task = asyncio.current_task()
                current_task.process = process
                # Aguarda a conclusão do processo e captura a saída
                stdout, stderr = await process.communicate()
                # Decodifica a saída e atualiza o status com base no resultado
                status = process.returncode == 0
                # Define o status final com base no resultado da execução
                final_status = "Success" if status else "Error"
                
                # Atualiza a lista de execuções com o status final
                self.update_execute_list(id, final_status)

                # Registra a saída no arquivo de logs
                # Se a execução foi bem-sucedida, registra a saída padrão
                if final_status == "Success":
                    content = f"-------------------------------------------------------------------------------------------------------------------\nProgram ID: {id}.\nProgram Name: {name}.\nFinish Hour: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}.\nProgram Type: {type_program}.\nProgram Path: {path}.\nType Run: {type_run}.\nOutput: {final_status}\n{self.safe_decode(stdout)}.\n-------------------------------------------------------------------------------------------------------------------\n"
                    self.manipulador.write_txt(self.manipulador.executed_txt, content)
                # Se houve um erro na execução, registra a saída de erro
                elif final_status == "Error":
                    content = f"-------------------------------------------------------------------------------------------------------------------\nProgram ID: {id}.\nProgram Name: {name}.\nFinish Hour: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}.\nProgram Type: {type_program}.\nProgram Path: {path}.\nType Run: {type_run}.\nOutput: {final_status}\n{self.safe_decode(stderr)}.\n-------------------------------------------------------------------------------------------------------------------\n"
                    self.manipulador.write_txt(self.manipulador.executed_txt, content)

            # Limpa a pasta master_files após a execução
            self.manipulador.dell_item(self.path_json)
        
        # Trata erros de cancelamento da tarefa
        except asyncio.CancelledError:
            # Se a tarefa for cancelada, mata o processo associado
            current_task = asyncio.current_task()
            # Se o processo estiver em execução, mata-o
            if hasattr(current_task, "process"):
                current_task.process.kill()
                await current_task.process.wait()
            
            # Atualiza o status para "Canceled" e registra a saída
            self.update_execute_list(id, "Error Run")
            
            content = f"-------------------------------------------------------------------------------------------------------------------\nProgram ID: {id}.\nProgram Name: {name}.\nFinish Hour: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}.\nProgram Type: {type_program}.\nProgram Path: {path}.\nType Run: {type_run}.\nOutput: Canceled by Error Run Process.\n-------------------------------------------------------------------------------------------------------------------\n"
            self.manipulador.write_txt(self.manipulador.executed_txt, content)
            
            # Limpa a pasta master_files após o cancelamento
            self.manipulador.clean_folder(self.master_files)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método safe_decode
#   Decodifica bytes de saída de processos, tentando múltiplas codificações para evitar erros.
#   Parâmetros:
#       output_bytes: Bytes a serem decodificados.
#   Retorna:
#       String decodificada.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def safe_decode(self, output_bytes):
            # Tenta decodificar usando UTF-8, se falhar tenta CP1252, e por fim Latin1
            try:
                return output_bytes.decode("utf-8")
            except UnicodeDecodeError:
                # tenta decodificar usando cp1252
                try:
                    return output_bytes.decode("cp1252")
                except UnicodeDecodeError:
                    # como último recurso, decodifica usando latin1
                    return output_bytes.decode("latin1", errors="replace")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método get_parameters
#   Extrai e processa parâmetros de uma string, incluindo a restauração de senhas criptografadas.
#   Parâmetros:
#       text_parameter: String contendo os parâmetros a serem extraídos.
#   Retorna:
#       Lista de parâmetros processados.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def get_parameters(self, text_parameter):
        # Expressão regular para capturar pares chave-valor no formato key: value
        padrao = r'(\w+):\s*(.*?)(?=,\w+:|$)'
        # Encontra todos os pares chave-valor na string de entrada
        correspond = re.findall(padrao, text_parameter)

        parameters = []
        # Itera sobre os pares chave-valor encontrados
        for key, value in correspond:
            value = value.strip()
            # Restaura senhas criptografadas, se aplicável
            if (key == "password" or key == "PasswordOut" or key == "PasswordIn") and value.startswith("b'"):
                # Tenta restaurar a senha, ignorando erros
                try:
                    value = self.hash.restore_password(value)
                except:
                    pass
            parameters.append(value)
        
        return parameters
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método update_execute_list
#   Atualiza o status de uma tarefa na lista de execuções e chama o callback de atualização, se fornecido.
#   Parâmetros:
#       id_program: ID do programa cuja tarefa deve ser atualizada.
#       status: Novo status da tarefa.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def update_execute_list(self, id_program, status):
        # Atualiza o status da tarefa na lista de execuções
        for i, item in enumerate(self.execute_list):
            # Verifica se o ID do programa corresponde
            if item[0] == str(id_program):
                # Atualiza o item com o novo status e a hora de término
                self.execute_list[i] = (
                    item[0], item[1], item[2],
                    f"{datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}",
                    status,  item[5]
                )
                break
        # Chama o callback de atualização, se fornecido
        if self.update_callback:
            self.update_callback()