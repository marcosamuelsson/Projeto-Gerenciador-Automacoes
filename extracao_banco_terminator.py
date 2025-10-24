# Importação das operações para manipulação do banco de dados do Terminator
from app.database.operationDBs import GenericDBOperations
# Importação da tablea onde os programas são registrados
from app.database.programsDB import ProgramsDB
# Importação da tabela onde os usuários são registrados
from app.database.usersDB import UsersDB
# Importação da tabela onde as configurações são registradas
from app.database.settingsDB import SettingsDB

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Classe para análise do banco de dados do Terminator
#   Aqui veremos os seguintes dados:
#       - Dados dos registros de programa da Tabela ProgramsDB
#       - Dados dos registros de usuários da Tabela UsersDB
#       - Dados dos registros de configurações da Tabela Settings
#
#   Todas as extrações são visualizadas na forma de json
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class AnaliseBanco:
    def __init__(self):
        self.programsdb = GenericDBOperations(ProgramsDB,"sqlite:///C:/Terminator/Database/executerDB.db")
        self.usersdb = GenericDBOperations(UsersDB,"sqlite:///C:/Terminator/Database/executerDB.db")
        self.settingsdb = GenericDBOperations(SettingsDB,"sqlite:///C:/Terminator/Database/executerDB.db")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Métodos para exibição dos dados
#   Parâmetros:
#       - Tabela que deseja visualizar (estão sendo chamadas no construtor da classe)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def MostrarDados(self, table):
        result = table.get_all()
        for dado in result:
            print("\n",dado)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#   Métodos para exibição dos dados
#   Só funciona se rodado o arquivo .py hospedeiro, não na chamada da classe
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    analise_banco = AnaliseBanco()
    print("Análise do banco de dados do Terminator")
    print()
    print(f"Dados dos registros de programa da Tabela ProgramsDB:")
    print(analise_banco.MostrarDados(analise_banco.programsdb))
    print("\n")
    print(f"Dados dos registros de usuários da Tabela UsersDB:")
    print(analise_banco.MostrarDados(analise_banco.usersdb))
    print("\n")
    print(f"Dados dos registros de configurações da Tabela SettingsDB:")
    print(analise_banco.MostrarDados(analise_banco.settingsdb))