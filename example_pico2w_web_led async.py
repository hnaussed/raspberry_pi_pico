from connect_2_wlan import connect_to_network,wlan
import machine
import uasyncio as asyncio 

led_onboard = machine.Pin("LED", machine.Pin.OUT)
led_onboard.value(0)
led_state = "LED is off"
 
html = """
<!DOCTYPE html>
<html>
    <head> <title>Raspberry Pi Pico W</title> </head>
    <body> <h1>Raspberry Pi Pico W</h1>
        <p>%s</p>
        <form action="%s">
           <input type="submit" value="%s" />
        </form>
    </body>
</html>
"""
 
async def serve_client(reader, writer):
    print("Client connected")  # Print message when client is connected
    request_line = await reader.readline()  # Read the HTTP request line
    print("Request:", request_line)         # Print the received request
    print("Request_line", type( request_line ))
    # Skip HTTP request headers
    while await reader.readline() != b"\r\n":
        print(" Empyt line ")

    request = str(request_line) 
    print("request:", type( request ))       # Convert request to string
    led_on = request.find('/led/on')   # Check if LED ON request is received
    led_off = request.find('/led/off') 
    print("led_on = " + str(led_on))
    print("led_off = " + str(led_off))

    led_on_2 = request.startswith("b\'GET /led/on")
    led_off_2 = request.startswith("GET /led/off")
    print("led_on = " + str(led_on_2))
    print("led_off = " + str(led_off_2))

    led_state = ""

    if led_on > 0:
        print("Client requested to turn the LED on.")
        led_onboard.value(1)
        led_state = "LED is on"

    if led_off > 0:
        print("Client requested to turn the LED off.")
        led_onboard.value(0)
        led_state = "LED is off"

    if led_state == "LED is on":
        button_link = "/led/off"
        button_text = "Turn LED off"
    else:
        button_link = "/led/on"
        button_text = "Turn LED on" 

    response = html % (led_state,button_link,button_text)
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')  
    writer.write(response)

    await writer.drain()     
    await writer.wait_closed() 
    print("Client disconnected")


async def main():
    connect_to_network()
    print('Setting up webserver...')  
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80)) 
    
    while True: 
        if not wlan.isconnected():  
            wlan.disconnect()       
            connect_to_network() 
        await asyncio.sleep(0.1)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()