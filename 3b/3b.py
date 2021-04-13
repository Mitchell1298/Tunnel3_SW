from lfv import Lfv
import threading
import time

class Bbb:
    def __init__(self, ip):
        self.lfv = Lfv(ip)
        self.thread = threading.Thread(target=self._update_thread)
        self.running = True
        self.thread.start()
        

    def _update_thread(self):
        self.last_light_state = [None] * 4
        self.last_barrier_position = [None] * 2
        self.last_barrier_direction = [None] * 2

        while self.running:
            time.sleep(0.5)
            #print("loop")
            try:
                for i in range(4):
                    state = self.lfv.get_traffic_light_status(i)
                    if (self.last_light_state[i] is None or state.value != self.last_light_state[i].value):
                        self.last_light_state[i] = state
                        print(str(i) + " " + str(state))

                for i in range(2):
                    barrier = [Lfv.BARRIER_1, Lfv.BARRIER_2]
                    position = self.lfv.get_barrier_position(barrier[i])
                    if (self.last_barrier_position[i] is None or position.value != self.last_barrier_position[i].value):
                        self.last_barrier_position[i] = position
                        print(str(i) + " " + str(position))

                for i in range(2):
                    barrier = [Lfv.BARRIER_1, Lfv.BARRIER_2]
                    direction = self.lfv.get_barrier_direction(barrier[i])
                    if (self.last_barrier_direction[i] is None or direction.value != self.last_barrier_direction[i].value):
                        self.last_barrier_direction[i] = direction
                        print(str(i) + " " + str(direction))
                
            except Exception as e:
                print(e)
            
if __name__ == "__main__":
    bbb = Bbb("192.168.0.47")
    bbb.lfv.set_traffic_light_off(1)
    bbb.lfv.open_barrier(Lfv.BARRIER_1)

    # Exit loop on ctrl+c
    try:
        while True:
            time.sleep(10.0)
    except:
        bbb.running = False