import json

import arcade
import arrow

from arcade import Sound, Text, color
from pyglet.media import Player

from acradio.core.music import State, choose_track
from acradio.core.weather import get_weather
from acradio.lib.application import View
from acradio.lib.paths import settings_path


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

        self.debug_text = Text("[NOT UPDATED]", x = 5, y = self.window.height - 5, anchor_y = "top",
                              font_name = "GohuFont 11 Nerd Font Mono", font_size = 11,
                              color = color.WHITE,
                              width = self.window.width,
                              multiline = True)

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
        self.last_weather_refresh = self.local_time

    def get_time(self) -> None:
        now = arrow.now().datetime
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        self.state = State(month, day, hour, minute, self.state.weather)
        self.last_time_refresh = self.local_time

    def setup(self) -> None:
        self.local_time = 0
        self.get_time()
        self.get_weather()

        self.update_track()

    def on_update(self, delta_time: float) -> bool | None:
        self.local_time += delta_time

        if self.local_time >= self.last_time_refresh + self.time_refresh_interval:
            self.get_time()

        if self.local_time >= self.last_weather_refresh + self.weather_refresh_interval:
            self.get_weather()

        self.update_track()
        self.update_debug_text()

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.R:
            self.player.delete()
            self.player = None
            with open(settings_path) as fp:
                settings = json.load(fp)
            self.state = State(0, 0, 0, 0, "none")
            self.location = settings["location"]
            self.setup()

    def update_debug_text(self) -> None:
        self.debug_text.text = f"{self.state.month}/{self.state.day} {self.state.hour}:{self.state.minute}\nLocation: {self.location}\nWeather: {self.state.weather}\n\nLocal Time: {self.local_time}\nLast Time Update: {self.last_time_refresh}\nLast Weather Update: {self.last_weather_refresh}\n\nCurrent Track: {self.current_track}\nVolume: {self.volume:.0%}"

    def on_draw(self) -> None:
        self.clear()
        self.debug_text.draw()
