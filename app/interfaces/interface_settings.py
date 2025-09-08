""" 
Código para a interface de registro de configurações utilizando customtkinter.
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importação das bibliotecas necessárias para o funcionamento do APP
#   Biblitecas externas:
#       tkinter: para a criação da interface gráfica
#       customtkinter: para a criação da interface gráfica
#       datetime: para a manipulação de datas e horas
#       CTkMessagebox: para exibir caixas de mensagem personalizadas
#       os: para manipulação de arquivos e pastas
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importação dos módulos criados para o APP:
#       manipulador: para manipulação de arquivos e pastas
#       TextViewerApp: para visualizar arquivos de log
#       GenericDBOperations, SettingsDB: para operações de banco de dados
#       Hash: para hash e verificação de senhas
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#       
import tkinter
from tkinter import filedialog
import customtkinter as ctk
from datetime import datetime
from CTkMessagebox import CTkMessagebox
from app.adm_files.manipulator import manipulador, os
from app.interfaces.interface_log import TextViewerApp
from app.database.settingsDB import SettingsDB
from app.database.operationDBs import GenericDBOperations
from app.security.password_hash import Hash

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Configuração de modo de aparência e tema do customtkinter
#   Define o modo de aparência para "dark" e o tema de cores para "green"
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
DARK_MODE = "dark"
ctk.set_appearance_mode(DARK_MODE)
ctk.set_default_color_theme("green")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Classe que gera a interface de registro/alteração das configurações
#   Herda de CTkToplevel para criar uma janela separada
#   Métodos principais da classe:
#       __init__: construtor da classe que inicializa a interface e seus componentes
#       open_log: método chamado por um botão para abrir o log do settings
#       on_closing: define como e o que fazer quando a janela for fechada
#       select_path: método chamado por um botão para o usuário selecionar o caminho de um arquivo
#       select_folder: método chamado por um botão para o usuário selecionar o caminho de uma pasta
#       add_folder: método para adicionar o caminho da pasta selecionada pelo usuário na lista de exclusão de arquivos
#       remove_folder: método para remover o caminho da pasta selecionada pelo usuário na lista de exclusçao de aquivos
#       change_visibility: método chamado por um botão que altera a visibilidade da senha
#       register_data: método que registra os dados inputados pelo usuário no banco de dados, tabela SettingsDB
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class Inter_Settings(ctk.CTkToplevel):
    def __init__(self, main_app, settings_data=None):
        # Cria uma instância do manipulador
        self.manipulador = manipulador()

        # Define a classe da interface principal
        self.main_app = main_app
        self.settings_data = settings_data
        # Esconde a janela principal
        self.main_app.withdraw()

        self.settingsdb = GenericDBOperations(SettingsDB, "sqlite:///C:/Terminator/Database/executerDB.db")

        # Chama o construtor da classe ctk.CTk
        super().__init__()

        # Define o título da janela
        self.title("Settings")

        # Faz com que o APP seja grande o sufuciente para preencher toda a tela
        self.resizable(False, False)
        
        # Define o tamanho da janela
        width = 550
        height = 450
        self.geometry(f"{width}x{height}")

        # Centraliza a janela na tela
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        # Definindo uma cor padrão
        self.bg_color = "#333333"

        # Aqui é definido o prinmeiro widget (raiz)
        self.main_container = ctk.CTkFrame(self, corner_radius=10, fg_color=self.bg_color)
        self.main_container.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        # Define um protocolo de fechamento repentino
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Layout grid configuration
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(2, weight=1)

        # Sub-container to center the form
        self.form_container = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color=self.bg_color)
        self.form_container.grid(row=0, column=0, sticky="n")

        # Frame para entrada do caminho do .bat + botão
        self.bat_path_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.bat_path_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Campo .bat Path
        self.entry_tableau_bat = ctk.CTkEntry(self.bat_path_frame, width=400, placeholder_text="Program Path")
        self.entry_tableau_bat.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Botão para selecionar o arquivo '.bat'
        self.button_path = ctk.CTkButton(self.bat_path_frame, text=".bat File", fg_color="#089c4c", width=70, height=35, command=self.select_path)
        self.button_path.grid(row=0, column=1, sticky="w")

        # Campo Senha
        # Frame para entrada de senha + botão de visualização
        self.password_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.password_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_password = ctk.CTkEntry(self.password_frame, width=400, show="*", placeholder_text="Password")
        self.entry_password.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.button_eye = ctk.CTkButton(self.password_frame,width=70,height=35,text="Show",fg_color="#089c4c",command=self.change_visibility)
        self.button_eye.grid(row=0, column=1, sticky="w")

        self.folder_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.folder_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.entry_folder = ctk.CTkEntry(self.folder_frame, width=400, placeholder_text="Select the path to clean")
        self.entry_folder.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.bt_select_folder = ctk.CTkButton( self.folder_frame, width=70, height=35, text="Browse", fg_color="#089c4c", command=lambda: self.select_folder(self.entry_folder))
        self.bt_select_folder.grid(row=0, column=1, sticky="w")

        # Frame que contém os botões e o listbox
        self.list_box_frame = ctk.CTkFrame(self.folder_frame, fg_color="transparent")
        self.list_box_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="w")

        # Sub-frame para os botões "+" e "-"
        self.buttons_frame = ctk.CTkFrame(self.list_box_frame, fg_color="transparent")
        self.buttons_frame.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        self.bt_add_folder = ctk.CTkButton(self.buttons_frame, text="+", fg_color="#089c4c", command=self.add_folder, width=30, height=30, font=("Arial", 20, "bold"))
        self.bt_add_folder.grid(row=0, column=0, padx=5, pady=5)

        self.bt_remove_folder = ctk.CTkButton(self.buttons_frame, text="-", fg_color="#089c4c", command=self.remove_folder, width=30, height=30, font=("Arial", 20, "bold"))
        self.bt_remove_folder.grid(row=1, column=0, padx=5, pady=5)

        # Listbox com largura ajustada
        self.folders_listbox = tkinter.Listbox(self.list_box_frame, width=57, height=5, bg=self.bg_color, fg="white", font=("Arial", 9, "bold"), justify="left", selectbackground="#089c4c")
        self.folders_listbox.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.folders_list = []

        self.bnt_register_container = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color=self.bg_color)
        self.bnt_register_container.grid(row=2, column=0, sticky="n")
        
        # Define o botão de confirmação de registro
        self.button_register = ctk.CTkButton(self.bnt_register_container, text="Save", fg_color="#089c4c", command=self.register_data)
        self.button_register.grid(row=5, column=1, pady=5, sticky="w")

        self.button_log_settings = ctk.CTkButton(self.bnt_register_container, text="History",  fg_color="#089c4c", command=lambda: self.open_log(self.manipulador.settings_txt, "Settings"))
        self.button_log_settings.grid(row=6, column=1, pady=5, sticky="w")

        if self.settings_data:
            self.entry_tableau_bat.insert(0, self.settings_data["tableau_bat"])
            self.entry_password.insert(0, Hash().restore_password(self.settings_data["password"]))
            self.folders_list = self.settings_data["paths_delete"].split(",") if self.settings_data["paths_delete"] else []
            for folder in self.folders_list:
                self.folders_listbox.insert(tkinter.END, folder)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que abre a janela de log txt das operações do banco Settings
#   Parâmetros:
#       path_log: caminho do arquivo .txt onde está armaenado o log
#       name_log: nome do log (apenas como modo de visualização no titulo da janela)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def open_log(self, path_log, name_log):
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
#   Método que define o que fazer e como fazer quando o usuário desejar fechar a janela repentinamente 
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def on_closing(self):       
        # Pergunta para o usuário se ele deseja realmente fechar a janela 
        result = CTkMessagebox(title="Confirmation", message="Do you really want to close the window?", icon="question", option_1="Yes", option_2="No", button_color="#089c4c", justify="center").get()
        if result == "Yes":
            if self.settingsdb.get_all() == []:
                cancel_inicialization = CTkMessagebox(title="Confirmation", message="The program cannot be started without the settings. Do you really want to cancel the program's initialization? (You will lose all previously entered data)", icon="question", option_1="Yes", option_2="No", button_color="#089c4c", justify="center").get()
                if cancel_inicialization == "Yes":
                    self.main_app.destroy()
            else:
                CTkMessagebox(title="Error", message="You closed the window incorrectly!", icon="warning", button_color="#089c4c", justify="center")
                self.destroy()
                self.destroy()
                self.main_app.after(100, lambda: [self.main_app.deiconify(), self.main_app.max_window()])   
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que abre uma janela de "diálogo de arquivo" para o usuário selecionar um arquivo
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def select_path(self):
        filetypes = [("Tableau Prep .bat file", "*.bat")]
        path = filedialog.askopenfilename(filetypes=filetypes)
        self.entry_tableau_bat.delete(0, tkinter.END)
        self.entry_tableau_bat.insert(0, path)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que abre uma janela de "diálogo de arquivo" para o usuário selecionar uma pasta
#   Parâmetros:
#       target_entry: parametro para definir qual entry colocar o dado selecionado (dessa forma consigo usar a mesma função para entry's diferentes)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#  
    def select_folder(self, target_entry):
        folder = filedialog.askdirectory()
        if folder:
            target_entry.delete(0, tkinter.END)
            target_entry.insert(0, folder)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para adicionar da lista de limpeza a pasta selecionada pelo usuário
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def add_folder(self):
        new_folder = f"{self.entry_folder.get()}"

        if new_folder != "":
            if new_folder not in self.folders_list: #and new_folder not in self.existing_folder:
                self.folders_list.append(new_folder)
                self.folders_listbox.insert(tkinter.END, new_folder)
                self.entry_folder.delete(0, tkinter.END)
                self.entry_folder.configure()
            else:
                CTkMessagebox(title="Error", message=f"Folder '{new_folder}' already added!", icon="warning", button_color="#089c4c", justify="center")
        else:
            CTkMessagebox(title="Error", message=f"Cannot add an empty value", icon="warning", button_color="#089c4c", justify="center")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para remover da lista de limpeza a pasta selecionada pelo usuário
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def remove_folder(self):
        selected_folder = self.folders_listbox.curselection()
        if selected_folder:
            index = selected_folder[0]
            self.folders_listbox.delete(index)
            del self.folders_list[index]
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para alterar a visibilidade da string password quando selecionada
#   Altera a visualização de "*" para caracteres normais e vice-versa
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def change_visibility(self):
            # Se a string que estiver contida no botão == "Show", quando aperta muda para "Hide" e o que estiver no entry fica normal
            if self.button_eye.cget("text") == "Show":
                self.button_eye.configure(text="Hide")
                self.entry_password.configure(show="")
            # Se não, muda para "Show" e o que estiver no entry fica como "*"
            else:
                self.button_eye.configure(text="Show")
                self.entry_password.configure(show="*")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para registrar os dados selecionados pelo usuário
#   Alguns dados são obrigatório:
#       tableau_bat
#       password
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def register_data(self):
        tableau_bat = self.entry_tableau_bat.get()
        password = self.entry_password.get()

        if not tableau_bat or not password:
            CTkMessagebox(
                title="Error",
                message="Fill in all required fields!",
                icon="warning",
                button_color="#089c4c",
                justify="center"
            )
            return
                
        settings_data = {
            "tableau_bat": tableau_bat,
            "password": Hash().create_hash(password),
            "paths_delete": ",".join(self.folders_list)
        }

        if hasattr(self, "settings_data") and self.settings_data:
            self.settingsdb.update(self.settings_data["id"], **settings_data)

            content = f"Settings Updated {datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}.\nTableau Bat: {tableau_bat}.\nPaths to delete: {self.folders_list}.\n"
            self.manipulador.write_txt(self.manipulador.settings_txt, content)

            CTkMessagebox(
                title="Success",
                message="Settings updated successfully!",
                icon="info",
                button_color="#089c4c",
                justify="center"
            )
        
        else:
            self.settingsdb.register(**settings_data)
            
            content = f"Settings Updated {datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}.\nTableau Bat: {tableau_bat}.\nPaths to delete: {self.folders_list}.\n"
            self.manipulador.write_txt(self.manipulador.settings_txt, content)
            
            CTkMessagebox(title="Success", message="Settings registered successfully!", icon="info", button_color="#089c4c", justify="center")
        
        self.destroy()
        self.main_app.after(100, lambda: [self.main_app.deiconify(), self.main_app.max_window()])