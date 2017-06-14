#!/usr/bin/env python
import socket, sys, threading
import ClientThread
import datetime


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def run(self):
        try:
            # socket, bind, listen
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serv_addr = (self.ip, self.port)
            self.sock.bind(serv_addr)
            self.sock.listen(2)
            print "Nasluchuje: " + self.ip + ":" + str(self.port)

            while True:
                connection, client_address = self.sock.accept()
                print "polaczono z :" + str(client_address)
                c = ClientThread.ClientThread(connection)
                c.start()



        except socket.error, e:
            print "error"


if __name__ == '__main__':
    s = Server('192.168.0.12', 6780)
    s.run()