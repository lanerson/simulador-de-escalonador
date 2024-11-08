fila_0 = []
fila_1 = [] # 
fila_2 = [] # fcfs
fila_3 = [] # es

Q0 = 10
Q1_GLOBAL = 15
Q3 = 30

def menuInput():
    n_processos = int(input("digite o total de processos: "))    
    for i in range(n_processos):
        burst = int(input(f"digite o tempo de surto do {i+1}º processo: "))
        es = int(input(f"digite a quantidade de operações E/S: "))
        novo_processo = []
        for j in range(es):
            novo_processo.append(burst)
            novo_processo.append(Q3)
        novo_processo.append(burst)
        fila_0.append([f"P{i}", novo_processo])

def menuTeste(conf):
    [burst, es] = [[50, 20], [1, 2]] if conf == 1 else [[8, 40, 10, 30], [3, 1, 2, 1]]
    for i in range(len(es)):
        novo_processo = []
        for j in range(es[i]):
            novo_processo.append(burst[i])
            novo_processo.append(Q3)
        novo_processo.append(burst[i])
        fila_0.append([f"P{i}", novo_processo])

def getOperacao(): # retorna a operação e a fila de maior prioridade
    if fila_0 != []:
        return fila_0[0][0], fila_0[0][1][0], "Q0"
    elif fila_1 != []:
        return fila_1[0][0], fila_1[0][1][0], "Q1"
    elif fila_2 != []:
        return fila_2[0][0], fila_2[0][1][0], "Q2"
    else:
        return "ocioso", 0, "ES"

def lidandoES(tempo):
    fila_3[0][1][0]-=tempo
    if fila_3[0][1][0] == 0:
        temp = fila_3[0]
        fila_3.pop(0)
        temp[1].pop(0)
        fila_0.append(temp)        

def escalonador(manual = 1):
    if manual == 0:
        menuInput()
    else:
        menuTeste(manual)    
    Q1 = Q1_GLOBAL       
    T = 0
    gantt = "0"
    contexto_fila = "Q0"
    contexto_op = "P0"    
    tempo = 0       
    while(len(fila_0 + fila_1 + fila_2 + fila_3) != 0):
        # pegando a operação e a fila de maior prioridade
        op_nome, op_temp, fila = getOperacao() 
        # print(T,op_nome, op_temp, fila)
        # atualização do diagrama
        if fila != contexto_fila or op_nome != contexto_op:
            gantt += f" {contexto_op} {T}"
            contexto_fila = fila
            contexto_op = op_nome   

        tam_fila_3 = len(fila_3)
        tempo = op_temp if fila_3 == [] else min(op_temp, fila_3[0][1][0])        
        if fila == "Q0":                    
            tempo = min(tempo, Q0) 
            fila_0[0][1][0]-=tempo
            temp = fila_0[0]
            fila_0.pop(0)                
            if temp[1][0] == 0: # passou um quantum
                temp[1].pop(0)
                if temp[1] != []:
                    fila_3.append(temp)                    
            else: # a operação terminou
                fila_1.append(temp)

        elif fila == "Q1":
            tempo = min(tempo, Q1)
            fila_1[0][1][0]-=tempo
            if tempo == op_temp or tempo == Q1:
                Q1 = Q1_GLOBAL
                temp = fila_1[0]
                fila_1.pop(0)
                if temp[1][0] == 0: # terminou a execução
                    temp[1].pop(0)                    
                    if temp[1] != []:
                        fila_3.append(temp)                        
                else: # passou um quantum
                    fila_2.append(temp)  
            else:
                Q1-=tempo          
        elif fila == "Q2":                        
            fila_2[0][1][0]-=tempo
            temp = fila_2[0]
            if tempo == op_temp:
                fila_2.pop(0)                                
                temp[1].pop(0)
                if temp[1] != []:
                    fila_3.append(temp)            

        elif fila == "ES": # todo mundo esperando pelo E/S
            tempo = fila_3[0][1][0]            

        if tam_fila_3 != 0:            
            lidandoES(tempo)

        T+=tempo
    
    gantt += f" {contexto_op} {T}"
    print(gantt)



if __name__ == "__main__":            
    # mude para 1 ou 2 para disparo automático
    escalonador(0) 