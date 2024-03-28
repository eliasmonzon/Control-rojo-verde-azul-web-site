
#Control de led RVA para esp 32 y 8266
import time
from machine import Pin, PWM
import network
import socket
import usocket
#configuracion de pines 
Rojo = Pin(15, Pin.OUT)
Verde = Pin(12, Pin.OUT)
Azul = Pin(13, Pin.OUT)

#credeciales wifi
ssid = 'E13'
password = 'elias1983'
wlan = network.WLAN(network.STA_IF)

wlan.active(True)
wlan.connect(ssid, password)

while wlan.isconnected() == False:
    pass

print('Conexion con el WiFi %s establecida' % ssid)
print(wlan.ifconfig())

a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
a.bind(('', 80))
a.listen(3)

def web_page():
#pagina web 
  html =  """
                             <center>
    <h1><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Control Rojo Verde Azul</h1></b><br>
    <body> 

        <b>&nbsp;Rojo&nbsp;&nbsp;</b>
        <a href="/?Rojo+"><button style='width:100px; height:35px; background-color: #ff5252'>Subir brillo</button></a>&nbsp;&nbsp;
        <a href="/?Rojo-"> <button style='width:100px; height:35px; background-color: #ff5252'>Bajar brillo</button></a><br><br>

        <b>&nbsp;Verde&nbsp;&nbsp;</b>
        <a href="/?Verde+"><button style='width:100px; height:35px; background-color: #00ff00'>Subir brillo</button></a>&nbsp;&nbsp;
        <a href="/?Verde-"> <button style='width:100px; height:35px; background-color: #00ff00'>Bajar brillo </button></a><br><br>

        <b>&nbsp;Azul&nbsp;&nbsp;</b>
        <a href="/?Azul+"><button style='width:100px; height:35px; background-color: #006c9a'>Subir brillo</button></a>&nbsp;&nbsp;
        <a href="/?Azul-"> <button style='width:100px; height:35px; background-color: #006c9a'>Bajar brillo </button></a><br><br>

       
    </body>
    """
  return html
duty_cycle = 0  # Inicializar el ciclo de trabajo

#funciones 
def subir_brillo(color_led):
    global duty_cycle
    duty_cycle += 30  # Aumentar el brillo en 50
    if duty_cycle > 1023:  # Limitar el ciclo de trabajo máximo
        duty_cycle = 1023
    color_led.duty(duty_cycle)
    time.sleep(0.1)  # Espera breve entre cada paso
    
def bajar_brillo(color_led):
    global duty_cycle
    duty_cycle -= 30  # Aumentar el brillo en 50
    if duty_cycle < 0:  # Limitar el ciclo de trabajo máximo
        duty_cycle = 0
    color_led.duty(duty_cycle)
    time.sleep(0.1)  # Espera breve entre cada paso

    

#control de cada led por pwm
Color_rojo = PWM(Rojo)
Color_verde = PWM(Verde)
Color_azul = PWM(Azul)


#bucle infinito
while True:
    conn,addr = a.accept()
    print('Nueva conexion desde:  %s' % str(addr))
    request = conn.recv(1024)
    print('Solicitud = %s' % str(request))
    request = str(request)
    
    if (request.find('/?Rojo+') == 6):
       
         subir_brillo(Color_rojo)
    if (request.find('/?Rojo-') == 6):
        
         bajar_brillo(Color_rojo)
        
    if (request.find('/?Verde+') == 6):
         subir_brillo(Color_verde)
         
    if (request.find('/?Verde-') == 6):
         bajar_brillo(Color_verde)
         
    if (request.find('/?Azul+') == 6):
        subir_brillo(Color_azul)
        
    if (request.find('/?Azul-') == 6):
       bajar_brillo(Color_azul)
        
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()