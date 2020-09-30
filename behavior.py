class Offense:
    def __init__(self, agent):
        self.agent = agent
    
    def passTheBall(self):
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
        Passwege zustellen: Bewege dich zum Ball(die Richtung die Ballfüher hat) halte aber Mindestabstand zu deinen Mitspielern
        '''
        self.agent.action = "cover players"

    def stayInFront(self):
        '''
        Spieler läuft maximal bis Mittellinie zurück
        '''
        self.agent.action = "stay in front"

    def attackBall(self):
        self.agent.action = "attack ball"


class Observer:
    def __init__(self, agent):
        self.defense = Defense(agent)
        self.offense = Offense(agent)
        
        '''
        playingOffense describes the state in which the agent is
        if the team is not in possession of the ball the 
        agent has to play defense so playingOffense is False
        '''
        self.playingOffense = False
        
    def ballPossession(self):
        '''
        test which team is in possession of the ball and 
        switch between offense and defense with adjusting
        self.playingOffense 
        possession means that the ball is in the radius of
        a player where the player can control it
        '''
        pass
    
    def amIGoalie(self):
        '''
        test if the agent is closest to its own goal
        if yes the agent is goalkeeper return True
        '''
        pass
    
    def amIDefender(self):
        '''
        if the agent is the second closest to its own goal
        It is call the defender
        '''
        pass
    
    def hasBall(self):
        '''
        if player is in possession of the ball return True.
        else False
        '''
        pass
    
    
    def think(self, perception):
        self.ballPossession(perception)
        if self.playingOffense:
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
            elif self.amIDefender(perception):
                if self.hasBall():
                    # start attack or pass the ball
                    if self.teammateIsOpen(perception) and openPlayerIsNotGoalie:
                        self.offense.passTheBall()
                    else:
                        self.offense.dribble()
                else:
                    self.offense.stayBehind()
            elif self.hasBall(perception):
                if goalOpen and closeToGoal:
                    self.offense.shoot()
                elif self.teammateIsOpen(perception) and teammateCloserToOponentsGoal():
                        self.offense.passTheBall()
                else:
                    self.offense.dribble()
            else:
                self.offense.getOpen()       
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