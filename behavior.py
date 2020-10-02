from spark_agent import SparkAgent

class Offense:
    def __init__(self, agent):
        self.agent = agent
        self.passReceiver= None

    
    def passTheBall(self):
        '''
        Passes the Ball to the player stored in passReceiver
        '''
        self.agent.action = "pass"
    
    def getOpen(self):
        self.agent.action = "get open"
    
    def stayBehind(self):
        self.agent.action = "stay behind"
    
    def dribble(self):
        self.agent.action = "dribble"

    def shoot(self):
        self.agent.action = "shoot"
    
class Defense:
    def __init__(self, agent):
        self.agent = agent
      
    def protectTheGoal(self):
        self.agent.action = "protect goal"
    
    def coverPlayers(self):
        '''
        The Player should try to step most efficiently into the paths possible passes
        could take. The Player also tries not to cluster to much with other teammates
        '''
        self.agent.action = "cover players"

    def stayInFront(self):
        '''
        The player only goes as far as the center line when playing defense, so its
        ready to strike fastly after the opponents turned the ball over.
        '''
        self.agent.action = "stay in front"

    def attackBall(self):
        '''
        The Player goes towards the ball and tries to steal it from the opponent.
        '''
        self.agent.action = "attack ball"


class Observer:
    def __init__(self, agent):
        self.defense = Defense(agent)
        self.offense = Offense(agent)
        
        
        '''
        playingOffense describes the state in which the player is
        if the team is not in possession of the ball the 
        player has to play defense so playingOffense will be False
        '''
        self.playingOffense = False
        
    def ballPossession(self, perception):
        '''
        test which team is in possession of the ball and 
        switch between offense and defense with adjusting
        self.playingOffense 
        possession means that the ball is in the radius of
        a player where the player can control it
        '''
        pass
    
    def amIGoalie(self, perception):
        '''
        test if the player is closest to his own goal
        if yes the player is goalkeeper return True.
        '''
        pass
    
    def amIDefender(self, perception):
        '''
        if the player is the second closest to his own goal
        It is call the defender. 
        '''
        pass
    
    def hasBall(self, perception):
        '''
        if a player is in possession of the ball return True.
        else False
        '''
        pass
        
    def teammateIsOpen(self, perception):
        '''
        test if a teammate closer to the oponents goal is open. If yes 
        store a Pointer to the teamate in self.offense.passReceiver 
        and return True.
        If not set self.offense.passReceiver to None and return False
        '''
        pass

    def goalOpen(self, perception):
        '''
        return True if the player could shoot at an open goal.
        Also test if the player is close enough to the goal.
        Else return False.
        '''
        

    
    
    def think(self, perception):
        self.ballPossession(perception)
        
        #### Offense ####
        if self.playingOffense:
            
            
            ## Player is Goalkeeper ##
            ''' 
            The Goalkeeper is the player thats closest to his own goal.
            He is supposed to stay behind and protect the goal if 
            doesn't have the ball, and ih he does, he should pass or 
            dribble if noone is open 
            '''
            if self.amIGoalie(perception):
                if self.hasBall(perception):
                    # start attack or pass the ball
                    if self.teammateIsOpen(perception):
                        self.offense.passTheBall()
                    if not self.teammateIsOpen(perception):
                        self.offense.dribble()
                else:
                    # protect goal
                    self.defense.protectTheGoal()


            ## Player is Defender ##
            '''
            There is only one Defender in our Scenario. He is the second 
            closest Person to his own goal. He behaves simliar to the 
            goalkeeper except that he is only supposed to stay behind 
            and not in the goal.
            '''
            elif self.amIDefender(perception):
                if self.hasBall():
                    # start attack or pass the ball
                    if self.teammateIsOpen(perception):
                        self.offense.passTheBall()
                    else:
                        self.offense.dribble()
                else:
                    self.offense.stayBehind()
             
             
            ## Player is neither Goalie nor Defender ##
            '''
            All other Players try to attack the opponents goal. They 
            shoot if the goal is free, pass ahead to an open teammate
            or dribble towards the goal.
            '''
            else:
                if self.hasBall(perception):
                    if self.goalOpen(perception):
                        self.offense.shoot()
                    elif self.teammateIsOpen(perception):
                            self.offense.passTheBall()
                    else:
                        self.offense.dribble()
                else:
                    self.offense.getOpen()    

        #### Denfense ####
        else:
            if self.amIGoalie(perception):
                self.defense.protectTheGoal()
            elif self.amIAttacker(perception):
                self.defense.stayInFront()
            elif self.closestToBall(perception):
                self.defense.attackBall()
            else:
                self.defense.coverPlayers()


class BehaviorAgent(SparkAgent):
    def __init__ (self):
        super(SparkAgent, self).__init__()
        self.action = None
        self.observer = Observer(self)
        self.think = self.observer.think(self.perception)
