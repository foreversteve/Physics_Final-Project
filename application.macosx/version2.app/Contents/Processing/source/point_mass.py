class PointMass:
    def __init__(self, mass, dis, vel): #perhaps add density
        self.mass = mass
        self.dis = dis
        self.vel = vel
        self.acc = PVector(0.0, 0.0)
        self.look = [random(255), random(255), random(255)]
        self.radius = (mass*3.0/(density*4.0*PI)) ** (1. / 3)
        self.past = [None] * 200
    def set_acc(self):
        for i in points:
            if i != self:
                t = PVector(i.dis.x - self.dis.x, i.dis.y - self.dis.y)
                r = t.mag()
                if r != 0:
                    t = t.div(r) #normal of currect force vector
                    t.mult(i.mass); t.mult(G); t.div(r); t.div(r) # a = GM/x^2
                    self.acc.add(t)
    def collide_planet(self):
        global points
        for planet in points:
            cp = planet.dis.copy()
            # print(cp)
            # print(self.dis)
            # print(planet.radius)
            # print()
            dif = cp.dist(self.dis)
            if dif < self.radius+planet.radius/2:
                # print("reached here")
                return True
        return False
        
    def check_collide(self):
        global player,fuel

        cp = player.dis.copy()
        dif = cp.dist(self.dis)
        #vector math
        if dif < self.radius/3*2:
            if self in fuel:
                return True
            vel_copy = copy.deepcopy(player.vel)
            if self.dis.y != player.dis.y:
                tangent = PVector(1,(player.dis.x - self.dis.x) / (self.dis.y - player.dis.y))
                tangent.normalize()
            else:
                tangent = PVector(0,1)
            factor = tangent.dot(player.vel)
            
            proj_v = tangent.mult(factor)
            vel_copy.sub(proj_v)
            if vel_copy.mag() > 11:
                print("Crashed with velocity:"+str(vel_copy.mag()))
                return True
            vel_copy.mult(2)
            player.vel.sub(vel_copy)
            player.vel.mult(0.4) #make the collision inelastic
            temp = copy.deepcopy(self.vel)
            val = temp.dot(player.vel)/player.vel.mag()
            # if val < -0.8:
            #     player.vel = PVector(0,0)
            #     player.vel.add(temp/4*3)
        
        return False
    def update(self):
        # self.boundary_collision()
        self.vel.add(self.acc)
        self.dis.add(self.vel)
        if time % 5 == 0:
            self.past.pop(0)
            self.past.append(self.dis.copy())
        self.acc = PVector(0.0, 0.0)
    def make(self):
        pushMatrix()
        noStroke()
        fill(color(self.look[0], self.look[1], self.look[2]))
        translate(self.dis.x, self.dis.y)
        circle(0,0,self.radius)
        popMatrix()
    def curvy(self):
        c = self.look
        dc = [self.look[0]/200, self.look[1]/200, self.look[2]/200]
        for i in range(199,1,-1):
            a = self.past[i]
            b = self.past[i-1]
            if a != None and b != None:
                nc = color(c[0]-(199-i)*dc[0], c[1]-(199-i)*dc[1], c[2]-(199-i)*dc[2])
                stroke(nc)
                line(a.x, a.y, b.x, b.y)
    def draw_fuel(self):
        global fuel_radius
        if not paused:
            self.update()
        fill(color(self.look[0], self.look[1], self.look[2]))
        circle(self.dis.x,self.dis.y,fuel_radius)
        
    def draw_launchpad(self,theta):
        pushMatrix()
        noStroke()
        translate(self.dis.x, self.dis.y)
        fill(255,255,0)
        rotate(theta)
        rect(-self.radius/5,self.radius/2,self.radius/5*2,2)
        popMatrix()
    def draww(self):
        # print('\n\n')
        global paused
        if not paused:
            self.update()
        self.make()
        self.curvy()
    def equal(self, other):
        if self.dis == other.dis and self.vel == other.vel and self.acc == other.vel and self.mass == other.mass:
            return True
        return False
    def display_vectors(self):
        stroke(255,255.0)
        line(self.dis.x,self.dis.y,self.dis.x+(self.vel.x)*20,self.dis.y+(self.vel.y)*20)#to be scaled by some constant
