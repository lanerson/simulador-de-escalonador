
fila_0 = []
fila_1 = []
fila_flfs = []
fila_es = []

gantt = "0 "

T = 1 # esse é o tempo em ms

TEMPO_0 = 10
TEMPO_1 = 15
TEMPO_ES = 30
OCIO = False


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

def vazio():
    return len(fila_0+fila_1+fila_flfs+fila_es) == 0

def lidandoFilas(tf0, tf1):
    global gantt
    global OCIO
    global T
    if len(fila_0) != 0:
        if gantt.split(" ")[-1] == "ocioso":
            OCIO = False
            gantt+=f" {T}"
            return tf0, tf1
        tf0 = lidandoFila0(tf0)        
    elif len(fila_1) != 0:        
        tf1 = lidandoFila1(tf1)        
    elif len(fila_flfs) != 0:        
        lidandoFilaFLFS()        
    elif OCIO == False:        
        gantt+=f" ocioso"         
        OCIO = True   

    return tf0, tf1

def lidandoFila0(tf0):   
    print("fila 0",fila_0)     
    fila_0[0][1][0]-=1
    tf0 -= 1
    global gantt
    if fila_0[0][1][0] == 0: # operação terminou
        # remove operação da lista        
        fila_0[0][1].remove(fila_0[0][1][0])
        # remove processo da fila
        temp = fila_0[0]
        fila_0.remove(temp)
        if len(temp[1]) != 0: # se ainda tem operações
            # adiciona processo na proxima fila
            fila_es.append(temp)
        gantt += f" {temp[0]} {T}" 
        return TEMPO_0
    if tf0 == 0:
        temp = fila_0[0]
        fila_0.remove(temp)        
        fila_1.append(temp)
        
        gantt += f" {temp[0]} {T}"
        return TEMPO_0
    else:
        return tf0
        


def lidandoFila1(tf1):   
    print("fila 1", fila_1)          
    fila_1[0][1][0] -= 1
    tf1 -= 1
    global gantt
    if fila_1[0][1][0] == 0: # operação terminou
        # remove operação da lista
        fila_1[0][1].remove(fila_1[0][1][0])
        # remove processo da fila
        temp = fila_1[0]
        fila_1.remove(temp)
        if len(temp[1]) != 0: # ainda tem operações
            # adiciona processo na próxima fila
            fila_es.append(temp)
        gantt += f" {temp[0]} {T}" 
        return TEMPO_1
    
    if tf1 == 0:
        temp = fila_1[0]
        fila_1.remove(temp)
        fila_flfs.append(temp)                
        gantt += f" {temp[0]} {T}" 
        return TEMPO_1
    else:
        return tf1
        


def lidandoFilaFLFS():  
    print("fila f", fila_flfs)      
    fila_flfs[0][1][0]-=1
    if fila_flfs[0][1][0] == 0: # se tiver terminado essa operação
        # remove da fila flfs
        temp = fila_flfs[0] 
        fila_flfs.remove(temp)        
        # remove esta da lista de operações do processo
        temp[1].remove(temp[1][0]) 
        # adiciona ao diagrama da gantt
        global gantt
        gantt += f" {temp[0]} {T}" 

        if len(temp[1]) != 0: # se ainda tiver operações no processo
            # adiciona processo na fila de E/S
            fila_es.append(temp) 
        

def lidandoES(tes):    
    print("fila e", fila_es)
    tes - 1
    if len(fila_es) == 0: # nenhum processo na fila
        return tes
    
    fila_es[0][1][0]-=1

    if fila_es[0][1][0] == 0: # operação terminou
        # remove processo da fila
        temp = fila_es[0]
        fila_es.remove(temp)
        # remove esta da lista de operações do processo
        temp[1].remove(temp[1][0])
        # manda o processo para a fila Q0
        fila_0.append(temp)        
        return TEMPO_ES
    else:        
        return tes

def execucao():
    global T
    tf0 = TEMPO_0
    tf1 = TEMPO_1
    tes = TEMPO_ES
    while(not(vazio())):
        tf0, tf1 = lidandoFilas(tf0,tf1)
        tes = lidandoES(tes)
        T+=1
    print(gantt)
        

        

if __name__ == "__main__":
    menuEntrada()
    execucao()