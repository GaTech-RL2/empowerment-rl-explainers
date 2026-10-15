"""Full-frame, cue-driven visual explanations. No paragraph panels.

Persistent objects change in response to the spoken experiment. Movement is a
demonstration (push, merge, reveal, compare), never a looping decoration.
All scenes are original teaching examples, not measurements from the papers.
"""
import math
from drawing import *

C=[CYAN,GOLD,PURPLE,GREEN]

def title(c,s):
    n=42
    while c.d.textlength(s,font=font(n,True))>1440:n-=1
    c.text(800,126,s,n,INK,True,'mm')

def label(c,x,y,s,color=MUTED,size=26):c.text(x,y,s,size,color,anchor='mm')

def mathline(c,items,y=777,size=42):
    if isinstance(items,str):items=[(items,INK)]
    widths=[c.d.textlength(s,font=font(size)) for s,_ in items]
    x=(1600-sum(widths))/2
    for (s,col),w in zip(items,widths):c.text(x,y,s,size,col,anchor='lm');x+=w

def dot(c,x,y,col=CYAN,r=15):
    c.circle(x,y,r+9,blend(BG,col,.11),blend(BG,col,.11),1)
    c.circle(x,y,r,col,col,2)
    c.circle(x-r*.27,y-r*.27,max(2,r*.19),INK,INK,1)

def trace(c,points,p,col=CYAN,width=5):
    end=c.path(points,ease(p),col,width);dot(c,*end,col,9);return end

def cross(c,x,y,col=RED,r=15):
    c.line([(x-r,y-r),(x+r,y+r)],col,4);c.line([(x-r,y+r),(x+r,y-r)],col,4)

def fan(c,x,y,angle=0,scale=1):
    for k in range(3):
        a=angle+k*math.tau/3
        pts=[(x,y),(x+44*scale*math.cos(a),y+44*scale*math.sin(a)),(x+24*scale*math.cos(a+.9),y+24*scale*math.sin(a+.9))]
        c.d.polygon(pts,fill=blend(BG,MUTED,.6))
    c.circle(x,y,7*scale,MUTED,INK,2)

def puck(c,cx=800,cy=380,s=1,mode='control',p=1,selected=0,hide=False,wind=0):
    X=lambda v:cx+s*v;Y=lambda v:cy+s*v
    c.d.rounded_rectangle((X(-320),Y(-100),X(320),Y(100)),radius=round(22*s),fill='#101c2a',outline=LINE,width=2)
    for i,x in enumerate([-230,230]):
        c.circle(X(x),Y(0),38*s,blend(BG,C[i],.5),None,2)
        c.line([(X(x),Y(-75)),(X(x),Y(75))],blend(BG,C[i],.2),1,True)
    for i,x in enumerate([-100,100]):
        col=C[i];active=i==selected
        c.circle(X(x),Y(180),31*s,blend(BG,col,.25) if hide else col,blend(BG,col,.25 if active and not hide else .05),3)
        if hide:label(c,X(x),Y(180),'?',MUTED,round(26*s))
        else:label(c,X(x),Y(180),'←' if i==0 else '→',col,round(30*s))
        a=(X(x),Y(141));b=(X((-230,230)[i]),Y(112))
        c.line([a,b],blend(BG,col,.28),2,True)
        if mode=='fan':cross(c,*pos(a,b,.5),r=10*s)
    if mode=='fan':
        fan(c,X(0),Y(-165),p*5,s)
        for x in [-38,0,38]:c.arrow((X(x),Y(-130)),(X(x),Y(-78)),MUTED,2)
        dest=230*(-1 if selected==0 else 1)
    else:dest=230*(-1 if selected==0 else 1)+wind*40
    posx=X(lerp(0,dest,ease(p)))
    c.line([(X(0),Y(0)),(posx,Y(0))],blend(BG,C[selected],.4),round(max(2,6*s)))
    dot(c,posx,Y(0),C[selected] if mode!='fan' else INK,22*s)

def clouds(c,separation=1,center=(800,430),scale=1,active=None,paths=False):
    for k in range(2):
        co=C[k];cx=center[0]+(-1 if k==0 else 1)*225*separation*scale;cy=center[1]
        if paths:
            for j in range(5):
                pts=[(center[0],cy+190*scale),(center[0]+(-1 if k==0 else 1)*90*scale,cy+(100+j*11)*scale),(cx+30*scale*math.sin(j),cy+(j-2)*32*scale)]
                c.line(pts,blend(BG,co,.35),2)
        for i in range(90):
            ang=i*2.39996;rr=math.sqrt(i/90)*125*scale
            x=cx+math.cos(ang)*rr;y=cy+math.sin(ang)*rr*.72
            col=blend(BG,co,.35+.5*(i%7)/6)
            c.circle(x,y,3.8*scale,col,col,1)
        c.circle(cx,cy,132*scale,blend(BG,co,.3),None,2)
        if active==k:dot(c,cx,cy,co,12*scale)

def histogram(c,values,x=800,y=620,w=540,h=300,labels=True,showvals=True,p=1):
    n=len(values);gap=w/n
    c.line([(x-w/2-15,y),(x+w/2+15,y)],LINE,2)
    for i,v in enumerate(values):
        cx=x-w/2+(i+.5)*gap;hh=max(1,v*h*ease(p))
        c.d.rounded_rectangle((cx-gap*.3,y-hh,cx+gap*.3,y),radius=5,fill=C[i%4])
        if showvals:label(c,cx,y-hh-24,f'{v:.2f}',C[i%4],25)
        if labels:dot(c,cx,y+35,C[i%4],8)

