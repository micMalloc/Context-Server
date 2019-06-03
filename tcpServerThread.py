
import socket, threading
from Handler import contextHandler
from Crawler import twitterCrawler


class TCPServerThread(threading.Thread):

    def __init__(self, tcpServerThreads, connections, connection, clientAddress):
        threading.Thread.__init__(self)

        self.tcpServerThreads = tcpServerThreads
        self.connections = connections
        self.connection = connection
        self.clientAddress = clientAddress
        self.twitterCrawler = twitterCrawler.TwitterCrawler()

    def run(self):
        try:
            self.twitterCrawler.run()

            while True:
                data = self.connection.recv(1024).decode('utf-8')

                if not data:
                    print("tcp server :: exit :", self.connection)
                    break
                print(data)

                handler = contextHandler.ContextHandler(data)

                if handler is None:
                    break

                handler.parse()

        except ConnectionError:
            print('Error Detection')
            self.connections.remove(self.connection)
            self.tcpServerThreads.remove(self)
            exit(0)
        self.connections.remove(self.connection)
        self.tcpServerThreads.remove(self)

    def send(self, message):
        print("tcp server :: ", message)
        try:
            for i in range(len(self.connections)):
                self.connections[i].sendall(message.encode())
        except ConnectionError:
            pass
