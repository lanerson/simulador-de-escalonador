
fila_0 = []
fila_1 = []
fila_flfs = []
fila_es = []

contexto = "P0"
fila = []

gantt = "0"
T = 0 # esse é o tempo em ms

TEMPO_0 = 10
TEMPO_1 = 15
TEMPO_ES = 30
OCIO = False

def situacaoFilas():
    return [len(fila_0), len(fila_1), len(fila_flfs), len(fila_es)]

def getContexto():
    global contexto
    if fila_0 != []:
        return fila_0[0][0]
    elif fila_1 != []:
        return fila_1[0][0]
    elif fila_flfs != []:
        return fila_flfs[0][0]
    else:
        return "ocioso"

def mudaGantt():
    global fila, gantt, contexto, T
    if fila == []:
        fila = situacaoFilas()
    elif fila != [] and fila != situacaoFilas():        
        fila = situacaoFilas()
        if contexto != getContexto():
            gantt += f" {contexto} {T}"
            contexto = getContexto()        
        
        
def menuTeste():    
    burst = [8,40,10,30]
    es= [3,1,2,1]
    # burst = [50,20]
    # es= [1,2]
    for i in range(len(burst)):
        novo_processo = []
        for j in range(es[i]):
            novo_processo.append(burst[i])
            novo_processo.append(TEMPO_ES)
        novo_processo.append(burst[i])
        fila_0.append([f'P{i}',novo_processo])



def menuEntrada():
    n_processos = int(input("Digite o total de processos na fila: "))
    for i in range(n_processos):
        n_burst = int(input(f"Digite a duração do surto de CPU para o {i+1}º processo: "))
        n_op = int(input(f"Digite o número de operações E/S para o {i+1}º processo: "))
        novo_processo = []
        for j in range(n_op):
            novo_processo.append(n_burst)
            novo_processo.append(TEMPO_ES)
        novo_processo.append(n_burst)
        fila_0.append([f'P{i}',novo_processo])

def tam():
    return len(fila_0+fila_1+fila_flfs+fila_es)

def lidandoFilas(tf0, tf1):
    global gantt, OCIO, T
    if len(fila_0) != 0:                
            # return tf0, tf1
        tf0 = lidandoFila0(tf0)        
    elif len(fila_1) != 0:        
        tf1 = lidandoFila1(tf1)        
    elif len(fila_flfs) != 0:        
        lidandoFilaFLFS()          

    return tf0, tf1

def lidandoFila0(tf0):                
    fila_0[0][1][0]-=1
    tf0 -= 1
    global gantt, fila_na_hora, quem_ta_executando

    if fila_0[0][1][0] == 0: # operação terminou
        # remove operação da lista        
        fila_0[0][1].remove(fila_0[0][1][0])
        # remove processo da fila
        temp = fila_0[0]
        fila_0.remove(temp)
        if len(temp[1]) != 0: # se ainda tem operações
            # adiciona processo na proxima fila
            fila_es.append(temp)                    
        return TEMPO_0    
    if tf0 <= 0:
        temp = fila_0[0]
        fila_0.remove(temp)        
        fila_1.append(temp)                
        return TEMPO_0
    else:        
        return tf0
    



def lidandoFila1(tf1):   
    tf1 -= 1
    fila_1[0][1][0] -= 1
    
    global gantt, T, fila_na_hora, quem_ta_executando
    if len(fila_0) > 0:            
            return tf1
    # print("fila 1", fila_1)          
    if fila_1[0][1][0] == 0: # operação terminou        
        # remove operação da lista
        fila_1[0][1].remove(fila_1[0][1][0])
        # remove processo da fila
        temp = fila_1[0]
        fila_1.remove(temp)
        if len(temp[1]) != 0: # ainda tem operações
            # adiciona processo na próxima fila
            fila_es.append(temp)                    
        return TEMPO_1
    
    if tf1 <= 0:
        temp = fila_1[0]
        fila_1.remove(temp)
        fila_flfs.append(temp)                                       
        return TEMPO_1
    else:               
        return tf1
        


def lidandoFilaFLFS():   
    fila_flfs[0][1][0]-=1
    global gantt, T, fila_na_hora, quem_ta_executando
    
    if len(fila_0) > 0:                        
        return      

    
    if fila_flfs[0][1][0] == 0: # se tiver terminado essa operação
        # remove da fila flfs
        temp = fila_flfs[0] 
        fila_flfs.remove(temp)        
        # remove esta da lista de operações do processo
        temp[1].remove(temp[1][0]) 
        # adiciona ao diagrama da gantt        

        if len(temp[1]) != 0: # se ainda tiver operações no processo
            # adiciona processo na fila de E/S
            fila_es.append(temp)             
        return
    
    
    # elif len(fila_es) != 0 and fila_es[0][1][0] == 0: # operação ES terminou então esse vai ser interrompido                                                                                                
    #         gantt += f" {fila_flfs[0][0]} {T}"  
    #         print("vem pra cá")                           

def lidandoES(tf1):           
    
    if len(fila_es) == 0: # nenhum processo na fila
        return tf1
    
    fila_es[0][1][0]-=1
    global T, gantt
    if fila_es[0][1][0] == 0: # operação terminou        
        # remove processo da fila
        temp = fila_es[0]
        fila_es.remove(temp)        
        # remove esta da lista de operações do processo
        temp[1].remove(temp[1][0])
        # manda o processo para a fila Q0
        
        fila_0.append(temp)        
        if len(fila_1) > 0 and len(fila_0) == 1:
            # T+=1
            print("chegou aqui f1", T)
            # tf1 = lidandoFila1(tf1)
        elif len(fila_flfs) > 0 and len(fila_0) == 1:
        # if len(fila_flfs) > 0 and len(fila_0+fila_1) == 1:
            # T+=1
            print("chegou aqui fs", T)
            print("tamanho", len(fila_1))
            # lidandoFilaFLFS()
    return tf1
    
saida = "0 P0 8 P1 18 P2 28 P3 38 P0 46 P1 61 P3 67 P2 77 P3 86 P1 97 P0 105 P1 109 P3 114 ocioso 127 P2 137 ocioso 157 P0 165 ocioso 187               P1 217        P3 242 P1 252 P3 257"
gabs  = "0 P0 8 P1 18 P2 28 P3 38 P0 46 P1 61 P3 68 P2 78 P3 86 P1 98 P0 106 P1 109 P3 114 ocioso 128 P2 138 ocioso 158 P0 166 ocioso 188 P1 198 P1 213 P1 218 P3 228 P3 243 P1 253 P3 258"
lista = range(258+1)#[67, 68, 77, 78, 105, 106, 227, 228, 242, 243]
def execucao():
    global T, gantt, fila_na_hora
    tf0 = TEMPO_0
    tf1 = TEMPO_1    
    while(not(tam() == 0)):  
        print(f'{T:03}', len(fila_0), len(fila_1), len(fila_flfs), len(fila_es))
        if T in lista:
            print("tempo: ",T)
            print(situacaoFilas())
            # print(fila_0)
            # print(fila_1)
            # print(fila_flfs)
            # print(fila_es)        
        tf0, tf1 = lidandoFilas(tf0,tf1)    
        T+=1        
        tf1 = lidandoES(tf1)     
        fila_na_hora = situacaoFilas()
        mudaGantt()
                                  
    print(gantt)
        
        

if __name__ == "__main__":
    # menuEntrada()
    menuTeste()
    execucao()