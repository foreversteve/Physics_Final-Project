add_library('peasycam')
import copy
from itertools import combinations 
time = 0    
# G = .015
G = 0.015 
speed = 1
density = .1
set_up = False
menu_State = 0

global map_num, font, player,img, fuel_radius, world, player_force, points, fuel, launch_pad, theta, paused, start_p, end_p, end_message #start means the starting planet

def randomDis():
    return PVector(float(random(world) - world/2), float(random(world) - world/2), float(random(world) - world/2))
     
def randomVel():
    return PVector(float(random(speed)), float(random(speed)), float(random(speed)))

class Player:
    def __init__(self, mass, dis, vel):
        self.mass = mass
        self.dis = dis
        self.vel = vel
        self.acc = PVector(0.0, 0.0)
        self.look = [random(255), random(255), random(255)]
        self.radius = ((mass*3.0/(density*4.0*PI)) ** (1. / 3))
        self.past = [None] * 200
        self.input_acc = PVector(0.0,0.0)
        self.fuelage = mass


    def make(self):
        pushMatrix()
        noStroke()
        fill(color(self.look[0], self.look[1], self.look[2]))
        translate(self.dis.x, self.dis.y)
        circle(0,0,self.radius)
        popMatrix()
    def set_acc(self):
        for i in points:
            if i != self:
                t = PVector(i.dis.x - self.dis.x, i.dis.y - self.dis.y)
                r = t.mag()
                if r != 0:
                    t = t.div(r) #normal of currect force vector
                    t.mult(i.mass); t.mult(G); t.div(r); t.div(r) # a = GM/x^2
                    self.acc.add(t)
    def update(self):
        self.acc.add(self.input_acc)
        self.vel.add(self.acc)
        self.dis.add(self.vel)
        self.boundary_collision()
        if time % 5 == 0:
            self.past.pop(0)
            self.past.append(self.dis.copy())
        self.acc = PVector(0.0, 0.0)
        self.input_acc = PVector(0.0,0.0)
        #update radius
        self.radius = ((self.mass*3.0/(density*4.0*PI)) ** (1. / 3))
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
    def boundary_collision(self):
        if self.dis.x > width-(self.radius):
            self.dis.x = width-(self.radius)
            self.vel.x *= -0.1
        elif self.dis.x < self.radius:
            self.dis.x = (self.radius)
            self.vel.x *= -0.1
        if self.dis.y > height-(self.radius):
            self.dis.y = height-(self.radius)
            self.vel.y *= -0.1
        elif self.dis.y < self.radius:
            self.dis.y = (self.radius)
            self.vel.y *= -0.1
    def display_vectors(self):
        # print(self.vel.x)
        # print(self.vel.y)
        stroke(255,255.0)
        line(self.dis.x,self.dis.y,self.dis.x+(self.vel.x)*20,self.dis.y+(self.vel.y)*20)#to be scaled by some constant
        # draw the arrows
        # pushMatrix()
        # noStroke()
        # translate(self.dis.x, self.dis.y)
        # circle(0,0,self.radius)
        # popMatrix()
    def draww(self):
        # print('\n\n')
        global paused
        if not paused:
            self.update()
        self.make()
        self.display_vectors()
        # self.curvy()
class PointMass:
    def __init__(self, mass, dis, vel): #perhaps add density
        self.mass = mass
        self.dis = dis
        self.vel = vel
        self.acc = PVector(0.0, 0.0)
        self.look = [random(255), random(255), random(255)]
        self.radius = (mass*3.0/(density*4.0*PI)) ** (1. / 3)
        self.past = [None] * 200
        self.fixed = False
    def set_acc(self):
        if self.fixed:
            return
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
            if vel_copy.mag() > 10:
                global end_message
                end_message = "Crashed with velocity:"+str(int(vel_copy.mag()*10)/10.)
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
        global launch_pad
        pushMatrix()
        noStroke()
        translate(self.dis.x, self.dis.y)
        fill(255,255,0)
        rotate(theta)
        # circle(launch_pad.x,launch_pad.y,10)
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


def destroy(fuel, s):
    for i in fuel:
        if i.mass == s.mass and i.dis == s.dis and i.vel == s.vel:
            fuel.remove(i)    

# def create_chaos():
#     points.add(PointMass(40+random(500), randomDis(), randomVel()))
#     while len(points) < num_points:
#         new = PointMass(40+random(500), randomDis(), randomVel())
#         include = True
#         for i in points:
#             if i.dis.x == new.dis.x and i.dis.y == new.dis.y and i.dis.z == new.dis.z:
#                 include = False
#         if include:
#             points.add(new)

def create_orbit():
    m1, m2, x1, v = 100.0, 9000.0, PVector(0.0,0.0,0.0), 5.0
    points.add(PointMass(m1, PVector(x1.x+100, x1.y, x1.z), PVector(0.0, 3.9, 0.0)))
    points.add(PointMass(m2, PVector(x1.x+50, x1.y, x1.z), PVector(0.0, 0.9, 0.0)))
    points.add(PointMass(m2, PVector(x1.x-150, x1.y, x1.z), PVector(0.0, -1.1, 0.0)))

