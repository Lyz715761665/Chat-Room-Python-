
# coding: utf-8

# In[16]:


import socket
#import threading
import threading
#import thread
    
#Host and port information for server
HOST=""
PORT=65432
BUFFER_SIZE=1024
#Using IPv4 and TCP socket type for s
#idea when sending a private message send two
#first is verfication and name of user
#second is actual message

curclients = {}
addresses = {}

def createclientThread():
    #Ask for client username and enters it in dictionary then creates a clientThread
    while True:
        check=True
        clientCon,clientAdd=sock.accept()
        addresses[clientCon] = clientAdd
        print("%s:%s has connected." % clientAdd) 
        clientCon.sendall(bytes("Welcome new friend!\n"+
        "Type in your chat usename[MUST BE 6 characters,no spaces and alphanumerical]and press enter!", "utf8")) 
        while(check==True):
            clientusername = clientCon.recv(BUFFER_SIZE).decode("utf8")
            if (len(clientusername)>6):
                clientusername=clientusername[0:6]
                if(clientusername in curclients.values()):
                    clientCon.sendall(bytes("The username you have chosen has already been taken.Please try another", "utf8"))
                else:     
                    check=False
            if (len(clientusername)<6):
                clientCon.sendall(bytes("The username chosen is too small to use.Please try again\n"+
        "Type in your chat usename[MUST BE 6 characters,no spaces and alphanumerical]and press enter!", "utf8"))     
            if (len(clientusername)==6):
                if(clientusername in curclients.values()):
                    clientCon.sendall(bytes("The username you have chosen has already been taken.Please try another", "utf8"))
                else:     
                    check=False

    #Update currrent client dictionary with [clientconnection]=clientusername
        curclients[clientCon] = clientusername
    #Create a thread dedicated to the connection between this client and the server
        threading.Thread(target=connectedClient,args=(clientCon,clientusername)).start()

    
#Maintains the client connection in lobby and allows them to interact   
def connectedClient(clientCon,clientusername):
    #First get client username then send to lobby
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % clientusername
    clientCon.sendall(bytes(welcome, "utf8"))
    clientCon.sendall(bytes("Please note to send a private message send /username message and @ for a list of current users in chat", "utf8"))
    newClientmsg = "%s has joined the chat.Be nice!" %  clientusername
    Broadcast(bytes(newClientmsg, "utf8"),"Server: ")           
    while True:
    #while connection between server and client is active
        clientmes = clientCon.recv(BUFFER_SIZE)
        
        if clientmes!= bytes("{quit}", "utf8"):
            if clientmes.decode("utf8")[0]=="@":
                #the next 5 character should be the username of intended client
                clientCon.sendall(bytes("Current in lobby are:", "utf8"))
                for client,name in curclients.items():
                    clientCon.sendall(bytes(name+"  ","utf8"))
        
        #If the message is meant to be public
            elif clientmes.decode("utf8")[0]!="/":
                Broadcast(clientmes, clientusername+": ")
            else:
                #the next 5 character should be the username of intended client
                clientCon.sendall(bytes(clientusername+"(sent a whisper)","utf8")+clientmes[7:])
                SendTo(clientmes,clientusername,clientCon)
                    
                
        else:
                    #if message is {quit} then client leaves lobby
            clientCon.sendall(bytes("{quit}", "utf8"))
            clientCon.close()
            del curclients[clientCon]
            Broadcast(bytes("%s has left the chat." % clientusername, "utf8"))
            break
                               
                               
def Broadcast(message,prefix=""):
    for client in curclients:
        #prefix is to identify who is the speaker of message
        client.sendall(bytes(prefix, "utf8")+message)
    

    
def SendTo(clientmes,prefix,clientsocket):
    found=False
    intendedclient=clientmes.decode("utf8")[1:7]
    for client,name in curclients.items():
        if(name==intendedclient):
            client.sendall(bytes(prefix+"(whispers to you): ", "utf8")+clientmes[8:])
            found=True
    if(found==False):
        clientsocket.sendall(bytes("Sorry but that person doesnt exist in our logs","utf8"));
        
            
                
    
    

if __name__ == "__main__":
    #Using 'with' so I dont have to use sock.close()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((HOST, PORT))
            sock.listen(10)
        #thread.start_new_thread( newClient,*sock.accept() )
            while True:
            #put client in a thread of main prohram waiths for thread to end
            #before closing the socket
                CLIENT=threading.Thread(target=createclientThread)
                CLIENT.start()
                CLIENT.join()

           
    #sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)       
   #if __name__ == "__main__":
    #sock.listen(5)
    #print("Waiting for connection...")
    #ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    #ACCEPT_THREAD.start()
    #ACCEPT_THREAD.join()
#SERVER.close()     
    
    

    

