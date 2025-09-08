""" 
Código para criação da tabela de usuários no banco de dados utilizando SQLAlchemy
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importação das bibliotecas necessárias
#   sqlalchemy: Biblioteca ORM para interagir com bancos de dados relacionais.
#   Column, Integer, String: Tipos de dados e construtores de colunas do SQLAlchemy.
#   declarative_base: Função para criar uma classe base para modelos declarativos.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
from sqlalchemy import Column, Integer, String
from app.database.base import Base
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Define o URL do banco
#   DATABASE_URL = "sqlite:///C:/Terminator/Database/executerDB.db"
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Define a classe UsersDB que representa a tabela "users" no banco de dados.
#   A classe herda de Base, que é a classe base declarativa do SQLAlchemy.
#   Cada atributo da classe corresponde a uma coluna na tabela do banco de dados:
#       id: Coluna do tipo Integer que é a chave primária da tabela.
#       user_name: Coluna do tipo String que armazena o nome do usuário.
#       user_code: Coluna do tipo String que armazena um código único para o usuário.
#       user_email: Coluna do tipo String que armazena o email do usuário.
#       password: Coluna do tipo String que armazena a senha do usuário (deve ser armazenada de forma segura, idealmente como um hash).
#       date_modified: Coluna do tipo String que armazena a data da última modificação do registro do usuário.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class UsersDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    user_code = Column(String, unique=True)
    user_email = Column(String)
    password = Column(String)
    date_modified = Column(String)