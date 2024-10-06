from acradio.lib.application import Window
from acradio.views.root import RootView
from resources import load_otf_font, load_font

def main() -> None:
    load_font("gohu")
    load_otf_font("Seurat Pro B")
    load_otf_font("Seurat Pro UB")
    load_otf_font("Seurat Pro DB")

    win = Window()
    root = RootView()

    win.show_view(root)
    win.run()