def junction(c,p=1,mode='open',cx=650,cy=430,scale=1,prepare=False):
    origin=(cx,cy);outs=[(cx+410*scale,cy-170*scale),(cx+480*scale,cy),(cx+410*scale,cy+170*scale)]
    for i,e in enumerate(outs):
        blocked=mode=='blocked' and i==1
        target=outs[0] if blocked else outs[1] if mode=='takeover' else e
        points=[origin,(cx+160*scale,cy+(target[1]-cy)*.55),target]
        c.line(points,blend(BG,C[i],.27),round(10*scale))
        if p>0:trace(c,points,p,C[i],max(2,round(4*scale)))
        c.d.rounded_rectangle((e[0]-40*scale,e[1]-35*scale,e[0]+40*scale,e[1]+35*scale),radius=9,outline=C[i],width=3)
        if blocked:c.box(cx+225*scale,cy-38*scale,74*scale,76*scale,color=RED,fill='#563c35')
    dot(c,*origin,INK,20*scale)
    if prepare:
        pts=[(cx-370*scale,cy+120*scale),(cx-180*scale,cy+120*scale),origin]
        c.line(pts,blend(BG,GOLD,.25),9);trace(c,pts,p,GOLD,5)
    return outs

def policy_loop(c,p=1,highlight=0):
    positions=[(410,350),(1190,350),(800,640)]
    names=['Choose a skill','Collect states','Learn the decoder']
    for i,(x,y) in enumerate(positions):
        col=C[i]
        c.d.rounded_rectangle((x-185,y-65,x+185,y+65),radius=18,fill=blend(BG,col,.07),outline=col if highlight==i else LINE,width=3)
        label(c,x,y,names[i],col,27)
        dest=positions[(i+1)%3]
        a=pos((x,y),dest,.26);b=pos((x,y),dest,.74)
        c.arrow(a,b,blend(BG,col,.4),4)
        if i==highlight:trace(c,[a,b],p,col,5)

def diayn(c,ch,b,u,p):
    if ch==0:
        if b<2:
            title(c,['Can you read the choice?','Same outcomes. Different cause.'][b])
            puck(c,cy=430,s=1.35,mode='control' if b==0 else 'fan',p=1 if b==0 and u else min(1,p*1.6),selected=u if b==1 else 0,hide=u==1 and b==0)
            if u==1:mathline(c,'choice → outcome' if b==0 else 'choice   ×   outcome',y=805,size=36)
        else:
            title(c,'Randomness is not control')
            puck(c,cx=415,cy=400,s=.95,p=1,selected=0)
            puck(c,cx=1185,cy=400,s=.95,p=min(1,p*1.8),mode='fan',selected=1)
            label(c,415,215,'CONNECTED',CYAN,25);label(c,1185,215,'DISCONNECTED',MUTED,25)
            if u:mathline(c,[('I(choice; outcome)',CYAN),(' = 1 bit',INK),('     vs.     0',MUTED)],size=36)
    elif ch==1:
        title(c,['A skill holds its identity','Read the clouds, not one endpoint','Different effects, flexible behavior'][b])
        sep=(.3+.7*ease(p)) if b==1 else 1
        clouds(c,sep,paths=b!=1,active=u if b==0 else None)
        if b==0:
            co=C[u];dot(c,800,645,co,20);label(c,800,710,'same label throughout',co,28)
        elif b==1:
            if u:mathline(c,[('less overlap',CYAN),(' → easier to decode',INK)],size=36)
        else:
            if u:mathline(c,[('distinct states',CYAN),(' + flexible actions',GOLD)],size=36)
            else:mathline(c,'DIAYN',size=54)
    elif ch==2:
        title(c,['Before and after observing a state','Reward the gain in evidence','A learned guesser gives a lower bound'][b])
        if b==0:
            vals=[.25]*4 if not u else [.8,.08,.07,.05]
            histogram(c,vals,p=min(1,p*2));label(c,800,235,'PRIOR' if not u else 'AFTER OBSERVING',MUTED,26)
        elif b==1:
            histogram(c,[.8,.08,.07,.05],x=520,w=430,h=300)
            label(c,1140,400,'after / before',MUTED,30)
            label(c,1140,490,'0.8 / 0.25',CYAN,58)
            mathline(c,[('reward',GREEN),(' = log(',INK),('after',CYAN),(' / ',INK),('before',GOLD),(')',INK)],size=42)
        else:
            x=340;y=540;w=920
            c.line([(x,y),(x+w,y)],LINE,7)
            left=x+150;right=x+770
            c.line([(left,y),(right,y)],GOLD,8)
            dot(c,left,y,CYAN);dot(c,right,y,GREEN)
            label(c,left,y+60,'decoder bound',CYAN,28);label(c,right,y+60,'true information',GREEN,28)
            if u:label(c,800,440,'gap ≥ 0',GOLD,44)
            mathline(c,[('I = decoder bound',CYAN),(' + KL gap',GOLD)],size=42)
    elif ch==3:
        q=[.8,.25,.05][b];col=[GREEN,MUTED,RED][b];r=math.log(q/.25)
        title(c,['Correct evidence earns reward','Chance gives no gain','A confident mistake is still a mistake'][b])
        vals=[q]+[(1-q)/3]*3;histogram(c,vals,x=540,w=560,h=350,p=min(1,p*2))
        c.line([(240,620-.25*350),(840,620-.25*350)],INK,2,True)
        label(c,1100,375,'true label: blue',CYAN,30)
        label(c,1100,465,f'{q:g} / 0.25',INK,54)
        if u:label(c,1100,570,f'{r:+.3f} nats' if r else '0 nats',col,48)
        if u:mathline(c,[('reward = log(',INK),(f'{q/.25:g}',CYAN),(')',INK)],size=40)
    elif ch==4:
        title(c,['The labels come from our own experiment','Behavior and decoding improve together','Learning changes the state distributions'][b])
        if b<2:
            policy_loop(c,p,2 if b==0 and u else 0 if b==0 else 1 if not u else 2)
            if b==1:label(c,800,215,'reward flows back to the policy',GREEN,30)
        else:
            clouds(c,.12+.88*ease(p),paths=True)
            if u:mathline(c,'features decide which differences count',size=34)
    else:
        title(c,['A menu of learned behaviors','Using a choice can consume it','From distinguishable skills to future options'][b])
        if b==0:
            for i in range(4):
                x=320+i*320;c.d.rounded_rectangle((x-110,310,x+110,550),radius=22,outline=C[i],width=3)
                pts=[(x,490),(x-35,420),(x+35,360)] if i%2 else [(x-60,440),(x,360),(x+60,440)]
                trace(c,pts,p,C[i],6)
            if u:mathline(c,'a repertoire ≠ every task',size=40)
        else:
            junction(c,p=1 if b==1 and not u else p,prepare=b==2)
            if b==1 and u:cross(c,800,410,RED,27);label(c,1070,210,'one-way exit',MUTED,28)
            if b==2 and u:mathline(c,'Where do choices remain available?',size=38)

