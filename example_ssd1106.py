import machine
import sh1106
 
sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)
display = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c,rotate=180)
 
display.text("Hello, Pico!", 0, 0, 1)
display.hline(0, 11, 128, 1)
display.text("Hello, Pico!", 0, 12, 1)
display.hline(0, 23, 128, 1)
display.text("Hello, Pico!", 0, 24, 1)
display.show()