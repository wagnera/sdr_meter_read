from rtlsdr import *

server = RtlSdrTcpServer(hostname='localhost', port=1234)
server.run_forever()
# Will listen for clients until Ctrl-C is pressed