def simplex(c,points=None,mix=True,p=1,x=800,y=500,scale=.9):
    v=[(x-360*scale,y+190*scale),(x+360*scale,y+190*scale),(x,y-300*scale)]
    c.d.polygon(v,fill='#101a29');c.line(v+[v[0]],LINE,3)
    for i,(xx,yy) in enumerate(v):
        dot(c,xx,yy,C[i],12);label(c,xx,yy+(40 if i<2 else -35),['blue','yellow','pink'][i],C[i],25)
    if points is None:points=[[1,0,0],[0,1,0],[0,0,1]]
    pts=[tuple(sum(row[i]*v[i][k] for i in range(3)) for k in range(2)) for row in points]
    for i,pt in enumerate(pts):
        if mix:c.line([pt,(x,y+26.6667*scale)],blend(BG,C[i],.45),2,True)
        dot(c,*pt,C[i],15)
    if mix:dot(c,x,y+26.6667*scale,INK,13);label(c,x+110*scale,y+20*scale,'average',INK,23)
    return pts

def channel(c,rows=3,mode='identity',p=1,x=420,y=290,dx=740,gap=155):
    for i in range(rows):
        dest=0 if i==3 else i
        if mode=='takeover':dest=1
        elif mode=='blocked' and i==1:dest=0
        a=(x,y+i*gap);end=(x+dx,y+dest*gap)
        c.line([a,end],blend(BG,C[i%4],.3),6);trace(c,[a,end],p,C[i%4],4)
        dot(c,*a,C[i%4],17)
        if mode=='noise':
            for j in range(2):
                e=(x+dx,y+j*gap);c.line([a,e],blend(BG,C[i%4],.4),4)
    for j in range(min(rows,3)):dot(c,x+dx,y+j*gap,C[j],20)

def geometry(c,ch,b,u,p):
    if ch==0:
        title(c,['Location changes the available choices','Different labels can have identical effects','Prepare to keep options open'][b])
        junction(c,p,mode='takeover' if b==0 and u else 'open',prepare=b==2)
        if b==1 and u:mathline(c,[('achieved',CYAN),(' ≤ ',INK),('available',GOLD)],size=44)
        if b==2 and not u:label(c,360,635,'prepare',GOLD,28)
    elif ch==1:
        title(c,['Three probabilities become one point','A triangle of distributions','Sample a future time'][b])
        if b==0:
            histogram(c,[.5,.25,.25],x=370,w=440,h=340)
            if u:
                c.arrow((650,450),(820,450),MUTED,4)
                simplex(c,[[.5,.25,.25]],False,x=1180,y=470,scale=.6)
        elif b==1:
            row=([1,0,0] if p<.28 else [.5,.5,0]) if not u else [1/3]*3
            simplex(c,[row],False)
            if u:mathline(c,'⅓ + ⅓ + ⅓ = 1',size=40)
        else:
            vals=[.35*.65**i for i in range(8)]
            for i,v in enumerate(vals):
                xx=260+i*155;hh=v*850*min(1,p*3)
                c.d.rectangle((xx-35,590-hh,xx+35,590),fill=CYAN)
                label(c,xx,635,str(i+1),MUTED,24)
            label(c,800,695,'future timestep',MUTED,26)
            if u:mathline(c,'(1 − γ) Σ γᵗ = 1',size=44)
    elif ch==2:
        title(c,['Each skill is a distribution','Compare each skill to the mixture','When the distributions merge, control vanishes'][b])
        strength=1-ease(p) if b==2 else 1
        rows=[[strength*(int(i==j))+(1-strength)/3 for j in range(3)] for i in range(3)]
        simplex(c,rows,mix=b>0 or u==1)
        if b==1 and u:mathline(c,[('I = ',INK),('weighted average',CYAN),(' KL divergence',INK)],size=35)
        if b==2 and u:mathline(c,'same effects → zero information',size=37)
    elif ch==3:
        title(c,['A duplicate button adds no effect','Noise makes the choices indistinguishable','Capacity optimizes the sampling probabilities'][b])
        if b==0:
            channel(c,4,p=p,y=260,gap=125)
            if u:mathline(c,'4 labels   ·   3 distinct outcomes',size=38)
        elif b==1:
            channel(c,2,mode='noise' if u else 'identity',p=p,y=350,gap=220)
            if u:mathline(c,'50 / 50 from either button → I = 0',size=37)
        else:
            simplex(c,mix=True)
            mathline(c,'C = minᵣ max_z KL(d_z ‖ r)' if u else 'C = max_p I(Z; S⁺)',size=38)
            if u:label(c,800,706,'KL radius, not Euclidean distance',MUTED,23)
    elif ch==4:
        title(c,['A wide menu does not choose your reward','Missing options are still missing','Specify the control channel'][b])
        if b<2:
            junction(c,p)
            if b==0 and u:
                c.text(1060,260,'★',55,GOLD,anchor='mm');label(c,1160,215,'wanted',GOLD,28)
            if b==1:
                c.line([(450,225),(450,650)],MUTED,12);dot(c,275,380,RED,26);cross(c,450,380,RED,25)
                if u:label(c,275,450,'unreachable',RED,25)
        else:
            names=['start','skills','observation','horizon']
            for i,name in enumerate(names):
                x=290+i*340;c.circle(x,450,105,C[i],blend(BG,C[i],.06),3);label(c,x,450,name,C[i],29)
            if u:mathline(c,'change the channel → change the capacity',size=34)
    else:
        title(c,['One policy prepares; another exercises a choice','The estimate can miss real opportunities','The probability picture becomes a learning system'][b])
        junction(c,p,prepare=True)
        label(c,330,610,'prepare',GOLD,28);label(c,1110,695,'choose a skill',CYAN,28)
        if b==1:mathline(c,'weak skills can underestimate a useful state',size=34)
        if b==2 and u:mathline(c,'skills → decoder → value → preparation',size=35)

