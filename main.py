from machine import Pin, SPI
import mtrx_disp
from sensor_pack.bus_service import SpiAdapter
import utime


if __name__ == '__main__':
    # bus_spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0, firstbit=SPI.MSB)
    bus_spi = SPI(0)
    chip_select = Pin(5, mode=Pin.OUT, value=True)
    adapter = SpiAdapter(bus=bus_spi, data_mode=None)
    display = mtrx_disp.Lmd7219(adapter, chip_select, 4)
    # display.text('1234', 0, 0, 1)
    # display.show()

    br = 0
    while True:
        lt = utime.localtime()
        str_t = f"{lt[4]:02}{lt[5]:02}"
        display.fill(0)   # clear frame buffer
        # display.text(str_t, 0, 0, 1)
        display.rect(0, 0, display.number<<3, 8, 1)
        display.show()
        utime.sleep_ms(1000)
        display.set_brightness(br)
        print(f"text: {str_t}; brightness: {br}")
        br += 1
        if 16 == br:
            br = 0
