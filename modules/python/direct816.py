import _direct816  # noqa: F401
import micropython
from array import array

try:
    from typing import TYPE_CHECKING
    from collections.abc import Callable

    if TYPE_CHECKING:
        uint = int

        def const(i: int) -> int:
            return i
except ImportError:
    TYPE_CHECKING = False
    Callable = object

max_pal = const(256)
palmask = const(max_pal - 1)
WIDTH = const(240)
HEIGHT = const(320)
BYTES_PER_PIXEL = const(2)


# Expected values 0..255
@micropython.viper
def rgb565(r: uint, g: uint, b: uint) -> uint:
    return ((r & 0b11111000) << 8 | (g & 0b11111100) << 3 | b >> 3) & 0xFFFF


# This is the format PicoVector stores colours in memory
@micropython.viper
def u32_rgb565(src: uint) -> uint:
    return (src & 0xF8) << 8 | (src & 0xFC00) >> 5 | (src & 0xF8_00_00) >> 19


def convert_palette(L: list[tuple[int, int, int]]):
    if len(L) > max_pal:
        raise ValueError(f"Palette is too large {len(L)} > {max_pal}")
    return array("H", [rgb565(*i) for i in L])


def generate_palette(f: Callable[[int], tuple[int, int, int]], count=max_pal):
    if count > max_pal:
        raise ValueError(f"Palette is too large {count} > {max_pal}")
    return array("H", [rgb565(*f(i)) for i in range(count)])


def load_palette(filename: str) -> list[int]:
    temp = array("H", bytearray(max_pal * 2))
    with open(filename, "rb") as f:
        size = f.readinto(temp)
        if size > 512:
            raise ValueError(f"Palette is too large: {size / 2} > {max_pal}")

    return temp


def make_palette_cycle(palette: list) -> list:
    if len(palette) != max_pal:
        raise ValueError("Palette has to have {max_pal} entries")

    # Compact palette by discarding every other entry
    for i in range(128):
        palette[i] = palette[2 * i]

    # Convert upper half into a mirror of the first half
    for i in range(128):
        palette[255 - i] = palette[i]

    return palette


@micropython.viper
def convert_pv_image16(img: object):
    iwidth = int(img.width)
    iheight = int(img.height)
    isize = uint(iwidth * iheight)

    pixels = array("H", bytearray(2 * isize))
    mask = array("B", bytearray(isize))

    dst_width = uint(iheight)
    dst_height = uint(iwidth)

    src: ptr32 = ptr32(img)

    dst: ptr16 = ptr16(pixels)

    for y in range(iheight):
        for x in range(iwidth):
            p32 = uint(src[y * iwidth + x])
            p16: uint = (
                (p32 & 0xF8) << 8 | (p32 & 0xFC00) >> 5 | (p32 & 0xF8_00_00) >> 19
            )
            dst[x * iheight + y] = p16
            mask[x * iheight + y] = 1 if int(p32 >> 24) == 255 else 0

    return pixels, mask, dst_width, dst_height


@micropython.viper
def blit_pv_image16(img, x: int, y: int, masked: bool, darken: bool):
    if x >= WIDTH:
        return
    if y >= HEIGHT:
        return

    iwidth = int(img[2])
    stride = uint(iwidth)
    x_skip = uint(0)
    if x < 0:
        iwidth += x
        x_skip = uint(-x)
        if iwidth <= 0:
            return
        x = 0
    if x + iwidth > WIDTH:
        iwidth = WIDTH - x

    iheight = int(img[3])
    y_skip = uint(0)
    if y < 0:
        iheight += y
        y_skip = uint(-y)
        if iheight <= 0:
            return
        y = 0
    if y + iheight > HEIGHT:
        iheight = HEIGHT - y

    origin = x + WIDTH * y

    src = ptr16(uint(ptr16(img[0])) + (x_skip + y_skip * stride) * BYTES_PER_PIXEL)
    mask = ptr8(uint(ptr8(img[1])) + (x_skip + y_skip * stride))
    dst = ptr16(uint(ptr16(display)) + origin * BYTES_PER_PIXEL)

    if masked:
        if darken:
            for py in range(iheight):
                for px in range(iwidth):
                    srcpos = px + py * stride
                    dstpos = px + py * WIDTH
                    if mask[srcpos]:
                        dst[dstpos] = src[srcpos]
                    else:
                        dst[dstpos] >>= 1
                        dst[dstpos] &= 0b01111_011111_01111
        else:
            for py in range(iheight):
                for px in range(iwidth):
                    srcpos = px + py * stride
                    dstpos = px + py * WIDTH
                    if mask[srcpos]:
                        dst[dstpos] = src[srcpos]
    else:
        for py in range(iheight):
            for px in range(iwidth):
                srcpos = px + py * stride
                dstpos = px + py * WIDTH
                dst[dstpos] = src[srcpos]