# Map1
def intital_setup0():
    m1, m2, x1, v = 50000.0, 400000.0, PVector(0.0,0.0,0.0), 5.0
    # points.add(PointMass(m1, PVector(x1.x+700, x1.y+700), PVector(0.0, 1.5)))
    global font,player,img, fuel_radius, world, player_force, points, fuel, theta, paused, launch_pad, start_p, end_p
    
    points = set()
    fuel = set()
    
    start_p = PointMass(m2, PVector(x1.x+width*4/5, x1.y+height/2), PVector(0.0, 3))
    start_p.radius = 200
    start_p.look = [255,47,0]
    points.add(start_p)
    end_p = PointMass(m2, PVector(x1.x+width/5, x1.y+height/2), PVector(0.0, -3))
    end_p.radius = 200
    end_p.look = [0,128,255]
    points.add(end_p)
    
    player = Player(100000,PVector(x1.x+width/5*4+start_p.radius/2, x1.y+height/2), PVector(0.0, 0.1))
    player_force = 200000
    
    # img = loadImage("nebula.jpg") #need to add image
    
    fuel_radius = 10
    world = 3000
    launch_pad = PVector(0,end_p.radius/2)
    theta = 0
    # font = loadFont("CourierNewPSMT-48.vlw")
    paused = True
    
#Map2
def initial_setup1():
    m1, m2, x1, v = 50000.0, 400000.0, PVector(0.0,0.0,0.0), 5.0
    # points.add(PointMass(m1, PVector(x1.x+700, x1.y+700), PVector(0.0, 1.5)))
    global font,player,img, fuel_radius, world, player_force, points, fuel, theta, paused, launch_pad, start_p, end_p
    
    points = set()
    fuel = set()
    
    start_p = PointMass(m2, PVector(width/4,height/2), PVector(0, 6))
    start_p.radius = 200
    start_p.look = [0,153,153]
    points.add(start_p)
    end_p = PointMass(m2, PVector(width/4*3, height/2), PVector(0, -6))
    end_p.radius = 200
    end_p.look = [102,0,204]
    points.add(end_p)
    
    third_p = PointMass(m2, PVector(width/2, height/2), PVector(0, 0))
    third_p.look = [0,102,204]
    third_p.fixed = True
    points.add(third_p)
    
    player = Player(100000,PVector(width/4+start_p.radius/2, height/4), PVector(0.0, 0.1))
    player_force = 200000
    
    # img = loadImage("nebula.jpg") #need to add image
    
    fuel_radius = 10
    world = 3000
    launch_pad = PVector(0,end_p.radius/2)
    theta = 0
    # font = loadFont("CourierNewPSMT-48.vlw")
    paused = True

def keyPressed():
    global player,fuel, fuel_radius, player_force,menu_State
    if menu_State == 0:
        return
    acc = player_force / player.mass
    acc1 = player_force / 10000 / 5
    if player.mass < 1005:
        print("No fuel left")
        return
    if ((key == 'W') or (key == 'w')):
        player.input_acc.add(PVector(0.0,-1.0 * acc))
        # Assume the fuel is accelerated for 1s in the rocket
        f= PointMass(1000, PVector(player.dis.x, player.dis.y+player.radius+fuel_radius), PVector(0.0, -1.0 * acc1))
        f.look = [255,255,0]
        fuel.add(f)
        player.mass -= 1000
    if ((key == 'S') or (key == 's')):
        player.input_acc.add(PVector(0.0,acc))
        f= PointMass(1000, PVector(player.dis.x, player.dis.y-player.radius-fuel_radius), PVector(0.0, -1.0 * acc1))
        f.look = [255,255,0]
        fuel.add(f)
        player.mass -= 1000
    if ((key == 'D') or (key == 'd')):
        player.input_acc.add(PVector(acc,0.0))
        f= PointMass(1000, PVector(player.dis.x-player.radius-fuel_radius, player.dis.y), PVector(acc1, 0.0))
        f.look = [255,255,0]
        fuel.add(f)
        player.mass -= 1000
    if ((key == 'A') or (key == 'a')):
        player.input_acc.add(PVector(-1.0 * acc,0.0))
        f= PointMass(1000, PVector(player.dis.x+player.radius+fuel_radius, player.dis.y), PVector(-1.0 * acc1, 0.0))

        f.look = [255,255,0]
        fuel.add(f)
        player.mass -= 1000

