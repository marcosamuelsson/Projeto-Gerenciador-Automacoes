""" 
Código para criação da tabela de configurações no banco de dados utilizando SQLAlchemy
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importa as bibliotecas necessárias
#   sqlalchemy: Biblioteca ORM para interagir com bancos de dados relacionais.
#   Column, String, Integer: Tipos de dados e construtores de colunas do SQLAlchemy.
#   Base: Classe base para definir modelos de banco de dados.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
from sqlalchemy import Column, String, Integer
from app.database.base import Base
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Define o URL do banco
#   DATABSE_URL = ""sqlite:///C:/Terminator/Database/executerDB.db"
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Cria a classe base para declarar as classes definitivas do banco de dados
#   Base = declarative_base()
#   Cada atributo da classe corresponde a uma coluna na tabela do banco de dados:
#       id: Identificador único para cada configuração.
#       tableau_bat: Caminho para o arquivo .bat do Tableau.
#       password: Senha criptografada para acesso ao sistema.
#       paths_delete: Lista de diretórios para limpeza automática.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class SettingsDB(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    tableau_bat = Column(String)
    password = Column(String)
    paths_delete = Column(String)