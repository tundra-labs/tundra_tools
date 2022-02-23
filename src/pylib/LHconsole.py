import threading
from win32com.shell import shell, shellcon
from threading  import Thread
from queue import Queue, Empty
import sys
import time
import subprocess


class LHconsole:
    def __init__(self, file_name=False):
        #steamPath = "D:\\Steam"
        #lh_path = steamPath + "\\steamapps\\common\\SteamVR\\tools\\lighthouse\\bin\\win32\\lighthouse_console.exe"
        lh_path = "..\\bin\\lighthouse\\win32\\lighthouse_console.exe"
        if file_name:
            self.console = subprocess.Popen(lh_path + "> "+file_name, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        else:
            self.console = subprocess.Popen(lh_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def start_background_thread(self):
        self.q = Queue()
        self.t = Thread(target=self.enqueue_output, args=(self.console.stdout, self.q))
        self.t.daemon = False # thread dies with the program
        self.t.start()

    def enqueue_output(self, out, queue):
        try:
            while True:
                out.flush()
                line = out.readline()
                if not line:
                    break;

                queue.put(line)
            #out.close()
        except:
            pass

    def read_output(self):
        rtn = ""
        loop = True
        i = 0
        match = 'lh>'
        self.console.stdout.flush()
        while (loop):
            out = self.console.stdout.read1(1)
            rtn = rtn + out.decode('utf-8')
            if rtn.endswith(match):
                loop = False
            #else:
            #    rtn = rtn + out.decode('utf-8')
        return (rtn)

    def read_line(self):
        try:  line = self.q.get_nowait().decode('utf-8') # or q.get(timeout=.1)
        except Empty:
            return False
        else: # got line
            return line

    def read_all(self):
        rtn = ""
        line = self.read_line()
        while line:
            rtn = rtn + line
            line = self.read_line()

        return rtn

    def read_cmd_output(self):
        rtn = ""
        match = 'lh>'
        loop = True
        self.console.stdout.flush()
        while(loop):
            try:
                line = self.q.get_nowait().decode('utf-8')
                data = line.rstrip()
                print("rco: ", data)
                if data.startswith(match):
                    print("rco: found match")
                    loop = False

                rtn = rtn + data
            except Empty:
                pass

        print("rco: returning")
        return rtn


    def read_char(self):
        out = self.console.stdout.read1(1)

    def cmd(self, cmd_string):
        command = cmd_string + '\r\n'
        self.console.stdin.write(bytes(command, 'utf-8'))
        self.console.stdin.flush()

    def record(self, imu=True, sample=True, raw=True):
        self.cmd('clear')
        print(self.read_output())
        if (imu):
            self.cmd('imu')
            print(self.read_output())
        if (sample):
            self.cmd('sample')
            print(self.read_output())
        if (raw):
            self.cmd('raw')
            print(self.read_output())
        self.cmd('record')
        print(self.read_output())

    def stop_and_save(self, file):
        self.cmd('record')
        print(self.read_output())
        self.cmd('save')
        time.sleep(1)
        print(self.read_output())
        #os.rename("lighthouse_console_save.txt",file)
        print('moved lighthouse_console_save.txt to '+file)

    def lh_cleanup(self):
        self.lh_exit()
        self.q.join()

    def lh_exit(self):
        self.cmd('exit')
        self.console.stdout.close()
