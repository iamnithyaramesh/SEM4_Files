import subprocess
from twisted.internet import reactor,defer

class PingProtocol:
    def __init__(self):
        self.defer=defer.Deferred()

    def ping(self,host):
        process=subprocess.Popen(['tracert','-h','4',host],stdout=subprocess.PIPE)
        output,err=process.communicate()
        if output:
            self.defer.callback(output)
        else:
            self.defer.errback(err)

def print_result(result):
    print(result.decode())

def error(error):
    print(error)

P=PingProtocol()
P.ping('google.com')
P.defer.addCallbacks(print_result,error)
reactor.run()


    