from collections.abc import Callable
from acradio.lib.utils import HasAddSubMul, map_range

class Fader:
    def __init__(self, min_val, max_val, fade_in: float, hold: float, fade_out: float, wrap = False) -> None:
        self.min_val = min_val
        self.max_val = max_val

        self.fade_in = fade_in
        self.hold = hold
        self.fade_out = fade_out

        self.wrap = wrap

        self.local_time = 0
        self.last_activation_time = float("-inf")

    def update(self, delta_time: float) -> None:
        self.local_time += delta_time

    @property
    def fade_in_end(self) -> float:
        return self.last_activation_time + self.fade_in

    @property
    def hold_end(self) -> float:
        return self.last_activation_time + self.fade_in + self.hold

    @property
    def fade_out_end(self) -> float:
        return self.last_activation_time + self.fade_in + self.hold + self.fade_out

    @property
    def value(self):
        if self.local_time < self.last_activation_time:
            v = self.min_val
        elif self.local_time < self.fade_in_end:
            v = map_range(self.local_time, self.last_activation_time, self.fade_in_end, self.min_val, self.max_val)
        elif self.local_time < self.hold_end:
            v = self.max_val
        elif self.local_time < self.fade_out_end:
            v = map_range(self.local_time, self.hold_end, self.fade_out_end, self.max_val, self.min_val)
        else:
            v = self.min_val

        return v if not self.wrap else self.wrap(v)

    def activate(self, time: float) -> None:
        self.last_activation_time = time
