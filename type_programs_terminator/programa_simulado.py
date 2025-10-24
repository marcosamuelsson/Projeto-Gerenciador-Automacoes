# Importa a biblioteca sys para manipulação de argumentos do sistema
import sys
# Função principal
def main():
    # Imprime os argumentos recebidos
    print("Argumentos recebidos:")
    # Itera sobre os argumentos do sistema/cmd
    # Sendo o primeiro argumento [0] sempre o próprio programa a ser rodado
    # Por isso, começamos a iteração a partir do segundo argumento [1]
    for arg in sys.argv[1:]:
        print(arg)
main()