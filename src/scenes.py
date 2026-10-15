"""Original mathematical animations. No paper figures or benchmark curves.

All probability-channel values are exact teaching examples. Geometry on the
simplex is illustrative: line length does not represent KL divergence.
"""
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from empowerment_lab import entropy,mutual_information,symmetric,variational_bound,threshold_prefix
from drawing import *
COLORS=[CYAN,PURPLE,GREEN,GOLD,RED,BLUE]

def heading(c,title,sub=''):
    c.text(78,166,title,25,INK,True)
    if sub:c.text(78,207,sub,18,MUTED)

def note(c,s,color=MUTED):c.wrap(78,588,s,865,20,color,leading=1.25)

def badge(c,x,y,value,label,color=CYAN,w=230):
    c.box(x,y,w,76,color=color)
    c.text(x+16,y+8,value,27,color,True)
    c.text(x+16,y+47,label,16,MUTED)

def bars(c,items,x=120,y=270,w=650,scale=1.5):
    for i,(label,v,color) in enumerate(items):
        yy=y+i*83
        c.text(x,yy,label,20,MUTED)
        c.box(x,yy+31,w,20,color=LINE,fill=BG)
        if v>0:c.d.rounded_rectangle((x,yy+31,x+w*min(v/scale,1),yy+51),radius=6,fill=color)
        c.text(x+w+18,yy+29,f'{v:.3f}',21,color,True)

def channel(c,p,b,ep):
    heading(c,'An action can be a message','Exact binary channel · natural logarithms · nats')
    e=[0,.5,.12][b]
    for i in range(2):
        for j in range(2):
            a=(235,310+i*155);d=(700,310+j*155);prob=(1-e) if i==j else e
            if prob:
                c.line([a,d],blend(BG,COLORS[i],.3+prob*.5),max(1,round(prob*8)))
                dot=pos(a,d,(p*5+i*.24+j*.12)%1);c.circle(*dot,7,COLORS[i],COLORS[i])
                mid=pos(a,d,.36 if i==j else .63);c.text(mid[0],mid[1]-27,f'{prob:.2f}',18,COLORS[i])
    for i in range(2):
        c.node(195,310+i*155,f'A={i}',COLORS[i],40)
        c.node(740,310+i*155,f'Y={i}',COLORS[i],40)
    c.text(195,251,'INPUT',17,MUTED,anchor='mm');c.text(740,251,'OUTCOME',17,MUTED,anchor='mm')
    c.text(470,545,f'I(A;Y) = {math.log(2)-entropy([e,1-e]):.3f} nats',26,ep['color'],True,'mm')
    note(c,['Reliable consequences make the action recoverable.','At 50% confusion, both actions have identical outcome distributions.','Capacity chooses the input prior; here symmetry makes it uniform.'][b])

def skills(c,p,b,ep):
    heading(c,'One identity, many timesteps','Original four-skill sketch · color denotes the latent skill Z')
    center=(470,397);c.node(*center,'s₀',MUTED,31)
    for z in range(4):
        a=z*math.pi/2+math.pi/4;end=(center[0]+240*math.cos(a),center[1]+133*math.sin(a))
        pts=[center]+[(center[0]+j/30*(end[0]-center[0]),center[1]+j/30*(end[1]-center[1])+10*math.sin(j*.3+z)*j/30) for j in range(1,31)]
        c.line(pts,blend(BG,COLORS[z],.35),7);dot=c.path(pts,.25+.75*((p*2+z*.1)%1),COLORS[z],4);c.circle(*dot,8,COLORS[z],COLORS[z])
        for k in range(18):
            aa=k*2.4;rr=4*math.sqrt(k)
            c.circle(end[0]+rr*math.cos(aa),end[1]+rr*math.sin(aa),3,COLORS[z],COLORS[z])
        c.text(end[0],end[1]+30,f'z = {z+1}',20,COLORS[z],True,'mm')
    note(c,['Hold Z fixed while the skill acts; do not resample it at every step.','The discriminator tries to identify Z from visited states.','Action entropy permits varied behavior within each recognizable skill.'][b])

