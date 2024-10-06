import itertools
from collections.abc import Sequence
from arcade import Rect, LRBT
from arcade.types import Color

from acradio.lib.draw_grad_rect import draw_rect_gradient


gradients = {
    0: [(0.0, 0x020111), (0.85, 0x020111), (1.0, 0x191621)],
    1: [(0.0, 0x020111), (0.6, 0x020111), (1.0, 0x20202C)],
    2: [(0.0, 0x020111), (0.1, 0x020111), (1.0, 0x3A3A52)],
    3: [(0.0, 0x20202C), (1.0, 0x515175)],
    4: [(0.0, 0x40405C), (0.8, 0x6F71AA), (1.0, 0x8A76AB)],
    5: [(0.0, 0xA44969), (0.5, 0x7072AB), (1.0, 0xCD82A0)],
    6: [(0.0, 0x757ABF), (0.6, 0x8583BE), (1.0, 0xEAB0D1)],
    7: [(0.0, 0x82ADDB), (1.0, 0xEBB2B1)],
    8: [(0.0, 0x94C5F8), (0.7, 0xA6E6FF), (1.0, 0xB1B5EA)],
    9: [(0.0, 0xB7EAFF), (1.0, 0x94DFFF)],
    10: [(0.0, 0x9BE2FE), (1.0, 0x67D1FB)],
    11: [(0.0, 0x90DFFE), (1.0, 0x38A3D1)],
    12: [(0.0, 0x57C1EB), (1.0, 0x246FA8)],
    13: [(0.0, 0x2D91C2), (1.0, 0x1E528E)],
    14: [(0.0, 0x90DFFE), (1.0, 0x38A3D1)],
    15: [(0.0, 0x2473AB), (0.7, 0x1E528E), (1.0, 0x5B7983)],
    16: [(0.0, 0x1E528E), (0.5, 0x265889), (1.0, 0x9DA671)],
    17: [(0.0, 0x154277), (0.3, 0x576E71), (0.7, 0xE1C45E), (1.0, 0xB26339)],
    18: [(0.0, 0x163C52), (0.3, 0x4F4F47), (0.6, 0xC5752D), (0.8, 0xB7490F), (1.0, 0x2F1107)],
    19: [(0.0, 0x071B26), (0.3, 0x071B26), (0.8, 0x8A3B12), (1.0, 0x240E03)],
    20: [(0.0, 0x010A10), (0.3, 0x010A10), (0.8, 0x59230B), (1.0, 0x2F1107)],
    21: [(0.0, 0x090401), (0.5, 0x090401), (1.0, 0x4B1D06)],
    22: [(0.0, 0x00000C), (0.8, 0x00000C), (1.0, 0x150800)],
    23: [(0.0, 0x00000C), (0.8, 0x00000C), (1.0, 0x150800)]
}

type StoppedGradient = Sequence[tuple[float, int]]

class GradientRect:
    def __init__(self, rect: Rect, gradient: StoppedGradient):
        self.rect = rect
        self.gradient = gradient

    def draw(self) -> None:
        for a, b in itertools.pairwise(self.gradient):
            draw_rect_gradient(
                LRBT(self.rect.left, self.rect.right,
                     self.rect.bottom + (self.rect.height * (1 - b[0])),
                     self.rect.bottom + (self.rect.height * (1 - a[0]))),
                     Color.from_uint24(a[1]), Color.from_uint24(b[1])
            )
