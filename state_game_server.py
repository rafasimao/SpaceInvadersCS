import pygame
from state import State
from player import Player
from invaders_manager import InvadersManager
from network_connector import NetworkListener
#from Invaders import Invaders

'''
Main game state. Might be the class where the whole game will run at.
'''
class StateGameServer(State, NetworkListener):

    players_list = list()
    #invader = Invaders(0)
    invader_manager = InvadersManager()

    def __init__(self, screen, inputManager, networkConnector):
        State.__init__(self, screen, inputManager, networkConnector)
        self.networkConnector.attach(self) #attach to the network handler
        
        self.board_bounds = pygame.Rect(0,0,screen.get_width(),screen.get_height())
        
        self.fontObj = pygame.font.Font('freesansbold.ttf', 22)
        
        
    def destroy(self):
        self.networkConnector.detach(self)
    
    
    '''Update'''
    def update(self, dt):
        if self.players_list.__len__() > 0:
            State.update(self, dt) 

            #Updates the game objects
            for player in self.players_list:
                player.update(dt)
            #self.invader.update(dt)
            self.invader_manager.update(dt)

            #treats projectiles hits        
            self._treat_invader_projectiles()
            self._treat_player_projectiles()
        
    'Make invaders projectiles collisions and perform the consequences'
    def _treat_invader_projectiles(self):
        if self.invader_manager.projectile_list.__len__() > 0: 
            #Goes through all the invaders projectiles
            for shot in self.invader_manager.projectile_list:
                #If it is out of the board game box, it is removed
                if not self._remove_if_out_of_board(self.invader_manager.projectile_list, shot):
                    #If it collides with the player, the player receives the damage and the projectile is removed
                    for player in self.players_list:
                        if shot.is_colliding_with(player):
                            #self.player.receive_hit()
                            self.invader_manager.projectile_list.remove(shot)

    'Make players projectiles collisions and perform the consequences'
    def _treat_player_projectiles(self):
        for player in self.players_list:
            if player.projectile_list.__len__() > 0: 
                #Goes through all the invaders projectiles
                for shot in player.projectile_list:
                    #If it is out of the board game box, it is removed
                    if not self._remove_if_out_of_board(player.projectile_list, shot):
                        collided = False
                        for invader in self.invader_manager.invaders_list:
                            if not collided and shot.is_colliding_with(invader):
                                player.projectile_list.remove(shot)
                                self.invader_manager.invaders_list.remove(invader)
                                player.increase_score(15)
                                #self.invader_manager.speedUp()
                                collided = True
                        
                    
    'Removes a projectile from a projectile list if it is out of the board bounds.' 
    'Returns True if it is removed and False if it is not.'
    def _remove_if_out_of_board(self, projectile_list, projectile):
        #If it is out of the board game box, it is removed
        if not self.board_bounds.colliderect(projectile.get_collision_box()):
            projectile_list.remove(projectile)
            return True
        
        return False

    
    '''Render'''
    def render(self):
        State.render(self) 
        #background
        self.screen.fill(pygame.Color(0,0,0))
        
        #render objects
        for player in self.players_list:
            player.render(self.screen)
        self.invader_manager.render(self.screen)
        
    
    def player_joined(self, player_id, topleft):
        NetworkListener.player_joined(self, player_id, topleft)
        
        print "player_joined: "+str(player_id)+" - "+str(topleft)
        
        player = Player()
        self.players_list.append(player)
        if player_id == -1:
            player.player_id = self.players_list.__len__()
            print str(player.player_id)
            #self.networkHandler.do_send()

