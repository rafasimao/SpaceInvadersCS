import pygame
from input_manager import InputManager
from state_game_server import StateGameServer
from server import start_server, run

#initiate the pygame
pygame.init()
fpsClock = pygame.time.Clock()
#print("initializing clock: ", fpsClock)

#Manager class
class Manager:

    ##Screen
    width, height = 950, 600
    size = width, height
    
    screen  = pygame.display.set_mode(size)

    pygame.display.set_caption("SpaceInvaders")        
    
    
    #Server
    server = start_server()
    
    #InputManager
    inputManager = InputManager()

    #Introduction state
    state = StateGameServer(screen, inputManager)
     
    #Main Loop
    def _run(self):
        self.gameOn = True
        
        while self.gameOn:
            run()
            dt = fpsClock.tick(30)

            #Inputs
            self.inputManager.update()
            
            #Updates
            self.update(dt)
                
            #Renders, put in the screen
            self.render()
        
    
    #Update
    def update(self, dt):
        #state updates
        new_state = self.state.update(dt)
        if (new_state == 0):
            return
       
    def set_state(self, state):
        self.state.destroy()
        self.state = state
    
    #Render
    def render(self):
        #state renders
        self.state.render()
        
        #updates the display
        pygame.display.update()
        
        

#Run the main loop
if "__main__" == __name__:
           
    manager = Manager()
    manager._run()