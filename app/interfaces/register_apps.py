""" 
Código para a interface de registro de App's utilizando customtkinter.
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importações de bibliotecas necessárias
#   Bibliotecas externas:
#       os: para manipulação de arquivos e pastas
#       tkinter: para a criação da interface gráfica
#       customtkinter: para a criação da interface gráfica
#       CTkMessagebox: para exibir caixas de mensagem personalizadas
#       filedialog: para exibir uma caixa de "diálogo de arquivos"
#       datetime: para a manipulação de datas e horas
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#  
#   Importação dos módulos criados para o APP:
#       manipulador: para manipulação de arquivos e pastas
#       ProgramsDB, UsersDB, GenericDBOperations: para operações de banco de dados
#       PasswordDialog: para abir uma janela pedindo um input de senha
#       Hash: para hash e verificação de senhas
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import os
import tkinter
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
from datetime import datetime
from app.adm_files.manipulator import manipulador
from app.database.programsDB import ProgramsDB
from app.database.usersDB import UsersDB
from app.database.operationDBs import GenericDBOperations
from app.security.password_dialog import PasswordDialog
from app.security.password_hash import Hash
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Configuração de modo de aparência e tema do customtkinter
#   Define o modo de aparência para "dark" e o tema de cores para "green"
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
DARK_MODE = "dark"
ctk.set_appearance_mode(DARK_MODE)
ctk.set_default_color_theme("green")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Classe que vai construir a Interface de cadastro de App's
#   Possui os seguintes Métodos:
#       __init__: construtor da classe que inicializa a interface e seus componentes
#       on_closing: define o que e como fazer quando o usuário decidir fecar a janela repentinamente
#       extension_path: define qual a extensão que deve ser procurada a partir do type_program
#       select_path: método para o usuário selecionar o caminho do arquivo de acordo com o extension_path
#       validate_hour: verifica se a hora que o usuário deseja inputar no schedule é válida
#       validate_minute: verifica se os minutos que o usuário deseja inputar np schedule são válidos
#       add_time: método para adicionar o horário e o dia da semana no schedule, caso seja válido
#       remove_time: método para remover o horário e o dia da semana no schedule
#       load_existing_times: método para verificar se o horário que o usuário deseja inputar já não existe no banco ou no próprio schedule
#       add_parameter: método para adicionar um parâmetro na lista de parâmetros de rodagem
#       remove_parameter: método para remover um parâmetro na lista de parâmetros
#       update_param_input: método para adicionar um botão caso o parâmetro seja uma senha ou adicionar outro tipo de botão caso seja um arquivo
#       select_path_for_param: método chamado pelo botão de seleção de arquivo do parâmetros para seleção de algum arquivo
#       change_visibility: méotdo chamado pelo botão de passowrd para alterar a visibilidade da senha parâmetro
#       register_data: método para registrar os dados inputados pelo usuário no banco de dados ProgramsDB
#   Parâmetros: 
#       ctk.CTk
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class Inter_Register_APP(ctk.CTkToplevel):
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Contrutuor da classe Register
#   No construtor é definida a estrutura da interface (seus widgets, textso, imagens)
#   ATENÇÃO: CASO QUEIRA ADICIONAR ELEMENTOS, SIGA O PADRÃO DA ESTRUTURA
#   Parâmetros: 
#       program_type: tipo do porgrama (pré-definido como "" string vazia)
#       program_data: dados do programa (caso seja um item novo é pré-definido como None, caso exista os dados é só colocar como parâmetro)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self, main_app, programtype="", program_data=None):
        # Cria uma instância do manipulador
        self.manipulador = manipulador()

        # Define a classe da interface principal
        self.main_app = main_app
        self.program_data = program_data
        self.main_app.withdraw()

        self.app_type = programtype
        self.programsdb = GenericDBOperations(ProgramsDB,"sqlite:///C:/Terminator/Database/executerDB.db")
        self.usersdb = GenericDBOperations(UsersDB, "sqlite:///C:/Terminator/Database/executerDB.db")

        # Chama o construtor da classe ctk.CTk
        super().__init__()

        # Define o título da Janela
        self.title("Register App")

        # Faz com que o APP seja grande o suficiente para preencher toda a tela
        self.resizable(False, False)
        
        # Define o tamanho da janela
        width = 550
        height = 670

        # Centraliza a janela na tela
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Definindo uma cor padrão
        self.bg_color = "#333333"

        # Aqui é definido o primeiro Widget. Widget raiz
        self.main_container = ctk.CTkFrame(self, corner_radius=10, fg_color=self.bg_color)
        self.main_container.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        # Define um protocolo de fechamento repentino
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Layout grid configuration
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(2, weight=1)
        self.main_container.grid_rowconfigure(3, weight=1)
        self.main_container.grid_rowconfigure(4, weight=1)

        # Sub-container to center the form
        self.form_container = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color=self.bg_color)
        self.form_container.grid(row=0, column=0, columnspan=2, sticky="n")

        # Campo Application Path
        self.entry_path = ctk.CTkEntry(self.form_container, width=400, placeholder_text="APP Path")
        self.entry_path.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Botão para selecionar o arquivo
        self.button_path = ctk.CTkButton(self.form_container, text="Browse", fg_color="#089c4c", command=self.select_path)
        self.button_path.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Campo Application Type (agora como Entry)
        self.entry_type = ctk.CTkEntry(self.form_container, width=200)
        self.entry_type.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_type.insert(0, self.app_type)
        self.entry_type.configure(state="readonly")

        # Campo Application Name
        self.entry_name = ctk.CTkEntry(self.form_container, width=400, placeholder_text="APP Name")
        self.entry_name.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        # Lista de opções para o dono (exemplo)
        self.owner_name_to_id = {user["user_name"]: user["id"] for user in self.usersdb.get_all()}
        owner_options = list(self.owner_name_to_id.keys())

        self.entry_owner_name = ctk.CTkComboBox(self.form_container, values=owner_options, width=400, state="readonly")
        self.entry_owner_name.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_owner_name.set("Select the Owner")

        # Campo Horários
        self.hours_container = ctk.CTkFrame(self.form_container, corner_radius=10, fg_color=self.bg_color)
        self.hours_container.grid(row=5, column=0, columnspan=2, sticky="n")

        self.frame_times = ctk.CTkFrame(self.hours_container, fg_color=self.bg_color)
        self.frame_times.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.hour_var = tkinter.StringVar(value="12")
        self.minute_var = tkinter.StringVar(value="00")
        self.day_var = tkinter.StringVar(value="Monday")

        vcmd_hour = self.register(self.validate_hour)
        vcmd_minute = self.register(self.validate_minute)

        self.spinbox_hour = tkinter.Spinbox(self.frame_times, from_=0, to=23, textvariable=self.hour_var, width=5, format="%02.0f", validate="key", validatecommand=(vcmd_hour, '%P'))
        self.spinbox_minute = tkinter.Spinbox(self.frame_times, from_=0, to=59, textvariable=self.minute_var, width=5, format="%02.0f", validate="key", validatecommand=(vcmd_minute, '%P'))
        dias_semana = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.spinbox_days = tkinter.Spinbox(self.frame_times, values=dias_semana, textvariable=self.day_var, width=10, state="readonly", wrap=True)

        # Campos de hora, minuto e dia
        self.spinbox_hour.grid(row=0, column=0, padx=5, pady=5)
        self.spinbox_minute.grid(row=0, column=1, padx=5, pady=5)
        self.spinbox_days.grid(row=0, column=2, padx=5, pady=5)

        # Botões lado a lado e centralizados
        self.button_add_time = ctk.CTkButton(self.frame_times, text="+", fg_color="#089c4c", command=self.add_time, width=30, height=30, font=("Arial", 20, "bold"))
        self.button_delete_time = ctk.CTkButton(self.frame_times, text="-", fg_color="#089c4c", command=self.remove_time, width=30, height=30, font=("Arial", 20, "bold"))

        self.button_add_time.grid(row=1, column=0, padx=5, pady=(0, 10))
        self.button_delete_time.grid(row=1, column=1, padx=5, pady=(0, 10))

        self.times_listbox = tkinter.Listbox(self.frame_times, width=15, height=5, bg=self.bg_color, fg="white", font=("Arial", 12, "bold"), justify="left", selectbackground="#089c4c")
        self.times_listbox.grid(row=0, column=3, rowspan=2, padx=10, pady=5)

        self.times_list = []        

        # ---------------------- Parâmetros ---------------------- #
        self.parameters_container = ctk.CTkFrame(self.form_container, corner_radius=10, fg_color=self.bg_color)
        self.parameters_container.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

        self.param_value_var = tkinter.StringVar()
        self.param_category_var = tkinter.StringVar(value="Select Category")

        self.entrys_parameters_container = ctk.CTkFrame(self.parameters_container, corner_radius=10, fg_color=self.bg_color)
        self.entrys_parameters_container.grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=10)

        self.combo_param_category = ctk.CTkComboBox(self.entrys_parameters_container,values=["password", "value", "path", "number"],width=150,state="readonly",variable=self.param_category_var,command=lambda _: self.update_param_input())
        self.combo_param_category.grid(row=0, column=0, padx=5, pady=5)

        # Campo de valor (inicial)
        self.entry_param_value = ctk.CTkEntry(self.entrys_parameters_container,width=210,placeholder_text="Value",textvariable=self.param_value_var)
        self.entry_param_value.grid(row=0, column=1, padx=5, pady=5)

        # Botão de seleção de caminho (inicialmente oculto)
        self.button_browse_path = ctk.CTkButton(self.entrys_parameters_container, text="Browse", fg_color="#089c4c", command=self.select_path_for_param, width=80 )
        
        # Só será exibido se a categoria for "path"
        # Botão de hide/show password
        self.button_hide_show = ctk.CTkButton(self.entrys_parameters_container, text="Show", corner_radius=5, fg_color="#089c4c", width=80, command=self.change_visibility)

        self.bt_parameters_frame = ctk.CTkFrame(self.entrys_parameters_container, corner_radius=0, fg_color=self.bg_color)
        self.bt_parameters_frame.grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=10)

        self.button_add_param = ctk.CTkButton(self.bt_parameters_frame, text="+", fg_color="#089c4c", command=self.add_parameter, width=30, height=30, font=("Arial", 20, "bold"))
        self.button_delete_param = ctk.CTkButton(self.bt_parameters_frame, text="-", fg_color="#089c4c", command=self.remove_parameter, width=30, height=30, font=("Arial", 20, "bold"))

        self.button_add_param.grid(row=1, column=0, padx=5, pady=(0, 10))
        self.button_delete_param.grid(row=1, column=1, padx=5, pady=(0, 10))

        self.params_listbox = tkinter.Listbox(self.parameters_container, width=42, height=5, bg=self.bg_color, fg="white", font=("Arial", 12, "bold"), justify="left", selectbackground="#089c4c")
        self.params_listbox.grid(row=2, column=0, rowspan=2, padx=10, pady=5)

        self.parameters_list = []

        self.bnt_register_container = ctk.CTkFrame(self.form_container, corner_radius=10, fg_color=self.bg_color)
        self.bnt_register_container.grid(row=7, column=0, columnspan=2, sticky="n")

        # Define o botão de confirmação de registro
        self.button_register = ctk.CTkButton(self.bnt_register_container, text="Save", fg_color="#089c4c", command=self.register_data)
        self.button_register.grid(row=5, column=1, pady=5, sticky="w")

        self.existing_times = self.load_existing_times()
        
        # Se os dados existirem, já preenche nos campos da interface
        if self.program_data:
            self.app_type = self.program_data["program_type"]
            
            self.entry_path.insert(0, self.program_data["program_path"])
            self.entry_type.configure(state="normal")
            self.entry_type.insert(0, self.program_data["program_type"])
            self.entry_type.configure(state="readonly")
            self.entry_name.insert(0, self.program_data["program_name"])

            owner_id = self.program_data["owner_id"]
            owner_name = next((name for name, uid in self.owner_name_to_id.items() if uid == owner_id), None)
            if owner_name:
                self.entry_owner_name.set(owner_name)

            self.times_list = self.program_data["schedule_list"].split(",") if self.program_data["schedule_list"] else []
            for time in self.times_list:
                self.times_listbox.insert(tkinter.END, time)
            
            self.parameters_list = self.program_data["parameters"].split(",") if self.program_data["parameters"] else []
            for parameter  in self.parameters_list:
                self.params_listbox.insert(tkinter.END, parameter)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que define o que fazer e como fazer caso o usuário feche repentnamente a janela
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def on_closing(self):
        result = CTkMessagebox(title="Confirmation", message="Do you really want to close the window?", icon="question", option_1="Yes", option_2="No", button_color="#089c4c", justify="center").get()
        if result == "Yes":
            CTkMessagebox(title="Error", message="You closed the window incorrectly!", icon="warning", button_color="#089c4c", justify="center")
            self.destroy()
            self.main_app.after(100, lambda: [self.main_app.deiconify(), self.main_app.max_window()])
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que define qual o tipo de extensão que o select_path deve usar
#   Parâmetros:
#       type_program: tipo do programa que o usuário quer cadastrar
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def extension_path(self, type_program):
        if type_program == "Python":
            filetypes = [("Python files", "*.py")]
            return filetypes
        elif type_program == "Executable":
            filetypes = [("Executable files", "*.exe")]
            return filetypes
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que abre uma janela de pesquisa de arquivo para o usuário selecionar o programa desejado
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#        
    def select_path(self):
        filetypes = self.extension_path(self.app_type)
        path = filedialog.askopenfilename(filetypes=filetypes)
        self.entry_path.delete(0, tkinter.END)
        self.entry_path.insert(0, path)
        
        self.entry_type.configure(state="normal")
        self.entry_type.delete(0, tkinter.END)
        self.entry_type.insert(0, self.app_type)
        self.entry_type.configure(state="readonly")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para validar a hora inputada pelo usuário
#   Parâmetros:
#       value: valor da hora inputada
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def validate_hour(self, value):
        if value.isdigit() and 0 <= int(value) <= 23:
            return True
        return False
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Méotodo para validar os minutos inputados pelo usuário
#   Parâmetros:
#       value: valor dos minutos inputados
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def validate_minute(self, value):
        if value.isdigit() and 0 <= int(value) <= 59:
            return True
        return False
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para adicionar o tempo na lista de tempos schedule de rodagem
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def add_time(self):
        new_time = f"{self.spinbox_hour.get()}:{self.spinbox_minute.get()}-{self.spinbox_days.get()}"
        if new_time not in self.times_list and new_time not in self.existing_times:
            self.times_list.append(new_time)
            self.times_listbox.insert(tkinter.END, new_time)
        else:
            CTkMessagebox(title="Error", message="Schedule already added!", icon="warning", button_color="#089c4c", justify="center")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para remover o tempo na lista de tempos schedule de rodagem
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def remove_time(self):
        selected_time = self.times_listbox.curselection()
        if selected_time:
            index = selected_time[0]
            self.times_listbox.delete(index)
            del self.times_list[index]
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para verificar se existe o tempo na lista de rodagem ou no próprio schedule do programa
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def load_existing_times(self):
        existing_times = []
        try:
            for app in self.programsdb.get_all():
                times = app["schedule_list"].strip().split(",")
                for time in times:
                    existing_times.append(time)

        except FileNotFoundError:
            pass

        return existing_times
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para adicionar o parâmetro na lista de parâmetros necessários pelo programa
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#     
    def add_parameter(self):
        value = self.param_value_var.get().strip()
        category = self.param_category_var.get()

        if not value or category == "Select Category":
            CTkMessagebox(
                title="Input Error",
                message="Please fill all parameter fields.",
                icon="warning",
                button_color="#089c4c",
                justify="center")
            return

        # Validação por categoria
        try:
            if category == "number":
                float(value)
            elif category == "value":
                value
            elif category == "path":
                if not os.path.exists(value):
                    raise ValueError("Invalid path.")
            elif category == "password":
                if len(value) < 4:
                    raise ValueError("Password too short.")
                value = Hash().create_hash(value)
                
        except Exception as e:
            CTkMessagebox(
                title="Validation Error",
                message=f"Invalid value for category '{category}': {e}",
                icon="warning",
                button_color="#089c4c",
                justify="center")
            return

        param_str = f"{category}: {value}"
        self.parameters_list.append(f"{category}: {value}")
        self.params_listbox.insert(tkinter.END, param_str)

        self.param_value_var.set("")
        self.entry_param_value.configure(show="")
        self.param_category_var.set("Select Category")
        self.button_hide_show.grid_forget()
        self.button_browse_path.grid_forget()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que remove o parâmetro da lista de parâmetros do programa
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def remove_parameter(self):
        selected = self.params_listbox.curselection()
        if selected:
            index = selected[0]
            self.params_listbox.delete(index)
            del self.parameters_list[index]
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para atualizar o entry de input de parâmetros e definir os botões de password e path caso seja selcionados
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def update_param_input(self):
        category = self.param_category_var.get()

        # Reset
        self.param_value_var.set("")
        self.button_hide_show.configure(text="Show")
        self.button_hide_show.grid_forget()
        self.button_browse_path.grid_forget()

        if category == "password":
            self.entry_param_value.configure(show="*")
            self.button_hide_show.grid(row=1, column=1, padx=5, pady=5)

        elif category == "path":
            self.button_browse_path.grid(row=1, column=1, padx=5, pady=5)
        else:
            self.entry_param_value.configure(show="")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Métod para selecionar o arquivo/pasta do parâmetro path (caso seja selecionado previamente)
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def select_path_for_param(self):
        path = filedialog.askopenfilename()
        if path:
            self.param_value_var.set(path)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para alterar a visibilidade do parâmetro senha (caso seja selcionado previamente)
#   Parâmetros
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def change_visibility(self):
        if self.button_hide_show.cget("text") == "Show":
            self.button_hide_show.configure(text="Hide")
            self.entry_param_value.configure(show="")
        else:
            self.button_hide_show.configure(text="Show")
            self.entry_param_value.configure(show="*")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para registrar o programa no banco de dados com os parâmetros e arquivos necessários cadastrados pelo usuário
#   Alguns parâmetros são mandatórios:
#       app_path: caminho completo do programa
#       program_type: tipo do programa 
#       app_name: nome do programa
#       owner_name: owner/dono do programa que será rodado
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def register_data(self):
        # Verifica se todos os campos obrigatórios estão preenchidos
        app_path = self.entry_path.get()
        program_type = self.entry_type.get()
        app_name = self.entry_name.get()
        owner_name = self.entry_owner_name.get()
        
        if not os.path.exists(app_path):
            CTkMessagebox(title="Error",
                          message=f"The '{app_path}' does not exist!",
                          icon="warning",
                          button_color="#089c4c",
                          justify="center")
            return
        
        if not app_path or program_type == "Select the Type" or not app_name or owner_name == "Select the Owner":
            CTkMessagebox(title="Error",
                          message="Fill in all required fields!",
                          icon="warning",
                          button_color="#089c4c",
                          justify="center")
            return
        
        if self.times_list == []:
            confirm = CTkMessagebox(title="Atencion!",
                                    message="This program does not have set schedules.\nDo you want to continue anyway?",
                                    icon="warning",
                                    option_1="Yes",
                                    option_2="No",
                                    button_color="#089c4c",
                                    justify="center").get()

            if confirm != "Yes":
                return

        # Verifica a senha do usuário selecionado
        owner_id = self.owner_name_to_id[owner_name]
        user = self.usersdb.get_by_column("id", owner_id)

        # Dados comuns
        program_data = {
            "program_path":app_path,
            "program_name":app_name,
            "program_type":program_type,
            "owner_id":owner_id,
            "schedule_list":','.join(self.times_list),
            "parameters":','.join(self.parameters_list),
            "date_modified":datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        }

        # Atualiza ou registra
        if hasattr(self, "program_data") and self.program_data:
            self.programsdb.update(self.program_data["id"], **program_data)
            content = f"Program: '{app_name}' Updated.\nHour Updated: {datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}.\nOwner: {owner_name}.\nProgram Type: {program_type}.\nList Hours: {self.times_list}\n"
            self.manipulador.write_txt(self.manipulador.programs_txt, content)
            
            CTkMessagebox(
                title="Success",
                message="APP updated successfully!",
                icon="info",button_color="#089c4c",
                justify="center")
            
        else:
            # Solicita a senha do usuário
            password_dialog = PasswordDialog(self)
            entered_password = password_dialog.get_password()

            if entered_password is None:
                return  # Usuário fechou a janela

            # Verifica a senha do usuário selecionado
            owner_id = self.owner_name_to_id[owner_name]
            user = self.usersdb.get_by_column("id", owner_id)

            if not user or (Hash().check_login(entered_password, user["password"]) != True):
                CTkMessagebox(
                    title="Error",
                    message="Incorrect password. Operation cancelled!",
                    icon="warning",
                    button_color="#089c4c",
                    justify="center")
                return

            self.programsdb.register(**program_data)

            content = f"Program: '{app_name}' Registered.\nHour Registered: {datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}.\nOwner: {owner_name}.\nProgram Type: {program_type}.\nList Hours:{self.times_list}\n"
            self.manipulador.write_txt(self.manipulador.programs_txt, content)
            
            CTkMessagebox(
                title="Success",
                message="APP registered successfully!",
                icon="info",
                button_color="#089c4c",
                justify="center")

        self.destroy()
        self.main_app.after(100, lambda: [self.main_app.deiconify(), self.main_app.max_window()])