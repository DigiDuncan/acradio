from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import TypedDict, NotRequired

from acradio.lib import paths

class Requirements(TypedDict):
    month: NotRequired[int]
    day: NotRequired[int]
    time: NotRequired[int]
    weather: NotRequired[str]
    priority: int

class FileJSON(TypedDict):
    music: dict[str, Requirements]
    location: str

@dataclass
class State:
    month: int
    day: int
    hour: int
    minute: int
    weather: str

    @property
    def time(self) -> int:
        return self.hour * 100 + self.minute

def load_tracks() -> dict[str, Requirements]:
    with open(paths.settings_path) as f:
        j: FileJSON = json.load(f)
    for v in j["music"].values():
        if "priority" not in v:
            v["priority"] = 0
    return j["music"]

tracks = load_tracks()

def choose_track(state: State) -> Path:
    state_dict = asdict(state)

    # Filter to only tracks that match our state
    possible_tracks: dict[str, Requirements] = {
        track: req
        for track, req in tracks.items()
        if all((state_dict[r] == v for r,v in req.items() if not (r == 'time' or r == 'priority')))
    }

    # Cull times too late (lteq)
    possible_tracks = {t: r for t, r in possible_tracks.items() if r.get("time", 0) <= state.time}

    # Sort by time and priority
    possible_tracks = dict(sorted(possible_tracks.items(), key=lambda item: (item[1]["time"], item[1]["priority"])))

    if not possible_tracks:
        raise ValueError("No valid track found!")

    file = list(possible_tracks.items())[-1][0]

    return paths.music_path / (file + ".mp3")
