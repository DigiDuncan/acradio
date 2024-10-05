from pathlib import Path
from appdirs import user_data_dir

data_path = Path(user_data_dir("ACRadio", "DigiDuncan"))
music_path = data_path / "music"
settings_path = data_path / "settings.json"
