import subprocess
from twisted.internet import reactor, defer

class PingProtocol: 
    def __init__ (self):
        self.deferred = defer.Deferred()

    def ping(self, host):
        process = subprocess.Popen(['ping', '-c', '4', host], stdout=subprocess.PIPE)
 
        output, error = process.communicate() 
        if error:
            self.deferred.errback(error) 
        else:
            self.deferred.callback(output)

def print_result(result): 
        print(result.decode())

def print_error(failure):
     print(failure)

protocol = PingProtocol()
protocol.ping('google.com')
protocol.deferred.addCallbacks(print_result, print_error) 
reactor.run()


class TracerouteCmd: 
    def __init__ (self):
        self.deferred = defer.Deferred()

    def traceroute(self, host):
        # process = subprocess.Popen(['traceroute', '-m', '10', host], stdout=subprocess.PIPE) 
        process = subprocess.Popen(['tracert', '-h', '10', host], stdout=subprocess.PIPE) 
        
        output, error = process.communicate()
        if error:
            self.deferred.errback(error) 
        else:
            self.deferred.callback(output)

def print_result(result):
    
     print(result.decode())

def print_error(failure): 
    print(failure)

protocol = TracerouteCmd()
protocol.traceroute('google.com') 
protocol.deferred.addCallbacks(print_result, print_error)
reactor.run()
