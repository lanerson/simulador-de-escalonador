
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

quem_ta_executando = 'P0'

def situacaoFilas():
    return [len(fila_0), len(fila_1), len(fila_flfs), len(fila_es)]

def menuTeste():
    
    # burst = [8,40,10,30]
    # es= [3,1,2,1]
    burst = [50,20]
    es= [1,2]
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
    # print("fila 0",fila_0)   
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
    # print("fila 1", fila_1)          
    fila_1[0][1][0] -= 1
    tf1 -= 1
    global gantt, T
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

        # if len(fila_es) != 0 and fila_es[0][1][0] == 1: # operação ES terminou então esse vai ser interrompido                                    
        #     print("veio pra cá também")                 
        #     gantt += f" {fila_1[0][0]} {T}" 
            
        return tf1
        


def lidandoFilaFLFS():         
    fila_flfs[0][1][0]-=1
    global gantt, T
    if fila_flfs[0][1][0] == 0: # se tiver terminado essa operação
        # remove da fila flfs
        temp = fila_flfs[0] 
        fila_flfs.remove(temp)        
        # remove esta da lista de operações do processo
        temp[1].remove(temp[1][0]) 
        # adiciona ao diagrama da gantt
        gantt += f" {temp[0]} {T}" 

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
    return tf1
    

lista = [143,144,145]
def execucao():
    global T, gantt
    tf0 = TEMPO_0
    tf1 = TEMPO_1    
    while(not(tam() == 0)):  
        # print(T)
        # print(fila_0)      
        # print(fila_1)      
        # print(fila_flfs)      
        # print(fila_es)      
        s_inicio = situacaoFilas()
        tf0, tf1 = lidandoFilas(tf0,tf1)    
        tf1 = lidandoES(tf1)     
        T+=1
        s_fim = situacaoFilas()
        if s_inicio[3] > s_fim[3] and (s_fim[1]+s_fim[2] > 0): 
            print("mostrando os tempos", T) 
            # fila_0[0][1][0]+=1   
            if(s_fim[1]>0):
                gantt += f" {fila_1[0][0]} {T}" 
                fila_1[0][1][0]-=1 
            elif(s_fim[2]>0):
                gantt += f" {fila_flfs[0][0]} {T}"
                fila_flfs[0][1][0]-=1 
            if s_fim[3] > 0:
                fila_es[0][1][0]-=1
            T+=1
                          
        if T in lista:
            print("mais testes", T)
            print(s_inicio)
            print(s_fim)
    print(gantt)
        
        

if __name__ == "__main__":
    # menuEntrada()
    menuTeste()
    execucao()