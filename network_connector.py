from network import poll
from threading import Thread

'''Used to attach the network listeners to the handler,
so that it can notify them when something happens'''
class NetworkConnector(object):
    _networkListeners = []
    
    'Used to add one object to the list of observers'
    def attach(self, networkListeners):
        if not networkListeners in self._networkListeners:
            self._networkListeners.append(networkListeners)

    'Used to take one object off the list of observers'
    def detach(self, networkListener):
        try:
            self._networkListeners.remove(networkListener)
        except ValueError:
            pass
        
        
    'Notifies the observers that the following event happened'
    def notify(self, method_name, *args):
        for networkListener in self._networkListeners:
            method = getattr(networkListener, method_name)
            method(*args)    
    
    
    'Must be defined by the subclass. Used to send a message to someone'
    def send_msg(self, msg, handler=None): pass
        
        
'''NetworkListener abstract class, must be extended to receive a message at the network'''
class NetworkListener(object):
    
    def player_joined(self, player_id, topleft): pass
    def player_left(self, player_id): pass
    def player_performed_action(self, player_id, action): pass
    
    def player_new_score(self, score): pass

    def invaders_changed_driection(self, new_direction): pass
    def invaders_shoot(self, new_projectile): pass

        
'''Keep polling'''
def periodic_poll():
    while 1:
        poll(timeout=0.05)  # seconds
        
'''Starts a new thread that will be continually polling to receive messages'''
def start_thread():
    thread = Thread(target=periodic_poll)
    thread.daemon = True  # die when the main thread dies 
    thread.start()
    
    