import json

import arcade
import arrow

from arcade import Sound, Text, color
from pyglet.media import Player

from acradio.core.music import State, choose_track
from acradio.core.weather import get_weather
from acradio.lib.application import View
from acradio.lib.fader import Fader
from acradio.lib.paths import settings_path
from acradio.lib.utils import clamp, map_range

day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


class RootView(View):

    def __init__(self):
        super().__init__()

        with open(settings_path) as fp:
            settings = json.load(fp)

        self.state = State(0, 0, 0, 0, "none")
        self.location = settings["location"]

        self.local_time = 0
        self.last_time_refresh = 0
        self.last_weather_refresh = 0

        self.time_refresh_interval = 1
        self.weather_refresh_interval = 600

        self.current_track = None

        self.player: Player = None
        self.get_ready_to_die = False
        self.got_ready_to_die_time = 0

        self.volume = 0.20
        self.debug = False

        self.volume_fader = Fader[float](0, 255, 0, 1, 1, int)

        self.debug_text = Text("[NOT UPDATED]", x = 5, y = self.window.height - 5, anchor_y = "top",
                              font_name = "GohuFont 11 Nerd Font Mono", font_size = 11,
                              color = color.WHITE,
                              width = self.window.width,
                              multiline = True)

        self.time_text = Text("??:??", x = self.window.center_x, y = self.window.center_y,
                              anchor_x = "center",
                              align = "center",
                              font_name = "FOT-Seurat Pro", font_size = 100,
                              color = color.WHITE)

        self.date_text = Text("Day MM/DD", x = self.time_text.right, y = self.time_text.bottom + 10,
                              anchor_y = "top", anchor_x = "right",
                              align = "right",
                              font_name = "FOT-Seurat Pro", font_size = 24,
                              color = color.WHITE)

        self.weather_text = Text("Weather", x = self.time_text.left, y = self.time_text.bottom + 10,
                              anchor_y = "top", anchor_x = "left",
                              align = "left",
                              font_name = "FOT-Seurat Pro", font_size = 24,
                              color = color.WHITE)

        self.volume_text = Text("Volume 40%", x = self.window.center_x, y = self.window.height - 10,
                              anchor_y = "top", anchor_x = "center",
                              align = "center",
                              font_name = "FOT-Seurat Pro", font_size = 24,
                              color = color.WHITE)

        self.setup()

    def update_track(self) -> None:
        _current_track = self.current_track
        self.current_track = choose_track(self.state)

        if self.player is None:
            sound = Sound(self.current_track)
            self.player = sound.play(volume = self.volume, loop = True)
            return

        if _current_track != self.current_track:
            self.get_ready_to_die = True
            self.got_ready_to_die_time = self.player.time

        if self.get_ready_to_die and self.player.time > self.got_ready_to_die_time:
            self.player.delete()
            self.player = None

    def get_weather(self) -> None:
        weather = get_weather(self.location)
        self.state = State(self.state.month, self.state.day, self.state.hour, self.state.minute, weather)
        self.weather_text.text = weather.title()
        self.last_weather_refresh = self.local_time

    def get_time(self) -> None:
        now = arrow.now().datetime
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        day_name = day_names[now.weekday()]
        self.state = State(month, day, hour, minute, self.state.weather)
        self.time_text.text = f"{hour:02}:{minute:02}"
        self.date_text.text = f"{day_name} {month}/{day:02}"
        self.last_time_refresh = self.local_time

    def setup(self) -> None:
        self.local_time = 0
        self.get_time()
        self.get_weather()

        self.update_track()

    def on_update(self, delta_time: float) -> bool | None:
        self.local_time += delta_time
        self.volume_fader.update(delta_time)

        if self.local_time >= self.last_time_refresh + self.time_refresh_interval:
            self.get_time()

        if self.local_time >= self.last_weather_refresh + self.weather_refresh_interval:
            self.get_weather()

        self.update_track()
        self.update_debug_text()

    def reset(self) -> None:
        self.player.delete()
        self.player = None
        with open(settings_path) as fp:
            settings = json.load(fp)
        self.state = State(0, 0, 0, 0, "none")
        self.location = settings["location"]
        self.setup()

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.R:
            self.reset()
        elif symbol == arcade.key.GRAVE:
            self.debug = not self.debug
        elif symbol == arcade.key.MINUS:
            self.volume -= 0.05
            self.volume = max(self.volume, 0)
            self.volume_text.text = f"Volume {self.volume * 2:.0%}"
            self.player.volume = self.volume
            self.volume_fader.activate(self.local_time)
        elif symbol == arcade.key.EQUAL:
            self.volume += 0.05
            self.volume = min(self.volume, 1)
            self.volume_text.text = f"Volume {self.volume * 2:.0%}"
            self.player.volume = self.volume
            self.volume_fader.activate(self.local_time)

    def update_debug_text(self) -> None:
        self.debug_text.text = f"{self.state.month}/{self.state.day} {self.state.hour}:{self.state.minute}\nLocation: {self.location}\nWeather: {self.state.weather}\n\nLocal Time: {self.local_time}\nLast Time Update: {self.last_time_refresh}\nLast Weather Update: {self.last_weather_refresh}\n\nCurrent Track: {self.current_track}\nVolume: {self.volume:.0%}"

    def on_draw(self) -> None:
        self.clear()
        self.time_text.draw()
        self.date_text.draw()
        self.weather_text.draw()

        volume_alpha = self.volume_fader.value
        self.volume_text.color = self.volume_text.color.replace(a = volume_alpha)
        if volume_alpha > 0:
            self.volume_text.draw()

        if self.debug:
            self.debug_text.draw()