def tool_icon(c,x,y,k,col=CYAN,s=1):
    if k==0: # hammer
        c.line([(x-24*s,y+35*s),(x+17*s,y-25*s)],col,round(9*s))
        c.line([(x-12*s,y-42*s),(x+45*s,y-8*s)],col,round(18*s))
    elif k==1: # slider / clamp
        c.line([(x-38*s,y-30*s),(x-38*s,y+30*s),(x+38*s,y+30*s),(x+38*s,y-30*s)],col,round(6*s))
        c.line([(x-15*s,y-4*s),(x+45*s,y-4*s)],col,round(7*s))
    elif k==2: # wheel
        c.circle(x,y,32*s,col,None,4)
        for i in range(6):
            a=i*math.pi/3;c.line([(x,y),(x+30*s*math.cos(a),y+30*s*math.sin(a))],col,3)
    else: # lever
        c.line([(x-30*s,y+30*s),(x+30*s,y+30*s)],col,5)
        c.line([(x,y+30*s),(x+28*s,y-30*s)],col,6);dot(c,x+28*s,y-30*s,col,8*s)

def workshop(c,p=1,enter=True,skills=False,small=False):
    c.d.rounded_rectangle((100,440,720,615),radius=20,fill='#101a29',outline=LINE,width=3)
    c.d.rounded_rectangle((700,240,1460,690),radius=25,fill='#121e2a',outline=LINE,width=3)
    c.d.rectangle((698,445,725,610),fill='#121e2a')
    label(c,350,390,'corridor',MUTED,27);label(c,1100,200,'workshop',CYAN,27)
    for k,(x,y) in enumerate([(950,335),(1260,335),(950,590),(1260,590)]):
        tool_icon(c,x,y,k,C[k],.85)
        if skills:
            pts=[(790,485),(850,485),(x,y)]
            c.line(pts,blend(BG,C[k],.3),4);trace(c,pts,p,C[k],3)
    a=(280,530);b=(790,485)
    if enter:
        pts=[a,(590,530),b];c.line(pts,blend(BG,GOLD,.3),7);trace(c,pts,p,GOLD,5)
    else:dot(c,*a,INK,20)

def bottlenecks(c,p=1):
    xs=[320,800,1280]
    for i,(x,name) in enumerate(zip(xs,['skills','features','decoder'])):
        c.d.rounded_rectangle((x-150,345,x+150,545),radius=20,outline=C[i],width=3,fill=blend(BG,C[i],.05))
        label(c,x,445,name,C[i],35)
        if i<2:c.arrow((x+165,445),(xs[i+1]-165,445),MUTED,4)

