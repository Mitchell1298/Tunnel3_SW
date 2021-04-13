from simple_websocket_server import WebSocketServer, WebSocket
from lfv import Lfv
from aaaa import Bbb
    

class SimpleChat(WebSocket):

    bbb = None
    
        
   
        
    
    def runCommand(self, command, parameter1 = None, parameter2 = None):
        command = command.lower()
        parameter1 = parameter1.lower()
        print("Command    : " + command)
        print("Parameter1 : " + parameter1)
        
        if (command == "slagboom"):
            self.controlSlagboom(parameter1, parameter2)
        elif (command == "stoplicht"):
            self.onStopLichtOff()
        elif (command == "camera"):
            self.controlCamera(parameter1, parameter2)
        else:
            self.broadcastMessage("Unkown command")
        
        
    def handle(self):
        try:
            #check if everything is configured
            if self.bbb == None:
                print("before super")
                #super(SimpleChat, self).__init__() 
                print("Constructor")
                self.bbb = Bbb("192.168.0.47")
                print ("BBB DONE")
                self.bbb.barrier_position_callback = self.on_barrier_position_changed
                self.bbb.barrier_direction_callback = self.on_barrier_direction_changed
        except Exception as e: print(e)
        
        
    
    
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
            
    def controlSlagboom(self, parameter1, parameter2):
        try:
            slagboom = None
            if (parameter1 == "1"):
                slagboom = self.bbb.lfv.BARRIER_1
            if (parameter1 == "2"):
                slagboom = self.bbb.lfv.BARRIER_2
            print("one")
            if parameter2 == "open":
                print("before open")
                self.bbb.lfv.open_barrier(Lfv.BARRIER_1)
                print("after open")
                self.broadcastMessage("Opened slagboom")
                print("two")
            elif parameter2 == "close":
                self.bbb.lfv.close_barrier(Lfv.BARRIER_1)
                self.broadcastMessage("Closed slagboom")
            elif parameter2 == "toggle":
                self.bbb.toggle_barrier(Lfv.BARRIER_1)
                self.broadcastMessage("Toggled slagboom")
        except Exception as e: print(e)
    def controlCamera(self, parameter1, parameter2):
        camera = None
        if (parameter1 == "1"):
            camera = self.bbb.lfv.CAMERA_1
        if (parameter1 == "2"):
            camera = self.bbb.lfv.CAMERA_2
        if (parameter1 == "3"):
            camera = self.bbb.lfv.CAMERA_3
        
        if (parameter2 == "up"):
            self.bbb.lfv.set_camera_orientation(camera, 0, -45, 45)
        elif (parameter2 == "down"):
            self.bbb.lfv.set_camera_orientation(camera, 0, 45, 45)
        elif (parameter2 == "left"):
            self.bbb.lfv.set_camera_orientation(camera, 45, 0, 45)
        elif (parameter2 == "right"):
            self.bbb.lfv.set_camera_orientation(camera, 315, 0, 45)
        elif (parameter2 == "home"):
            self.bbb.lfv.set_camera_orientation(camera, 15, 0, 45)
        elif (parameter2 == "zoomin"):
            self.bbb.lfv.set_camera_orientation(camera, 15, 0, 10)
        elif (parameter2 == "zoomout"):
            self.bbb.lfv.set_camera_orientation(camera, 15, 0, 45)    
        else:
            self.broadcastMessage("Unkown Camera Command")
        self.broadcastMessage("Adjusted camera")
            
    def broadcastMessage(self, message):
        print("Broadcast: " + message)
        for client in clients:
            client.send_message(message)
    #callback functions
    def on_barrier_position_changed(self, barrier, position):
        self.broadcastMessage(str(barrier) + " " + str(position.value))
        #print(str(barrier) + " " + str(position))

    def on_barrier_direction_changed(self, barrier, direction):
        print("ik doe niks")
        #print(str(barrier) + " " + str(direction))
        #self.broadcastMessage(str(barrier) + " " + str(direction))

clients = []

server = WebSocketServer('', 8000, SimpleChat)
server.serve_forever()