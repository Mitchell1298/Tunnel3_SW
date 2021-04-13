from simple_websocket_server import WebSocketServer, WebSocket
from lfv import Lfv

    

class SimpleChat(WebSocket):

    lfv = Lfv("192.168.0.47")
    def initialise(self):
        print("Initialise")
        
        
    
    def runCommand(self, command, parameter1 = None, parameter2 = None):
        command = command.lower()
        parameter1 = parameter1.lower()
        print("Command    : " + command)
        print("Parameter1 : " + parameter1)
        
        if (command == "slagboom"):
            self.controlSlagboom(parameter1)
        elif (command == "stoplicht"):
            self.onStopLichtOff()
        elif (command == "camera"):
            self.controlCamera(parameter1, parameter2)
        else:
            self.broadcastMessage("Unkown command")
         
        
        
        
    def handle(self):
        print("Received: " + str(self.data))
        parts = self.data.split()

        print(parts)
        if len(parts) == 2:
            print("running cmd")
            try:
                self.runCommand(parts[0], parts[1])
            except Exception as e: print(e)
        if len(parts) == 3:
            print("running cmd")
            try:
                self.runCommand(parts[0], parts[1], parts[2])
            except Exception as e: print(e)
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
        self.broadcastMessage("stoplicht is off")
            
    def controlSlagboom(self, parameter1):
        try:
            if parameter1 == "open":
                self.lfv.open_barrier(Lfv.BARRIER_1)
                self.broadcastMessage("Opened slagboom")
            
            elif parameter1 == "close":
                self.lfv.close_barrier(Lfv.BARRIER_1)
                self.broadcastMessage("Closed slagboom")
        except Exception as e: print(e)
    def controlCamera(self, parameter1, parameter2):
        camera = None
        if (parameter1 == "1"):
            camera = self.lfv.CAMERA_1
        if (parameter1 == "2"):
            camera = self.lfv.CAMERA_2
        if (parameter1 == "3"):
            camera = self.lfv.CAMERA_3
        
        if (parameter2 == "up"):
            self.lfv.set_camera_orientation(camera, 0, -45, 45)
        elif (parameter2 == "down"):
            self.lfv.set_camera_orientation(camera, 0, 45, 45)
        elif (parameter2 == "left"):
            self.lfv.set_camera_orientation(camera, 45, 0, 45)
        elif (parameter2 == "right"):
            self.lfv.set_camera_orientation(camera, 315, 0, 45)
        elif (parameter2 == "home"):
            self.lfv.set_camera_orientation(camera, 15, 0, 45)
        elif (parameter2 == "zoomin"):
            self.lfv.set_camera_orientation(camera, 15, 0, 10)
        elif (parameter2 == "zoomout"):
            self.lfv.set_camera_orientation(camera, 15, 0, 45)    
        else:
            self.broadcastMessage("Unkown Camera Command")
        self.broadcastMessage("Adjusted camera")
            
    def broadcastMessage(self, message):
        print("Broadcast: " + message)
        for client in clients:
            client.send_message(message)
        

clients = []

server = WebSocketServer('', 8000, SimpleChat)
server.serve_forever()