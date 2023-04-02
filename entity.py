class entity():
    def init(self):
        self.name = "Duckie"
        self.health = 100
        self.moral = 100
        self.level=1
        self.points=0
        self.isAlive = True
    
    def receive(self, moral_income, health_income):
        self.health=self.health-health_income
        self.moral=self.moral-moral_income
    
    def level_up(self, points):
        if points >= self.level*10:
            self.points = points=self.level*10
            self.level=self.level+1