
import threading
from win32com.shell import shell, shellcon
from threading  import Thread
from queue import Queue, Empty
import sys
import time
import subprocess


class lh_console:
    
    def __init__(self,file_name=False):
        #steamPath = "D:\\Steam"
        #lh_path = steamPath + "\\steamapps\\common\\SteamVR\\tools\\lighthouse\\bin\\win32\\lighthouse_console.exe"
        lh_path = "lighthouse_console.exe"
        if file_name:
            self.console = subprocess.Popen(lh_path + "> "+file_name, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        else:
            self.console = subprocess.Popen(lh_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    
    def start_background_thread(self):
        self.q = Queue()
        self.t = Thread(target=self.enqueue_output, args=(self.console.stdout, self.q))
        self.t.daemon = True # thread dies with the program
        self.t.start()
    
    def enqueue_output(self, out, queue):
        try:
            for line in iter(out.readline, b''):
                queue.put(line)
            out.close()
        except:
            pass
    
    def communicate(self,input):
        stdout, stderr = self.console.communicate(input=bytes(input,'utf-8'))
        return [stdout,stderr]
    
    def read_output(self):
        rtn = ""
        loop = True
        i = 0
        match = 'lh>'
        self.console.stdout.flush()
        while (loop):
            out = self.console.stdout.read1(1)
            rtn = rtn + out.decode('utf-8')
            if match == rtn[-3:]:
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
    
    def read_char(self):
        out = self.console.stdout.read1(1)
    
    def cmd(self,cmd_string):
        self.console.stdin.write(bytes(cmd_string+'\n','utf-8'))
        self.console.stdin.flush()
        
    def record(self,imu=True,sample=True,raw=True):
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
        
    def stop_and_save(self,file):
        self.cmd('record')
        print(self.read_output())
        self.cmd('save')
        time.sleep(1)
        print(self.read_output())
        #os.rename("lighthouse_console_save.txt",file)
        print('moved lighthouse_console_save.txt to '+file)
        
    def capture_tdm_csv(self,filename,time_period=60):
        t1 = threading.Thread(target = self.capture_tdm_csv_thread, args = (filename,time_period))
        t1.start()

    def capture_tdm_csv_thread(self,file_name,time_period):
        c = lh_console()
        c.start_background_thread()
        c.cmd("dis")
        c.cmd("dump")
        time.sleep(time_period)
        c.cmd("dump")
        time.sleep(10)
        tdm = c.read_all()
        c.cmd("exit")
        tdm = tdm.split("\n")
        tdm_data = []
        bs_info = {}
        master_csv = []
        master_csv_line = ['total','invalid','runts','sync_miss',
                           '408081F6:0 period','408081F6:0 ppm','408081F6:0 sync sensors','408081F6:0 sample sensors','408081F6:0 multi-hit sensors',
                           '408081F6:1 period','408081F6:1 ppm','408081F6:1 sync sensors','408081F6:1 sample sensors','408081F6:1 multi-hit sensors',
                           '267A5331:0 period','267A5331:0 ppm','267A5331:0 sync sensors','267A5331:0 sample sensors','267A5331:0 multi-hit sensors',
                           '267A5331:1 period','267A5331:1 ppm','267A5331:1 sync sensors','267A5331:1 sample sensors','267A5331:1 multi-hit sensors']
        start = False
        l = 0
        for line in tdm:
            if l == 0:
                if line[:3]=='TDM':
                    if master_csv_line != []:
                        master_csv.append(master_csv_line)
                        master_csv_line = []
                    l=1
                    d = re.split('=| ',line)

                    tdm_data.append([int(d[2]),int(d[4]),int(d[6]),int(d[8])])
                    master_csv_line = master_csv_line + [int(d[2]),int(d[4]),int(d[6]),int(d[8])]
            else:
                if line[:4] == '    ':
                    d = re.split('=| |:',line.strip())
                    bs_info.setdefault(d[0],{0:[],1:[]})
                    bs_info[d[0]][int(d[1])].append([int(d[4]),int(d[6]),float(d[8]),float(d[10]),float(d[12])])
                    master_csv_line = master_csv_line + [int(d[4]),int(d[6]),float(d[8]),float(d[10]),float(d[12])]
                    if l <3:
                        l = l+1
                    else:
                        l = 0

        with open(file_name, "w") as f:
            writer = csv.writer(f,lineterminator='\n')
            writer.writerows(master_csv)
        
    def lh_exit(self):
        self.cmd('exit')
        self.console.stdout.close()