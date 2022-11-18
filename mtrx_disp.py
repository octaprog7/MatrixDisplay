from sensor_pack.bus_service import SpiAdapter
from sensor_pack.base_sensor import Device, check_value
from machine import Pin
from micropython import const
import framebuf


class Lmd7219(Device):
    """MicroPython class for work with MAX7219 led matrix 8x8 display"""

    cmd_nop = const(0)
    cmd_digit0 = const(1)
    cmd_decode_mode = const(9)
    cmd_intensity = const(10)
    cmd_scan_limit = const(11)
    cmd_shutdown = const(12)
    cmd_display_test = const(15)

    def __init__(self, adapter: SpiAdapter, address: Pin, number: int):
        """number - количество элементов дисплея 8х8 led точек. От 1 до 32."""
        super().__init__(adapter, address, True)
        self.number = check_value(number, range(1, 33), f"Invalid number: {number}")
        self.buffer = bytearray(8 * number)
        fb = framebuf.FrameBuffer(self.buffer, 8 * number, 8, framebuf.MONO_HLSB)
        self.framebuf = fb
        #
        # framebuf info: http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
        self.fill = fb.fill     # (col)
        self.pixel = fb.pixel   # (x, y[, c])
        self.hline = fb.hline   # (x, y, w, col)
        self.vline = fb.vline   # (x, y, h, col)
        # self.line = fb.line     # (x1, y1, x2, y2, col)
        self.rect = fb.rect     # (x, y, w, h, col)
        # self.fill_rect = fb.fill_rect  # (x, y, w, h, col)
        self.text = fb.text  # (string, x, y, col=1)
        # self.scroll = fb.scroll  # (dx, dy)
        # self.blit = fb.blit  # (fbuf, x, y[, key])
        #
        self.msb_first = False
        self.init()

    def _setup_bus(self):
        """Настройки для правильной передачи данных по шине.
        Settings for correct bus communication"""
        if self.msb_first:
            # self.adapter.bus.firstbit = SPI.MSB
            ...
        else:
            # self.adapter.bus.firstbit = SPI.LSB
            ...
        self.adapter.use_data_mode_pin = False

    def _write(self, buf: bytes, enable_cs_ctrl: bool = True):
        """Запись данных по шине адресату.
        enable_cs_ctrl - включить управление выводом chip_enable
        Writing data on the bus to the destination.
        enable_cs_ctrl - enable chip selection control"""
        # адаптер могут использовать несколько устройств на шине, поэтому,
        # перед каждой записью в шину необходима настройка!
        # the adapter can be used by several devices on the bus, therefore,
        # before each write to the bus, configuration is necessary!
        self._setup_bus()
        # запись во все элементы отображения
        if enable_cs_ctrl:
            self.address.low()
        for _ in range(self.number):
            self.adapter.write(self.address, buf)
        if enable_cs_ctrl:
            self.address.high()

    def init(self):
        self._setup_bus()
        for command, data in (
            (Lmd7219.cmd_shutdown, 0),
            (Lmd7219.cmd_display_test, 0),
            (Lmd7219.cmd_scan_limit, 7),
            (Lmd7219.cmd_decode_mode, 0),
            (Lmd7219.cmd_shutdown, 1),
        ):
            self._write(bytes((command, data)))

    def set_brightness(self, value):
        self._setup_bus()
        if not 0 <= value <= 15:
            raise ValueError(f"Brightness out of range: {value}")
        self._write(bytes((Lmd7219.cmd_intensity, value)))
    
    def show(self):
        self._setup_bus()
        num = self.number
        for y in range(8):
            self.address.low()
            for m in range(num):
                a = Lmd7219.cmd_digit0 + y
                b = self.buffer[(y * num) + m]
                # self.adapter.bus.write(bytearray((a, b)))
                self.adapter.bus.write(bytearray((a, b)))
            self.address.high()

    def fill(self, color: int = 0):
        """Fill the entire FrameBuffer with the specified color."""
        self.fill(color)

    def set_pixel(self, x: int, y: int, color: int = 1):
        """Set the specified pixel to the given color."""
        self.pixel(x, y, color)

    def get_pixel(self, x: int, y: int):
        """Get the color value of the specified pixel."""
        return self.pixel(x, y)

    def rect(self, x: int, y: int, width: int, height: int, color: int = 1):
        """Draw a rectangle at the given location, size and color.
        The fill parameter can be set to True to fill the rectangle. Otherwise just a one pixel outline is drawn."""
        self.rect(x, y, width, height, color)

    def horiz_line(self, x: int, y: int, width: int, color: int = 1):
        """Draw horizontal line"""
        self.hline(x, y, width, color)

    def vert_line(self, x: int, y: int, height: int, color: int = 1):
        """Draw vertical line"""
        self.vline(x, y, height, color)