def bound(c,p,b,ep):
    heading(c,'A decoder creates a trainable surrogate','Exact toy expectation, not a learned neural estimate')
    W=symmetric(4,.2);prior=[.25]*4;quality=[.1,.6,1.][b]
    I=mutual_information(W,prior);B=variational_bound(W,prior,quality)
    bars(c,[('True mutual information',I,CYAN),('Variational objective',B,ep['color']),('Average posterior KL gap',I-B,GOLD)],scale=math.log(4))
    note(c,['The exact posterior would require knowledge of the skill channel.','A normalized decoder gives a lower bound in population expectation.','When the decoder equals the posterior, the gap closes.'][b])

def reward(c,p,b,ep):
    heading(c,'The reward is a log likelihood ratio','Four equally likely skills · log q(z|s) − log 0.25')
    vals=[.8,.25,.05];q=vals[b];r=math.log(q/.25)
    for j,v in enumerate([q]+[(1-q)/3]*3):
        x=195+j*172;h=v*275
        c.d.rounded_rectangle((x,530-h,x+90,530),radius=6,fill=COLORS[j]);c.text(x+45,548,f'z={j+1}',20,COLORS[j],anchor='mm')
        c.text(x+45,510-h,f'{v:.2f}',22,INK,anchor='mm')
    c.line([(140,530-.25*275),(880,530-.25*275)],MUTED,2,True)
    c.text(870,530-.25*275-25,'prior = 0.25',18,MUTED,anchor='ra')
    c.text(470,257,f'Correct label z=1: reward {r:+.3f} nats',27,ep['color'],True,'mm')
    note(c,['Confident and correct: ln(0.8 / 0.25) = ln 3.2.','A chance-level prediction produces zero reward.','An incorrect low probability produces negative reward.'][b])

def training(c,p,b,ep):
    heading(c,'Learn a decoder and a skill policy','Schematic training loop · no fabricated learning curve')
    boxes=[(120,275,'Sample a skill Z','Hold it for the rollout'),(580,275,'Collect (s, z)','Add labeled experience'),(580,450,'Fit q(z | s)','Supervised classification'),(120,450,'Improve π(a | s,z)','Intrinsic reward + entropy')]
    for i,(x,y,title,sub) in enumerate(boxes):
        co=COLORS[i] if i in ([0,1] if b==0 else [2] if b==1 else [3]) else MUTED
        c.box(x,y,270,91,color=co);c.text(x+135,y+27,title,22,co,True,'mm');c.text(x+135,y+63,sub,17,MUTED,anchor='mm')
    for a,d in [((390,321),(577,321)),((715,367),(715,448)),((580,496),(395,496)),((255,450),(255,369))]:
        c.arrow(a,d,ep['color'],3);dot=pos(a,d,(p*5)%1);c.circle(*dot,6,INK,INK)
    note(c,'The reward changes as the discriminator improves; the two optimizers interact.')

def options(c,p,b,ep):
    heading(c,'A junction has options that an exit may lose','Original finite-endpoint channel · each exit is one way')
    hub=(420,403);outs=[(770,272),(830,402),(770,532)]
    c.node(*hub,'hub',ep['color'],47)
    c.arrow((145,403),(365,403),INK,4);c.text(235,364,'prepare',21,INK,anchor='mm')
    for i,end in enumerate(outs):
        c.arrow((hub[0]+52,hub[1]),(end[0]-46,end[1]),COLORS[i],4)
        c.node(*end,f'exit {i+1}',COLORS[i],43)
        dot=pos((hub[0]+52,hub[1]),(end[0]-46,end[1]),(p*3+i*.15)%1);c.circle(*dot,6,COLORS[i],COLORS[i])
    c.text(420,479,'C = ln 3',22,ep['color'],True,'mm');c.text(170,468,'seek a starting state',17,MUTED,anchor='mm')
    note(c,['Skills exercise available choices.','Potential empowerment asks which choices can be made available.','An outer policy seeks good starting states for the inner skills.'][b])

