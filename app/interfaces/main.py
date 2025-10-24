""" 
Código para criar uma janela principal utilizando customtkinter, que permite ao usuário interagir com diversas funcionalidades, 
como visualizar programas executados, agendar execuções, gerenciar programas e usuários, e ajustar configurações.
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.2.2
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
#       Image: para manipulação de imagens 
#       openpyxl: para manipulação de dados de planilhas excel
#       filedialog: para exibição de diálogos de seleção de arquivos
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importação dos módulos criados para o APP:
#       manipulador: para manipulação de arquivos e pastas
#       Create_Excel: para criação do template de schedule com os dados de horário do banco
#       PasswordDialog: para exibir uma janela de diálogo para confirmação de senha
#       Hash: para hash e verificação de senhas
#       Window_UserSelector: para selecionar um usário que irá manipular o schedule
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
#       PixelArtIcon: para criar o ícone da janela
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import ctypes
import tkinter.ttk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from app.adm_files.manipulator import manipulador, Path, os
from app.adm_files.create_excel_template import Create_Excel, openpyxl
from app.security.password_dialog import PasswordDialog
from app.security.password_hash import Hash
from app.interfaces.select_user import Window_UserSelector
from app.interfaces.director import Window_Selector
from app.interfaces.register_apps import Inter_Register_APP, datetime, filedialog
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
from app.images.create_icon import PixelArtIcon, Image

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
#       create_export: método acionado para criação de um template de schedule aceito pela importação
#       import_schedule: método acionado para importação do template gerado e modificado pelo usuário
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
        # Criação de pastas para armezenar os aruivos 
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
        self.manipulador.create_folders(self.manipulador.image_folder)
        
        # Criação do ícone do app
        self.pixel_art = PixelArtIcon().create_icon()

        # Define a data e hora atual para registros
        self.data_atual_txt = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

        # Registro de arquivos de logs. 
        # Log de programas que já foram executados
        self.executed_content = f"Start Program - {self.data_atual_txt}\n"
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
        self.db_users = GenericDBOperations(UsersDB, "sqlite:///C:/Terminator/Database/executerDB.db")
        self.db_settings = GenericDBOperations(SettingsDB, "sqlite:///C:/Terminator/Database/executerDB.db")
       
        # Chama o construtor da classe ctk.CTk
        super().__init__()

        # Define o título do APP
        self.title("Terminator 1.2.2")

        # Define o tamanho inicial da janela e o tamanho mínimo
        self.minsize(1000, 600)

        # Acresenta o ícone ao app
        self.wm_iconbitmap(default=self.manipulador.icon_terminator)

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
        self.left_side_panel.configure(fg_color="#000000")
        
        # Logo do app na tela iDnicial
        # Carrega a imagem do ícone
        self.icon_image = Image.open(self.manipulador.icon_terminator)
        self.ctk_image = ctk.CTkImage(light_image=self.icon_image, dark_image=self.icon_image, size=(200, 200))

        # Cria o label com a imagem e posiciona abaixo do título
        self.icon_label = ctk.CTkLabel(self.left_side_panel, image=self.ctk_image, text="")
        self.icon_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # self.left_side_panel WIDGET
        # Aqui é definido o logo que ficará no APP
        self.logo_label = ctk.CTkLabel(self.left_side_panel, text="Terminator 1.2.2", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(20, 10))

        # Botões do left_side_panel
        # Dicionário para armazenar os botões e facilitar a seleção
        self.buttons = {}

        # Botão Executed -> chama o método self.executed para mostrar os programas que já foram executados
        self.bt_executed = ctk.CTkButton(self.left_side_panel, text="Executed", command=self.executed, fg_color="#089c4c", width=200, height=50, font=("Arial", 17))
        self.bt_executed.grid(row=2, column=0, padx=20, pady=10)
        self.buttons["executed"] = self.bt_executed

        # Botão Schedule -> chama o método self.open_schedule para mostrar os programas agendados
        self.schedule_bt = ctk.CTkButton(self.left_side_panel, text="Schedule", command=self.open_schedule, fg_color="#089c4c", width=200, height=50, font=("Arial", 17))
        self.schedule_bt.grid(row=3, column=0, padx=20, pady=10)
        self.buttons["schedule"] = self.schedule_bt
        
        # Botão Programs -> chama o método self.open_programs para mostrar os programas cadastrados
        self.bt_programs = ctk.CTkButton(self.left_side_panel, text="Programs", command=self.open_programs, fg_color="#089c4c", width=200, height=50, font=("Arial", 17))
        self.bt_programs.grid(row=4, column=0, padx=20, pady=10)
        self.buttons["programs"] = self.bt_programs

        # Botão Users -> chama o método self.users para mostrar os usuários cadastrados
        self.user_bt = ctk.CTkButton(self.left_side_panel, text="Users", command=self.users, fg_color="#089c4c", width=200, height=50, font=("Arial", 17))
        self.user_bt.grid(row=5, column=0, padx=20, pady=10)
        self.buttons["users"] = self.user_bt

        # Botão Settings -> chama o método self._settings para mostrar as configurações do sistema
        self.settings_bt = ctk.CTkButton(self.left_side_panel, text="Settings", command=self._settings, fg_color="#089c4c", width=200, height=50, font=('Arial', 17))
        self.settings_bt.grid(row=15, column=0, padx=20, pady=10)

        # right_side_panel -> tem os conteúdos que mudam conforme o botão clicado no left_side_panel
        self.right_side_panel = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color="#000000")
        self.right_side_panel.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5)
        
        # Conteúdo inicial da right_side_panel
        self.right_dashboard = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color="#000000")
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

        # Instancia o usuário de seleção para o import de schedule
        self.selected_user = None

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
        self.button_frame = ctk.CTkFrame(self.right_dashboard, fg_color="#000000")
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
        self.style.configure("Treeview", background="#000000", foreground="white", fieldbackground="#000000", font=("Arial", 12, "normal"))
        self.style.configure("Treeview.Heading", background="#000000", foreground="white", fieldbackground="#000000", font=("Arial", 12, "bold"))
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
        self.button_frame = ctk.CTkFrame(self.right_dashboard, fg_color="#000000")
        self.button_frame.pack(pady=10)

        # Botão para exportar o schedule
        self.export_schedule_btn = ctk.CTkButton(self.button_frame, text="Export Schedule", command=self.create_export, fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.export_schedule_btn.pack(side=tkinter.LEFT, padx=10)

        # Botão para importar o scheduel
        self.import_schedule_btn = ctk.CTkButton(self.button_frame, text="Import Schedule", command=self.import_schedule, fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.import_schedule_btn.pack(side=tkinter.LEFT, padx=10)
        
        # Cria a tabela para exibir os programas agendados
        # Colunas da tabela:
        #   Program Path: caminho do aplicativo agendado
        #   Program Name: nome do aplicativo agendado
        #   Program Type: tipo do aplicativo agendado
        #   Days: dias da semana em que o programa será executado
        #   Execute Hour: horário em que o programa será executado
        columns = ("Program Name", "Program Path", "Program Type", "Days", "Execute Hour")
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
        self.style.configure("Treeview", background="#000000", foreground="white", fieldbackground="#000000", font=("Arial", 12, "normal"))
        self.style.configure("Treeview.Heading", background="#000000", foreground="white", fieldbackground="#000000", font=("Arial", 12, "bold"))
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
                    schedules.append((program["program_name"], partial_path, program["program_type"], day, hour))
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
#   Método 'create_export' para criar um excel template de importação de schedule de programas
#   Pede o caminho da pasta e o nome do arquivo para fazer o export
#   Utiliza a classe 'Create_Excel' de 'create_excel_template.py' 
#   Pega todos os schedules cadastrados no banco e coloca no arquivo para fazer a importação mais facilmente
#   Parâmetros:
#       Nenhum  
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def create_export(self):
        # Pede o caminho da pasta e o nome do arquivo
        file_name = filedialog.asksaveasfilename(title="Select the folder to save the Template Schedule", initialfile="Template_Schedule.xlsx", filetypes=[("Excel Files", "*.xlsx")])
        # Se o caminho for selecionado
        if file_name:
            # Instancia a classe
            excel = Create_Excel(file_name)
            # Adciona a primeira aba do excel 
            excel.add_sheet("Schedule")
            # Define as colunas da primeira aba
            excel.add_head("Schedule", ["Program", "Program", "HOUR", "MINUTE", "DAY_WEEK"])
            # Lista temporária para armazenar os dados antes de ordenar
            schedule_sort = []
            # Pega os dados do banco de dados para colocar no export
            for data in self.db_programs.get_all():
                # Separa os schedules para melhor tratamento de dados macro
                schedules = data['schedule_list'].split(',')
                for sche in schedules:
                    # Tenta fazer a separação dos dados micro
                    try:
                        # Separa tempo de dia
                        timepart, day = sche.split('-')
                        # Separa hora de minuto
                        hour, minute = timepart.split(':')
                        schedule_sort.append([data["id"], data["program_name"], int(hour), int(minute), day])
                    except:
                        schedule_sort.append([data["id"], data["program_name"], "", "", ""])

            # Ordena os dados por hora e minuto
            schedule_sort.sort(key=lambda x: (x[2] if isinstance(x[2], int) else 999, x[3] if isinstance(x[3], int) else 999))
            # Adiciona os dados ordenados ao Excel
            for row in schedule_sort:
                hour_str = str(row[2]).zfill(2) if row[2] is not None else ""
                minute_str = str(row[3]).zfill(2) if row[3] is not None else ""
                excel.add_line("Schedule", [row[0], row[1], hour_str, minute_str, row[4]])
            # Sheet number 2
            excel.add_sheet("Caption")
            excel.add_head("Caption", ["Caption and Atentions"])
            caption = "Program -> Program ID registered in the database. Can be verified in the Terminator 'Programs' tab.\n'Program_Name' -> Name of the program registered in the database. Can be verified in the Terminator 'Programs' tab.\n'HOUR' -> Time the program should run.\n'MINUTE' -> Minute the program should run.\n'DAY_WEEK' -> Day of the week the program should run."
            atencion1 = "ATENTION: PROGRAMS MUST BE PREVIOUSLY REGISTERED BEFORE IMPORTING ANY TYPE OF PROGRAM INTO THE RUNNING SCHEDULE!"
            atencion2 = "ATENTION: THE DATA FROM 'HOUR', 'MINUTE' AND 'DAY_WEEK' WILL BE CONCATENATED BY THE APP TO GENERATE THE SCHEDULE ACCEPTED BY THE DATABASE,\nSO 'HOUR' AND 'MINUTE' MUST CONTAIN EXACTLY TWO CHARACTERS AND 'DAY_WEEK' MUST BE THE DAYS OF THE WEEK IN ENGLISH!"
            atencion3 = "ATENTION: THE DATA ENTERED HERE WILL REPLACE YOUR CURRENT DATA. CHECK EACH SCHEDULE TO AVOID REWORK!"
            atencion4 = "The days used are:"
            days_list = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
            excel.add_line("Caption", [caption])
            excel.add_line("Caption", [atencion1])
            excel.add_line("Caption", [atencion2])
            excel.add_line("Caption", [atencion3])
            excel.add_line("Caption", [atencion4])
            for day in days_list:
                excel.add_line("Caption", [day])
            # Seve the export
            excel.save()
            CTkMessagebox(title="Success",message=f"Schedule Template Exported Successfully in:\n{file_name}'.",icon="check",button_color="#089c4c",justify="center")
            excel.open_excel_file()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método 'import_scheduele' para importar os dados de um excel com informações do schedule de rodagem dos programas
#   Pede o caminho completo do arquivo com os dados
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def import_schedule(self):
        list_user = []
        users_values = self.db_users.get_all()
        if users_values != []:
            # Abre a janela de registro de configurações
            password_dialog_adm = PasswordDialog(self)
            # Pega a senha do usuário antes de permitir o acesso às importação
            entered_password_adm = password_dialog_adm.get_password()
            # Verifica se a senha está correta
            if not Hash().check_login(entered_password_adm, self.db_settings.get_by_column("id", 1)["password"]):
                CTkMessagebox(
                    title="Error",
                    message="Incorrect password. Action canceled!",
                    icon="warning",
                    button_color="#089c4c",
                    justify="center"
                )
                self.folder_cleaner.stop()
                return
            # Para cada usuário
            for user in self.db_users.get_all():
                id_user = user["id"]
                name = user["user_name"]
                sesa = user["user_code"]
                # Cria uma string com os dados do usuário e adciona na lista
                user_data = f"{id_user}-{name}-{sesa}"
                list_user.append(user_data)
            # Abre a janela de seleção de usuário
            selector_window = Window_UserSelector(self, list_user)
            # Espera a janela ser fechada
            self.wait_window(selector_window)  
            # Pega o id do usuário selecionado
            id_user, name_user, sesa_user = self.selected_user.split("-")
            # Procura o usuário na base de dados
            user = self.db_users.get_by_column("id", id_user)
            # Se o usuário não existir retorna erro
            if not user:
                CTkMessagebox(title="Error", message="User does not find!", icon="warning", button_color="#089c4c", justify="center")
                return
            # Solicita a senha do dono
            password_dialog = PasswordDialog(self, user_or_adm=f"USER: {self.selected_user}")
            entered_password = password_dialog.get_password()
            # Verifica se a senha está correta
            # Se a senha estiver correta, abre a janela de alteração do usuário
            if not Hash().check_login(entered_password, user["password"]) == True:
                CTkMessagebox(
                    title="Error",
                    message="Incorrect password. Action canceled!",
                    icon="warning",
                    button_color="#089c4c",
                    justify="center"
                )
                self.folder_cleaner.stop()
                return
            # Abre o diálogo para seleção do arquivo de agendamento
            file_import_schedule = filedialog.askopenfilename(title="Select the Excel to import the Schedules", filetypes=[("Excel Files", "*.xlsx")])
            # Se o arquivo for selecionado
            if file_import_schedule:
                # Tenta abrir o arquivo
                try:
                    schedule_book = openpyxl.load_workbook(filename=file_import_schedule)
                # Retorna erro se o arquivo não puder ser aberto
                except Exception as e:
                    CTkMessagebox(
                        title="Error",
                        message=f"It is not possible open the file: {file_import_schedule}.\nCheck the error:\n{e}.",
                        icon="warning",
                        button_color="#089c4c",
                        justify="center"
                    )
                    return
                # Verifica se a aba "Schedule" existe
                if "Schedule" in schedule_book.sheetnames:
                    # Inicia o registro de importação
                    content_initiated_import = f"-------------------------------------------------------------------------------------------------------------------\nInitiated Schedule Import. Responsible Owner: {self.selected_user}\n"
                    self.manipulador.write_txt(self.manipulador.programs_txt, content_initiated_import)
                    # Obtém a aba "Schedule"
                    sheet = schedule_book["Schedule"]
                    line_list = [item for item in sheet.iter_rows(values_only=True)]
                    del line_list[0]  # Remove header

                    program_schedule_map = {}
                    agrouped = {}
                    duplicated_entries = []
                    # Para cada id, nome, hora, minuto e dia nos dados obtidos
                    for program_id, program_name, hour, minute, day in line_list:
                        # Verifica se os campos obrigatórios estão preenchidos:
                        if hour is None or minute is None or day is None:
                            content_hour_minute = f"The hour, minute, or day is missing for Program ID '{program_id}', Program Name '{program_name}'. Entry ignored.\n"
                            self.manipulador.write_txt(self.manipulador.programs_txt, content_hour_minute)
                            continue
                        # Tenta converter hora e minuto
                        try:
                            hour = int(hour)
                            minute = int(minute)
                        # Se hour ou minute não forem válidos retorna um erro
                        except ValueError:
                            content_error_int = f"It was not possible convert to integer the hour and/or minute for Program ID '{program_id}', Program Name '{program_name}'. Entry ignored.\n"
                            self.manipulador.write_txt(self.manipulador.programs_txt, content_error_int)
                            continue
                        # Verifica se a hora e o minuto estão dentro dos limites válidos
                        if not (0 <= hour < 24) or not (0 <= minute < 60):
                            content_error_hour_minute = f"The hour and/or minute is invalid for Program ID '{program_id}', Program Name '{program_name}'. Entry ignored.\n"
                            self.manipulador.write_txt(self.manipulador.programs_txt, content_error_hour_minute)
                            continue
                        # Lista de dias possíveis 
                        days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                        # Verifica se o dia é válido
                        if day.upper() not in [item.upper() for item in days_of_week]:
                            content_day = f"Invalid day of the week: {day}.\nMust be one of the following: {', '.join(days_of_week)}.\n"
                            self.manipulador.write_txt(self.manipulador.programs_txt, content_day)
                            continue
                        # Tenta criar a chave e o formato de hora
                        key = (program_id, program_name)
                        format_hour = f"{str(hour).zfill(2)}:{str(minute).zfill(2)}-{day}"
                        # Se a chave não existir no mapa, cria um novo conjunto
                        if key not in program_schedule_map:
                            program_schedule_map[key] = set()
                        # Se o formato de hora já estiver no conjunto, é uma entrada duplicada
                        # Verifica se há conflitos com programas iguais
                        if format_hour in program_schedule_map[key]:
                            content_duplicate = f"Duplicate schedule entry found for same program: '{format_hour}' already assigned to Program ID '{program_id}', Program Name '{program_name}'. Entry ignored.\n"
                            self.manipulador.write_txt(self.manipulador.programs_txt, content_duplicate)
                            duplicated_entries.append((key, format_hour))
                            continue
                        # Se o formato de hora já estiver no conjunto, é uma entrada duplicada
                        # Verifica se há conflitos com outros programas
                        for other_key, hours in program_schedule_map.items():
                            if other_key != key and format_hour in hours:
                                content_duplicate = f"Duplicate schedule entry found for different programs: '{format_hour}' already assigned to Program ID '{other_key[0]}', Program Name '{other_key[1]}'. Entry for Program ID '{program_id}', Program Name '{program_name}' ignored.\n"
                                self.manipulador.write_txt(self.manipulador.programs_txt, content_duplicate)
                                duplicated_entries.append((key, format_hour))
                                break
                        # Se não houver conflitos, adiciona a entrada ao mapa
                        else:
                            program_schedule_map[key].add(format_hour)

                            if key not in agrouped:
                                agrouped[key] = []
                            agrouped[key].append(format_hour)

                    # Para a rodagem automática para atualizar o schedule
                    self.end_scheduler()

                    # Limpa o campo schedule
                    self.db_programs.clear_field("schedule_list")

                    # Data atual para registro no banco
                    atual_date = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

                    # Iteração sobre os dados agrupados
                    for (program_id, program_name), schedule_hours in agrouped.items():
                        schedule_hours.sort()
                        # Agora junta todos os dados das horas formatadas
                        schedule_final = ",".join(schedule_hours)
                        self.db_programs.update_schedule_by_program(program_id=program_id, program_name=program_name, schdedule_final=schedule_final, modified_date=atual_date, manipulador=self.manipulador)

                    # Inicia novamente a rodagem automática com o banco de schedule atualizado
                    self.start_scheduler()
                    self.open_schedule()

                    # Escreve no log de programas quem e quando modificou o schedule
                    content = f"Schedule Loaded. Responsible Owner: {self.selected_user}.\nCheck the new schedules in the Terminator Schedule tab.\nModified Date: {atual_date}.\n-------------------------------------------------------------------------------------------------------------------\n"
                    self.manipulador.write_txt(self.manipulador.programs_txt, content)
                    CTkMessagebox(title="Success",message=f"Schedule Template Imported Successfully.",icon="check",button_color="#089c4c",justify="center")

                else:
                    CTkMessagebox(title="Error",message="The file is wrong: sheet 'Schedule' does not exist. \nFirst export the template!.", icon="warning",button_color="#089c4c",justify="center")
                    return
        else:
            CTkMessagebox(title="Error",message="There are no registered users. \nYou must register users before registering programs.", icon="warning",button_color="#089c4c",justify="center")
            return
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
        self.button_frame = ctk.CTkFrame(self.right_dashboard, fg_color="#000000")
        self.button_frame.pack(pady=10)
        # Botão Add Program -> chama o método self.add_programs para adicionar um novo programa
        self.add_programs_button = ctk.CTkButton(self.button_frame, text="Add Program", command=self.add_programs, fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.add_programs_button.pack(side=tkinter.LEFT, padx=10)
        # Botão Change Program -> chama o método self.change_programs para alterar um programa existente
        self.change_programs_button = ctk.CTkButton(self.button_frame, text="Change Program", command=self.change_programs, fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.change_programs_button.pack(side=tkinter.LEFT, padx=10)
        # Botão Delete Program -> chama o método self.delete_programs para excluir um programa existente
        self.delete_programs_button = ctk.CTkButton(self.button_frame, text="Delete Program", command=self.delete_programs, fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.delete_programs_button.pack(side=tkinter.LEFT, padx=10)
        # Botão History -> chama o método self.open_log para abrir a interface de visualização de logs
        self.logs_button = ctk.CTkButton(self.button_frame, text="History", command=lambda: self.open_log(self.manipulador.programs_txt, "Programs"), fg_color="#089c4c", width=100, height=50, font=("Arial", 17))
        self.logs_button.pack(side=tkinter.LEFT, padx=10)
        # Cria a tabela para exibir os programas cadastrados
        # Colunas da tabela:
        #   ID: identificador único do programa
        #   Program Path: caminho do programa
        #   Program Type: tipo do programa
        #   Program Name: nome do programa
        #   Owner: proprietário do programa
        #   Date Modified: data da última modificação do programa
        columns = ("ID", "Program Name", "Program Path", "Program Type", "Owner", "Date Modified")
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
        self.style.configure("Treeview", background="#000000", foreground="white", fieldbackground="#000000", font=("Arial", 12, "normal"))
        self.style.configure("Treeview.Heading", background="#000000", foreground="white", fieldbackground="#000000", font=("Arial", 12, "bold"))
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
            programs.append((app["id"], app["program_name"], partial_path, app["program_type"], owner_name, app["date_modified"]))
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
        self.button_frame = ctk.CTkFrame(self.right_dashboard, fg_color="#000000")
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
        self.style.configure("Treeview", background="#000000", foreground="white", fieldbackground="#000000", font=("Arial", 12, "normal"))
        self.style.configure("Treeview.Heading", background="#000000", foreground="white", fieldbackground="#000000", font=("Arial", 12, "bold"))
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
            menu.entryconfig(index, background="#000000", foreground="white", activebackground="#089c4c", activeforeground="white")
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

        user_values = f"{user["id"]}-{user["user_name"]}-{user["user_code"]}"
        # Solicita a senha do dono
        password_dialog = PasswordDialog(self, user_or_adm=f"USER: {user_values}")
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

        user_values = f"{user["id"]}-{user["user_name"]}-{user["user_code"]}"
        # Solicita a senha do dono
        password_dialog = PasswordDialog(self, user_or_adm=f"USER: {user_values}\nOR\nADM USER")
        entered_password = password_dialog.get_password()
        
        if Hash().check_login(entered_password, user["password"]) == True or (Hash().check_login(entered_password, self.db_settings.get_by_column("id", 1)["password"]) == True):
            # Deleta o programa
            self.end_scheduler()
            self.db_programs.delete(program_id)
            # Registra a ação no log de programas
            content = f"-------------------------------------------------------------------------------------------------------------------\nProgram Name: '{values[3].strip()}' Deleted.\nHour Deleted {datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}.\nOwner: {values[5].strip()}.\nProgram Type: {values[2].strip()}\n-------------------------------------------------------------------------------------------------------------------\n"
            self.manipulador.write_txt(self.manipulador.programs_txt, content)

            CTkMessagebox(title="Program deleted",message=f"Program '{program['program_name']}' has been deleted.",icon="check",button_color="#089c4c",justify="center")

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
            option_1="Close",
            # fade_in_duration=0.05,
            button_color="#089c4c",
            justify="center"
        )

        # Simula clique no botão após 3 segundos
        def close_box():
            try:
                msg_box.event_generate("<<MessageboxClose>>")
                msg_box.button_event("Close")
            except Exception as e:
                print(e)

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
                                content = f"-------------------------------------------------------------------------------------------------------------------\nProgram '{values[1].strip()}' Canceled.\nStart Hour: {values[2].strip()}.\nCanceled Hour: {datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}.\nType Run: {values[5].strip()}\n-------------------------------------------------------------------------------------------------------------------\n"
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
        
        user_values = f"{user["id"]}-{user["user_name"]}-{user["user_code"]}"
        # Solicita a senha do dono
        password_dialog = PasswordDialog(self, user_or_adm=f"USER: {user_values}\nOR\nADM USER")
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

        user_values = f"{user["id"]}-{user["user_name"]}-{user["user_code"]}"
        # Solicita a senha do dono
        password_dialog = PasswordDialog(self)
        entered_password = password_dialog.get_password()
        # Verifica se a senha está correta
        # Se a senha estiver correta, deleta o usuário e todos os programas dele
        if (Hash().check_login(entered_password, self.db_settings.get_by_column("id", 1)["password"]) == True):
            # Deleta todos os programas do usuário
            try:
                self.db_programs.delete_by_column("owner_id", user["id"])
            except:
                pass
            # Deleta o usuário
            self.db_users.delete(user["id"])
            # Registra a ação no log de usuários
            content = f"-------------------------------------------------------------------------------------------------------------------\nUser '{user_values[1].strip()}' Deleted.\nHour Deleted: {datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}.\nUser Code: {user_values[2].strip()}.\nUser E-mail: {user_values[3].strip()}\n-------------------------------------------------------------------------------------------------------------------\n"
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