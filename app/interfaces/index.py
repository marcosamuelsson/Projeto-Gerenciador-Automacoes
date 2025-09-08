""" 
Código para criar uma janela principal utilizando customtkinter, que permite ao usuário interagir com diversas funcionalidades, 
como visualizar programas executados, agendar execuções, gerenciar programas e usuários, e ajustar configurações.
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importação das bibliotecas necessárias para o funcionamento do APP
#   Bibliotecas externas:
#       customtkinter: para a criação da interface gráfica
#       tkinter: para a criação da interface gráfica
#       CTkMessagebox: para exibir caixas de mensagem personalizadas
#       ctypes: para manipulação de janelas no Windows
#       asyncio: para execução assíncrona de tarefas
#       datetime: para manipulação de datas e horas
#       os: para manipulação de arquivos e pastas
#       tkinter.ttk: para widgets avançados do tkinter
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importação dos módulos criados para o APP:
#       manipulador: para manipulação de arquivos e pastas
#       PasswordDialog: para exibir uma janela de diálogo para confirmação de senha
#       Hash: para hash e verificação de senhas
#       Window_Selector: para selecionar diferentes janelas de interface
#       Inter_Register_APP: para registrar novos aplicativos
#       Inter_Register_PREP: para registrar novos preparativos
#       Inter_Settings: para ajustar configurações do aplicativo
#       Inter_register_users: para registrar novos usuários
#       TextViewerApp: para visualizar arquivos de log
#       GenericDBOperations, UsersDB, ProgramsDB, SettingsDB: para operações de banco de dados
#       Runner: para executar tarefas assíncronas
#       read_schedule: para ler o cronograma de execuções
#       FolderCleaner: para limpar pastas temporárias
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import ctypes
import tkinter.ttk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from app.adm_files.manipulator import manipulador, Path, os
from app.security.password_dialog import PasswordDialog
from app.security.password_hash import Hash
from app.interfaces.director import Window_Selector
from app.interfaces.register_apps import Inter_Register_APP, datetime
from app.interfaces.register_prep import Inter_Register_PREP
from app.interfaces.interface_settings import Inter_Settings
from app.interfaces.register_users import Inter_register_users
from app.interfaces.interface_log import TextViewerApp
from app.database.operationDBs import GenericDBOperations
from app.database.usersDB import UsersDB
from app.database.programsDB import ProgramsDB
from app.database.settingsDB import SettingsDB
from app.executer.runner import Runner, asyncio
from app.executer.read_schedule import read_schedule
from app.executer.cleaner import FolderCleaner
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Configuração do modo de aparência e tema padrão do customtkinter
#   Define o modo de aparência para "dark" (escuro) e o tema de cores para "green" (verde)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
DARK_MODE = "dark"
ctk.set_appearance_mode(DARK_MODE)
ctk.set_default_color_theme("green")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Classe principal do aplicativo que gera a janela principal
#   A classe App herda de ctk.CTk e define a estrutura da interface (widgets, textos, imagens)  
#   A classe também gerencia a interação do usuário com o aplicativo    
#   ATENÇÃO: CASO QUEIRA ADICIONAR MAIS ELEMENTOS, SIGA O PADRÃO DA ESTRUTURA
#   Métodos principais da classe:   
#       __init__: construtor da classe que inicializa a interface e seus componentes
#       max_window: maximiza a janela do aplicativo
#       executed: exibe a interface de programas executados
#       update_executed: atualiza a lista de programas executados
#       open_schedule: exibe a interface de agendamento de execuções
#       open_programs: exibe a interface de gerenciamento de programas
#       users: exibe a interface de gerenciamento de usuários
#       _settings: exibe a interface de configurações
#       clear_frame: limpa os widgets de um frame
#       show_filter_menu: exibe o menu de filtro para uma coluna da tabela
#       clear_filter: limpa os filtros aplicados na tabela
#       stop_execution: para a execução de programas agendados
#       process_loop: gerencia o loop assíncrono para execução de tarefas
#       start_scheduler: inicia o agendador de tarefas
#       settings: carrega as configurações salvas no banco de dados
#       open_log: abre a interface de visualização de logs
#       users_authentication: autentica o usuário para acessar áreas restritas
#       select_button: destaca o botão selecionado na barra lateral
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class App(ctk.CTk):
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Construtor da classe App
#   Inicializa a interface principal do aplicativo, cria pastas e arquivos necessários, configura o banco de dados, define a estrutura da interface (widgets, textos, 
#   imagens) e inicia o loop assíncrono para execução de tarefas
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self):
        # Criação de pastas para armezenar os aruquivos
        self.manipulador = manipulador()

        # Criação das pastas necessárias. Se já existirem, não faz nada.
        # Cada pasta tem uma função específica:
        # maestro_folder: pasta raiz do aplicativo
        # database_folder: pasta para armazenar o banco de dados
        # master_folder: pasta para armazenar arquivos mestres
        # logs_folder: pasta para armazenar arquivos de logs
        self.manipulador.create_folders(self.manipulador.maestro_folder)
        self.manipulador.create_folders(self.manipulador.database_folder)
        self.manipulador.create_folders(self.manipulador.master_folder)
        self.manipulador.create_folders(self.manipulador.logs_folder)

        # Define a data e hora atual para registros
        self.data_atual_txt = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

        # Registro de arquivos de logs. 
        # Log de programas que já foram executados
        self.executed_content = f"Start application - {self.data_atual_txt}\n"
        if not os.path.exists(self.manipulador.executed_txt):
            self.manipulador.create_txt(self.manipulador.executed_txt, self.executed_content)
        else:
            self.manipulador.write_txt(self.manipulador.executed_txt, self.executed_content)

        # Log de programas cadastrados
        self.programs_content = f"Program's Data Base created - {self.data_atual_txt}\n"
        self.manipulador.create_txt(self.manipulador.programs_txt, self.programs_content)

        # Log de usuários cadastrados
        self.users_content = f"User's Data Base created - {self.data_atual_txt}\n"
        self.manipulador.create_txt(self.manipulador.users_txt, self.users_content)

        # Log de configurações do sistema
        self.settings_content = f"Settings Data Base created - {self.data_atual_txt}\n"
        self.manipulador.create_txt(self.manipulador.settings_txt, self.settings_content)

        # Configuração do banco de dados
        self.db_programs = GenericDBOperations(ProgramsDB, "sqlite:///C:/Terminator/Database/executerDB.db")
        self.db_users = GenericDBOperations(UsersDB, "sqlite:///C://Terminator/Database/executerDB.db")
        self.db_settings = GenericDBOperations(SettingsDB, "sqlite:///C:/Terminator/Database/executerDB.db")
       
        # Chama o construtor da classe ctk.CTk
        super().__init__()

        # Define o título do APP
        self.title("Terminator")

        # Define o tamanho inicial da janela e o tamanho mínimo
        self.minsize(1000, 600)

        # Centralizar a janela
        self.update_idletasks()  # Garante que a geometria esteja atualizada
        # after 200ms para garantir que a janela seja maximizada após a inicialização
        self.after(200, self.max_window)

        # main_container -> tem left_side_panel e right_side_panel dentro dele. É o container principal.
        self.main_container = ctk.CTkFrame(self, corner_radius=10)
        self.main_container.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)
        
        # left_side_panel -> tem os botões de navegação. Botões que ficam do lado esquerdo.
        self.left_side_panel = ctk.CTkFrame(self.main_container, width=150, corner_radius=10)
        self.left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False, padx=5, pady=5)
        
        # Configuração do grid para o left_side_panel
        self.left_side_panel.grid_columnconfigure(0, weight=1)
        self.left_side_panel.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.left_side_panel.grid_rowconfigure((6, 7), weight=1)
        
        # self.left_side_panel WIDGET
        # Aqui é definido o logo que ficará no APP
        self.logo_label = ctk.CTkLabel(self.left_side_panel, text="Terminator", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Botões do left_side_panel
        # Dicionário para armazenar os botões e facilitar a seleção
        self.buttons = {}

        # Botão Executed -> chama o método self.executed para mostrar os programas que já foram executados
        self.bt_executed = ctk.CTkButton(self.left_side_panel, text="Executed", command=self.executed, fg_color="#089c4c", width=200, height=50, font=("Arial", 17))
        self.bt_executed.grid(row=1, column=0, padx=20, pady=10)
        self.buttons["executed"] = self.bt_executed

        # Botão Schedule -> chama o método self.open_schedule para mostrar os programas agendados
        self.schedule_bt = ctk.CTkButton(self.left_side_panel, text="Schedule", command=self.open_schedule, fg_color="#089c4c", width=200, height=50, font=("Arial", 17))
        self.schedule_bt.grid(row=2, column=0, padx=20, pady=10)
        self.buttons["schedule"] = self.schedule_bt
        
        # Botão Programs -> chama o método self.open_programs para mostrar os programas cadastrados
        self.bt_programs = ctk.CTkButton(self.left_side_panel, text="Programs", command=self.open_programs, fg_color="#089c4c", width=200, height=50, font=("Arial", 17))
        self.bt_programs.grid(row=3, column=0, padx=20, pady=10)
        self.buttons["programs"] = self.bt_programs

        # Botão Users -> chama o método self.users para mostrar os usuários cadastrados
        self.user_bt = ctk.CTkButton(self.left_side_panel, text="Users", command=self.users, fg_color="#089c4c", width=200, height=50, font=("Arial", 17))
        self.user_bt.grid(row=4, column=0, padx=20, pady=10)
        self.buttons["users"] = self.user_bt

        # Botão Settings -> chama o método self._settings para mostrar as configurações do sistema
        self.settings_bt = ctk.CTkButton(self.left_side_panel, text="Settings", command=self._settings, fg_color="#089c4c", width=200, height=50, font=('Arial', 17))
        self.settings_bt.grid(row=15, column=0, padx=20, pady=10)

        # right_side_panel -> tem os conteúdos que mudam conforme o botão clicado no left_side_panel
        self.right_side_panel = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color="#000811")
        self.right_side_panel.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5)
        
        # Conteúdo inicial da right_side_panel
        self.right_dashboard = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color="#000811")
        self.right_dashboard.pack(in_=self.right_side_panel, side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
        
        # Dicionário para armazenar os filtros aplicados nas tabelas
        self.day_order = {"Sun": 0, "Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6}

        # Inicia o processamento do loop asyncio dentro do tkinter
        self.runner = Runner(update_callback=self.update_executed)
        # Pega a lista de execuções do runner
        self.execute_list = self.runner.execute_list
        
        # loop assíncrono para executar tarefas em segundo plano
        self.loop = asyncio.get_event_loop()
        # Processa o loop assíncrono
        self.process_loop()

        # Inicia as tarefas agendadas e a limpeza de pastas temporárias
        self.value_type = None        
        # Limpeza de pastas temporárias
        self.folder_cleaner = FolderCleaner(self.manipulador)
        self.folder_cleaner.start()

        # Função para verificar se é a primeira vez que o programa está sendo executado.
        # Se for, cria o usuário admin padrão a partir do banco de dados registrado pelo usuário
        self.after(0, self.settings)
        # Inicia o agendador de tarefas
        self.start_scheduler()
        # Ao iniciar, abre a tela de programas que já foram executados
        self.executed()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método select_button para destacar o botão selecionado na barra lateral 
#   Parâmetros:
#       selected_name: nome do botão selecionado
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def select_button(self, selected_name):
        # Itera sobre os botões e atualiza a cor de fundo
        for name, button in self.buttons.items():
            # Se o nome do botão for igual ao nome selecionado, muda a cor de fundo para indicar que está ativo
            if name == selected_name:
                button.configure(fg_color="#055e2e")  # Cor de botão ativo
            else:
                button.configure(fg_color="#089c4c")  # Cor padrão
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método max_window para maximizar a janela do aplicativo
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def max_window(self):
        # Tenta maximizar a janela do aplicativo
        try:
            # Obtém o identificador da janela atual
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            # Maximiza a janela usando o identificador
            ctypes.windll.user32.ShowWindow(hwnd, 3)  # 3 = SW_MAXIMIZE
        except Exception as e:
            print("Error to try turn max window", e)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método executed para exibir a interface de programas executados
#   Cria uma tabela com todos os programas que já foram executados, ordenados pela data de execução
#   Disponibiliza filtragem na tabela com o botão logo abaixo para retirar o filtro
#   Aqui é onde será definido o que será apresentado na janela
#   ATENÇÃO: CASO QUEIRA ADICIONAR MAIS ELEMENTOS, SIGA O PADRÃO DA ESTRUTURA
#   Parâmetros 
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def executed(self):       
        # Destaca o botão Executed na barra lateral
        self.select_button("executed")
        # Limpa o conteúdo atual da right_dashboard
        self.clear_frame(self.right_dashboard)
        # Cria o frame para os botões acima da tabela
        self.button_frame = ctk.CTkFrame(self.right_dashboard, fg_color="#000811")
        self.button_frame.pack(pady=10)
        # Botão Stop -> chama o método self.stop_execution para parar a execução de programas agendados
        self.stop_run = ctk.CTkButton(self.button_frame, text="Stop", command=self.stop_execution, fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.stop_run.pack(side=tkinter.LEFT, padx=10)
        # Botão History -> chama o método self.open_log para abrir a interface de visualização de logs
        self.history_executed = ctk.CTkButton(self.button_frame, text="History", command=lambda: self.open_log(self.manipulador.executed_txt, "Executed"), fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.history_executed.pack(side=tkinter.LEFT, padx=10)

        # Cria a tabela para exibir os programas executados
        # Colunas da tabela:
        #   Run ID: identificador único da execução
        #   Program Name: nome do programa executado
        #   Start: data e hora de início da execução
        #   Finished: data e hora de término da execução
        #   Status: status da execução (sucesso, falha, etc.)
        #   Type Run: tipo de execução (manual, agendada, etc.)
        columns = ("Run ID", "Program Name", "Start", "Finished", "Status", "Type Run")
        # Cria a Treeview para exibir os dados
        self.executed_table = tkinter.ttk.Treeview(self.right_dashboard, columns=columns, show="headings")
        # Configura os cabeçalhos das colunas
        for col in columns:
            self.executed_table.heading(col, text=col, command=lambda c=col: self.show_filter_menu(c, self.executed_table))
        # Configura as cores das linhas ímpares e pares
        self.executed_table.tag_configure('oddrow', background='#000820')
        self.executed_table.tag_configure('evenrow', background='#000800')
        # Configura o estilo da tabela
        self.style = tkinter.ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#000811", foreground="white", fieldbackground="#000811", font=("Arial", 12, "normal"))
        self.style.configure("Treeview.Heading", background="#000811", foreground="white", fieldbackground="#000811", font=("Arial", 12, "bold"))
        self.style.map('Treeview', background=[('selected', '#089c4c')])
        self.style.map('Treeview.Heading', background=[('selected', '#089c4c')])

        # Itera sobre a lista de execuções e insere cada execução na tabela
        for i, run in enumerate(self.execute_list):
            tag = 'oddrow' if i % 2 == 0 else 'evenrow'
            self.executed_table.insert("", tkinter.END, values=run, tags=(tag,))

        # Exibe a tabela na interface        
        self.executed_table.pack(fill=tkinter.BOTH, expand=True, padx=5, pady=5)
        # Botão Clear Filter -> chama o método self.clear_filter para limpar os filtros aplicados na tabela
        self.clear_filter_bt = ctk.CTkButton(self.right_dashboard, text="Clear Filter", command=lambda: self.clear_filter(self.executed_table, self.execute_list), fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.clear_filter_bt.pack(pady=10)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método update_executed para atualizar a lista de programas executados
#   Atualiza a tabela de programas executados com os dados mais recentes
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def update_executed(self):
        # Tenta atualizar a tabela de programas executados
        try:
            # Verifica se o widget existe e está visível
            if hasattr(self, 'executed_table') and self.executed_table.winfo_exists():
                # Limpa a tabela
                for item in self.executed_table.get_children():
                    self.executed_table.delete(item)

                # Reinsere os dados atualizados
                for i, run in enumerate(self.execute_list):
                    tag = 'oddrow' if i % 2 == 0 else 'evenrow'
                    self.executed_table.insert("", tkinter.END, values=run, tags=(tag,))
        except Exception as e:
            print(f"Error to try update the eecutables table: {e}")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método open_schedule para exibir a interface de agendamento de execuções
#   Cria uma tabela com todos os programas agendados e seus respectivos horários
#   Disponibiliza filtragem na tabela com o botão logo abaixo para retirar o filtro
#   Aqui é onde será definido o que será apresentado na janela
#   ATENÇÃO: CASO QUEIRA ADICIONAR MAIS ELEMENTOS, SIGA O PADRÃO DA ESTRUTURA
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def open_schedule(self):
        # Destaca o botão Schedule na barra lateral
        self.select_button("schedule")
        # Limpa o conteúdo atual da right_dashboard
        self.clear_frame(self.right_dashboard)
        
        # Cria o frame para os botões da rigth_dashboard
        self.button_frame = ctk.CTkFrame(self.right_dashboard, fg_color="#000811")
        self.button_frame.pack(pady=10)

        # Botão para exportar o schedule
        self.export_schedule = ctk.CTkButton(self.button_frame, text="Export Schedule", command="", fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.export_schedule.pack(side=tkinter.LEFT, padx=10)

        # Botão para importar o scheduel
        self.import_schedule = ctk.CTkButton(self.button_frame, text="Import Schedule", command="", fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.import_schedule.pack(side=tkinter.LEFT, padx=10)
        
        # Cria a tabela para exibir os programas agendados
        # Colunas da tabela:
        #   Program Path: caminho do programa agendado
        #   Program Name: nome do programa agendado
        #   Program Type: tipo do programa agendado
        #   Days: dias da semana em que o programa será executado
        #   Execute Hour: horário em que o programa será executado
        columns = ("Program Path", "Program Name", "Program Type", "Days", "Execute Hour")
        # Cria a Treeview para exibir os dados
        self.schedule_table = tkinter.ttk.Treeview(self.right_dashboard, columns=columns, show="headings")
        # Configura os cabeçalhos das colunas
        for col in columns:
            self.schedule_table.heading(col, text=col, command=lambda c=col: self.show_filter_menu(c, self.schedule_table))
        
        # Configura as cores das linhas ímpares e pares
        self.schedule_table.tag_configure('oddrow', background='#000820')
        self.schedule_table.tag_configure('evenrow', background='#000800')
        # Configura o estilo da tabela
        self.style = tkinter.ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#000811", foreground="white", fieldbackground="#000811", font=("Arial", 12, "normal"))
        self.style.configure("Treeview.Heading", background="#000811", foreground="white", fieldbackground="#000811", font=("Arial", 12, "bold"))
        self.style.map('Treeview', background=[('selected', '#089c4c')])
        self.style.map('Treeview.Heading', background=[('selected', '#089c4c')])
        # Coleta os dados dos programas agendados do banco de dados
        schedules = []
        # Itera sobre os programas cadastrados no banco de dados
        for program in self.db_programs.get_all():
            # Verifica se o programa tem uma lista de horários agendados
            if program["schedule_list"] != "":
                # Separa os horários agendados por vírgula
                horarios = program["schedule_list"].split(",")
                # Extrai o caminho completo do programa e cria um caminho parcial para exibição
                full_path = Path(program["program_path"])
                partial_path = Path("") / full_path.parts[-2] / full_path.name
                # Itera sobre os horários agendados e adiciona à lista de schedules
                for hora in horarios:
                    # Separa o horário e o dia
                    hour = hora.split("-")[0]
                    day = hora.split("-")[1]
                    # Adiciona uma tupla com as informações do programa agendado
                    schedules.append((partial_path, program["program_name"], program["program_type"], day, hour))
        # Ordena a lista de schedules por dia da semana e horário
        schedules = sorted(schedules,key=lambda x: (self.day_order.get(x[3], 7), datetime.strptime(x[4], "%H:%M")))

        # Insere os dados na tabela
        for i, schedule in enumerate(schedules):    
            self.schedule_table.insert("", tkinter.END, values=schedule, tag = 'oddrow' if i % 2 == 0 else 'evenrow')
        # Exibe a tabela na interface
        self.schedule_table.pack(fill=tkinter.BOTH, expand=True, padx=5, pady=5)
        # Botão Clear Filter -> chama o método self.clear_filter para limpar os filtros aplicados na tabela
        self.clear_filter_bt = ctk.CTkButton(self.right_dashboard, text="Clear Filter", command=lambda: self.clear_filter(self.schedule_table, schedules), fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.clear_filter_bt.pack(pady=10)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método open_programs para exibir a interface de gerenciamento de programas
#   Cria botões para CADASTRO, ALTERAÇÃO, EXCLUSÃO de PROGRAMAS
#   Cria uma tabela com todos os PROGRAMAS cadastrados e quando foram modificados
#   Disponibiliza filtragem na tabela com o botão logo abaixo para retirar o filtro
#   Aqui é onde será definido o que será apresentado na janela
#   ATENÇÃO: CASO QUEIRA ADICIONAR MAIS ELEMENTOS, SIGA O PADRÃO DA ESTRUTURA
#   Parâmetros:
#       Nenhum  
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def open_programs(self):
        # Destaca o botão Programs na barra lateral
        self.select_button("programs")
        # Limpa o conteúdo atual da right_dashboard
        self.clear_frame(self.right_dashboard)
        # Cria o frame para os botões acima da tabela
        self.button_frame = ctk.CTkFrame(self.right_dashboard, fg_color="#000811")
        self.button_frame.pack(pady=10)
        # Botão Add App -> chama o método self.add_programs para adicionar um novo programa
        self.add_programs_button = ctk.CTkButton(self.button_frame, text="Add App", command=self.add_programs, fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.add_programs_button.pack(side=tkinter.LEFT, padx=10)
        # Botão Change App -> chama o método self.change_programs para alterar um programa existente
        self.change_programs_button = ctk.CTkButton(self.button_frame, text="Change App", command=self.change_programs, fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.change_programs_button.pack(side=tkinter.LEFT, padx=10)
        # Botão Delete App -> chama o método self.delete_programs para excluir um programa existente
        self.delete_programs_button = ctk.CTkButton(self.button_frame, text="Delete App", command=self.delete_programs, fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.delete_programs_button.pack(side=tkinter.LEFT, padx=10)
        # Botão History -> chama o método self.open_log para abrir a interface de visualização de logs
        self.logs_button = ctk.CTkButton(self.button_frame, text="History", command=lambda: self.open_log(self.manipulador.programs_txt, "Programs"), fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.logs_button.pack(side=tkinter.LEFT, padx=10)
        # Cria a tabela para exibir os programas cadastrados
        # Colunas da tabela:
        #   ID: identificador único do programa
        #   Application Path: caminho do programa
        #   Application Type: tipo do programa
        #   Application Name: nome do programa
        #   Owner: proprietário do programa
        #   Date Modified: data da última modificação do programa
        columns = ("ID", "Application Path", "Application Type", "Application Name", "Owner", "Date Modified")
        # Cria a Treeview para exibir os dados
        self.program_table = tkinter.ttk.Treeview(self.right_dashboard, columns=columns, show="headings")
        # Configura os cabeçalhos das colunas
        for col in columns:
            self.program_table.heading(col, text=col, command=lambda c=col: self.show_filter_menu(c, self.program_table))
        # Configura as cores das linhas ímpares e pares
        self.program_table.tag_configure('oddrow', background='#000820')
        self.program_table.tag_configure('evenrow', background='#000800')
        self.program_table.bind("<Double-1>", self.run_programs_ondemmand)
        # Configura o estilo da tabela
        self.style = tkinter.ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#000811", foreground="white", fieldbackground="#000811", font=("Arial", 12, "normal"))
        self.style.configure("Treeview.Heading", background="#000811", foreground="white", fieldbackground="#000811", font=("Arial", 12, "bold"))
        self.style.map('Treeview', background=[('selected', '#089c4c')])
        self.style.map('Treeview.Heading', background=[('selected', '#089c4c')])

        # Cria um dicionário id → nome dos usuários
        user_id_to_name = {user["id"]: user["user_name"] for user in self.db_users.get_all()}
        # Coleta os dados dos programas cadastrados do banco de dados
        programs = []
        # Itera sobre os programas cadastrados no banco de dados
        for app in self.db_programs.get_all():
            # Pega o nome do proprietário a partir do id
            owner_id = app.get("owner_id")  # substitua por app["user_id"] se for esse o nome do campo
            owner_name = user_id_to_name.get(owner_id, "Unknown")
            # Extrai o caminho completo do programa e cria um caminho parcial para exibição
            full_path = Path(app["program_path"])
            partial_path = Path("") / full_path.parts[-2] / full_path.name
            # Adiciona uma tupla com as informações do programa
            programs.append((app["id"], partial_path, app["program_type"], app["program_name"], owner_name, app["date_modified"]))
        # Insere os dados na tabela
        for i, app in enumerate(programs):
            tag = 'oddrow' if i % 2 == 0 else 'evenrow'
            self.program_table.insert("", tkinter.END, values=app, tag=tag)
        # Exibe a tabela na interface
        self.program_table.pack(fill=tkinter.BOTH, expand=True, padx=5, pady=5)
        # Botão Clear Filter -> chama o método self.clear_filter para limpar os filtros aplicados na tabela
        self.clear_filter_bt = ctk.CTkButton(self.right_dashboard, text="Clear Filter", command=lambda: self.clear_filter(self.program_table, programs), fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.clear_filter_bt.pack(pady=10)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método users para exibir a interface de gerenciamento de usuários
#   Cria botões para CADASTRO, ALTERAÇÃO, EXCLUSÃO de USUÁRIOS
#   Cria uma tabela com todos os USUÁRIOS cadastrados e quando foram modificados
#   Disponibiliza filtragem na tabela com o botão logo abaixo para retirar o filtro
#   Aqui é onde será definido o que será apresentado na janela
#   ATENÇÃO: CASO QUEIRA ADICIONAR MAIS ELEMENTOS, SIGA O PADRÃO DA ESTRUTURA
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def users(self):
        # Destaca o botão Users na barra lateral
        self.select_button("users")
        # Limpa o conteúdo atual da right_dashboard
        self.clear_frame(self.right_dashboard)
        # Cria o frame para os botões acima da tabela
        self.button_frame = ctk.CTkFrame(self.right_dashboard, fg_color="#000811")
        self.button_frame.pack(pady=10)
        # Botão Add User -> chama o método self.add_user para adicionar um novo usuário
        self.add_user_button = ctk.CTkButton(self.button_frame, text="Add User", command=self.add_user, fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.add_user_button.pack(side=tkinter.LEFT, padx=10)
        # Botão Change User -> chama o método self.change_user para alterar um usuário existente
        self.change_user_button = ctk.CTkButton(self.button_frame, text="Change User", command=self.change_user, fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.change_user_button.pack(side=tkinter.LEFT, padx=10)
        # Botão Delete User -> chama o método self.delete_user para excluir um usuário existente
        self.delete_user_button = ctk.CTkButton(self.button_frame, text="Delete User", command=self.delete_user, fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.delete_user_button.pack(side=tkinter.LEFT, padx=10)
        # Botão History -> chama o método self.open_log para abrir a interface de visualização de logs
        self.logs_user_button = ctk.CTkButton(self.button_frame, text="History", command=lambda: self.open_log(self.manipulador.users_txt, "Users"), fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.logs_user_button.pack(side=tkinter.LEFT, padx=10)
        # Cria a tabela para exibir os usuários cadastrados
        # Colunas da tabela:
        #   ID: identificador único do usuário
        #   User Name: nome do usuário
        #   User SESA: código SESA do usuário
        #   User E-mail: e-mail do usuário
        #   Date Created: data da criação do usuário
        # Cria a Treeview para exibir os dados    
        columns = ("ID", "User Name", "User SESA", "User E-mail", "Date Created")
        # Cria a Treeview para exibir os dados
        self.user_table = tkinter.ttk.Treeview(self.right_dashboard, columns=columns, show="headings")
        # Configura os cabeçalhos das colunas
        for col in columns:
            self.user_table.heading(col, text=col, command=lambda c=col: self.show_filter_menu(c, self.user_table))
        # Configura as cores das linhas ímpares e pares
        self.user_table.tag_configure('oddrow', background='#000820')
        self.user_table.tag_configure('evenrow', background='#000800')
        # Configura o estilo da tabela
        self.style = tkinter.ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#000811", foreground="white", fieldbackground="#000811", font=("Arial", 12, "normal"))
        self.style.configure("Treeview.Heading", background="#000811", foreground="white", fieldbackground="#000811", font=("Arial", 12, "bold"))
        self.style.map('Treeview', background=[('selected', '#089c4c')])
        self.style.map('Treeview.Heading', background=[('selected', '#089c4c')])
        # Coleta os dados dos usuários cadastrados do banco de dados
        users = []
        # Itera sobre os usuários cadastrados no banco de dados
        for user in self.db_users.get_all():
            users.append((user["id"], user["user_name"], user["user_code"], user["user_email"], user["date_modified"]))
        # Insere os dados na tabela
        for i, user in enumerate(users):
            self.user_table.insert("", tkinter.END, values=user, tag = 'oddrow' if i % 2 == 0 else 'evenrow')
        # Exibe a tabela na interface
        self.user_table.pack(fill=tkinter.BOTH, expand=True, padx=5, pady=5)
        # Botão Clear Filter -> chama o método self.clear_filter para limpar os filtros aplicados na tabela
        self.clear_filter_bt = ctk.CTkButton(self.right_dashboard, text="Clear Filter", command=lambda: self.clear_filter(self.user_table, users), fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.clear_filter_bt.pack(pady=10)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método show_filter_menu para exibir o menu de filtragem ao clicar no cabeçalho da coluna
#   Parâmetros:
#       column: nome da coluna clicada
#       table_: tabela onde o filtro será aplicado
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def show_filter_menu(self, column, table_):
        # Cria o menu de contexto
        menu = tkinter.Menu(self.right_dashboard, tearoff=0, selectcolor="#089c4c")
        # Adiciona as opções de filtro ao menu
        unique_values = sorted(set(table_.set(item, column) for item in table_.get_children()))
        # Adiciona a opção de limpar o filtro
        for value in unique_values:
            menu.add_command(label=value, command=lambda v=value: self.apply_filter(column, v, table_=table_))
     
        # Configurar o estilo de cada entrada do menu
        for index in range(menu.index(tkinter.END) + 1):
            menu.entryconfig(index, background="#000811", foreground="white", activebackground="#089c4c", activeforeground="white")
        # Exibe o menu na posição do cursor
        menu.post(self.right_dashboard.winfo_pointerx(), self.right_dashboard.winfo_pointery())

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método apply_filter para aplicar o filtro selecionado na tabela
#   Parâmetros:
#       column: nome da coluna onde o filtro será aplicado
#       filter_value: valor do filtro selecionado
#       table_: tabela onde o filtro será aplicado
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def apply_filter(self, column, filter_value, table_):
        # Configura as cores das linhas ímpares e pares
        for row in table_.get_children():
            # Pega o valor da célula na coluna especificada
            value = table_.set(row, column)
            if value == filter_value:
                table_.reattach(row, '', 'end')
            # Se o valor não corresponder, remove a linha da exibição
            else:
                table_.detach(row)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método clear_filter para limpar todos os filtros aplicados na tabela
#   Parâmetros:
#       table_: tabela onde o filtro será limpo
#       data_base: dados originais para repopular a tabela
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def clear_filter(self, table_, data_base):
        # Configura as cores das linhas ímpares e pares
        table_.tag_configure('oddrow', background='#000820')
        table_.tag_configure('evenrow', background='#000800')
        # Limpa a tabela e repopula com os dados originais
        for row in table_.get_children():
            table_.delete(row)
        # Reinsere os dados originais na tabela
        for i, app in enumerate(data_base):
            table_.insert("", tkinter.END, values=app, tag = 'oddrow' if i % 2 == 0 else 'evenrow')
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método add_programs para adicionar um novo programa
#   Abre a janela de seleção do tipo de programa (Executável, Python ou Prep
#   Conforme o tipo selecionado, abre a janela de cadastro correspondente
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def add_programs(self):
        # Verifica se há usuários cadastrados antes de permitir o cadastro de programas
        if self.db_users.get_all() == []:
            CTkMessagebox(title="Error",message="There are no registered users. \nYou must register users before registering programs.", icon="warning",button_color="#089c4c",justify="center")
            return
        # Abre a janela de seleção do tipo de programa
        else:
            # Zera o valor do tipo de programa
            self.value_type = None
            director = Window_Selector(self)
            self.wait_window(director)
            # Conforme o tipo selecionado, abre a janela de cadastro correspondente
            if self.value_type == "Executable" or self.value_type == "Python":
                self.end_scheduler()
                register_app = Inter_Register_APP(self, self.value_type)
                self.wait_window(register_app) 
                self.open_programs()  
                self.start_scheduler()
            # Se o tipo for Prep, abre a janela de cadastro de Prep
            elif self.value_type == "Prep":
                self.end_scheduler()
                register_prep = Inter_Register_PREP(self, self.value_type)
                self.wait_window(register_prep)
                self.open_programs()
                self.start_scheduler()
            
            # Se nenhum tipo for selecionado, exibe uma mensagem de erro
            elif self.value_type == "" or self.value_type == "Select the type of program":
                CTkMessagebox(title="Error", message="No type selected!", icon="warning", button_color="#089c4c", justify="center")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método change_programs para alterar um programa existente
#   Solicita a senha do dono do programa antes de permitir a alteração
#   Conforme o tipo do programa, abre a janela de alteração correspondente
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def change_programs(self):
        # Verifica se foi selecionado algum programa na tabela
        selected_item = self.program_table.selection()
        if not selected_item:
            CTkMessagebox(title="Error", message="Select a program to edit!", icon="warning", button_color="#089c4c")
            return

        # Pega os dados do programa selecionado
        values = self.program_table.item(selected_item[0], "values")
        program_name = values[0].strip()  # remove espaços extras
        program = self.db_programs.get_by_column("id", program_name)
        
        # Se o programa não for encontrado, exibe uma mensagem de erro
        if not program:
            CTkMessagebox(title="Error", message=f"Program '{program_name}' not found in database!", icon="warning", button_color="#089c4c")
            return
        
        # Busca o dono do programa
        user = self.db_users.get_by_column("id", program["owner_id"])
        if not user:
            CTkMessagebox(title="Error",message="Owner of the program not found!",icon="warning",button_color="#089c4c",justify="center")
            return

        # Solicita a senha do dono
        password_dialog = PasswordDialog(self)
        # Pega a senha digitada
        entered_password = password_dialog.get_password()

        # Verifica se a senha está correta
        # Se a senha estiver correta, abre a janela de alteração correspondente ao tipo do programa
        # Se a senha estiver incorreta, exibe uma mensagem de erro
        if (Hash().check_login(entered_password, user["password"]) == True):
            if program["program_type"] == "Python" or program["program_type"] == "Executable":
                # Encerra o agendador antes de abrir a janela de alteração
                self.end_scheduler()
                # Abre a janela de alteração do programa
                change_program = Inter_Register_APP(self, program_data=program)
                # Aguarda a janela ser fechada
                self.wait_window(change_program)
                # Reabre a tabela de programas e reinicia o agendador
                self.open_programs()
                # Iniciar o agendador novamente
                self.start_scheduler()
            elif program["program_type"] == "Prep":
                # Encerra o agendador antes de abrir a janela de alteração
                self.end_scheduler()
                # Abre a janela de alteração do programa Prep
                change_program = Inter_Register_PREP(self, prep_data=program)
                # Aguarda a janela ser fechada
                self.wait_window(change_program)
                # Reabre a tabela de programas e reinicia o agendador
                self.open_programs()
                # Iniciar o agendador novamente
                self.start_scheduler()
        else:
            CTkMessagebox(title="Error",message="Incorrect password. Action canceled!",icon="warning",button_color="#089c4c",justify="center")
            return
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método delete_programs para excluir um programa existente
#   Solicita a senha do dono do programa antes de permitir a exclusão
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def delete_programs(self):
        # Encerra o agendador antes de excluir o programa
        self.end_scheduler()

        # Verifica se foi selecionado algum programa na tabela
        selected_item = self.program_table.selection()
        if not selected_item:
            CTkMessagebox(title="Error",message="Select a program to delete!",icon="warning",button_color="#089c4c",justify="center")
            return
        # Pega os dados do programa selecionado
        values = self.program_table.item(selected_item[0], "values")
        program_id = values[0].strip()
        program = self.db_programs.get_by_column("id", program_id)

        # Se o programa não for encontrado, exibe uma mensagem de erro
        if not program:
            CTkMessagebox(title="Error",message="Program not found in the database!",icon="warning",button_color="#089c4c",justify="center")
            return

        # Busca o dono do programa
        user = self.db_users.get_by_column("id", program["owner_id"])
        if not user:
            CTkMessagebox(title="Error",message="Owner of the program not found!",icon="warning",button_color="#089c4c",justify="center")
            return

        # Solicita a senha do dono
        password_dialog = PasswordDialog(self)
        entered_password = password_dialog.get_password()
        
        if Hash().check_login(entered_password, user["password"]) == True or (Hash().check_login(entered_password, self.db_settings.get_by_column("id", 1)["password"]) == True):
            # Deleta o programa
            self.end_scheduler()
            self.db_programs.delete(program_id)
            # Registra a ação no log de programas
            content = f"Program Name: '{values[3].strip()}' Deleted.\nHour Deleted {datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}.\nOwner: {values[5].strip()}.\nProgram Type: {values[2].strip()}.\n"
            self.manipulador.write_txt(self.manipulador.programs_txt, content)

            CTkMessagebox(title="Porgram deleted",message=f"Program '{program['program_name']}' has been deleted.",icon="check",button_color="#089c4c",justify="center")

            self.open_programs()  # Atualiza a tabela, se você tiver esse método
            self.start_scheduler()  # Iniciar o agendador novamente

        else:
            CTkMessagebox(title="Error",message="Incorrect password. Action canceled!",icon="warning",button_color="#089c4c",justify="center")
            return        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método process_loop para processar o loop de eventos assíncronos
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def process_loop(self):
        # Processa o loop de eventos assíncronos
        # Tenta executar o loop de eventos
        # Se ocorrer algum erro, exibe uma mensagem de erro
        # Finalmente, agenda a próxima chamada do método após 100 ms
        try:
            self.loop.call_soon(self.loop.stop)
            self.loop.run_forever()
        except Exception as e:
            print(f"Erro no loop: {e}")
        finally:
            self.after(100, self.process_loop)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método run_programs_ondemmand para executar um programa selecionado na tabela de programas
#   Parâmetros:
#       event: evento de clique duplo na tabela
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#       
    def run_programs_ondemmand(self, event):
        # Pega o item selecionado na tabela
        selected_item = self.program_table.selection()
        # Verifica se foi selecionado algum programa na tabela
        if not selected_item:
            CTkMessagebox(title="Error", message="Select a program to run!", icon="warning", button_color="#089c4c", justify="center")
            return

        # Pega os dados do programa selecionado
        values = self.program_table.item(selected_item[0], "values")
        program_id = values[0].strip()
        program = self.db_programs.get_by_column("id", program_id)

        # Se o programa não for encontrado, exibe uma mensagem de erro
        if not program:
            CTkMessagebox(title="Error", message="Program not found in the database!", icon="warning", button_color="#089c4c", justify="center")
            return

        # Pega os dados do programa
        program_type = program["program_type"]
        program_name = program["program_name"]
        program_path = program["program_path"]
        program_parameters = program["parameters"]

        # Cria uma nova tarefa para executar o programa
        # Adiciona a tarefa na lista de tarefas on-demand
        id = len(self.runner.ondemmand_tasks_list) + 1
        # Cria a tarefa assíncrona
        task = self.loop.create_task(self.runner.tasks_ondemmand("Manually", id, f"{program_id} - {program_name}", program_type, program_path, program_parameters))
        task.exec_id = str(id)
        # Adiciona a tarefa na lista de tarefas on-demand
        self.runner.ondemmand_tasks_list.append(task)
        # Adiciona a execução na lista de execuções
        self.show_temp_message()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método show_temp_message para exibir uma mensagem temporária de sucesso
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def show_temp_message(self):
        # Cria a CTkMessagebox com botão padrão
        msg_box = CTkMessagebox(
            title="Sucesso",
            message="Operação concluída com sucesso!",
            icon="check",
            option_1="Fechar",
            # fade_in_duration=0.05,
            button_color="#089c4c",
            justify="center"
        )

        # Simula clique no botão após 3 segundos
        def close_box():
            try:
                msg_box.event_generate("<<MessageboxClose>>")
                msg_box.button_event("Fechar")
            except Exception as e:
                print("Erro ao tentar fechar a messagebox:", e)

        # Agenda o fechamento da messagebox após 2 segundos
        self.after(2000, close_box)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método stop_execution para cancelar uma execução em andamento
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def stop_execution(self):
        # Pega o item selecionado na tabela
        selected_item = self.executed_table.selection()
        # Verifica se foi selecionado algum programa na tabela
        if not selected_item:
            CTkMessagebox(title="Error", message="Select a run to stop.", icon="info", button_color="#089c4c")
            return

        # Pega os dados da execução selecionada
        values = self.executed_table.item(selected_item[0], "values")
        exec_id = str(values[0])
        
        # Verifica se a execução está em andamento
        if values[4] == "On Going":
            # Tenta cancelar nas listas de tarefas
            for task_list in [self.runner.automatic_tasks, self.runner.ondemmand_tasks_list]:
                for i, task in enumerate(task_list):
                    if hasattr(task, "exec_id") and str(task.exec_id) == exec_id:
                        task.cancel()
                        # Atualiza status na lista de execuções
                        for j, item in enumerate(self.execute_list):
                            # Se o ID da execução for igual ao ID da tarefa cancelada
                            if item[0] == exec_id:
                                # Atualiza o status para "Canceled"
                                self.execute_list[j] = (item[0], item[1], item[2], item[3], "Canceled", item[5])
                                content = f"Program '{values[1].strip()}' Canceled.\nStart Hour: {values[2].strip()}.\nCanceled Hour: {datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}.\nType Run: {values[5].strip()}.\n"
                                self.manipulador.write_txt(self.manipulador.executed_txt, content)
                                # Atualiza a tabela de execuções
                                self.update_executed()
                                break
                        return

            CTkMessagebox(title="Error", message="Unable to cancel assigned task.", icon="warning", button_color="#089c4c")
        else:
            CTkMessagebox(title="Error", message="It is only possible to cancel the execution with status equal to 'On Going'")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método start_scheduler para iniciar o agendador automático de tarefas
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def start_scheduler(self):
        # Inicia o agendador automático de tarefas
        self.scheduler = read_schedule(self.runner, self.db_programs)
        self.loop.create_task(self.scheduler.start())

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método end_scheduler para encerrar o agendador automático de tarefas
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def end_scheduler(self):
        # Encerra o agendador automático de tarefas
        # Se o agendador existir, para-o
        if hasattr(self, "scheduler"):
            self.scheduler.stop()
            print("Automatic scheduler ended")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método add_user para adicionar um novo usuário
#   Solicita a senha do dono antes de permitir o cadastro
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def add_user(self):
        # Pedi a senha root da tabela settings
        password_dialog = PasswordDialog(self)
        entered_password = password_dialog.get_password()

        # Verifica se a senha está correta
        if (Hash().check_login(entered_password, self.db_settings.get_by_column("id", 1)["password"]) != True):
            CTkMessagebox(title="Error",message="Incorrect password. Action canceled!", icon="warning",button_color="#089c4c",justify="center")
            return
        # Se a senha estiver correta, abre a janela de cadastro de usuário
        register_user = Inter_register_users(self)
        self.wait_window(register_user)  # Espera a janela de registro ser fechada
        self.users()  # Atualiza a lista de usuários
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método change_user para alterar um usuário existente
#   Solicita a senha do dono ou do próprio usuário antes de permitir a alteração
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def change_user(self):
        # Pega o item selecionado na tabela
        selected_item = self.user_table.selection()
        # Verifica se foi selecionado algum usuário na tabela
        if not selected_item:
            CTkMessagebox(title="Error", message="Select some item to change!", icon="warning", button_color="#089c4c", justify="center")
            return
        # Pega os dados do usuário selecionado
        user_values = self.user_table.item(selected_item[0], "values")
        id_user = user_values[0]
        # Busca o usuário no banco de dados
        user = self.db_users.get_by_column("id", id_user)
        # Se o usuário não for encontrado, exibe uma mensagem de erro
        if not user:
            CTkMessagebox(title="Error", message="User does not find!", icon="warning", button_color="#089c4c", justify="center")
            return
        
        # Solicita a senha ao dono
        password_dialog = PasswordDialog(self)
        entered_password = password_dialog.get_password()
        # Verifica se a senha está correta
        # Se a senha estiver correta, abre a janela de alteração do usuário
        if Hash().check_login(entered_password, user["password"]) == True or (Hash().check_login(entered_password, self.db_settings.get_by_column("id", 1)["password"]) == True):
            change_user = Inter_register_users(self, user_data=user)
            self.wait_window(change_user)
            self.users()
        
        else:
            CTkMessagebox(title="Error", message="Incorrect password. Action canceled!", icon="warning", button_color="#089c4c", justify="center")
            return
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método delete_user para excluir um usuário existente
#   Solicita a senha do dono ou do próprio usuário antes de permitir a exclusão
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def delete_user(self):
        # Pega o item selecionado na tabela
        selected_item = self.user_table.selection()
        # Verifica se foi selecionado algum usuário na tabela
        if not selected_item:
            CTkMessagebox(title="Error", message="Select some item to delete!", icon="warning", button_color="#089c4c", justify="center")
            return
        # Pega os dados do usuário selecionado
        user_values = self.user_table.item(selected_item[0], "values")
        id_user = user_values[0]
        # Busca o usuário no banco de dados
        user = self.db_users.get_by_column("id", id_user)
        # Se o usuário não for encontrado, exibe uma mensagem de erro
        if not user:
            CTkMessagebox(title="Error", message="User does not find!", icon="warning", button_color="#089c4c", justify="center")
            return

        # Solicita a senha do dono
        password_dialog = PasswordDialog(self)
        entered_password = password_dialog.get_password()
        # Verifica se a senha está correta
        # Se a senha estiver correta, deleta o usuário e todos os programas dele
        if Hash().check_login(entered_password, user["password"]) == True or (Hash().check_login(entered_password, self.db_settings.get_by_column("id", 1)["password"]) == True):
            # Deleta todos os programas do usuário
            try:
                self.db_programs.delete_by_column("owner_id", user["id"])
            except:
                pass
            # Deleta o usuário
            self.db_users.delete(user["id"])
            # Registra a ação no log de usuários
            content = f"User '{user_values[1].strip()}' Deleted.\nHour Deleted: {datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}.\nUser Code: {user_values[2].strip()}.\nUser E-mail: {user_values[3].strip()}"
            self.manipulador.write_txt(self.manipulador.users_txt, content)
            CTkMessagebox(title="User Deleted", message=f"User '{user['user_name']}' and his programs have been deleted", icon="check", button_color="#089c4c", justify="center")
            # Atualiza a lista de usuários
            self.users()
            
        else:
            CTkMessagebox(title="Error", message="Incorrect password. Action canceled!", icon="warning", button_color="#089c4c", justify="center")
            return
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método settings para verificar se as configurações estão definidas
#   Se não estiverem, abre a janela de configurações
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def settings(self):
        # Pega as configurações do banco de dados
        settings_data = self.db_settings.get_all()
        # Verifica se as configurações estão definidas
        if settings_data == []:
            CTkMessagebox(
                title="Configuration Registration",
                message="Settings need to be set before running programs.",
                icon="info",
                button_color="#089c4c",
                justify="center"
            )

            # Cria e espera a janela de registro
            register_window = Inter_Settings(self)
            self.wait_window(register_window)
            try:
                self.after(100, self.folder_cleaner.stop)
            finally:
                self.after(100, self.folder_cleaner.start)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para abrir a janela de registro das configurações (settings)
#   Parâmteros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def _settings(self):
        # Abre a janela de registro das configurações (settings)
        password_dialog = PasswordDialog(self)
        # Solicita a senha do usuário antes de permitir o acesso às configurações
        entered_password = password_dialog.get_password()
        
        # Verifica se a senha está correta
        if not Hash().check_login(entered_password, self.db_settings.get_by_column("id", 1)["password"]):
            CTkMessagebox(
                title="Error",
                message="Incorrect password. Action canceled!",
                icon="warning",
                button_color="#089c4c",
                justify="center"
            )
            self.folder_cleaner.stop()
            return

        # Pega os dados do banco
        setting = self.db_settings.get_by_column("id", 1)
        # Abre a janela da Interface
        sett = Inter_Settings(self, setting)
        # Espera a janela terminar o processo
        self.wait_window(sett)

        # Após confirmação, inicia o limpador
        try:
            self.after(100, self.folder_cleaner.stop)
        finally:
            self.after(100, self.folder_cleaner.start)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para abrir uma janela com os textos do Log
#   Parâmetros:
#       caminho do log;
#       nome do log (para aparecer no APP Bar da janela)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def open_log(self, path_log, name_log):
        # Se o caminho do log não existir retorna um erro
        if not os.path.exists(path_log):
            CTkMessagebox(
                title="Error",
                message=f"The log '{path_log}' does not exist.",
                icon="warning",
                button_color="#089c4c",
                justify="center"
            )
            self.folder_cleaner.stop()
            return

        # Abre a janela de log 
        TextViewerApp(path_log, name_log)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para limpar o frame direito onde ficam as informações
#   Toda vez que um usuário apertar um botão da esquerda, esse método apaga as informações para inputar novas
#   Parâmetros:
#       sel.{frame}
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#    
    # Limpa os widgets que contém o caminho do arquivo e o QR CODE na janela do APP
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()