def simplex(c,p,b,ep):
    heading(c,'Occupancies live in a probability simplex','Each point is a distribution over three outcomes')
    verts=[(485,260),(180,540),(790,540)]
    c.d.polygon(verts,fill='#16253c',outline=LINE);c.line(verts+[verts[0]],MUTED,2)
    for i,v in enumerate(verts):c.text(v[0],v[1]+(-28 if i==0 else 22),f'Outcome {i+1}',19,COLORS[i],anchor='mm')
    rows=[[.82,.1,.08],[.1,.8,.1],[.12,.12,.76]]
    points=[tuple(sum(row[i]*verts[i][k] for i in range(3)) for k in range(2)) for row in rows]
    w=[.25+.12*math.sin(p*2*math.pi),.35,.4-.12*math.sin(p*2*math.pi)]
    mix=tuple(sum(w[i]*points[i][k] for i in range(3)) for k in range(2))
    c.line(points+[points[0]],ep['color'],2,True)
    for i,pt in enumerate(points):
        if b>0:c.line([pt,mix],COLORS[i],3)
        c.circle(*pt,10,COLORS[i],COLORS[i]);c.text(pt[0]+15,pt[1]-20,f'd{i+1}',20,COLORS[i],True)
    c.circle(*mix,11,INK,INK);c.text(mix[0]+18,mix[1]+10,'mixture',19,INK)
    if b==2:c.text(811,352,'Σ weights = 1',18,MUTED,anchor='mm')
    note(c,'These lines show probability mixtures. Their Euclidean lengths are not KL distances.')

def radius(c,p,b,ep):
    simplex(c,p,b,ep)
    c.box(75,164,880,74,color=BG,fill=BG)
    c.text(78,166,'Information is a weighted KL radius',25,INK,True)
    c.text(78,207,['Compare each skill with its mixture.','Average KL with the skill prior.','Only capacity optimization gives the minimax-radius dual.'][b],18,MUTED)

