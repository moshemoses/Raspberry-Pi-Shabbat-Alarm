#grabs your latitude, longitude and Time zone
import requests, json, datetime
current_year = datetime.datetime.now().strftime('%Y')
loc_request=requests.get('http://ip-api.com/json')
type(loc_request)
loc_request.status_code==requests.codes.ok
loc_request_json_data = loc_request.text
Location_info = json.loads(loc_request_json_data)

# your location data
longi = str(Location_info['lon'])
latit = str(Location_info['lat'])
city = Location_info['city']
region = Location_info['timezone']

#using your location data to get customized shabbos data
#link is for master heb cal calendar api
heb_cal_address='http://www.hebcal.com/hebcal/?v=1&cfg=json&maj=on&min=on&mod=on&nx=on&year='+current_year+'&month=x&ss=on&mf=on&c=on&geo=pos&latitude=['+latit+']&longitude=['+longi+']&tzid=['+region+']&m=50&s=off'


#begin main loop
while 1>0:
    import json, requests, datetime, time
    from subprocess import call

    res = requests.get(heb_cal_address)
    ready = json.loads(res.text)

    #beginning of main while loop that should hold until candles followed by havdala

    #parsing json for times
    data = ready.get('items')

    for i in range(0, len(data)):
        if data[i].get('category') == 'candles' or data[i].get('category') == 'havdalah':
            smell = data[i].get('date')
            smelly = smell.split('T')
            datex = smelly[0]
            time = smelly[1].split('-')
            timex = time[0]
            date_plus_time = datex +" "+ timex
            #date_obj is next candlelighting time and date
            date_obj = datetime.datetime.strptime(date_plus_time, '%Y-%m-%d %H:%M:%S')
            if date_obj >= datetime.datetime.now():
                upcoming_shabbos = date_obj
                candle_date = upcoming_shabbos.strftime('%A %B %d %Y')
                candle_time = upcoming_shabbos.strftime('%I %M %p')
               
                #phrase variable should be activated by push button
                phrase = "Candlelighting on " + candle_date + " will be at " + candle_time
                candles_now = "Candlelighting time has arrived" *5
                havdalah_now = "It's time to make havdalah" * 5
                break
   

    
    if data[i].get('category') == 'candles':
        now = candles_now
    else:
        now = havdalah_now
    
    def button_push():
        print('button push')
        import RPi.GPIO as GPIO
        import time, datetime
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        while True:
            input_state = GPIO.input(18)
            if input_state == False:
                from subprocess import call
                call(["espeak","-s140 -ven+18 -z",phrase])
                time.sleep

    def alarm1(startTime):
        import RPi.GPIO as GPIO
        import time, datetime
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        while datetime.datetime.now() <= startTime:
            input_state = GPIO.input(18)
            if input_state == False:
                from subprocess import call
                call(["espeak","-s140 -ven+18 -z",phrase])
            time.sleep(1)
        from subprocess import call
        call(["espeak","-s140 -ven+18 -z",now])
        print("in alarm" + now+datetime.datetime.now())

    
    alarm1(upcoming_shabbos)
             

    









    







 
    

