import Tkinter as tk
import random
import math
import time
from PIL import Image, ImageTk

Ball_group=set()
L=[]
ball_num = 0
for i in range(0,11):
    if i%2==0:
        L.append([0 for i in range(8) ])
    else:
        L.append([0 for i in range(7) ])
        
red=[]
blue=[]
yellow=[]
L[0] = [1,1,1,1,1,1,1,1]


root = tk.Tk()
c = tk.Canvas(width=400, height=650)
c.pack()
w = c.create_text(230,600, anchor = "nw",text="You've launched %d ball" % ball_num, activefill = 'red')
image = Image.open("title.gif")
image = image.resize((250, 70), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image)
panel = tk.Label(root, image = img)
panel.pack(side = 'bottom')

class Ball:
    def __init__(self,master,pos_x,pos_y,color):
        self.master = master
        self.shape = c.create_oval(pos_x,pos_y, pos_x+50, pos_y+50, fill = color)
        self.active = True
        self.speedx = 0
        self.speedy = 0
        self.pos = c.coords(self.shape)
        self.inL=[-1,-1]
        self.color=color
        self.child=set()
        self.parent=set()
        self.childf=set()
        self.parentf=set()
    def ball_update(self):
        c.move(self.shape, self.speedx, self.speedy)
        self.pos = c.coords(self.shape)
        if self.pos[2] >= 400 or self.pos[0] <= 0:
            self.speedx *= -1
        if self.pos[1]<=0:
            self.speedx=0
            self.speedy=0
            c.coords(self.shape,int(self.pos[0]/50)*50,0,int(self.pos[0]/50)*50+50,50)
            self.pos[0]=int(self.pos[0]/50)*50
            self.pos[1]=0
            self.pos[2]=int(self.pos[0]/50)*50+50
            self.pos[3]=50
      
            
            y=int(self.pos[0]/50) 
            
            L[0][y]=1
            self.inL[0]=0
            self.inL[1]=y
            self.active =False
        

        for other_ball in Ball_group.difference({self}):
            collide(self,other_ball)

        if self.active == False:
            global w
            c.delete(w)
            global ball_num
            ball_num = ball_num+1
            w = c.create_text(250,600, anchor = "nw",text="You've launched %d ball" % ball_num)
            time.sleep(.05)
            input=set()
            input.add(self)
            same_color(input)
            killing(self)
            for ball in Ball_group:
                if len(ball.parentf)==0:
                    input=set()
                    input.add(ball)
                    falling_group(input)
                    falling(ball)
            for ball in Ball_group:
                ball.parentf=set()
                ball.childf=set()
            if len(Ball_group) == 0:
                w = c.create_text(200,250, text="You won! But keep playing if you like", font = ('Helvetica',20), fill = 'green')

                    
                    

      
    def move_active(self):
        if self.active:
            self.ball_update()
            self.master.after(10,self.move_active)
    def shoot(self,event):
        self.speedx = (c.coords(arrow_item)[0]-200)/8
        self.speedy = (c.coords(arrow_item)[1]-675)/8
        self.move_active()

xy = [(200, 550), (200, 625)]
arrow_item = c.create_line(xy,arrow=tk.FIRST)
center = 200, 625








def same_color(these_balls): #these_balls: a set contains balls in a generation
    
    for this_ball in these_balls:
        for other_ball in Ball_group.difference({this_ball}):
            if dist(this_ball.pos, other_ball.pos) <= 57 and this_ball.color == other_ball.color:
                    #two balls are in a cluster if they have the same color and the the distance between them is less than 57
                if len(other_ball.parent.intersection(this_ball.parent))==0 and other_ball not in this_ball.parent:
                    #If "other_ball" is neither "this_ball"'s parent nor in the same generation with "this_ball", "this_ball" is "other_ball"'s parent
                        other_ball.parent.add(this_ball)
                        this_ball.child.add(other_ball)
    
                       
    next_group=set()#A set containing all "children" of the previous generation
    for this_ball in these_balls:
        if len(this_ball.child)!=0:
            for a_child in this_ball.child:
                next_group.add(a_child)
    
    
    if len(next_group)==0:
        return#If this genration does not have any child, the recursion is terminated
    else:
        same_color(next_group)#If this generation has "childrren", same_color() is called again to find the next generation. 
        
        