def scaling(c,ch,b,u,p):
    if ch==0:
        title(c,['Reach a place where more can happen','Two policies, two jobs','Prepare the world, then choose an effect'][b])
        workshop(c,p,enter=b>0 or bool(u),skills=(b==1 and u) or b==2)
        if b==1:mathline(c,[('prepare',GOLD),('  →  ',INK),('exercise a skill',CYAN)],size=42)
    elif ch==1:
        title(c,['Read a skill from its future effect','The starting state supplies context','A low score has two possible causes'][b])
        if b==0:
            channel(c,3,p=p,x=350,dx=650,y=310,gap=145)
            if u:
                c.arrow((1070,455),(1250,455),MUTED,3);label(c,1360,455,'guess',CYAN,32)
            label(c,350,240,'skill',MUTED,26);label(c,1000,240,'future',MUTED,26)
        elif b==1:
            dot(c,300,350,GOLD,35);label(c,300,285,'start',GOLD,30)
            dot(c,300,590,CYAN,35);label(c,300,660,'future',CYAN,30)
            c.arrow((350,350),(750,465),GOLD,4);c.arrow((350,590),(750,465),CYAN,4)
            c.box(780,390,400,150,'decoder',PURPLE,size=40)
            if u:mathline(c,'q(skill | start, future)',size=44)
        else:
            clouds(c,1 if u else .05,center=(550,440),scale=.8)
            label(c,1150,420,'?' if u else '=',GOLD,100)
            label(c,1150,550,'weak decoder' if u else 'overlapping effects',MUTED,30)
    elif ch==2:
        title(c,['Predict the return instead of rerunning every skill','Normalize the discounted future','A fitted value can overestimate'][b])
        if b==0:
            for i in range(4):
                x=280+i*230;tool_icon(c,x,400,i,C[i]);c.arrow((x,470),(800,610),blend(BG,C[i],.6),3)
            c.box(630,620,340,90,'V(start)',GREEN,size=38)
            if u:label(c,800,250,'a learned prediction',GREEN,32)
        elif b==1:
            vals=[.35*.65**i for i in range(7)]
            for i,v in enumerate(vals):
                x=300+i*165;c.d.rectangle((x-45,600-v*900,x+45,600),fill=CYAN)
            mathline(c,[('(1 − γ)',GOLD),(' × discounted return',INK)],size=42)
            if u:label(c,800,260,'keep the scale factor',GOLD,32)
        else:
            c.line([(300,530),(1300,530)],LINE,7)
            dot(c,600,530,GREEN,20);label(c,600,600,'true information',GREEN,28)
            vx=lerp(420,1060,p) if u else 420;dot(c,vx,470,CYAN,20)
            label(c,vx,395,'fitted value',CYAN,30)
            if u:mathline(c,'an estimate is not a certificate',size=38)
    elif ch==3:
        title(c,['Prepare, then demonstrate','The two learning problems interact','Check the prediction against real effects'][b])
        workshop(c,1 if u else p,enter=True,skills=bool(u) or b>0)
        if b==0:mathline(c,[('preparation',GOLD),('  →  ',INK),('skill rollout',CYAN)],size=40)
        if b==1 and u:mathline(c,'bad estimates can attract the policy',size=36)
        if b==2:mathline(c,'available → achieved → measured',size=38)
    elif ch==4:
        title(c,['An encoder can erase a real distinction','More pixels need not mean more control','Three bottlenecks shape the score'][b])
        if b==0:
            dot(c,330,350,CYAN,25);dot(c,330,610,GOLD,25)
            c.arrow((380,350),(760,470),CYAN,4);c.arrow((380,610),(760,470),GOLD,4)
            c.box(790,390,350,160,'same feature',MUTED,size=32)
            if u:mathline(c,'different effects → identical encoding',size=35)
        elif b==1:
            puck(c,cy=420,s=1.2,p=1,selected=u)
            c.circle(1320,280,36,GOLD,GOLD if u else BG,3);label(c,1320,350,'independent light',MUTED,24)
            if u:mathline(c,'more variation ≠ more information',size=36)
        else:
            bottlenecks(c,p)
            if u:mathline(c,'improve and test each part',size=36)
    else:
        title(c,['Hold the starting state fixed','Distinguish the target from its approximation','The workshop is the whole picture'][b])
        if b==0:
            channel(c,3,p=p,y=300,gap=150)
            label(c,800,230,'repeat on held-out experience',GREEN,30)
            if u:mathline(c,'test preparation separately',size=38)
        elif b==1:
            bottlenecks(c,p)
            if u:mathline(c,'equations and implementation in the companion',size=32)
        else:
            workshop(c,p,skills=True)
            if u:mathline(c,'reach places where you can do more',size=38)

def world(c,x=800,y=465,s=1,wall=0,wind=1,puckpos=0,action=False,p=1):
    # Wallpaper, physical context, controlled object are separate visual layers.
    X=lambda xx:x+xx*s;Y=lambda yy:y+yy*s
    c.d.rounded_rectangle((X(-330),Y(-190),X(330),Y(150)),radius=14,fill='#142133',outline=LINE,width=2)
    for i in range(14):
        col=blend(BG,PURPLE if (i+wall)%2 else GREEN,.23)
        xx=-310+i*47;c.line([(X(xx),Y(-170)),(X(xx+30),Y(-65))],col,max(2,round(9*s)))
    c.d.polygon([(X(-330),Y(150)),(X(330),Y(150)),(X(270),Y(-30)),(X(-270),Y(-30))],fill='#223344',outline=LINE)
    c.line([(X(-260),Y(70)),(X(260),Y(70))],MUTED,2)
    if action:
        c.arrow((X(-220),Y(70)),(X(-80),Y(70)),CYAN,5)
    px=X(lerp(0,puckpos,p));dot(c,px,Y(70),CYAN,24*s)
    fan(c,X(235),Y(-95),p*2,s*.7)
    for j in range(3):
        yy=Y(-105+j*19);a=X(205 if wind<0 else 90);b=X(90 if wind<0 else 205)
        c.arrow((a,yy),(b,yy),GOLD,2)

def pair_worlds(c,wall=1,wind=-1,move=False,p=1):
    world(c,420,450,.85,wall=0,wind=1,puckpos=130 if move else 0,action=move,p=p)
    world(c,1180,450,.85,wall=wall,wind=wind,puckpos=-80 if move and wind<0 else 130 if move else 0,action=move,p=p)

