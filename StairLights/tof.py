from vl53l1x import VL53L1X
import machine

class TOF(VL53L1X):
    def __init__(self):
        super().__init__(self, )
        

    def average(tof, samples=32):
        l = []
        [l.append(tof.read()) for i in range(samples)]
        avg = sum(l) / len(l)
        lo_error = avg - 20
        hi_error = avg + 20
        return lo_error, avg, hi_error