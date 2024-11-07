fila_0 = []
fila_1 = []
fila_flfs = []
fila_es = []

gantt = "0"
T = 1  # esse é o tempo em ms

TEMPO_0 = 10
TEMPO_1 = 15
TEMPO_ES = 30
OCIO = False

def situacaoFilas():
    return [len(fila_0), len(fila_1), len(fila_flfs), len(fila_es)]

def menuTeste():    
    burst = [50, 20]
    es = [1, 2]
    for i in range(len(burst)):
        novo_processo = []
        for j in range(es[i]):
            novo_processo.append(burst[i])
            novo_processo.append(TEMPO_ES)
        novo_processo.append(burst[i])
        fila_0.append([f'P{i}', novo_processo])

def tam():
    return len(fila_0) + len(fila_1) + len(fila_flfs) + len(fila_es)

def lidandoFilas(tf0, tf1):
    global gantt, OCIO, T
    if len(fila_0) != 0:
        if OCIO:
            OCIO = False
            gantt += f" {T}"
            # fila_0[0][1][0]+=1
        tf0 = lidandoFila0(tf0)        
    elif len(fila_1) != 0:        
        tf1 = lidandoFila1(tf1)        
    elif len(fila_flfs) != 0:        
        lidandoFilaFLFS()      
    elif not OCIO:        
        gantt += " ocioso"
        OCIO = True   

    return tf0, tf1

def lidandoFila0(tf0):            
    fila_0[0][1][0] -= 1
    tf0 -= 1
    global gantt, T

    if fila_0[0][1][0] == 0:  # operação terminou
        temp = fila_0.pop(0)
        temp[1].pop(0)
        if len(temp[1]) != 0:  
            fila_es.append(temp)  # vai para a fila de E/S
        gantt += f" {temp[0]} {T}"
        return TEMPO_0

    if tf0 <= 0:
        temp = fila_0.pop(0)
        fila_1.append(temp)
        gantt += f" {temp[0]} {T}"
        return TEMPO_0

    return tf0

def lidandoFila1(tf1):       
    fila_1[0][1][0] -= 1
    tf1 -= 1
    global gantt, T
    
    if fila_1[0][1][0] == 0:  # operação terminou        
        temp = fila_1.pop(0)
        temp[1].pop(0)
        if len(temp[1]) != 0:  
            fila_es.append(temp)  
        gantt += f" {temp[0]} {T}"
        return TEMPO_1
    
    if tf1 <= 0:
        temp = fila_1.pop(0)
        fila_flfs.append(temp)
        gantt += f" {temp[0]} {T}"         
        return TEMPO_1

    return tf1

def lidandoFilaFLFS():         
    fila_flfs[0][1][0] -= 1
    global gantt, T

    if fila_flfs[0][1][0] == 0:
        temp = fila_flfs.pop(0)
        temp[1].pop(0)
        gantt += f" {temp[0]} {T}"

        if len(temp[1]) != 0:  
            fila_es.append(temp)

def lidandoES():           
    if len(fila_es) == 0:
        return
    
    fila_es[0][1][0] -= 1
    if fila_es[0][1][0] == 0:  # operação terminou        
        temp = fila_es.pop(0)
        temp[1].pop(0)
        fila_0.append(temp)  

def execucao():
    global T, gantt
    tf0 = TEMPO_0
    tf1 = TEMPO_1    
    while tam() > 0:  
        tf0, tf1 = lidandoFilas(tf0, tf1)    
        lidandoES()     
        T += 1
    print(gantt)
        
if __name__ == "__main__":
    menuTeste()
    execucao()