def representation(c,ch,b,u,p):
    if ch==0:
        title(c,['What should this robot remember?','Changing pixels can leave the task unchanged','Three different kinds of state'][b])
        if b<2:
            world(c,s=1.5,wall=u if b==1 else 0,wind=1,puckpos=100,action=b==0,p=p)
            if b==0 and u:
                label(c,520,740,'puck',CYAN,28);label(c,800,740,'wind',GOLD,28);label(c,1080,740,'wallpaper',PURPLE,28)
            if b==1 and u:mathline(c,'Which differences change what I can do?',size=36,y=820)
        else:
            for i,(name,col) in enumerate([('controllable',CYAN),('relevant context',GOLD),('independent clutter',PURPLE)]):
                x=320+i*480
                if i==0:dot(c,x,420,col,45)
                elif i==1:fan(c,x,420,p,1.5)
                else:
                    for j in range(5):c.line([(x-65+j*32,360),(x-40+j*32,480)],col,8)
                label(c,x,570,name,col,28)
    elif ch==1:
        title(c,['Keep the effect of the chosen push','Wind is uncontrollable, but relevant','Wallpaper can change without changing the transition'][b])
        if b==0:
            world(c,s=1.5,wind=1,puckpos=150 if u else -150,action=True,p=p)
            if u:mathline(c,'preserve distinguishable effects',size=36,y=820)
        else:
            pair_worlds(c,wall=1 if b==2 else 0,wind=1 if b==2 else -1,move=True,p=p)
            label(c,800,450,'=' if b==2 else '≠',GREEN if b==2 else GOLD,60)
            if u:mathline(c,'same dynamics' if b==2 else 'same push · different dynamics',size=38)
    elif ch==2:
        title(c,['Forward: what happens under the same action?','Do not merge different dynamics','Compare distributions, not one sample'][b])
        if b<2:
            pair_worlds(c,wall=1 if b==0 else 0,wind=1 if b==0 else -1,move=True,p=p)
            if u:mathline(c,'one representation can suffice' if b==0 else 'retain the wind',size=38)
        else:
            clouds(c,.75 if u else .25)
            if u:mathline(c,'match the future distributions across actions',size=34)
    elif ch==3:
        title(c,['Backward: what could have caused this?','Keep the relevant predecessor evidence','Minimality rules out keeping everything'][b])
        if b<2:
            for i in range(2):
                yy=350+i*220;dot(c,330,yy,C[i],28)
                c.arrow((1100,460),(390,yy),C[i],4)
                label(c,330,yy+65,'left push' if i==0 else 'right push',C[i],26)
            dot(c,1180,460,CYAN,40);label(c,1180,560,'observed outcome',INK,28)
            if b==1 and u:mathline(c,'irrelevant wallpaper adds no predecessor evidence',size=32)
        else:
            for i,(name,col) in enumerate([('puck',CYAN),('wind',GOLD),('wallpaper',PURPLE)]):
                xx=420+i*380;c.box(xx-125,370,250,150,name,col,size=32)
                if i==2 and u:cross(c,xx,445,RED,60)
            mathline(c,'optimality + minimality are assumptions',size=37)
    elif ch==4:
        title(c,['An independent light adds outcomes','The nuisance factor cancels','Change the dependence, change the conclusion'][b])
        if b==0:
            for i in range(2):
                for j in range(2):
                    x=360+i*820;y=335+j*235;dot(c,x,y,C[i],25)
                    c.circle(x+150,y,27,GOLD,GOLD if j else BG,3)
            if u:mathline(c,'the puck already reveals the skill',size=36)
        elif b==1:
            label(c,530,380,'p(puck | skill)',CYAN,42);label(c,1080,380,'× p(light)',GOLD,42)
            c.line([(300,450),(1320,450)],INK,3)
            label(c,530,520,'p(puck)',CYAN,42);label(c,1080,520,'× p(light)',GOLD,42)
            if u:
                c.line([(950,345),(1210,415)],RED,4);c.line([(950,485),(1210,555)],RED,4)
                mathline(c,'I(skill; puck, light) = I(skill; puck)',size=35)
        else:
            dot(c,400,440,CYAN,38);c.circle(1200,440,42,GOLD,GOLD,3)
            c.arrow((470,440),(1120,440),RED,5)
            label(c,400,540,'skill',CYAN,30);label(c,1200,540,'light',GOLD,30)
            if u:mathline(c,'independence must be checked',size=40)
    else:
        title(c,['Intervene on one factor at a time','Test the behavior supported by the representation','Remember control, context, and clutter'][b])
        if b<2:
            pair_worlds(c,wall=1,wind=-1 if u else 1,move=b==1,p=p)
            if b==0:mathline(c,'change wind → change prediction' if u else 'change wallpaper → preserve prediction',size=35)
            else:mathline(c,'can the policy still choose different outcomes?',size=35)
        else:
            world(c,s=1.4,wind=1,puckpos=150,action=True,p=p)
            if u:mathline(c,[('control',CYAN),(' · ',INK),('context',GOLD),(' · ',INK),('clutter',PURPLE)],size=40,y=820)

def person(c,x,y,col=INK,s=1):
    c.circle(x,y-45*s,20*s,col,None,3)
    c.line([(x,y-24*s),(x,y+40*s)],col,4)
    c.line([(x-35*s,y+10*s),(x,y-10*s),(x+35*s,y+10*s)],col,4)
    c.line([(x-30*s,y+83*s),(x,y+40*s),(x+30*s,y+83*s)],col,4)

def routes(c,mode='open',p=1,helper=False):
    origin=(580,445);outs=[(1200,265),(1300,445),(1200,625)]
    person(c,390,400,INK,1.2)
    c.arrow((455,445),(540,445),INK,3)
    for i,e in enumerate(outs):
        target=outs[0] if mode=='blocked' and i==1 else outs[1] if mode=='takeover' else e
        pts=[origin,(820,445+(target[1]-445)*.4),target]
        c.line(pts,blend(BG,C[i],.25),9);trace(c,pts,p,C[i],4)
        c.d.rounded_rectangle((e[0]-35,e[1]-33,e[0]+35,e[1]+33),radius=7,outline=C[i],width=3)
    if mode=='blocked' or helper:
        boxy=lerp(445,730,p) if helper else 445
        c.box(880,boxy-38,82,76,color=RED,fill='#574138')
        if helper:
            c.box(770,boxy-32,70,60,color=GREEN,fill='#193b36');c.circle(782,boxy+33,8,GREEN,GREEN);c.circle(829,boxy+33,8,GREEN,GREEN)
            c.arrow((845,boxy),(875,boxy),GREEN,3)
    dot(c,*origin,INK,14)

def predictors(c,u=0,p=1):
    histogram(c,[.94,.03,.03],x=420,w=430,y=620,h=320,p=p)
    label(c,420,245,'knows the action',CYAN,30)
    if u:
        histogram(c,[1/3]*3,x=1180,w=430,y=620,h=320,p=p)
        label(c,1180,245,'does not know it',GOLD,30)

