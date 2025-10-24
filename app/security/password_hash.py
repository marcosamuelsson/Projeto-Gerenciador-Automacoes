""" 
Código para hash de senhas utilizando a biblioteca cryptography.
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importações de bibliotecas necessárias:
#       base64: codifica a chave derivada para que possa ser usada pelo Fernet
#       Fernet: Criptografa e descriptografa senhas de forma segura.
#       PBKDF2HMAC: Deriva uma chave segura a partir da senha base "Schneider"
#       hashes: Define o algoritmo de hash usado pelo PBKDF2HMAC
#       default_backend: Necessário para inicializar o PBKDF2HMAC
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Classe que encapsula toda a lógica de derivação de chave, criptografia, verificação e restauração de senhas.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class Hash:
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Construtor da classe Hash
#   Inicializa a classe e gera uma chave criptográfica segura a partir de uma senha base.
#   Passos:
#       Define um salt fixo (sequência de bytes) para garantir consistência na geração da chave.
#        Usa PBKDF2HMAC para derivar uma chave segura a partir da senha base "Schneider".
#        Codifica essa chave em Base64 para torná-la compatível com o Fernet.
#        Cria um objeto Fernet com essa chave, que será usado para criptografar e descriptografar senhas.
#   Parâmetros:
#       base_password_key: chave para gerar a criptografia
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self, base_password_key="Schneider"):
        # Deriva uma chave segura a partir da senha base
        salt = b'\x00' * 16  # Salt fixo para consistência
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=default_backend()
        )
        chave = base64.urlsafe_b64encode(kdf.derive(base_password_key.encode()))
        self.fernet = Fernet(chave)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para criptografar a senha fornecida.
#   Parâmetros:
#       password
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def create_hash(self, password):
        return self.fernet.encrypt(password.encode())
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para verificar se a senha digitada pelo usuário corresponde à senha armazenada (criptografada).
#   Parâmetros:
#       entered_password: senha digitada pelo usuário
#       password_stored: no banco de dados do usuário
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def check_login(self, entered_password, password_stored):
        try:
            senha_original = self.fernet.decrypt(password_stored).decode()
            return entered_password == senha_original
        except Exception as e:
            return False
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Método para recuperar/descriptografar a senha original a partir da versão criptografada.
#   Parâmetros:
#       password_stored: senha armazenada no banco de dados do usuário
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def restore_password(self, password_stored):
        try:            
            if isinstance(password_stored, str):
                if password_stored.startswith("b'") and password_stored.endswith("'"):
                    # Remove o b' e o ' final, e converte para bytes
                    password_stored = password_stored[2:-1].encode('utf-8')
                else:
                    # Caso seja uma string comum (base64), apenas codifica
                    password_stored = password_stored.encode('utf-8')

            return self.fernet.decrypt(password_stored).decode()
        except Exception as e:
            return None