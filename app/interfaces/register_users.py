""" 
Código para a interface de registro de usuários utilizando customtkinter.
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importações de bibliotecas necessárias
#   Bibliotecas externas:
#       tkinter: para a criação da interface gráfica
#       customtkinter: para a criação da interface gráfica
#       CTkMessagebox: para exibir caixas de mensagem personalizadas
#       datetime: para a manipulação de datas e horas
#       math: verifica se uma determinada expressão regular casa com o início de uma string
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importação dos móduglos criados para o APP
#       manipulador: para manipulação de arquivos e pastas
#       UsersDB, GenericDBOperations: para operações de banco de dados
#       Hash: para hash e verificação de senhas
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import tkinter
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from datetime import datetime
from re import match
from app.adm_files.manipulator import manipulador
from app.database.usersDB import UsersDB
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
#   Classe que vai construir a Interface de cadastro de App's
#   Possui os seguintes Métodos:
#       __init__: contrutor da classe que inicializa a interface e seus componentes
#       on_closing: determina o que e como fazer caso o usuário deseje fechar a janela repentinamente
#       validate_email: verifica se o e-mail inputado é válido
#       change_visibility: altera a visualização de senha de caracteres normais para "*"
#       register_data: registra os dados do usuário no banco
#   Parâmetros: ctk.CTk
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class Inter_register_users(ctk.CTkToplevel):
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Contrutuor da classe Register
#   No construtor é definida a estrutura da interface (seus widgets, textso, imagens)
#   ATENÇÃO: CASO QUEIRA ADICIONAR ELEMENTOS, SIGA O PADRÃO DA ESTRUTURA
#   Parâmetros:
#       main_app: referência da janela principal do APP
#       user_data: define como None caso seja o cadastro de um usuário novo (caso não seja, pega os dados do usuário como parâmetro para preenchimento dos campos) 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self, main_app, user_data=None):
        # Cria uma instância do manipulador
        self.manipulador = manipulador()

        # Define a classe da interface principal
        self.main_app = main_app
        self.user_data = user_data
        # Esconde a janela principal
        self.main_app.withdraw() 

        self.userdb = GenericDBOperations(UsersDB, "sqlite:///C:/Terminator/Database/executerDB.db")

        # Chama o construtor da classe ctk.CTk
        super().__init__()

        # Define o título da Janela
        self.title("Register User")
        
        # ícone da janela
        self.wm_iconbitmap(self.manipulador.icon_terminator)
        
        # Faz com que o APP seja grande o suficiente para preencher toda a tela
        self.resizable(False, False)
        
        # Define o tamanho da janela
        width = 500
        height = 260
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
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(2, weight=1)

        # Sub-container to center the form
        self.form_container = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color=self.bg_color)
        self.form_container.grid(row=0, column=0, columnspan=2, sticky="n")

        # Campo User Name
        self.entry_user_name = ctk.CTkEntry(self.form_container, width=400, placeholder_text="User Name")
        self.entry_user_name.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Campo User SESA
        self.entry_user_sesa = ctk.CTkEntry(self.form_container, width=400, placeholder_text="SESA User")
        self.entry_user_sesa.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Campo Email
        self.entry_user_email = ctk.CTkEntry(self.form_container, width=400, placeholder_text="E-mail")
        self.entry_user_email.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Campo Senha
        # Frame para entrada de senha + botão de visualização
        self.password_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.password_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.entry_user_password = ctk.CTkEntry(self.password_frame, width=300, show="*", placeholder_text="Password")
        self.entry_user_password.pack(side="left", fill="x", expand=True)

        self.button_eye = ctk.CTkButton(self.password_frame, width=70, height=35, text="Show", corner_radius=5, fg_color="#089c4c", command=self.change_visibility)
        self.button_eye.pack(side='left', padx=(5, 0), pady=0)

        self.bnt_register_container = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color=self.bg_color)
        self.bnt_register_container.grid(row=2, column=0, columnspan=2, sticky="n")

        # Define o botão de confirmação de registro
        self.button_register = ctk.CTkButton(self.bnt_register_container, text="Save", fg_color="#089c4c", command=self.register_data)
        self.button_register.grid(row=5, column=1, pady=5, sticky="w")

        # Se os dados do usuário existirem, preenche os dados nos campos
        # Além disso, define que somente o campo de senha seja redefinido
        # Os outros dados devem permanecer os mesmos
        if self.user_data:
            self.entry_user_name.insert(0, self.user_data["user_name"])
            self.entry_user_name.configure(state="readonly")
            self.entry_user_sesa.insert(0, self.user_data["user_code"])
            self.entry_user_sesa.configure(state="readonly")
            self.entry_user_email.insert(0, self.user_data["user_email"])
            self.entry_user_email.configure(state="readonly")
            self.entry_user_password.insert(0, Hash().restore_password(self.user_data["password"]))
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
#   Método que verifica se o email inputado pelo usuário é válido a partir de uma expressão regular
#   Parâmetros:
#       e-mail
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def validate_email(self, email):
        standard = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        correspondence = match(standard, email)
        validate = correspondence is not None
        return validate
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para alterar a visibilidade do parâmetro senha do usuário
#   Parâmetros
#       Nenhum
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def change_visibility(self):
            if self.button_eye.cget("text") == "Show":
                self.button_eye.configure(text="Hide")
                self.entry_user_password.configure(show="")
            else:
                self.button_eye.configure(text="Show")
                self.entry_user_password.configure(show="*")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para registrar o usuário no banco de dados
#   Alguns parâmetros são mandatórios:
#       user_name: nome do usuário
#       user_sesa: SESA do usuário 
#       user_email: e-mail do usuário
#       user_password: senha do usuário
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def register_data(self):
        user_name = self.entry_user_name.get()
        user_sesa = self.entry_user_sesa.get().upper()
        user_email = self.entry_user_email.get()
        user_password = self.entry_user_password.get()

        if not user_name or not user_sesa or not user_email or not user_password:
            CTkMessagebox(title="Error", message="All fields are required!", icon="warning", button_color="#089c4c", justify="center")
            return
        
        if bool(match(r"^SESA\d+$", user_sesa)) == False:
            CTkMessagebox(title="Error", message=f"The SESA '{user_sesa}' is not valid", icon="warning", button_color="#089c4c", justify="center")
            return

        if self.validate_email(user_email) == False:
            CTkMessagebox(title="Error", message=f"The email '{user_email}' is not valid", icon="warning", button_color="#089c4c", justify="center")
            return
        
        password_hash = Hash().create_hash(user_password)
        
        user_data = {
            "user_name":user_name,
            "user_code":user_sesa,
            "user_email":user_email,
            "password":password_hash,
            "date_modified":datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        }

        if hasattr(self, "user_data") and self.user_data:
            self.userdb.update(self.user_data["id"], **user_data)
            content = f"-------------------------------------------------------------------------------------------------------------------\nUser {user_name} Updated.\nHour Updated: {datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}.\nUser Code: {user_sesa}.\nUser E-mail: {user_email}.\n-------------------------------------------------------------------------------------------------------------------\n"
            self.manipulador.write_txt(self.manipulador.users_txt, content)

            CTkMessagebox(
                title="Success",
                message="User updated successfully!",
                icon="info",
                button_color="#089c4c",
                justify="center"
            )
        else:
            existing_user = self.userdb.session.query(UsersDB).filter_by(user_code=user_sesa).first()
            if existing_user:
                CTkMessagebox(
                    title="Erro",
                    message="This SESA code is already registered!",
                    icon="warning",
                    button_color="#089c4c",
                    justify="center"
                )
                return
            self.userdb.register(**user_data)

            content = f"-------------------------------------------------------------------------------------------------------------------\nUser {user_name} Registered.\nHour Registered: {datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}.\nUser Code: {user_sesa}.\nUser E-mail: {user_email}.\n-------------------------------------------------------------------------------------------------------------------\n"
            self.manipulador.write_txt(self.manipulador.users_txt, content)

            CTkMessagebox(title="Success", message="Data registered successfully!", icon="info", button_color="#089c4c", justify="center")
        
        self.destroy()
        self.main_app.after(100, lambda: [self.main_app.deiconify(), self.main_app.max_window()])