def assistance(c,ch,b,u,p):
    if ch==0:
        title(c,['Move the obstacle, or make the choice?','Clear the route and preserve the decision','Measure the human’s influence'][b])
        if b==0:routes(c,'blocked' if not u else 'open',p,helper=bool(u))
        elif b==1:routes(c,'open' if not u else 'takeover',p)
        else:
            routes(c,'open',p)
            if u:mathline(c,[('human choice',CYAN),(' → ',INK),('future',GOLD)],size=42)
    elif ch==1:
        title(c,['The human supplies the input','Human behavior supplies the sampling distribution','Unused choices are hard to infer from behavior'][b])
        if b==0:
            routes(c,'open',p)
            if u:mathline(c,'I(human action; future | context)',size=40)
        else:
            histogram(c,[1,0,0] if b==2 else [.6,.3,.1],x=800,y=625,w=780,h=350,p=p)
            if u:mathline(c,'observed information ≠ optimized capacity' if b==1 else 'no action variation → no observed information',size=34)
    elif ch==2:
        title(c,['Give one predictor the human’s action','Compare against the action-blind prediction','Learn by matching interactions and futures'][b])
        if b<2:
            predictors(c,1 if b==1 else u,p)
            if b==1 and u:mathline(c,'log [ p(future | action, context) / p(future | context) ]',size=30)
        else:
            for i in range(3):
                yy=300+i*160;dot(c,400,yy,C[i],24)
                j=i if not u else (i+1)%3;dot(c,1200,300+j*160,C[j],24)
                c.line([(445,yy),(1150,300+j*160)],C[i] if not u else LINE,3)
            label(c,800,225,'matched' if not u else 'reference pairs',GREEN if not u else MUTED,32)
            if u:mathline(c,'contrastive scores estimate density ratios',size=34)
    elif ch==3:
        title(c,['Both scores use the same reference','Subtract the scores; the reference cancels','Use the signal to make choices more effective'][b])
        if b<2:
            label(c,530,365,'action-aware log probability',CYAN,34)
            label(c,1170,365,'− log reference',GOLD,34)
            label(c,530,550,'action-blind log probability',PURPLE,34)
            label(c,1170,550,'− log reference',GOLD,34)
            if b==1:
                label(c,180,550,'−',INK,64)
                c.line([(300,630),(1400,630)],INK,3)
                c.line([(1010,335),(1340,395)],RED,4);c.line([(1010,520),(1340,580)],RED,4)
            if b==1 and u:mathline(c,'log [ p(future | action, context) / p(future | context) ]',size=30)
        else:
            routes(c,'open',p,helper=True)
            if u:mathline(c,'separate the futures of different human choices',size=33)
    elif ch==4:
        title(c,['Blocked route → cleared route','Takeover merges every human choice','Whose agency are we measuring?'][b])
        if b==0:routes(c,'open' if u else 'blocked',p,helper=bool(u))
        elif b==1:
            routes(c,'takeover',p)
            if u:mathline(c,'I(human choice; destination) = 0',size=39)
        else:
            person(c,460,410,INK,1.7);c.box(1020,355,170,160,'robot',GREEN,size=32)
            c.arrow((580,450),(970,450),MUTED,4)
            mathline(c,'assistant capability ≠ human influence',size=37)
    else:
        title(c,['More choices need not mean better choices','The reward connection has assumptions','Clear the route; leave the choice'][b])
        if b==0:
            routes(c,'open',p)
            if u:
                for x,y in [(1200,265),(1300,445),(1200,625)]:cross(c,x,y,RED,24)
                mathline(c,'influence does not specify every preference',size=34)
        elif b==1:
            for i,name in enumerate(['human model','tasks','dynamics']):
                x=350+450*i;c.circle(x,450,135,C[i],blend(BG,C[i],.06),3);label(c,x,450,name,C[i],30)
            if u:mathline(c,'the assumptions carry the connection',size=36)
        else:
            routes(c,'open',p,helper=True)
            if u:mathline(c,'the human still determines the future',size=38)

TOKENS=['I','recommend','we','approve','this','request']
PROBS=[.98,.95,.9,.15,.9,.85]

def sentence(c,branch=True,p=1,showchoice=True):
    label(c,500,445,'I recommend we',INK,56)
    if branch:
        for i,(word,col,yy) in enumerate([('approve',CYAN,330),('reject',GOLD,565)]):
            pts=[(800,445),(940,yy),(1050,yy)]
            c.line(pts,blend(BG,col,.3),5);trace(c,pts,p,col,4)
            if showchoice:label(c,1220,yy,word,col,57)
            else:label(c,1220,yy,'?',col,57)
    else:label(c,1160,445,'approve',CYAN,56)

def tokenrow(c,accepted=3,probabilities=True,y=390):
    xs=[210,440,665,885,1105,1350];widths=[100,310,120,260,160,270]
    for i,(x,w,t) in enumerate(zip(xs,widths,TOKENS)):
        co=CYAN if i<accepted else GOLD if i==3 else MUTED
        fill=blend(BG,co,.12) if i<accepted else BG
        c.d.rounded_rectangle((x-w/2,y-48,x+w/2,y+48),radius=12,fill=fill,outline=co,width=2)
        label(c,x,y,t,co,32)
        if probabilities:label(c,x,y+95,f'{PROBS[i]:.2f}',co,27)

def budget(c,limit=1,current=.177,overshoot=False,p=1):
    x=220;y=670;w=1160;scale=w/3
    c.d.rounded_rectangle((x,y-24,x+w,y+24),radius=12,fill='#182438')
    end=x+min(3,current)*scale*ease(p)
    if end>x:c.d.rounded_rectangle((x,y-24,end,y+24),radius=12,fill=RED if overshoot else CYAN)
    lx=x+limit*scale;c.line([(lx,y-65),(lx,y+62)],GOLD,4)
    label(c,lx,y+94,f'budget = {limit:g}',GOLD,26)
    label(c,x,y-70,'cumulative surprise',MUTED,25)
    label(c,min(end+80,1400),y,f'{current:.2f}',INK,27)