def capacity_scene(c,p,b,ep):
    if b==0:
        heading(c,'Count outcomes, not input names','Five input labels; only three distinct deterministic outputs')
        for i in range(5):
            a=(230,270+i*63);end=(735,300+(i%3)*105)
            c.node(190,a[1],str(i+1),COLORS[i%3],24);c.arrow(a,end,COLORS[i%3],3)
            dot=pos(a,end,(p*4+i*.1)%1);c.circle(*dot,5,COLORS[i%3],COLORS[i%3])
        for j in range(3):c.node(775,300+j*105,'Y'+str(j+1),COLORS[j],31)
        c.text(490,550,'C = ln 3, not ln 5',26,ep['color'],True,'mm')
        note(c,'Duplicating a channel row does not add a distinguishable future.')
        return
    if b==2:
        heading(c,'Many random outcomes; no input influence','Eight equally likely outcomes under either action')
        for i in range(2):c.node(180,330+i*145,'A'+str(i),COLORS[i],36)
        for j in range(8):
            end=(685+(j%4)*65,330+(j//4)*145)
            for i in range(2):c.line([(220,330+i*145),end],blend(BG,COLORS[i],.25),1)
            c.circle(*end,14,ep['color'],ep['color'] if j==int(p*24)%8 else None)
        c.text(515,550,'H(Y) = ln 8     I(A;Y) = 0',26,ep['color'],True,'mm')
        note(c,'Output diversity alone does not establish controllability.')
        return
    heading(c,'Noise can erase a controllable distinction','Binary symmetric channel · C = ln 2 − h(ε)')
    c.axes(135,525,655,245,'confusion probability ε','capacity (nats)')
    fn=lambda e:math.log(2)-entropy([e,1-e])
    c.curve(fn,ymax=math.log(2),x=135,y=525,w=655,h=245,color=ep['color'])
    e=(.5+.5*math.sin(p*11))
    v=fn(e);pt=(135+655*e,525-245*v/math.log(2))
    c.line([(pt[0],525),pt],MUTED,2,True);c.circle(*pt,9,ep['color'],ep['color'])
    for x,l in [(135,'0'),(462.5,'0.5'),(790,'1')]:c.text(x,550,l,19,MUTED,anchor='mm')
    c.text(95,280,'ln 2',17,MUTED,anchor='mm');c.text(825,360,f'{v:.3f}',27,ep['color'],True)
    note(c,['Reliable control has high capacity.','At ε = 0.5, actions cannot be recovered from outcomes.','A predictable inversion still transmits the input label.'][b])

def geometry_limit(c,p,b,ep):
    heading(c,'A distinction can be irrelevant to a task','Original example: four controllable indicator colors')
    for i in range(4):
        x=180+i*208;c.box(x-50,290,100,105,color=COLORS[i]);c.circle(x,342,28,COLORS[i],COLORS[i] if int(p*8)%4==i else None)
        c.text(x,428,'reward = 0',18,MUTED,anchor='mm')
    badge(c,152,480,'ln 4 nats','Control over indicator colors',ep['color'],310)
    badge(c,512,480,'0 task gain','The desired object never moves',GOLD,350)
    note(c,'Empowerment values reliable distinctions. Reward specifies which distinctions are useful.')

def two_policy(c,p,b,ep):
    heading(c,'Two policies solve different problems','Prepare a context → execute a skill from that context')
    c.box(85,325,200,120,'start',MUTED);hub=(495,385)
    c.arrow((290,385),(435,385),INK,5);c.node(*hub,'tools',ep['color'],53)
    c.text(350,307,'outer policy μ',20,INK,anchor='mm')
    c.text(496,476,'estimated empowerment',18,ep['color'],anchor='mm')
    for z in range(4):
        end=(830,270+z*84);co=COLORS[z]
        c.arrow((549,385),(786,end[1]),co,3);c.node(*end,str(z+1),co,29)
        dot=pos((549,385),(786,end[1]),(p*4+z*.17)%1);c.circle(*dot,6,co,co)
    c.text(745,247,'inner skills π(· | s,z)',20,MUTED,anchor='mm')
    c.text(190,498,'Which context?',22,INK,anchor='mm');c.text(800,568,'What can I do here?',22,ep['color'],anchor='mm')
    note(c,['Probe the skills available in a context.','Use a learned decoder and value function to estimate control.','Reward the outer policy for reaching more capable contexts.'][b])

def decoder(c,p,b,ep):
    heading(c,'A future outcome carries evidence about Z','Compare the inferred skill probability to its prior')
    for x,y,label in [(115,300,'start s₀'),(115,440,'future s⁺')]:
        c.box(x,y,175,80,label,CYAN);c.arrow((295,y+40),(403,408),CYAN,3)
    c.box(410,355,190,105,'decoder q',ep['color']);c.arrow((607,408),(700,408),ep['color'],4)
    post=[.7,.1,.1,.1] if b<2 else [.85,.05,.05,.05]
    for z,q in enumerate(post):
        yy=290+z*67;c.text(720,yy,f'z{z+1}',18,COLORS[z]);c.line([(765,yy+14),(765+150*q,yy+14)],COLORS[z],14);c.text(930,yy,f'{q:.2f}',18,COLORS[z],anchor='ra')
    note(c,'Normalized scores must define a probability distribution; raw logits are not log posterior ratios.')

def value(c,p,b,ep):
    heading(c,'There are two distinct approximation gaps','Exact population objects shown here; learned critics add estimation error')
    bars(c,[('Channel capacity',math.log(4),GOLD),('Information in current skill family',.93,CYAN),('Information decoded by q',.68,ep['color'])],scale=1.5)
    note(c,['A normalized discounted return averages over a random future time.','Weak skills and an imperfect decoder reduce different quantities.','A finite-data value prediction need not be a valid pointwise lower bound.'][b])

def rollout(c,p,b,ep):
    heading(c,'One rollout has two stages','Training data must cover preparation and skill execution')
    c.text(260,277,'1. PREPARE',21,INK,True,'mm');c.text(712,277,'2. BRANCH',21,ep['color'],True,'mm')
    path=[(105,440),(205,430),(290,400),(390,400),(470,390)]
    c.line(path,LINE,6);dot=c.path(path,(p*2)%1,INK,5);c.circle(*dot,8,INK,INK)
    c.node(500,390,'s₀',MUTED,30)
    for z in range(4):
        end=(865,282+z*76);pts=[(535,390),(650,390+(z-1.5)*23),end]
        c.line(pts,blend(BG,COLORS[z],.35),5);dot=c.path(pts,(p*3+z*.2)%1,COLORS[z],3);c.circle(*dot,7,COLORS[z],COLORS[z])
    c.box(210,510,575,52,'Replay buffer → decoder, skill values, outer policy',LINE,size=19)
    note(c,'The changing outer policy changes which contexts the skills learn to control.')

def bottleneck(c,p,b,ep):
    heading(c,'Choose what counts as an outcome','Measurement and resolution are part of the problem definition')
    c.box(90,295,230,190,color=MUTED);c.text(205,321,'full state',23,INK,True,'mm')
    for j,label in enumerate(['tool position','indicator color','tiny vibration']):c.text(112,356+j*35,label,19,COLORS[j])
    c.arrow((330,390),(410,390),MUTED);c.box(420,340,190,105,'g(s) + noise',ep['color']);c.arrow((620,390),(700,390),ep['color'])
    c.box(710,295,220,190,color=ep['color']);c.text(820,326,'measured future',20,INK,True,'mm')
    for j in range(16):
        ang=j*2.4;r=26+12*math.sin(p*13+j);c.circle(820+r*math.cos(ang),408+r*math.sin(ang),4,ep['color'],ep['color'])
    c.text(815,460,'coarse resolution',16,MUTED,anchor='mm')
    note(c,'Independent measurement noise cannot increase mutual information: data processing applies.')

def features(c,p,b,ep):
    heading(c,'Control-relevant is broader than controllable','A wind variable can matter even when the agent cannot change it')
    labels=[('Y','controllable','object position',CYAN),('W','uncontrolled, relevant','wind direction',GOLD),('E','irrelevant process','background flicker',PURPLE)]
    for i,(sym,title,example,col) in enumerate(labels):
        x=95+i*288;c.box(x,275,260,250,color=col);c.node(x+130,334,sym,col,32);c.text(x+130,399,title,17,col,True,'mm');c.text(x+130,437,example,19,MUTED,anchor='mm')
        if i==0:c.circle(x+75+100*((p*2)%1),480,7,col,col)
        if i==1:c.arrow((x+90,483),(x+170,463+15*math.sin(p*10)),col)
        if i==2:
            for k in range(5):c.circle(x+65+k*32,480,6,col,col if (k+int(p*12))%2 else BG)
    note(c,'Discarding everything the agent cannot control would also discard useful context.')

def factorization(c,p,b,ep):
    heading(c,'Two representations, two roles','A start-state encoder and a future-state encoder enter the decoder')
    for x,label,col in [(115,'s₀',CYAN),(705,'s⁺',PURPLE)]:
        c.node(x+85,290,label,col,35);c.arrow((x+85,330),(x+85,375),col)
        c.box(x,385,170,72,'φ(s₀)' if x==115 else 'ψ(s⁺)',col)
    c.arrow((290,420),(405,420),CYAN);c.arrow((700,420),(580,420),PURPLE)
    c.box(410,370,165,105,'q(z | φ, ψ)',ep['color'],size=22)
    c.text(493,519,'Enough information to decode the skill',23,ep['color'],True,'mm')
    note(c,'An optimal decoder can retain extra details; minimal representations are an additional condition.')

def equivalence(c,p,b,ep,backward=False):
    heading(c,'Backward: compare incoming evidence' if backward else 'Forward: compare outgoing possibilities',
        'Equal skill posteriors can alias outcomes' if backward else 'Actions may be matched by their effects under the theorem assumptions')
    left=[(240,315),(240,485)];right=[(760,280),(760,400),(760,520)]
    for i,xy in enumerate(left):c.node(*xy,('y' if backward else 's')+str(i+1),ep['color'],35)
    for j,xy in enumerate(right):c.node(*xy,('z' if backward else 'next')+str(j+1),COLORS[j],36)
    for i,xy in enumerate(left):
        for j,end in enumerate(right):
            a=(xy[0]+40,xy[1]);d=(end[0]-40,end[1]);a,d=(d,a) if backward else (a,d)
            c.arrow(a,d,blend(BG,COLORS[j],.7),2);dot=pos(a,d,(p*3+j*.2)%1);c.circle(*dot,5,COLORS[j],COLORS[j])
    c.text(470,550,'Same posterior ≠ same future dynamics' if backward else 'Compare distributions, not image similarity',22,ep['color'],True,'mm')
    note(c,'Backward aliasing does not imply forward aliasing.' if backward else 'Matching transitions alone is not a universal neural representation guarantee.')

def invariance(c,p,b,ep):
    heading(c,'An independent nuisance cancels','Exact finite-channel factorization: p(y,e|z) = p(y|z) p(e)')
    c.box(100,285,335,250,color=CYAN);c.box(535,285,335,250,color=PURPLE)
    for z in range(2):
        yy=345+z*110;c.text(125,yy,f'z={z}',20,COLORS[z]);c.line([(210,yy+12),(380,yy+12)],COLORS[z],7)
        for k in range(4):
            x=580+k*73;c.circle(x,yy+10,8,COLORS[z],COLORS[z] if int(p*10+k)%3 else None)
    c.text(267,258,'controlled Y',21,CYAN,anchor='mm');c.text(703,258,'joint (Y, nuisance E)',21,PURPLE,anchor='mm')
    c.text(485,420,'=',38,INK,True,'mm');c.text(485,563,'I(Z; Y,E) = I(Z; Y)',28,ep['color'],True,'mm')
    note(c,'The nuisance changes the outcome entropy but contributes no information about the skill.')

def human(c,p,b,ep):
    heading(c,'Empower the human’s actions','Original three-action channel · the assistant changes the environment')
    clearance=[0,.55,1][b]
    for i in range(3):
        a=(230,288+i*116);c.node(190,a[1],f'H{i+1}',COLORS[i],32)
        row=[1,0,0] if i==0 else ([1-clearance,clearance,0] if i==1 else [1-clearance,0,clearance])
        for j,v in enumerate(row):
            if v:
                end=(720,288+j*116);c.line([a,end],blend(BG,COLORS[i],.7),max(2,round(v*7)));dot=pos(a,end,(p*4+i*.13)%1);c.circle(*dot,6,COLORS[i],COLORS[i])
    for j in range(3):c.node(760,288+j*116,f'Y{j+1}',COLORS[j],32)
    c.text(480,258,f'path clearance = {clearance:.2f}',22,ep['color'],True,'mm')
    note(c,'The robot’s own action diversity is not the target; human influence over outcomes is.')

def human_prior(c,p,b,ep):
    heading(c,'Available choices and exercised choices differ','Perfect three-output channel; only the human action prior changes')
    prior=[[1/3]*3,[.8,.1,.1],[1,0,0]][b]
    bars(c,[('Human action entropy',entropy(prior),CYAN),('Effective mutual information',entropy(prior),ep['color']),('Channel capacity',math.log(3),GOLD)],scale=math.log(3))
    note(c,'A deterministic action has zero label entropy. This does not mean the action is useless.')

def contrastive(c,p,b,ep):
    heading(c,'Two contrastive predictors share a reference','Controlled and uncontrolled future distributions')
    for j,(label,sub,col) in enumerate([('f(s, aᴿ, aᴴ, g)','include human action',CYAN),('g₀(s, aᴿ, g)','average over human actions',PURPLE)]):
        yy=282+j*150;c.box(95,yy,260,102,color=col);c.text(225,yy+31,label,22,col,True,'mm');c.text(225,yy+72,sub,16,MUTED,anchor='mm')
        c.arrow((360,yy+51),(465,yy+51),col);c.box(470,yy,430,102,color=col)
        c.text(685,yy+31,'log conditional future density',21,col,anchor='mm');c.text(685,yy+72,'− log shared reference marginal',19,MUTED,anchor='mm')
    note(c,'Density-ratio interpretations require the ideal contrastive optimum and consistent sampling.')

def ratio(c,p,b,ep):
    heading(c,'Subtract scores to isolate human influence','The same reference distribution cancels algebraically')
    c.text(135,298,'controlled future',28,CYAN,True);c.text(565,298,'− reference',28,MUTED)
    c.text(135,398,'uncontrolled future',28,PURPLE,True);c.text(565,398,'− reference',28,MUTED)
    c.text(88,398,'−',32,INK,True);c.line([(105,451),(887,451)],MUTED,2)
    if b>=1:
        for y in (310,410):c.line([(555,y),(794,y)],RED,4)
    c.text(487,507,'log p(future | human action, context)',24,ep['color'],True,'mm')
    c.text(487,546,'− log p(future | context)',24,ep['color'],True,'mm')
    note(c,'Average over human actions and their futures to obtain conditional mutual information.')

def takeover(c,p,b,ep):
    heading(c,'Three interventions, three different channels','Declared toy example: a single completed outcome need not preserve choice')
    titles=['Blocked','Path cleared','Full takeover']
    for k,title in enumerate(titles):
        x=95+k*292;co=ep['color'] if k==b else MUTED;c.box(x,270,265,290,color=co);c.text(x+132,299,title,22,co,True,'mm')
        for i in range(3):
            start=(x+45,360+i*61);end=(x+218,360+(i if k==1 else 0)*61)
            c.circle(*start,9,COLORS[i],COLORS[i]);c.arrow(start,end,COLORS[i],2)
        c.text(x+132,530,'I = ln 3' if k==1 else 'I = 0',24,co,True,'mm')
    note(c,'Use empowerment alongside the human’s actual objectives; it is a proxy with assumptions.')

def text_scene(c,p,b,ep,mode='text'):
    titles={'text':'Let the human keep the consequential choice','surprisal':'A model probability is a proxy, not an oracle','threshold':'Accumulate surprise until the budget is spent','finetune':'Select a target, then train on that target'}
    heading(c,titles.get(mode,titles['text']),'Invented token probabilities · illustrative, not an LLM measurement')
    tokens=['I','recommend','we','approve','this','request'];probs=[.98,.95,.9,.15,.9,.85]
    budget=[.12,1.5,3.0][b] if mode=='threshold' else 1.5
    result=threshold_prefix(probs,budget)
    for i,(tok,pr) in enumerate(zip(tokens,probs)):
        x=85+i*145;on=i<result['accepted'];co=GREEN if on else GOLD if i==3 else MUTED
        c.box(x,282,130,69,tok,co,size=20);c.text(x+65,375,f'p = {pr:.2f}',19,co,anchor='mm')
    if mode=='finetune':
        for i,(a,s) in enumerate([('offline prefix','I recommend'),('selected target','we'),('supervised update','predict the target')]):
            x=95+i*292;c.box(x,437,260,108,color=COLORS[i]);c.text(x+130,465,a,20,COLORS[i],True,'mm');c.text(x+130,506,s,19,MUTED,anchor='mm')
    else:
        c.line([(110,547),(911,547)],LINE,2)
        pts=[(150+i*145,547-v/3.2*130) for i,v in enumerate(result['cumulative'])]
        c.line(pts,ep['color'],4)
        for i,pt in enumerate(pts):c.circle(*pt,6,ep['color'],ep['color']);c.text(pt[0],pt[1]-24,f'{result["cumulative"][i]:.2f}',17,MUTED,anchor='mm')
        yy=547-budget/3.2*130;c.line([(110,yy),(911,yy)],GOLD,2,True)
        c.text(910,yy-24,f'budget η = {budget:.2f}',18,GOLD,anchor='ra')
    note(c,'The automation stops before the first token that would reach or exceed the surprise budget.' if mode!='finetune' else 'This is selective supervised fine-tuning, not an exact empowerment policy gradient.')

def entropy_scene(c,p,b,ep):
    heading(c,'High action entropy is only an upper bound','Same action distribution; different consequences')
    bars(c,[('Human action entropy H(A)',math.log(2),GOLD),('I(A;Y) with reliable consequences',math.log(2),CYAN),('I(A;Y) with independent outcomes',0,PURPLE)],scale=.75)
    note(c,'The inequality I(A;Y) ≤ H(A) cannot be reversed: uncertainty alone is not control.')

def evaluation(c,p,b,ep,mode):
    configs={
      'evaluation':('Separate evidence for three claims',[('PREPARATION','Do better contexts become reachable?'),('ESTIMATION','Do decoded skills really differ?'),('TRANSFER','Does a downstream task improve?')]),
      'representation_audit':('Audit the representation, not just its size',[('SUFFICIENCY','Does skill decoding still work?'),('INVARIANCE','Do irrelevant changes cancel?'),('SENSITIVITY','Does relevant context remain?')]),
      'assistance_limit':('Assumptions are part of the result',[('MODEL','Specified human action model'),('REWARDS','Specified reward distribution'),('EVALUATION','Human outcomes and task success')]),
      'language_evaluation':('Does the proxy help the person?',[('SIMULATION','Check likelihood calibration'),('HUMAN STUDY','18 people; 78% preference reported'),('SCOPE','Task completion, errors, agency')])}
    title,items=configs[mode];heading(c,title,'Read the source and scope notes in the companion')
    for i,(label,body) in enumerate(items):
        x=95+i*292;co=ep['color'] if b==i else MUTED;c.box(x,282,264,261,color=co)
        c.text(x+132,324,f'0{i+1}',37,co,True,'mm');c.text(x+132,377,label,19,co,True,'mm');c.wrap(x+22,420,body,222,21,INK)
        if i==b:c.line([(x+24,523),(x+24+216*(.5+.5*math.sin(p*6)**2),523)],co,3)
    note(c,'The examples explain mechanisms. They do not reproduce the papers’ experimental results.')


def scene(c,visual,p,b,ep):
    fns={'channel':channel,'skills':skills,'bound':bound,'reward':reward,'training':training,'options':options,'simplex':simplex,'radius':radius,'capacity':capacity_scene,'geometry_limit':geometry_limit,'two_policy':two_policy,'decoder':decoder,'value':value,'rollout':rollout,'bottleneck':bottleneck,'features':features,'factorization':factorization,'invariance':invariance,'human':human,'human_prior':human_prior,'contrastive':contrastive,'ratio':ratio,'takeover':takeover,'entropy':entropy_scene}
    if visual in fns:fns[visual](c,p,b,ep)
    elif visual in ('forward','backward'):equivalence(c,p,b,ep,visual=='backward')
    elif visual in ('text','surprisal','threshold','finetune'):text_scene(c,p,b,ep,visual)
    elif visual in ('evaluation','representation_audit','assistance_limit','language_evaluation'):evaluation(c,p,b,ep,visual)
    else:raise ValueError('Unknown scene '+visual)
