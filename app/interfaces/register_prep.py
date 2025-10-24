""" 
Codigo para a interface de registro de Prep's utilizando customtkinter.
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.1
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importações de bibliotecas necessárias
#   Bibliotecas externas:
#       os: para manipulação de arquivos e pastas
#       re: para expressões regulares
#       ast: para manipulação de estruturas de dados
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
import re
import ast
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
#   Parâmetros: ctk.CTk
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Classe que vai construir a Interface de cadastro de App's
#   Possui os seguintes Métodos:
#       __init__: construtor da classe que inicializa a interface e seus componentes
#       on_closing: define o que e como fazer quando o usuário decidir fecar a janela repentinamente
#       toggle_senha: método para alternar a visibilidade da senha
#       validar_campos_out: método para validar os campos de saída
#       validar_campos_in: método para validar os campos de entrada
#       obter_dados_output: método para obter os dados de saída
#       obter_dados_input: método para obter os dados de entrada
#       preencher_output: método para preencher os campos de saída com os dados obtidos
#       preencher_input: método para preencher os campos de entrada com os dados obtidos
#       limpar_output: método para limpar os campos de saída
#       limpar_input: método para limpar os campos de entrada
#       atualizar_status_output: método para atualizar o status dos campos de saída
#       atualizar_status_input: método para atualizar o status dos campos de entrada
#       próximo_output: método para avançar para o próximo conjunto de dados de saída
#       proximo_input: método para avançar para o próximo conjunto de dados de entrada
#       voltar_output: método para voltar para o conjunto de dados de saída anterior
#       voltar_input: método para voltar para o conjunto de dados de entrada anterior
#       deletar_output: método para deletar o conjunto de dados de saída atual
#       deletar_input: método para deletar o conjunto de dados de entrada atual
#       extension_path: define qual a extensão que deve ser procurada a partir do type_program
#       select_path: método para o usuário selecionar o caminho do arquivo de acordo com o extension_path
#       validate_hour: verifica se a hora que o usuário deseja inputar no schedule é válida
#       validate_minute: verifica se os minutos que o usuário deseja inputar np schedule são válidos
#       add_time: método para adicionar o horário e o dia da semana no schedule, caso seja válido
#       remove_time: método para remover o horário e o dia da semana no schedule
#       load_existing_times: método para verificar se o horário que o usuário deseja inputar já não existe no banco ou no próprio schedule
#       register_data: método para registrar os dados inputados pelo usuário no banco de dados ProgramsDB
#   Parâmetros: 
#       ctk.CTk
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class Inter_Register_PREP(ctk.CTkToplevel):
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Contrutuor da classe Register
#   No construtor é definida a estrutura da interface (seus widgets, textso, imagens)
#   ATENÇÃO: CASO QUEIRA ADICIONAR ELEMENTOS, SIGA O PADRÃO DA ESTRUTURA
#   Parâmetros: 
#       prep_type: tipo do porgrama (pré-definido como "" string vazia)
#       prep_data: dados do prep (caso seja um item novo é pré-definido como None, caso exista os dados é só colocar como parâmetro)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self, main_app, preptype="", prep_data=None):
        # Cria uma instância do manipulador
        self.manipulador = manipulador()
        
        # Define a classe da interface principal
        self.main_app = main_app
        self.prep_data = prep_data
        self.main_app.withdraw()

        self.prep_type = preptype

        self.programsdb = GenericDBOperations(ProgramsDB, "sqlite:///C:/Terminator/Database/executerDB.db")
        self.usersdb = GenericDBOperations(UsersDB, "sqlite:///C:/Terminator/Database/executerDB.db")

        # Chama o construtor da classe ctk.CTk
        super().__init__()

        # Define o título da Janela
        self.title("Register Prep")
        
        # ícone da janela
        self.wm_iconbitmap(self.manipulador.icon_terminator)
        
        # Faz com que o APP seja grande o suficiente para preencher toda a tela
        self.resizable(False, False)
        
        # Define o tamanho da janela
        width = 550
        height = 730
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
        self.entry_path = ctk.CTkEntry(self.form_container, width=400, placeholder_text="PREP Path")
        self.entry_path.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Botão para selecionar o arquivo
        self.button_path = ctk.CTkButton(self.form_container, text="Browse", fg_color="#089c4c", command=self.select_path)
        self.button_path.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Campo Application Type (agora como Entry)
        self.entry_type = ctk.CTkEntry(self.form_container, width=200, placeholder_text="PREP Type")
        self.entry_type.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_type.insert(0, self.prep_type)
        self.entry_type.configure(state="readonly")

        # Campo Application Name
        self.entry_name = ctk.CTkEntry(self.form_container, width=400, placeholder_text="PREP Name")
        self.entry_name.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        # Lista de opções para o dono 
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
        days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.spinbox_days = tkinter.Spinbox(self.frame_times, values=days_of_week, textvariable=self.day_var, width=10, state="readonly", wrap=True)

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

        # ---------------------- Output Connections ---------------------- #
        self.output_connections = ctk.CTkFrame(self.parameters_container, corner_radius=10, fg_color=self.bg_color)
        self.output_connections.grid(row=0, column=0, columnspan=2, sticky="w", padx=4, pady=5)

        # Label para exibir o número de conexões de saída
        self.label_out = ctk.CTkLabel(self.output_connections, text="Output Connections: 0", text_color="white")
        self.label_out.grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky="w")
        # Entry fields para as conexões de saída
        self.username_out = ctk.CTkEntry(self.output_connections, width=197.5, placeholder_text="Username Output")
        self.username_out.grid(row=1, column=0, pady=5)
        # Entry field para a senha de output
        self.password_out = ctk.CTkEntry(self.output_connections, width=197.5, placeholder_text="Password Output", show="*")
        self.password_out.grid(row=2, column=0, pady=5)
        # Entry field para a URL do servidor de output
        self.server_url_out = ctk.CTkEntry(self.output_connections, width=197.5, placeholder_text="Server URL Output")
        self.server_url_out.grid(row=3, column=0, pady=5)
        # Entry field para a URL do conteúdo de output
        self.content_url_out = ctk.CTkEntry(self.output_connections, width=197.5, placeholder_text="Content URL Output")
        self.content_url_out.grid(row=4, column=0, pady=5)
        # Frame de navegação para as conexões de saída
        self.nav_frame_out = ctk.CTkFrame(self.output_connections, corner_radius=10, fg_color=self.bg_color)
        self.nav_frame_out.grid(row=5, column=0, columnspan=2, pady=(10, 5), sticky="w")
        # Botões de navegação
        # Botão "Anterior"
        self.btn_prev_output = ctk.CTkButton(self.nav_frame_out, text="⬅", width=40, fg_color="#089c4c", command=self.voltar_output)
        self.btn_prev_output.grid(row=0, column=0, padx=5)
        # Botão "Excluir"
        self.btn_delete_output = ctk.CTkButton(self.nav_frame_out, text="🗑", width=40, fg_color="#c0392b", command=self.deletar_output)
        self.btn_delete_output.grid(row=0, column=1, padx=5)
        # Botão "Próximo"
        self.btn_next_output = ctk.CTkButton(self.nav_frame_out, text="➡", width=40, fg_color="#089c4c", command=self.proximo_output, state="disabled")
        self.btn_next_output.grid(row=0, column=2, padx=5)
        # Booleano para mostrar/ocultar a senha de output
        self.mostrando_senha_out = False
        # Botão para mostrar/ocultar a senha de output
        self.btn_ver_senha_out = ctk.CTkButton(self.nav_frame_out, text="👁", width=40, fg_color="#089c4c", command=lambda: self.toggle_senha(self.password_out, self.btn_ver_senha_out, 'mostrando_senha_out'))
        self.btn_ver_senha_out.grid(row=0, column=3, padx=5)

        # Variáveis para controle de saída
        self.output_list = []
        # Contadores para rastrear a saída
        self.output_index = None

        # Loop para validar campos de saída
        for entry in [self.username_out, self.password_out, self.server_url_out, self.content_url_out]:
            entry.bind("<KeyRelease>", lambda e: self.validar_campos_out())

        # ---------------------- Input Connections ---------------------- #
        # Frame para as conexões de entrada
        self.input_connections = ctk.CTkFrame(self.parameters_container, corner_radius=10, fg_color=self.bg_color)
        self.input_connections.grid(row=0, column=2, columnspan=2, sticky="nsew", padx=4, pady=5)
        # Label para o número de conexões de entrada
        self.label_in = ctk.CTkLabel(self.input_connections, text="Input Connections: 0", text_color="white")
        self.label_in.grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky="w")
        # Entry fields para o username de entrada
        self.username_in = ctk.CTkEntry(self.input_connections, width=197.5, placeholder_text="Username Input")
        self.username_in.grid(row=1, column=0, pady=5)
        # Entry fields para a senha de entrada
        self.password_in = ctk.CTkEntry(self.input_connections, width=197.5, placeholder_text="Password Input", show="*")
        self.password_in.grid(row=2, column=0, pady=5)
        # Entry fields para o hostname de entrada
        self.hostname_in = ctk.CTkEntry(self.input_connections, width=197.5, placeholder_text="Hostname Input")
        self.hostname_in.grid(row=3, column=0, pady=5)
        # Entry fields para a URL de conteúdo de entrada
        self.content_url_in = ctk.CTkEntry(self.input_connections, width=197.5, placeholder_text="Content URL Input")
        self.content_url_in.grid(row=4, column=0, pady=5)
        # Frame para a navegação de entrada
        self.nav_frame_in = ctk.CTkFrame(self.input_connections, corner_radius=10, fg_color=self.bg_color)
        self.nav_frame_in.grid(row=5, column=0, columnspan=2, pady=(10, 5), sticky="w")
        # Botões de navegação
        # Botão "Anterior"
        self.btn_prev_input = ctk.CTkButton(self.nav_frame_in, text="⬅", width=40, fg_color="#089c4c", command=self.voltar_input)
        self.btn_prev_input.grid(row=0, column=0, padx=5)
        # Botão "Excluir"
        self.btn_delete_input = ctk.CTkButton(self.nav_frame_in, text="🗑", width=40, fg_color="#c0392b", command=self.deletar_input)
        self.btn_delete_input.grid(row=0, column=1, padx=5)
        # Botão "Próximo"
        self.btn_next_input = ctk.CTkButton(self.nav_frame_in, text="➡", width=40, fg_color="#089c4c", command=self.proximo_input, state="disabled")
        self.btn_next_input.grid(row=0, column=2, padx=5)
        # Booleano para mostrar/ocultar a senha de input
        self.mostrando_senha_in = False
        # Botão para mostrar/ocultar a senha de input
        self.btn_ver_senha_in = ctk.CTkButton(self.nav_frame_in, text="👁", width=40, fg_color="#089c4c", command=lambda: self.toggle_senha(self.password_in, self.btn_ver_senha_in, 'mostrando_senha_in'))
        self.btn_ver_senha_in.grid(row=0, column=3, padx=(5, 0))

        # Variáveis para controle de entrada
        self.input_list = []
        # Contadores para rastrear a entrada
        self.input_index = None

        # Loop para validar campos de entrada
        for entry in [self.username_in, self.password_in, self.hostname_in, self.content_url_in]:
            entry.bind("<KeyRelease>", lambda e: self.validar_campos_in())
        
        # Lista para armazenar os parâmetros do prep
        self.parameters_list = []
        # Botão para registrar os dados do prep no banco de dados
        self.bnt_register_container = ctk.CTkFrame(self.form_container, corner_radius=10, fg_color=self.bg_color)
        self.bnt_register_container.grid(row=7, column=0, columnspan=2, sticky="n")

        # Define o botão de confirmação de registro
        self.button_register = ctk.CTkButton(self.bnt_register_container, text="Save", fg_color="#089c4c", command=self.register_data)
        self.button_register.grid(row=5, column=1, pady=5, sticky="w")

        self.existing_times = self.load_existing_times()
        
        # ---------- Recarregar dados se prep_data existir ----------
        if self.prep_data:
            self.entry_path.insert(0, self.prep_data["program_path"])
            self.entry_type.configure(state="normal")
            self.entry_type.insert(0, self.prep_data["program_type"])
            self.entry_type.configure(state="readonly")
            self.entry_name.insert(0, self.prep_data["program_name"])

            owner_id = self.prep_data["owner_id"]
            owner_name = next((name for name, uid in self.owner_name_to_id.items() if uid == owner_id), None)
            if owner_name:
                self.entry_owner_name.set(owner_name)
                self.entry_owner_name.configure(state="disabled")

            self.times_list = self.prep_data["schedule_list"].split(",") if self.prep_data["schedule_list"] else []
            for time in self.times_list:
                self.times_listbox.insert(tkinter.END, time)

            # Extrair a string de parâmetros
            param_str = self.prep_data['parameters']

            # Encontrar todos os blocos Output e Input
            output_matches = re.findall(r"Output:\{(.*?)\}(?=,Output:|,Input:|$)", param_str)
            input_matches = re.findall(r"Input:\{(.*?)\}(?=,Output:|,Input:|$)", param_str)

            # Converter para listas de dicionários JSON válidos
            output_data = [ast.literal_eval('{' + match + '}') for match in output_matches]
            input_data = [ast.literal_eval('{' + match + '}') for match in input_matches]

            # Verifica se existe dados de saída
            if output_data:
                # Se existir, faz a cópia da lista
                self.output_list = output_data.copy()
                # Restaura as senhas criptografadas de cada saída
                for data in self.output_list:
                    data["PasswordOut"] = Hash().restore_password(data["PasswordOut"])
                # Configura a primeira saída para mostrar nos campos
                self.output_index = 0
                self.preencher_output(self.output_list[0])
                self.atualizar_status_output()
            # Se não, configura a primeira saída como None (não existe) e limpa os campos
            else:
                self.output_index = None
                self.limpar_output()
            # Verifica se existe dados de entrada
            if input_data:
                # Se existir, faz a cópia da lista
                self.input_list = input_data.copy()
                # Restaura as senhas criptografadas de cada entrada
                for data in self.input_list:
                    data["PasswordIn"] = Hash().restore_password(data["PasswordIn"])
                # Configura a primeira entrada para mostrar nos campos
                self.input_index = 0
                self.preencher_input(self.input_list[0])
                self.atualizar_status_input()
            # Se não, configura a primeira entrada como None (não existe) e limpa os campos
            else:
                self.input_index = None
                self.limpar_input()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que define o que fazer e como fazer caso o usuário feche repentnamente a janela
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def on_closing(self):
        result = CTkMessagebox(
            title="Confirmation", 
            message="Do you really want to close the window?", 
            icon="question", 
            option_1="Yes", 
            option_2="No", 
            button_color="#089c4c", 
            justify="center").get()
        
        if result == "Yes":
            CTkMessagebox(
                title="Error", 
                message="You closed the window incorrectly!", 
                icon="warning", 
                button_color="#089c4c", 
                justify="center")
            
            self.destroy()
            self.main_app.after(100, lambda: [self.main_app.deiconify(), self.main_app.max_window()])

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que alterna a visibilidade da senha nos campos de entrada e saída
#   Parâmetros:
#       entry_widget: O campo de entrada da senha
#       button_widget: O botão que alterna a visibilidade
#       state_attr: O atributo que mantém o estado de visibilidade
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def toggle_senha(self, entry_widget, button_widget, state_attr):
        mostrando = getattr(self, state_attr, False)
        if mostrando:
            entry_widget.configure(show="*")
            button_widget.configure(text="👁")
            setattr(self, state_attr, False)
        else:
            entry_widget.configure(show="")
            button_widget.configure(text="🙈")
            setattr(self, state_attr, True)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que valida os campos de saída
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def validar_campos_out(self):
        preenchidos = all(entry.get().strip() != "" for entry in
                          [self.username_out, self.password_out, self.server_url_out])
        self.btn_next_output.configure(state="normal" if preenchidos else "disabled")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que valida os campos de saída
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def validar_campos_in(self):
        preenchidos = all(entry.get().strip() != "" for entry in
                          [self.username_in, self.password_in, self.hostname_in])
        self.btn_next_input.configure(state="normal" if preenchidos else "disabled")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que obtém os dados dos campos de saída
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def obter_dados_output(self):
        return {
            "UsernameOut": self.username_out.get().strip(),
            "PasswordOut": self.password_out.get().strip(),
            "ServerURLOut": self.server_url_out.get().strip(),
            "ContentURLOut": self.content_url_out.get().strip(),
        }
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que obtém os dados dos campos de entrada
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def obter_dados_input(self):
        return {
            "UsernameIn": self.username_in.get().strip(),
            "PasswordIn": self.password_in.get().strip(),
            "HostnameIn": self.hostname_in.get().strip(),
            "ContentURLIn": self.content_url_in.get().strip(),
        }
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que preenche os campos de saída com os dados fornecidos
#   Parâmetros:
#       dados - Um dicionário contendo os dados a serem preenchidos nos campos de saída
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def preencher_output(self, dados):
        for e in [self.username_out, self.password_out, self.server_url_out, self.content_url_out]:
            e.delete(0, tkinter.END)
        self.username_out.insert(0, dados.get("UsernameOut", ""))
        self.password_out.insert(0, dados.get("PasswordOut", ""))
        self.server_url_out.insert(0, dados.get("ServerURLOut", ""))
        self.content_url_out.insert(0, dados.get("ContentURLOut", ""))
        self.validar_campos_out()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que preenche os campos de entrada com os dados fornecidos
#   Parâmetros:
#       dados - Um dicionário contendo os dados a serem preenchidos nos campos de entrada
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def preencher_input(self, dados):
        for e in [self.username_in, self.password_in, self.hostname_in, self.content_url_in]:
            e.delete(0, tkinter.END)
        self.username_in.insert(0, dados.get("UsernameIn", ""))
        self.password_in.insert(0, dados.get("PasswordIn", ""))
        self.hostname_in.insert(0, dados.get("HostnameIn", ""))
        self.content_url_in.insert(0, dados.get("ContentURLIn", ""))
        self.validar_campos_in()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para limpar os campos de saída
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def limpar_output(self):
        for e in [self.username_out, self.password_out, self.server_url_out, self.content_url_out]:
            e.delete(0, tkinter.END)
        self.validar_campos_out()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para limpar os campos de entrada
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def limpar_input(self):
        for e in [self.username_in, self.password_in, self.hostname_in, self.content_url_in]:
            e.delete(0, tkinter.END)
        self.validar_campos_in()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para atualizar o label de status das saídas
#   Parâmetros:
#       Nennhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def atualizar_status_output(self):
        if not self.output_list:
            self.label_out.configure(text="Output Connections: 0")
        elif self.output_index is None:
            self.label_out.configure(text=f"New Output Connection — {len(self.output_list)} saved.")
        else:
            self.label_out.configure(text=f"Output Connections: {self.output_index + 1} of {len(self.output_list)}")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para atualizar o label de status das saídas
#   Parâmetros:
#       Nennhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def atualizar_status_input(self):
        if not self.input_list:
            self.label_in.configure(text="Input Connections: 0")
        elif self.input_index is None:
            self.label_in.configure(text=f"New Input Connection — {len(self.input_list)} saved.")
        else:
            self.label_in.configure(text=f"Input Connections: {self.input_index + 1} of {len(self.input_list)}")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método chamado pelo botão Next. 
#   Chama o próximo item da lista, mostra os dados nos campos e salva o item anterior na lista
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def proximo_output(self):
        dados = self.obter_dados_output()
        if self.output_index is None:
            self.output_list.append(dados)
            self.limpar_output()
            self.atualizar_status_output()
            return
        self.output_list[self.output_index] = dados
        if self.output_index < len(self.output_list) - 1:
            self.output_index += 1
            self.preencher_output(self.output_list[self.output_index])
        else:
            self.output_index = None
            self.limpar_output()
        
        self.atualizar_status_output()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método chamado pelo botão Next. 
#   Chama o próximo item da lista, mostra os dados nos campos e salva o item anterior na lista
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def proximo_input(self):
        dados = self.obter_dados_input()
        if self.input_index is None:
            self.input_list.append(dados)
            self.limpar_input()
            self.atualizar_status_input()
            return
        self.input_list[self.input_index] = dados
        if self.input_index < len(self.input_list) - 1:
            self.input_index += 1
            self.preencher_input(self.input_list[self.input_index])
        else:
            self.input_index = None
            self.limpar_input()

        self.atualizar_status_input()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método chamado pelo botão Back
#   Chama o item anterior da lista e mostra os dados nos campos (não salva o item anterior a esse na lista)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def voltar_output(self):
        if not self.output_list:
            return
        dados = self.obter_dados_output()
        if self.output_index is None:
            self.output_index = len(self.output_list) - 1
            self.preencher_output(self.output_list[self.output_index])
        else:
            self.output_list[self.output_index] = dados
            if self.output_index > 0:
                self.output_index -= 1
                self.preencher_output(self.output_list[self.output_index])
            else:
                self.output_index = None
                self.limpar_output()
        self.atualizar_status_output()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método chamado pelo botão Back
#   Chama o item anterior da lista e mostra os dados nos campos (não salva o item anterior a esse na lista)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def voltar_input(self):
        if not self.input_list:
            return
        dados = self.obter_dados_input()
        if self.input_index is None:
            self.input_index = len(self.input_list) - 1
            self.preencher_input(self.input_list[self.input_index])
        else:
            self.input_list[self.input_index] = dados
            if self.input_index > 0:
                self.input_index -= 1
                self.preencher_input(self.input_list[self.input_index])
            else:
                self.input_index = None
                self.limpar_input()
        self.atualizar_status_input()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método chamado pelo botão Lixeira
#   Deleta o item atual da lista e mostra o próximo item
#   O próximo item pode ser da direita. Se nçao existir mostra o da esquerda. Se não existir não mostra nada e reseta tudo
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def deletar_output(self):
        if not self.output_list or self.output_index is None:
            return
        self.output_list.pop(self.output_index)
        if not self.output_list:
            self.output_index = None
            self.limpar_output()
        else:
            if self.output_index >= len(self.output_list):
                self.output_index = len(self.output_list) - 1
            self.preencher_output(self.output_list[self.output_index])
        self.atualizar_status_output()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método chamado pelo botão Lixeira
#   Deleta o item atual da lista e mostra o próximo item
#   O próximo item pode ser da direita. Se nçao existir mostra o da esquerda. Se não existir não mostra nada e reseta tudo
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def deletar_input(self):
        if not self.input_list or self.input_index is None:
            return
        self.input_list.pop(self.input_index)
        if not self.input_list:
            self.input_index = None
            self.limpar_input()
        else:
            if self.input_index >= len(self.input_list):
                self.input_index = len(self.input_list) - 1
            self.preencher_input(self.input_list[self.input_index])
        self.atualizar_status_input()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método que abre uma janela de pesquisa de arquivo para o usuário selecionar o prep desejado
#   Parâmetros:
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#        
    def select_path(self):
        filetypes = [("Tableau Flow", "*.tfl"), ("Tableau Flow", "*.tflx")]
        path = filedialog.askopenfilename(filetypes=filetypes)
        self.entry_path.delete(0, tkinter.END)
        self.entry_path.insert(0, path)
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
            CTkMessagebox(
                title="Error", 
                message="Schedule already added!", 
                icon="warning", 
                button_color="#089c4c", 
                justify="center")
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
#   Método para verificar se existe o tempo na lista de rodagem ou no próprio schedule do prep
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
#   Método para registrar o prep no banco de dados com os parâmetros e arquivos necessários cadastrados pelo usuário
#   Alguns parâmetros são mandatórios:
#       prep_path: caminho completo do prep
#       prep_type: tipo do prep 
#       prep_name: nome do prep
#       owner_name: owner/dono do prep que será rodado
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def register_data(self):
        # Verifica se todos os campos obrigatórios estão preenchidos
        prep_path = self.entry_path.get()
        prep_type = self.entry_type.get()
        prep_name = self.entry_name.get()
        owner_name = self.entry_owner_name.get()
        
        # Verifica se o caminho do prep existe
        if not os.path.exists(prep_path):
            CTkMessagebox(title="Error",
                          message=f"The '{prep_path}' does not exist!",
                          icon="warning",
                          button_color="#089c4c",
                          justify="center")
            return
        # Verifica se todos os campos obrigatórios estão preenchidos
        if not prep_path or prep_type == "Select the Type" or not prep_name or owner_name == "Select the Owner":
            CTkMessagebox(
                title="Error",
                message="Fill in all required fields!",
                icon="warning",
                button_color="#089c4c",
                justify="center")
            return
        # Verifica se existem horários definidos
        # Se não existir, pergunta se deseja continuar
        if self.times_list == []:
            confirm = CTkMessagebox(
                        title="Atention!",
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
    
        # Adicionando os parâmetros de Output do prep
        if self.output_list != []:
            for out_data in self.output_list:
                # Criptografa a senha e a substituí no json
                password_hash = Hash().create_hash(out_data["PasswordOut"])
                out_data["PasswordOut"] = password_hash
                out_data_str = str(out_data)
                self.parameters_list.append(f"Output:{out_data_str}")
        
        if self.input_list != []:
            for in_data in self.input_list:
                # Criptografa a senha e a substituí no json
                password_hash = Hash().create_hash(in_data["PasswordIn"])
                in_data["PasswordIn"] = password_hash
                in_data_str = str(in_data)
                self.parameters_list.append(f"Input:{in_data_str}")

        # Dados comuns
        prep_data = {
            "program_path": prep_path,
            "program_name": prep_name,
            "program_type": prep_type,
            "owner_id": owner_id,
            "schedule_list": ','.join(self.times_list),
            "parameters": ','.join(self.parameters_list),
            "date_modified": datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        }

        # Atualiza ou registra
        if hasattr(self, "prep_data") and self.prep_data:
            self.programsdb.update(self.prep_data["id"], **prep_data)
            content = f"-------------------------------------------------------------------------------------------------------------------\nPrep: {prep_name} Updated.\nHour Updated: {datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}.\nOwner: {owner_name}.\nProgram Type: {prep_type}.\nList Hours: {self.times_list}\n-------------------------------------------------------------------------------------------------------------------\n"
            self.manipulador.write_txt(self.manipulador.programs_txt, content)
            CTkMessagebox(
                title="Success",
                message="PREP updated successfully!",
                icon="info",
                button_color="#089c4c",
                justify="center")
        else:
            # Pega os dados do usuário
            owner_id = self.owner_name_to_id[owner_name]
            user = self.usersdb.get_by_column("id", owner_id)

            user_string = f"{user["id"]}-{user["user_name"]}-{user["user_code"]}"
            # Solicita a senha do usuário
            password_dialog = PasswordDialog(self, user_or_adm=f"USER: {user_string}")
            entered_password = password_dialog.get_password()

            if entered_password is None:
                return  # Usuário fechou a janela

            # Verifica a senha do usuário selecionado
            if not user or (Hash().check_login(entered_password, user["password"]) != True):
                CTkMessagebox(
                    title="Error",
                    message="Incorrect password. Operation cancelled!",
                    icon="warning",
                    button_color="#089c4c",
                    justify="center")
                return

            # Registra os dados no banco
            self.programsdb.register(**prep_data)

            content = f"-------------------------------------------------------------------------------------------------------------------\nPrep: {prep_name} Registered.\nHour Registered: {datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}.\nOwner: {owner_name}.\nProgram Type: {prep_type}.\nList Hours: {self.times_list}\n-------------------------------------------------------------------------------------------------------------------\n"
            self.manipulador.write_txt(self.manipulador.programs_txt, content)
            # Retorna mensagem de sucesso                              
            CTkMessagebox(
                title="Success",
                message="PREP registered successfully!",
                icon="info",
                button_color="#089c4c",
                justify="center")
        # Fecha a janela de cadastro de prep
        self.destroy()
        self.main_app.after(100, lambda: [self.main_app.deiconify(), self.main_app.max_window()])