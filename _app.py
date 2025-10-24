""" 
Código para gerenciar a execução de um aplicativo com interface gráfica utilizando o customtkinter.
A ideia é que não permita abrir mais de uma vez o app, mesmo que o usuário tente.
Code by: Marco Antônio Samuelsson
Data: 18/09/2025
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importação das bibliotecas necessárias para o funcionamento do APP
#   Bibliotecas externas:
#       os: para manipulação de arquivos e diretórios
#       sys: para manipulação de parâmetros e funções do sistema
#       tempfile: para criação de arquivos temporários
#       psutil: para verificação de processos em execução
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Bibliotecas internas:
#       App: chamada do app
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import os
import sys
import tempfile
import psutil  # pip install psutil
from app.interfaces.main import App

# Criação do arquivo de lock
lockfile = os.path.join(tempfile.gettempdir(), 'my_app.lock')
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Função para verificar se o app já está em execução
#   Parametros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def is_already_running():
    # Verifica se o arquivo de lock existe
    if os.path.exists(lockfile):
        # Se existir, tenta ler o PID do processo
        try:
            with open(lockfile, 'r') as f:
                pid = int(f.read())
            # Verifica se o processo ainda está ativo
            if psutil.pid_exists(pid):
                return True
            else:
                # Processo não existe mais, remove o lock
                os.remove(lockfile)
        except Exception:
            # Se houver erro ao ler o arquivo, remove o lock
            os.remove(lockfile)

    # Cria o arquivo de lock com o PID atual
    with open(lockfile, 'w') as f:
        f.write(str(os.getpid()))
    return False
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Função para limpar o arquivo de lock
#   Parametros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def cleanup_lock():
    # Verifica se o arquivo de lock existe
    if os.path.exists(lockfile):
        # Se existir, tenta ler o PID do processo
        try:
            os.remove(lockfile)
        except Exception:
            pass
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Verifica se o app já está em execução
if is_already_running():
    sys.exit(0)

# Tenta iniciar o App
try:
    app = App()
    app.mainloop()

# Finaliza o App
finally:
    cleanup_lock()