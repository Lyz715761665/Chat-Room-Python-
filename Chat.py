
# coding: utf-8

# In[ ]:


import socket
#import threading
#import threading
import _thread
    
#Host and port infor for server
HOST=""
PORT=""
BUFFER_SIZE=1024
#Using IPv4 and TCP socket type for s
#idea when sending a private message send two
#first is verfication and name of user
#second is actual message

curclients = {}
addresses = {}

def clientThread(clientCon,clientAdd):
     clientCon.send(bytes("Welcome new friend!"+
                          "Type in your chat usename[MUST BE 5 characters backslash is not allowed] and press enter!", "utf8"))
           
    clientusername = client.recv(BUFFER_SIZE).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % clientusername
    clientCon.send(bytes(welcome, "utf8"))
    clientCon.send(bytes("Please note to send a private message send /username+message", "utf8"))
    newClientmsg = "%s has joined the chat.Be nice!" %  clientusername
    Broadcast(bytes(msg, "utf8"))
    curclients[clientCon] = clientusername
        while True:
            clientmes = client.recv(BUFFER_SIZE)
            if clientmes!= bytes("{quit}", "utf8"):
                #first check if public
                if clientmes.decode("utf8")[0]!="/":
                    Broadcast(clientmes, clientusername+": ")
                else:
                    intendedclient=clientmes.decode("utf8")[1:6]
                    for client,name in curclients.items():
                        if((name==intendedclient):
                            client.sendall(bytes(clientusername+"(whisper): ", "utf8")+clientmes[7:])
                else:
                    client.send(bytes("{quit}", "utf8"))
                    client.close()
                    del curclients[client]
                    broadcast(bytes("%s has left the chat." % clientusername, "utf8"))
                    break
                               
                               
def Broadcast(message,prefix=""):
    for client in curclients:
        client.send()
    
def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)
    
def SendTo(message,prefix,usernames):
    for client,name in curclients.items():
        for user in usernames:
            if(name==user):
                client.send(bytes(prefix, "utf8")+msg)
                
    
    

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        #thread.start_new_thread( newClient,*sock.accept() )
        while True:
            clientCon,clientAdd=sock.accept()
            print("%s:%s has connected." % clientAdd)  
            addresses[clientCon] = clientAdd
            start_new_thread(clientthread,(clientCon,clientAdd))   
           
    #sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)       
   #if __name__ == "__main__":
    #sock.listen(5)
    #print("Waiting for connection...")
    #ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    #ACCEPT_THREAD.start()
    #ACCEPT_THREAD.join()
#SERVER.close()     
    
    

    