def mouseClicked():
    # Swtiches between inital_menu, game_menu, and end_menu
    global paused,set_up,menu_State,points, map_num, time
    if menu_State == 0:
        # Reset to initial conditions for actual game
        if mouseX < width/2+100 and mouseX > width/2-40:
            to_nextMenu = False
            if mouseY < height/2+100 and mouseY > height/2+60:
                to_nextMenu = True
                map_num = 0
            if mouseY < height/2+200 and mouseY > height/2+160:
                to_nextMenu = True
                map_num = 1
            if to_nextMenu:
                points = set()
                set_up = False
                paused = True
                time = 0
                menu_State = 1
            return
    elif menu_State == 1:
        if mouseX < 250:
            if mouseY < 140 and mouseY > 70:
                paused = not paused
            elif mouseY < 200:
                set_up = False
                time = 0
                paused = True
    elif menu_State == 2:
        if mouseX < width/2+100 and mouseX > width/2-200:
            if mouseY < height/2+100 and mouseY > height/2+60:
                menu_State = 1
                paused = True
                time = 0
                set_up = False
            if mouseY < height/2+200 and mouseY > height/2+160:
                menu_State = 0
                time = 0
                set_up = False


def display_values():
    global player,font,end_p
    textFont(font,48)
    # textFont("Courier New");
    fill(255,125,0)
    # stroke(255)
    # line(50,70,250,70)
    # line(50,120,250,120)
    # line(50,160,250,160)
    # line(50,200,250,200)
    text("Start/Pause",50,100)
    text("Restart",50,200)
    temp = PVector(int(player.vel.x*10)/10.,int(player.vel.y*10)/10.)
    temp2 = PVector(int(end_p.vel.x*10)/10.,int(end_p.vel.y*10)/10.)
    textFont(font,24)
    text("Player Velocity: " + str(temp),width/10*7,height/10)
    text("End Planet Velocity: "+ str(temp2), width/10*7,height/20*3)
    fill(0,128,255)
    text("Time Remaining: " + str(4000-time),width/10-100,height/10*9)

def check_win():
    global launch_pad, player, end_p, end_message
    end_cor = end_p.dis.copy()
    end_cor.add(launch_pad)

    end_cor.sub(player.dis)
    # fill(255)
    # text(str(int(end_cor.mag()*10)/10.),width-200,height/2)
    if end_cor.mag() < 30:
        pv = player.vel.copy()
        plv = end_p.vel.copy()
        if pv.dot(plv)/(plv.mag()) < 0.8:
            return 1
        else:
            end_message = "DEFEAT: CRASHED TOO HARD"
            return 0
    if time > 4000:
        end_message = "DEFEAT: ran out of time"
        return 0
    return 15
def draw_menu():
    global font
    font = loadFont("CourierNewPSMT-48.vlw")
    fill(255)
    textFont(font,100)
    textAlign(CENTER)
    text("Solar",width/2,height/2)
    textFont(font,48)
    text("Map 1", width/2, height/2+100)
    text("Map 2", width/2, height/2+200)
    textAlign(LEFT)
    
    stroke(255)

def setup_menu():
    global points,paused
    points = set()
    
    m1, m2, x1, v = 50000.0, 400000.0, PVector(0.0,0.0,0.0), 5.0
    start_p = PointMass(m2, PVector(x1.x+width*4/5, x1.y+height/2), PVector(0.0, 3))
    start_p.radius = 200
    start_p.look = [255,47,0]
    points.add(start_p)
    end_p = PointMass(m2, PVector(x1.x+width/5, x1.y+height/2), PVector(0.0, -3))
    end_p.radius = 200
    end_p.look = [0,128,255]
    points.add(end_p)
    
    paused = False
def draw_endMenu():
    global end_message, font
    fill(255)
    textFont(font,48)
    textAlign(CENTER);
    text(end_message, width/2, height/2)
    textFont(font,32)
    text("Restart",width/2, height/2+100)
    text("Main Menu", width/2, height/2+200)
    textAlign(LEFT);
def setup():
    # fullScreen(P2D)
    size(2048,1400)
    # size(2454,1853)
    # frameRate(30)
    # create_chaos()
    
def draw():
    global end_message, map_num,menu_State,time,points,player,start_p,end_p,img,paused,theta,launch_pad,set_up
    background(0)
    lights()
    if menu_State == 0:
        if not set_up:
            print("set_up")
            setup_menu()
            set_up = True
        
        # time += 1
        draw_menu()
        for k in range(7):
            for i in points:
                # i.boundary_collision()
                i.set_acc()
        for i in points:
            i.draww()
        
    if menu_State == 1:
        if not set_up:
            if map_num == 0:
                intital_setup0()
            else:
                initial_setup1()
            set_up = True
        end_p.draw_launchpad(theta)
        display_values()
        if not paused:
            time += 1
            launch_pad.rotate(theta)
            theta += 0.05
            theta = theta%360
            win = check_win()
            if win == 1:
                end_message = "VICTORY"
                menu_State = 2
                return
            if win == 0:
                menu_State = 2
                return
            for f in fuel:
                if f.check_collide() or f.collide_planet():
                    destroy(fuel,f)
                else:
                    f.set_acc()
            for k in range(7):
                for i in points:
                    # i.boundary_collision()
                    i.set_acc()
                    if i.check_collide():
                        menu_State = 2
                    

            player.set_acc()
        
        # make_fields()
        for i in points:
            i.draww()
            i.display_vectors()
        for f in fuel:
            f.draw_fuel()
        player.draww()
    if menu_State == 2:
        draw_endMenu()
