from time import sleep
from machine import Pin,ADC
import connectWifi
from microWebSrv import MicroWebSrv
import utime
def _httpHandlerDHTGet(httpClient, httpResponse):
    global count
    count=0
    f = open("webFolder//a.txt", "w")
    f.close()
    f = open("webFolder//a.txt", "a")
    global max1
    global prev_max
    global l
    global prev_status
    global reading
    while count!=5000:
        sleep(.0002)
        count=(count%5000)+1
        I=reading.read()
        l.append(I)
        #logging.debug('{0}'.format(I))
        f.write('%s:%s\n' % ( utime.ticks_us(),I))
        k=l.pop(0)
    max1=max(l)
    print(l)
    status="OFF"
    current=(max1/4096)*30
    if max1<400:
        status="OFF"
    
    elif prev_status!="OFF" and (max1>prev_max*1.1 or max1<prev_max*0.9):
        status="Faulty"
    else:
        status="ON"
    prev_status=status
    data = 'Current = {0:.1f}A  Status = {1}'.format(current,status)
    prev_max=max1   
    httpResponse.WriteResponseOk(
        headers = ({'Cache-Control': 'no-cache'}),
        contentType = 'text/event-stream',
        contentCharset = 'UTF-8',
        content = 'temp: {1}\n\n current: {2}\n\n voltage: {3}\n\ndata: {0}\n\n'.format(data,"1","2","3") )

connectWifi.connect()
l=[]
prev_max=0
prev_status="OFF"
reading=ADC(Pin(35))
f = open("webFolder//a.txt", "a")
f.write("Now the file has more content!")
f.close()



while len(l)<150:
    l.append(reading.read())
    sleep(.0002)
max1=max(l)
print(l)
count=0
routeHandlers = [ ( "/dht", "GET",  _httpHandlerDHTGet ) ]
srv = MicroWebSrv(routeHandlers=routeHandlers, webPath='webFolder')
srv.Start(threaded=False)




