processos=[]

fila_0 = []
fila_1 = []
fila_2 = []
fila_es = []

menu_principal = """Bem-vindo ao simulador de escalonador

1 - Criar processo
2 - Iniciar execução
3 - Mostrar fila
4 - Excluir processo da fila
5 - Limpar fila de processos
6 - Sair

R - """

menu_processo = """1 - Adicionar operação de CPU
2 - Adicionar operação de E/S
3 - Finalizar processo

Escolha - """

def criar_processo():
    nome = str(input("qual o nome do processo que deseja criar? "))
    key = '1'    
    novo_processo = {}
    while(key != '3'):
        key=str(input(menu_processo))
        if(key == '1' or key == '2'):
            valor = int(str(input("qual o tempo de burst dessa operação? ")))
            tipo = "CPU" if key == '1' else "ES"
            novo_processo.update({tipo:valor})
    if len(novo_processo):
        print("processo criado com sucesso")
        processos.append({nome:novo_processo})    

def listar_processos():
    tam = len(processos)
    if tam:
        for i,j in enumerate(processos.keys()):
            print(f"{i+1} - {j}")
    else:
        print("Fila vazia")

def execucao():
    pass

def menu():
    escolha = '0'
    while(escolha != '6'):
        escolha = str(input(menu_principal))
        if(escolha == '1'):
            criar_processo()
        elif(escolha == '2'):
            execucao()
        elif(escolha == '3'):
            listar_processos()
        elif(escolha == '4'):
            listar_processos()
            del_processo = int(input("digite o numero do processo que deseja excluir: "))
            processos.remove(processos[del_processo-1])
        elif(escolha == '5'):
            processos.clear()
            print("A fila está vazia")     
        elif(escolha == '6'):
            pass
        else:
            print("Escolha inválida!\n")

if __name__ == "__main__":
    menu()