def language(c,ch,b,u,p):
    if ch==0:
        title(c,['Where should the assistant stop?','Predictable work, then a human decision','One prefix, two consequential continuations'][b])
        sentence(c,p=p,showchoice=b!=1 or bool(u))
        if b==0 and u:
            c.line([(885,260),(885,650)],GREEN,3,True);label(c,885,725,'handoff',GREEN,30)
        if b==1 and u:mathline(c,'entropy · surprisal · empowerment',size=36)
    elif ch==1:
        title(c,['Information cannot exceed choice entropy','Unpredictable choices can still be ignored','Likelihood is a proxy for the handoff'][b])
        if b==0:
            sentence(c,p=p)
            if u:mathline(c,[('I(choice; outcome)',CYAN),(' ≤ ',INK),('H(choice)',GOLD)],size=42)
        elif b==1:
            channel(c,2,mode='takeover',p=p,y=350,gap=200)
            if u:mathline(c,'uncertain input · fixed output · zero influence',size=35)
        else:
            c.circle(450,440,115,CYAN,None,3);label(c,450,440,'likelihood',CYAN,34)
            c.arrow((590,440),(1010,440),MUTED,4)
            c.circle(1160,440,115,GOLD,None,3);label(c,1160,440,'handoff',GOLD,34)
            if u:mathline(c,'useful proxy ≠ exact empowerment',size=38)
    elif ch==2:
        title(c,['Less likely tokens spend more surprise','One sample differs from an expectation','Surprise can come from model error'][b])
        if b==0:
            x0=300;y0=660;w=1000;h=380
            c.arrow((x0,y0),(x0+w+40,y0),MUTED,3);c.arrow((x0,y0),(x0,y0-h-40),MUTED,3)
            pts=[(x0+w*v,y0-h*(-math.log(max(v,.03)))/3.6) for v in [i/200 for i in range(6,201)]]
            c.line(pts,CYAN,4);prob=.9-.8*ease(p) if u else .9
            xx=x0+w*prob;yy=y0-h*(-math.log(prob))/3.6;dot(c,xx,yy,GOLD,15)
            label(c,xx,yy-50,f'p = {prob:.1f}',GOLD,29)
            label(c,1320,710,'probability',MUTED,26)
            mathline(c,'surprisal = −log p(token)',size=42,y=805)
        elif b==1:
            label(c,800,380,'one token:  −log q(token)',CYAN,44)
            if u:label(c,800,560,'average:  H(p) + KL(p ‖ q)',GOLD,44)
            mathline(c,'model mismatch adds surprise',size=36)
        else:
            for i,(s,col) in enumerate([('rare name',PURPLE),('familiar decision',CYAN)]):
                xx=470+660*i;c.box(xx-220,350,440,180,s,col,size=34)
            if u:mathline(c,'surprise and consequence can disagree',size=38)
    elif ch==3:
        title(c,['Accumulate a surprise budget','The next word crosses the threshold','Accept only prefixes strictly below the budget'][b])
        base=sum(-math.log(q) for q in PROBS[:3]);total=base-math.log(PROBS[3])
        tokenrow(c,accepted=3,probabilities=b<2)
        if b<2:
            budget(c,current=total if b==1 and not u else base,overshoot=b==1 and not u,p=p)
            if b==1 and u:
                c.line([(760,290),(760,550)],GREEN,4);label(c,760,220,'stop before approve',GREEN,30)
        else:
            mathline(c,'B(prefix) < η' if not u else 'p(prefix) > exp(−η)',y=680,size=49)
    elif ch==4:
        title(c,['Train on the selected prefix','A larger budget permits more automation','Target selection, then supervised fine-tuning'][b])
        if b<2:
            accepted=(6 if u else 2) if b==1 else 3
            tokenrow(c,accepted=accepted,probabilities=False)
            if b==0:
                c.arrow((490,485),(800,610),CYAN,4);c.box(600,625,400,95,'training targets',CYAN,size=32)
                if u:
                    c.line([(770,330),(1480,450)],MUTED,3);label(c,1150,540,'excluded continuation',MUTED,26)
            else:
                limit=3 if u else .1;budget(c,limit=limit,current=sum(-math.log(q) for q in PROBS[:accepted]),p=p)
        else:
            for i,s in enumerate(['score','select prefix','fine-tune']):
                x=350+450*i;c.box(x-160,370,320,170,s,C[i],size=31)
                if i<2:c.arrow((x+180,455),(x+270,455),MUTED,4)
            if u:mathline(c,'a practical procedure built from a proxy',size=35)
    else:
        title(c,['Evaluate the handoff, including unnecessary pauses','Measure outcomes and retained human influence','Useful progress, with the choice still open'][b])
        if b==0:
            sentence(c,p=p)
            if u:mathline(c,'too many handoffs can remove the convenience',size=34)
        elif b==1:
            for i,(s,col) in enumerate([('task outcomes',CYAN),('human influence',GOLD)]):
                x=450+i*700;c.circle(x,440,170,col,blend(BG,col,.06),3);label(c,x,440,s,col,32)
            if u:mathline(c,'evaluate both in the intended setting',size=37)
        else:
            sentence(c,p=p)
            person(c,900,690,GREEN,.7)
            c.line([(900,275),(900,590)],GREEN,3,True)
            if u:mathline(c,'Whose choices remain in the future?',size=38,y=830)

def draw_film(c,id,ch,b,u,p):
    globals()[id](c,ch,b,u,p)
