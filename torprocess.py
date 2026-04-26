import os, requests, sys, traceback, hashlib, re, base64, json;
import requests, signal, socket, subprocess, time, threading;

class TorProcess:
    def __init__(self):
        self.port = self.new_port();
        self.done = "Bootstrapped 100% (done): Done";
        self.open = False;
        self.process = None;
        self.torrc = "/tmp/" + str(self.port);
        if not os.path.exists(self.torrc):
            os.makedirs(self.torrc);
        self.torrc += "/torrc";
        self.th = None;
        with open(self.torrc, "w") as f:
            f.write("SocksPort " + str(self.port) + "\n");
            f.write("DataDirectory /tmp/" + str(self.port) + "\n");
   
    def __is_port_in_use__(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    def new_port(self):
        for i in range(6000, 7000):
            if not self.__is_port_in_use__(i):
                return i;
        return None;

    def initialize(self):
        self.th = threading.Thread(target=self.__initialize__);
        self.th.start();
        #self.th.join();
        while True:
            if self.open:
                return;
            time.sleep(1);
    def __initialize__(self):
        self.process = subprocess.Popen( ["tor", "-f", self.torrc], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE);
        while True:
            if self.process == None:
                break;
            linha = self.process.stdout.readline().decode("utf-8").strip();
            if linha != "":
                print(linha);
                if linha.find(self.done) > 0:
                    self.open = True;
                    print("Open == true");
    def kill(self):
        os.kill(self.process.pid, signal.SIGKILL);
        time.sleep(3);
        self.process = None;
        self.th = None;
