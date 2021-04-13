from lfv import Lfv, BarrierDirection, BarrierPosition
import threading
import time

class Bbb:
    def __init__(self, ip):
        self.lfv = Lfv(ip)
        self.thread = threading.Thread(target=self._update_thread)
        self.running = True

        self.lights_state_callback = None
        self.barrier_position_callback = None
        self.barrier_direction_callback = None
        self.lights_level_callback = None

        self.thread.start()


    def toggle_barrier(self, barrier):
        b = [Lfv.BARRIER_1, Lfv.BARRIER_2]
        if self.last_barrier_direction[b.index(barrier)] == BarrierDirection.NONE:
            if self.last_barrier_position[b.index(barrier)] == BarrierPosition.UP:
                self.lfv.close_barrier(barrier)
            elif self.last_barrier_position[b.index(barrier)] == BarrierPosition.DOWN:
                self.lfv.open_barrier(barrier)
        

    def _update_thread(self):
        self.last_light_state = [None] * 4
        self.last_barrier_position = [None] * 2
        self.last_barrier_direction = [None] * 2
        self.last_light_level = [None] * 7

        while self.running:
            time.sleep(0.5)
            #print("loop")
            try:
                for i in range(4):
                    state = self.lfv.get_traffic_light_status(i)
                    if (self.last_light_state[i] is None or state.value != self.last_light_state[i].value):
                        self.last_light_state[i] = state
                        if self.lights_state_callback is not None:
                            self.lights_state_callback(i, state)

                for i in range(2):
                    barrier = [Lfv.BARRIER_1, Lfv.BARRIER_2]
                    position = self.lfv.get_barrier_position(barrier[i])
                    if (self.last_barrier_position[i] is None or position.value != self.last_barrier_position[i].value):
                        self.last_barrier_position[i] = position
                        if self.barrier_position_callback is not None:
                            self.barrier_position_callback(i, position)

                for i in range(2):
                    barrier = [Lfv.BARRIER_1, Lfv.BARRIER_2]
                    direction = self.lfv.get_barrier_direction(barrier[i])
                    if (self.last_barrier_direction[i] is None or direction.value != self.last_barrier_direction[i].value):
                        self.last_barrier_direction[i] = direction
                        if self.barrier_direction_callback is not None:
                            self.barrier_direction_callback(i, direction)

                for i in range(7):
                    level = self.lfv.get_lights_level_zone(i)
                    if (self.last_light_level[i] is None or level != self.last_light_level[i]):
                        self.last_light_level[i] = level
                        if self.lights_level_callback is not None:
                            self.lights_level_callback(i, level)
                
            except Exception as e:
                print(e)


def on_barrier_position_changed(barrier, position):
    print(str(barrier) + " " + str(position))

def on_barrier_direction_changed(barrier, direction):
    print(str(barrier) + " " + str(direction))
            
if __name__ == "__main__":
    bbb = Bbb("192.168.0.47")
    bbb.barrier_position_callback = on_barrier_position_changed
    bbb.barrier_direction_callback = on_barrier_direction_changed

    time.sleep(1.0)

    bbb.lfv.set_traffic_light_off(1)

    bbb.toggle_barrier(Lfv.BARRIER_2)
    

    # Exit loop on ctrl+c
    try:
        while True:
            time.sleep(1.0)
            bbb.toggle_barrier(Lfv.BARRIER_2)
    except:
        bbb.running = False