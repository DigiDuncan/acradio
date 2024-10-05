from acradio.lib.application import Window
from acradio.views.root import RootView
from resources import load_font

def main() -> None:
    load_font("gohu")

    win = Window()
    root = RootView()

    win.show_view(root)
    win.run()