def falling_group(these_balls):#"these_ball": a set contains balls in a generation
       
       for this_ball in these_balls:
           for other_ball in Ball_group.difference({this_ball}):
               if dist(this_ball.pos, other_ball.pos) <= 57 :
                 #Two balls are in a cluster if  the distance between them is less than 57
                   if len(other_ball.parentf.intersection(this_ball.parentf))==0 and other_ball not in this_ball.parentf:
                        #If "other_ball" is neither "this_ball"'s parent nor in the same generation with "this_ball", "this_ball" is "other_ball"'s parent
                       other_ball.parentf.add(this_ball)
                       this_ball.childf.add(other_ball)
       next_group=set()#A set containing all "children" of the previous generation
       for this_ball in these_balls:
           if len(this_ball.childf)!=0:
               for a_child in this_ball.childf:
                   next_group.add(a_child)
       if len(next_group)==0:
            return#If this genration does not have any child, the recursion is terminated 
       else:
           
            falling_group(next_group)#If this generation has "children", falling_group() is called again to find the next generation.
            
       
def falling(this_ball):#this_ball: the ball shot(the "root" ball) by the user
    falling_balls=set() #A set contains balls in a cluster 
    if this_ball.inL[0]==0:
         connect_top=True#If the "root" ball is in the first row, this cluster touches the top, then this cluster should not fall 
    else:
        connect_top=False
        falling_balls.add(this_ball)#if the "root" ball is not in the first row, we assume this cluster does not touch the top and initialize  "connect_top" as false
    pre_group=set() # A group contains all balls in a generation
    pre_group.add(this_ball)
    while len(pre_group)>0 and connect_top==False:
                next_group=set()
                for ball in pre_group:
                    for a_child in ball.childf:
                        next_group.add(a_child)
                for ball in next_group:
                    falling_balls.add(ball)
                    if ball.inL[0]==0:
                        connect_top=True
                pre_group=next_group
    

    if connect_top==False: #If this is no ball touching the top of the canvas, this cluster should fall
       
        for ball in falling_balls:
            ball.speedy=5
            ball.active=True
            ball.move_active() 
   
    

def killing(this_ball):
     pre_group=set()#a set containing all balls in the same generation
     pre_group.add(this_ball)
     kill_group=set()#a set containing all balls in a  cluster
     kill_group.add(this_ball)
     while len(pre_group)>0:
                next_group=set()
                for ball in pre_group:
                    for a_child in ball.child:
                        next_group.add(a_child)
                for ball in next_group:
                    kill_group.add(ball)
                pre_group=next_group
                    
     if len(kill_group)>=3:#If there are more than 3 balls sticks together, we kill these balls
        for ball in kill_group:
            c.delete(ball.shape)
            Ball_group.discard(ball)



def getangle(event):
    dx = c.canvasx(event.x) - center[0]
    dy = c.canvasy(event.y) - center[1]
    try:
        return complex(dx, dy) / abs(complex(dx, dy))
    except ZeroDivisionError:
        return 0.0 # cannot determine angle
def press(event):
    # calculate angle at start point
    global start
    start = getangle(event)
def motion(event):
    # calculate current angle relative to initial angle
    global start
    angle = getangle(event) / start
    offset = complex(center[0], center[1])
    newxy = []
    for x, y in xy:
        v = angle * (complex(x, y) - offset) + offset
        newxy.append(v.real)
        newxy.append(v.imag)
    if newxy[1]>587.5:
        if newxy[0]<200-75*math.cos(math.pi/6):
            newxy[0] = math.cos(5*math.pi/6)*75+200
            newxy[1] = 625-math.sin(5*math.pi/6)*75
            c.coords(arrow_item,newxy[0],newxy[1],center[0],center[1])
        else:
            newxy[0] = math.cos(math.pi/6)*75+200
            newxy[1] = 625-math.sin(math.pi/6)*75
            c.coords(arrow_item,newxy[0],newxy[1],center[0],center[1])
    c.coords(arrow_item,newxy[0],newxy[1],center[0],center[1])

def create_circle():
    color=['red','blue','yellow']
    next_color=random.randint(0,2)
    ball = Ball(master=root,pos_x=175,pos_y=600,color=color[next_color])
    c.bind("<ButtonRelease-1>",ball.shoot)
    Ball_group.add(ball)
    return ball
def create_original_circle(i,j):
    if i%2 == 0:
        color=['red','blue','yellow']
        next_color=random.randint(0,2)
        ball_original = Ball(master=root,pos_x=j*50,pos_y=i*50,color=color[next_color])
        
    else:
        color=['red','blue','yellow']
        next_color=random.randint(0,2)
        ball_original = Ball(master=root,pos_x=j*50+25,pos_y=i*50,color=color[next_color])
    ball_original.inL[0]=i
    ball_original.inL[1]=j
    Ball_group.add(ball_original)
    L[i][j]=1
 
    return ball_original

