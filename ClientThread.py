import random
import socket, threading
import Questions


class ClientThread(threading.Thread):
    punkty = 0
    maksLiczba = len(Questions.PYTANIA)

    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection

    def losujLiczby(self, ileLiczb):
        liczby = []
        i = 0
        while i < ileLiczb:
            liczba = random.randint(0, self.maksLiczba - 1)
            if liczby.count(liczba) == 0:
                liczby.append(liczba)
                i += 1
        return liczby

    def run(self):
        data = self.connection.recv(1024)
        print "otrzymalem na start: " + data
        # obsluga odbierania i wysylania danych
        self.connection.sendall("Czy chcesz sie zalogowac? t/n.")
        data = self.connection.recv(1024)

        if data == 't': #logowanie
            print 'logowanie..'
            self.name = 'Zalogowany'
        else:
            self.name = 'Gosc'

        print "zmiana"
        self.connection.sendall("Ile pytan chcesz?")
        data = self.connection.recv(1024)
        print self.getName() + "wybral: " + data
        data = int(data)
        numeryPytan = self.losujLiczby( data)
        print ("wylosowane liczby dla: " + self.getName() + str(numeryPytan) )
        for x in range(0,data):
            i = numeryPytan[x]
            print "i: " + str(i)

            print "otrzymalem: " + str(data)

            pytanie = str(Questions.PYTANIA[i]['pytanie'])
            odpowiedzi = str(Questions.PYTANIA[i]['odpowiedzi'])
            correctAnswer = str(Questions.PYTANIA[i]['odpok']).lower()

            if data == 'exit' or data == '':
                endConn = "koniec polaczenia"
                self.connection.sendall(endConn)
                print endConn + "with: " + self.getName()
                break

            self.connection.sendall(pytanie + odpowiedzi)

            userRecv = str(self.connection.recv(1024))
            userRecv = userRecv.lower()
            print self.getName() + ": "+ userRecv +", correct: " + correctAnswer
            if userRecv == correctAnswer:
                feedback = "odpowiedz poprawna +1 punkt"
                self.punkty += 1
            else:
                feedback = "odpowiedz niepoprawna"
            self.connection.sendall(feedback + ", liczba Twoich punktow to: " + str(self.punkty))
