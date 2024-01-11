from queue import Queue
import socket
import threading


target = "TARGETIP" #da sostituire con l'ip bersaglio // use target IP
Queue =Queue()
open_ports = []

def portscan(port):
    try: 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target,port))
        return True
    except:
        return False
    
    
def get_ports(mode):
    if mode == 1: 
        for port in range(1,1024): #limitiamo alle porte più conosciute per la prima modalità
            Queue.put(port)
    elif mode == 2:
        for port in range (1, 49152): #aggiungiamo le porte riservate
            Queue.put(port)
    elif mode == 3: 
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
        for port in ports:
            Queue.put(port)
    elif mode == 4: 
        ports = input("Che porte vuoi cercare? Separale con uno spazio: ") 
        ports = ports.split()
        ports = list(map(int, ports))
        for port in ports:
            Queue.put(port)



#aggiungiamo la funzione che ci permette di ottenere le porte dalla queue, scannerizzarle e mostrare i risultati 
#// adding worker function to get port numbers from the queue, scanning and printing the res
            
def worker(): 
    while not Queue.empty():
        port = Queue.get()
        if portscan(port):
            print(" La porta {} è aperta ".format(port)) #print the port is open in italian
            open_ports.append(port)
        else:
            print("La porta {} è chiusa".format(port)) #Port is closed, this is not recommended as we don't care about closed ports

def run_scanner(threads, mode):
    get_ports(mode)
    thread_list = []

    for t in range(threads):
        thread = threading.thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread  in thread_list:
        thread.join()

    print("le porte aperte sono: ", open_ports)

#run_scanner(100,1) to use a hundred threads, it can be increased and depends on the computer power