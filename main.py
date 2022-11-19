from machine import Pin, SPI
import mtrx_disp
from sensor_pack.bus_service import SpiAdapter
import utime


if __name__ == '__main__':
    bus_spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0, firstbit=SPI.MSB)
    # bus_spi = SPI(0)
    chip_select = Pin(5, mode=Pin.OUT, value=True)
    adapter = SpiAdapter(bus=bus_spi, data_mode=None)
    display = mtrx_disp.Lmd7219(adapter, chip_select, 4)
    
    switch = False
    
    for txt in "Clck", "Demo", "7219", "MMss":
        display.fill(0)   # clear frame buffer
        display.text(txt, 0, 0, 1)
        display.show()
        utime.sleep_ms(3000)

    br = 0
    while True:
        lt = utime.localtime()
        # min and sec
        str_t = f"{lt[4]:02}{lt[5]:02}"
        display.fill(0)   # clear frame buffer
        display.text(str_t, 0, 0, 1)

        if switch:
            a, b = 15, 16
        else:
            a, b = 16, 15

        display.vert_line(a, 0, 3, 1)
        display.vert_line(b, 5, 3, 1)

        switch = not switch
        # display.rect(0, 0, display.number << 3, 8, 1)
        # display.set_pixel(1, 1, 1)
        # display.set_pixel(10, 5, 1)
        display.show()
        print(f"text: {str_t}; brightness: {br}")
        utime.sleep_ms(1000)
        display.set_brightness(br)
        br += 1
        if 16 == br:
            br = 0
