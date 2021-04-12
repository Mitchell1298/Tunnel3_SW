from simple_websocket_server import WebSocketServer, WebSocket


    

class SimpleChat(WebSocket):
    def runCommand(self, command, parameter1):
        command = command.lower()
        parameter1 = parameter1.lower()
        print("Command    : " + command)
        print("Parameter1 : " + parameter1)
        
        if (command == "slagboom"):
            self.controlSlagboom(parameter1)
        elif (command == "stoplicht"):
            self.onStopLichtOff()
        else:
            print("Unknown command")
         
        
        
        
    def handle(self):
        print("Received: " + str(self.data))
        parts = self.data.split()

        print(parts)
        if len(parts) == 2:
            print("running cmd")
            self.runCommand(parts[0], parts[1]) 
        #for client in clients:
        #    if client != self:
        #        client.send_message(self.address[0] + u' - ' + self.data)
        #self.send_message(self.address[0] + u' - ' + self.data)

    def connected(self):
        print(self.address, 'connected')
        for client in clients:
            client.send_message(self.address[0] + u' - connected')
        clients.append(self)

    def handle_close(self):
        clients.remove(self)
        print(self.address, 'closed')
        for client in clients:
            client.send_message(self.address[0] + u' - disconnected')
            
    def onStopLichtOff(self):
        for client in clients:
            client.send_message("stoplicht is off")
            
    def controlSlagboom(self, parameter1):
        if parameter1 == "open":
            print("Opened slagboom")
        elif parameter1 == "close":
            print("Closed slagboom")
        

clients = []

server = WebSocketServer('', 8000, SimpleChat)
server.serve_forever()