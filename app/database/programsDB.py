""" 
Código para criação da tabela de programas no banco de dados utilizando SQLAlchemy
Code by: Marco Antonio Samuelsson
Data: 29/08/2025
Versão: 1.0
Qualquer modificação ou cópia deste código deve ser autorizada pelo autor!
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Importa as bibliotecas necessárias
#   sqlalchemy: Biblioteca para mapeamento objeto-relacional (ORM) em Python.
#   Column, Integer, String: Tipos de dados e construtores de colunas do SQLAlchemy.
#   Base: Classe base para a definição de modelos de banco de dados.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
from sqlalchemy import Column, Integer, String
from app.database.base import Base
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Define o URL do banco
#   DATABSE_URL = "sqlite:///C:/Terminator/Database/executerDB.db"
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Cria a classe ProgramsDB que representa a tabela 'programs' no banco de dados.
#   A classe herda de Base, que é a classe base para todos os modelos declarativos do SQLAlchemy.
#   Cada atributo da classe corresponde a uma coluna na tabela do banco de dados:   
#       id: Coluna inteira que serve como chave primária.
#       program_path: Coluna string que armazena o caminho do programa.
#       program_name: Coluna string que armazena o nome do programa.
#       program_type: Coluna string que indica o tipo do programa (e.g., Executable, Python).
#       owner_id: Coluna inteira que referencia o ID do proprietário do programa.
#       schedule_list: Coluna string que armazena a lista de agendamentos do programa.
#       parameters: Coluna string que armazena os parâmetros do programa.
#       date_modified: Coluna string que registra a data da última modificação.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class ProgramsDB(Base):
    __tablename__ = 'programs'
    id = Column(Integer, primary_key=True)
    program_path = Column(String)
    program_name = Column(String)
    program_type = Column(String)
    owner_id = Column(Integer)
    schedule_list = Column(String)
    parameters = Column(String)
    date_modified = Column(String)