def collide(a_object, other_object): #a_object: a ball shot by the user; 
                                     #other_object: the ball that is collided by the ball shot
                                     
    #determine whether two balls collide
    if dist(a_object.pos, other_object.pos)<50: 
        a_object.speedx=0 #as long as a_object collides other_object, a_object stops
        a_object.speedy=0
        
        
    #move a_object to the nearest appropriate posiotion
        if a_object.pos[0]<other_object.pos[0]: #If a_object collides a_object from the left
            if other_object.inL[1]==0: #If other_object is the first ball in its row from the left
                c.coords(a_object.shape,other_object.pos[0]-25,other_object.pos[1]+50,other_object.pos[0]+25,other_object.pos[1]+100)
                a_object.pos[0]=other_object.pos[0]-25#move a_object to the first position in the row that is below the other_object
                a_object.pos[1]=other_object.pos[1]+50
                a_object.pos[2]=other_object.pos[0]+25
                a_object.pos[3]=other_object.pos[1]+100
            else:
                if L[other_object.inL[0]][other_object.inL[1]-1]==0:#if the position on the left of other_object is empty
                    c.coords(a_object.shape,other_object.pos[0]-50,other_object.pos[1],other_object.pos[0],other_object.pos[1]+50)
                    a_object.pos[0]=other_object.pos[0]-50#move a_object to the position on the left of other_object
                    a_object.pos[1]=other_object.pos[1]+1
                    a_object.pos[2]=other_object.pos[0]+0
                    a_object.pos[3]=other_object.pos[1]+50
                else: #Since the left position is occupied, we move a_object to the left but below other_object
                    c.coords(a_object.shape,other_object.pos[0]-25,other_object.pos[1]+50,other_object.pos[0]+25,other_object.pos[1]+100)
                    a_object.pos[0]=other_object.pos[0]-25
                    a_object.pos[1]=other_object.pos[1]+50
                    a_object.pos[2]=other_object.pos[0]+25
                    a_object.pos[3]=other_object.pos[1]+100
       
        else: #If a_object collides other_object from the right
            if other_object.inL[1]==6 and other_object.inL[0]%2==1: #If the ball collided is the last ball in its row and the row number odd
                c.coords(a_object.shape,other_object.pos[0]+25,other_object.pos[1]+50,other_object.pos[0]+75,other_object.pos[1]+100)
                a_object.pos[0]=other_object.pos[0]+25#move a_object to the last position of the row that is below other_object
                a_object.pos[1]=other_object.pos[1]+50
                a_object.pos[2]=other_object.pos[0]+75
                a_object.pos[3]=other_object.pos[1]+100
            else:
                if L[other_object.inL[0]][other_object.inL[1]+1]==0:#if the position on the right of other_object is empty
                    c.coords(a_object.shape,other_object.pos[0]+50,other_object.pos[1],other_object.pos[0]+100,other_object.pos[1]+50)
                    a_object.pos[0]=other_object.pos[0]+50 #move a_object to the position on the right of the ball collided
                    a_object.pos[1]=other_object.pos[1]
                    a_object.pos[2]=other_object.pos[0]+100
                    a_object.pos[3]=other_object.pos[1]+50
                else:#Since the right position is occupied, we move a_object to the right but below other_object
                    c.coords(a_object.shape,other_object.pos[0]+25,other_object.pos[1]+50,other_object.pos[0]+75,other_object.pos[1]+100)
                    a_object.pos[0]=other_object.pos[0]+25
                    a_object.pos[1]=other_object.pos[1]+50
                    a_object.pos[2]=other_object.pos[0]+75
                    a_object.pos[3]=other_object.pos[1]+100
        
        #stop updating a_object
        a_object.active =False 
        
        #record the final position of a_object
        y=int(a_object.pos[1]/50)
        if y%2==0:
            x=int(a_object.pos[0]/50)
        else:
            x=int((a_object.pos[0]-25)/50)
        L[y][x]=1
        a_object.inL[0]=y
        a_object.inL[1]=x


    
def dist(p, q):
    return math.sqrt((0.5*(p[0]+p[2]) - 0.5*(q[0]+q[2])) ** 2 + (0.5*(p[1]+p[3]) - 0.5*(q[1]+q[3])) ** 2)    

c.bind("<Button-1>", press)
c.bind("<B1-Motion>", motion)
buttonimage = Image.open("button.gif")
buttonimage = buttonimage.resize((60, 60), Image.ANTIALIAS)
buttonimg = ImageTk.PhotoImage(buttonimage)
b = tk.Button(root,command=create_circle, height = 70, width = 60)
b.config(image = buttonimg)
b.pack()
for i in range(10):
    for j in range(len(L[i])):
        if L[i][j] == 1:
            create_original_circle(i,j)

root.mainloop()
