"""Exact finite-channel teaching experiments, in nats (Python standard library).

Run: python3 code/empowerment_lab.py
Tests: python3 -m unittest discover -s code -p 'test_*.py'
These examples illustrate the papers; they do not reproduce neural RL agents.
Rows of W are p(outcome | input); p is the input distribution.
"""
import json, math


def entropy(p):
    return -sum(x*math.log(x) for x in p if x>0)


def validate(W,p):
    assert W and len(p)==len(W) and len(W[0])>0
    for row in [p,*W]:
        assert all(math.isfinite(x) and x>=0 for x in row)
        assert abs(sum(row)-1)<1e-9
    assert all(len(row)==len(W[0]) for row in W)


def mutual_information(W,p):
    validate(W,p)
    marginal=[sum(p[z]*W[z][j] for z in range(len(p))) for j in range(len(W[0]))]
    return sum(p[z]*v*math.log(v/marginal[j]) for z,row in enumerate(W) for j,v in enumerate(row) if p[z]>0 and v>0)


def capacity(W,tol=1e-10,max_iter=10000):
    """Blahut–Arimoto with a certified finite-channel lower/upper gap.

    I(p,W) <= capacity <= max_z KL(W_z || pW).
    At a nonconverged stopping point the returned gap remains explicit.
    """
    p=[1/len(W)]*len(W);validate(W,p)
    for it in range(max_iter):
        marginal=[sum(p[z]*W[z][j] for z in range(len(p))) for j in range(len(W[0]))]
        D=[sum(v*math.log(v/marginal[j]) for j,v in enumerate(row) if v>0) for row in W]
        lo=sum(a*b for a,b in zip(p,D));hi=max(D)
        if hi-lo<=tol or it==max_iter-1:break
        update=[a*math.exp(d-hi) for a,d in zip(p,D)];total=sum(update)
        p=[a/total for a in update]
    return dict(value=lo,upper=hi,gap=hi-lo,prior=p,iterations=it+1)


def symmetric(k,noise):
    return [[(1-noise)*(i==j)+noise/k for j in range(k)] for i in range(k)]


def posterior(W,p):
    validate(W,p)
    marginal=[sum(p[z]*W[z][j] for z in range(len(p))) for j in range(len(W[0]))]
    return [[p[z]*W[z][j]/marginal[j] if marginal[j]>0 else p[z] for z in range(len(p))] for j in range(len(W[0]))]


def variational_bound(W,p,decoder_quality=1.):
    """q blends the exact posterior with the uniform distribution.

    The expectation is exact here. A learned critic on finite data has no
    pointwise lower-bound guarantee merely because this identity exists.
    """
    post=posterior(W,p);k=len(p)
    q=[[(1-decoder_quality)/k+decoder_quality*v for v in row] for row in post]
    return sum(p[z]*W[z][j]*math.log(q[j][z]/p[z]) for z in range(k) for j in range(len(W[0])) if p[z]*W[z][j]>0)


def nuisance_channel(W,q):
    return [[v*r for v in row for r in q] for row in W]


def assistance_channel(clearance,takeover):
    base=[[1.,0,0],[1-clearance,clearance,0],[1-clearance,0,clearance]]
    return [[(1-takeover)*v+takeover*(j==0) for j,v in enumerate(row)] for row in base]


def threshold_prefix(probabilities,budget):
    assert budget>=0 and all(0<p<=1 for p in probabilities)
    cumulative=[];total=0.;accepted=0
    for p in probabilities:
        total-=math.log(p);cumulative.append(total)
        if total<budget:accepted+=1
    return dict(accepted=accepted,cumulative=cumulative,sequence_floor=math.exp(-budget))


def examples():
    W=symmetric(4,.2);p=[.25]*4
    return dict(diayn=dict(information=mutual_information(W,p),bound=variational_bound(W,p,.7),capacity=capacity(W)),
        independent_nuisance=dict(before=mutual_information(W,p),after=mutual_information(nuisance_channel(W,[.1,.9]),p)),
        assistance=dict(blocked=capacity(assistance_channel(0,0)),clear=capacity(assistance_channel(1,0)),takeover=capacity(assistance_channel(1,1))),
        language=threshold_prefix([.98,.95,.9,.15,.9,.85],1.5))

if __name__=='__main__': print(json.dumps(examples(),indent=2))
