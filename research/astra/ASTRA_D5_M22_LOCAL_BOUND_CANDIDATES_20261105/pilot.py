"""Fixed two-case M22 real-kernel pilot, rigorous dyadic enclosures.
Not a full-domain certificate. No external dependencies or floating proof arithmetic.
"""
from fractions import Fraction as F
from math import isqrt,comb,factorial,prod
from pathlib import Path
import json,time,hashlib
ROOT=Path(__file__).resolve().parent
CONTRACT=json.loads((ROOT/'contract.json').read_text())
BITS=CONTRACT['precision_bits']; SCALE=1<<BITS
def floor(q):return q.numerator//q.denominator
def ceil(q):return -((-q.numerator)//q.denominator)
class I:
    __slots__=('lo','hi')
    def __init__(self,a=0,b=None,raw=False):
        if raw:self.lo,self.hi=int(a),int(b)
        else:
            a=F(a);b=a if b is None else F(b)
            self.lo=floor(a*SCALE);self.hi=ceil(b*SCALE)
        assert self.lo<=self.hi
    @staticmethod
    def cv(x):return x if isinstance(x,I) else I(x)
    def __add__(self,b):
        b=self.cv(b);return I(self.lo+b.lo,self.hi+b.hi,raw=True)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo,raw=True)
    def __sub__(self,b):return self+-self.cv(b)
    def __rsub__(self,b):return self.cv(b)+-self
    def __mul__(self,b):
        b=self.cv(b)
        if self is b:
            lo=0 if self.lo<=0<=self.hi else min(self.lo*self.lo,self.hi*self.hi)
            hi=max(self.lo*self.lo,self.hi*self.hi)
        else:
            p=(self.lo*b.lo,self.lo*b.hi,self.hi*b.lo,self.hi*b.hi);lo=min(p);hi=max(p)
        return I(lo//SCALE,-((-hi)//SCALE),raw=True)
    __rmul__=__mul__
    def inv(self):
        assert not(self.lo<=0<=self.hi),('division interval crosses zero',self.rec())
        return I((SCALE*SCALE)//self.hi,-((-SCALE*SCALE)//self.lo),raw=True)
    def __truediv__(self,b):return self*self.cv(b).inv()
    def __rtruediv__(self,b):return self.cv(b)*self.inv()
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        if n==0:return I(1)
        if n==1:return self
        a=self**(n//2);a=a*a
        return a*self if n%2 else a
    def sqrt(self):
        assert self.lo>0,('nonpositive root lower bound',self.rec())
        lo=isqrt(self.lo*SCALE);hi=isqrt(self.hi*SCALE)
        if hi*hi<self.hi*SCALE:hi+=1
        assert lo*lo<=self.lo*SCALE and hi*hi>=self.hi*SCALE
        return I(lo,hi,raw=True)
    def cap(self,lo,hi):
        # [lo,hi] must be a mathematically certified physical enclosure.
        b=I(lo,hi);return I(max(self.lo,b.lo),min(self.hi,b.hi),raw=True)
    def rec(self):return [str(F(self.lo,SCALE)),str(F(self.hi,SCALE))]
    def zero(self):return self.lo==self.hi==0

IND=[(i,j) for n in range(5) for i in range(3) for j in range(3) if i+j==n]
class J:
    __slots__=('c',)
    def __init__(self,x=0,c=None):
        self.c={ij:I(0) for ij in IND} if c is None else c
        if c is None:self.c[(0,0)]=I.cv(x)
    @staticmethod
    def cv(x):return x if isinstance(x,J) else J(x)
    @staticmethod
    def var(x,axis):
        r=J(x);r.c[(1,0) if axis==0 else (0,1)]=I(1);return r
    def __add__(self,b):
        b=self.cv(b);return J(c={k:self.c[k]+b.c[k] for k in IND})
    __radd__=__add__
    def __neg__(self):return J(c={k:-self.c[k] for k in IND})
    def __sub__(self,b):return self+-self.cv(b)
    def __rsub__(self,b):return self.cv(b)+-self
    def __mul__(self,b):
        b=self.cv(b);out={}
        for i,j in IND:
            out[i,j]=sum((self.c[a,b0]*b.c[i-a,j-b0] for a in range(i+1) for b0 in range(j+1)),I(0))
        return J(c=out)
    __rmul__=__mul__
    def inv(self):
        out={}
        for i,j in IND:
            if i==j==0:out[i,j]=self.c[i,j].inv();continue
            v=sum((self.c[a,b]*out[i-a,j-b] for a in range(i+1) for b in range(j+1) if a+b),I(0))
            out[i,j]=-v/self.c[0,0]
        return J(c=out)
    def __truediv__(self,b):return self*self.cv(b).inv()
    def __rtruediv__(self,b):return self.cv(b)*self.inv()
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        if n==0:return J(1)
        if n==1:return self
        a=self**(n//2);a=a*a
        return a*self if n%2 else a
    def sqrt(self):
        out={}
        for i,j in IND:
            if i==j==0:out[i,j]=self.c[i,j].sqrt();continue
            v=sum((out[a,b]*out[i-a,j-b] for a in range(i+1) for b in range(j+1)
                   if (a,b)!=(0,0) and (a,b)!=(i,j)),I(0))
            out[i,j]=(self.c[i,j]-v)/(2*out[0,0])
        return J(c=out)
    def cap(self,lo,hi):
        r=J(c=self.c.copy());r.c[0,0]=r.c[0,0].cap(lo,hi);return r
    def zslice(self,n):return [factorial(n)*self.c[i,n] for i in range(3)]

def av(x):return x if isinstance(x,list) else [I.cv(x),I(0),I(0)]
def aa(a,b):return [x+y for x,y in zip(av(a),av(b))]
def am(a,b):
    a,b=av(a),av(b)
    return [sum((a[j]*b[i-j] for j in range(i+1)),I(0)) for i in range(3)]
def asc(a,c):return am(a,c)
def pa(a,b):
    out=[av(0) for _ in range(max(len(a),len(b)))]
    for i in range(len(out)):out[i]=aa(a[i] if i<len(a) else 0,b[i] if i<len(b) else 0)
    return out
def pm(a,b):
    out=[av(0) for _ in range(len(a)+len(b)-1)]
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]=aa(out[i+j],am(x,y))
    return out
def ps(a,b):return [am(x,b) for x in a]
def shift(a,n=1):return [av(0) for _ in range(n)]+a
def scalarpoly(p):return [x[0] for x in p]
def ipadd(a,b):
    return [ (a[i] if i<len(a) else I(0))+(b[i] if i<len(b) else I(0))
            for i in range(max(len(a),len(b)))]
def ipmul(a,b):
    r=[I(0) for _ in range(len(a)+len(b)-1)]
    for i,x in enumerate(a):
        for j,y in enumerate(b):r[i+j]=r[i+j]+x*y
    return r
def ips(a,b):return [x*b for x in a]
def ish(a,n=1):return [I(0) for _ in range(n)]+a

def kernel(ulo,uhi,ll,lh,zl,zh,eps,qcap):
    u=J.var(I(ulo,uhi),0);z=J.var(I(zl,zh),1);lam=J(I(ll,lh))
    mu=(eps*(1-u*u)/(1+u*u)).cap(-1,1)
    a2=(1-mu*mu).cap(0,1)
    dd=a2+(lam*mu-z)**2
    zmax=max(abs(zl),abs(zh))
    dd=dd.cap((ll-zmax)**2,(1+zmax)**2)
    d=dd.sqrt()
    w2=(lam*lam+(1-lam*lam)*mu*mu).cap(ll*ll,1);w=w2.sqrt()
    h=(lam-z*mu).cap(ll-zmax,lh+zmax)
    L=w*d+h
    V=h-lam*dd
    P=(h*h*(2*dd-a2)-2*a2*V*V)/(dd*dd)
    Q0=a2*h*V*V/(dd*dd)
    jac=4*u/(1+u*u)**2
    ac=jac*P/(lam*L);bc=jac*Q0/(lam*L*L)
    q=(a2*((1-lam*lam)*mu+lam*z)**2/(L*L)).cap(0,qcap)
    U=[ac+bc,ac*q-bc]
    Us=[p.zslice(0) for p in U];Uz=[p.zslice(1) for p in U];Uzz=[p.zslice(2) for p in U]
    qa=q.zslice(0);qz=q.zslice(1);qzz=q.zslice(2)
    y=[av(1),qa]
    n2=pa(pa(pm(pm(y,y),Uzz),ps(shift(pm(y,Uz)),asc(qz,-4))),
          pa(ps(shift(Us,2),asc(am(qz,qz),6)),ps(shift(pm(y,Us)),asc(qzz,-2))))
    assert len(n2)==4
    n20=scalarpoly(n2);n2u=[a[1] for a in n2];n2uu=[2*a[2] for a in n2]
    yi=[I(1),qa[0]]
    n4=ipadd(ipadd(ipmul(ipmul(yi,yi),n2uu),ips(ish(ipmul(yi,n2u)),-8*qa[1])),
             ipadd(ips(ish(n20,2),20*qa[1]*qa[1]),ips(ish(ipmul(yi,n20)),-8*qa[2])))
    assert len(n4)==6
    return qa[0],n20,n4

def moment(coeff,r,q):
    # Combine numerator coefficients before q-Horner evaluation.
    N=CONTRACT['moment_N'];terms=[]
    for m in range(N+1):
        terms.append(((-1)**m*comb(r+m-1,m))*sum((a/F(2*(j+m)+1) for j,a in enumerate(coeff)),I(0)))
    finite=terms[-1]
    for a in reversed(terms[:-1]):finite=finite*q+a
    Jd=len(coeff)-1
    beta=[sum((coeff[j]*F(comb(i,j),comb(Jd,j)) for j in range(i+1)),I(0)) for i in range(Jd+1)]
    weights=[F(comb(Jd,i)*2**(Jd-i)*factorial(Jd-i),
               prod(2*(N+1+i+l)+1 for l in range(Jd-i+1))) for i in range(Jd+1)]
    # q^25 is nonnegative; use its exact upper bound on the dyadic interval.
    factor=(I(F(q.hi,SCALE))**(N+1))*comb(r+N,N+1)
    bpos=sum((I(F(max(0,b.hi),SCALE))*wt for b,wt in zip(beta,weights)),I(0))
    bneg=sum((I(F(max(0,-b.lo),SCALE))*wt for b,wt in zip(beta,weights)),I(0))
    mpos=sum((I(F(max(0,a.hi),SCALE))/F(2*(j+N+1)+1) for j,a in enumerate(coeff)),I(0))
    mneg=sum((I(F(max(0,-a.lo),SCALE))/F(2*(j+N+1)+1) for j,a in enumerate(coeff)),I(0))
    lowtail=min((factor*bpos).hi,(factor*mpos).hi)
    hitail=min((factor*bneg).hi,(factor*mneg).hi)
    return I(finite.lo-lowtail,finite.hi+hitail,raw=True),finite,lowtail,hitail

def checks():
    # Interval primitives are checked against exact Fraction arithmetic, not floats.
    for a,b,c,d in [(F(-2),F(3),F(-4),F(5)),(F(1,3),F(2,3),F(2),F(4))]:
        x,y=I(a,b),I(c,d);p=x*y
        assert F(p.lo,SCALE)<=min(a*c,a*d,b*c,b*d)
        assert F(p.hi,SCALE)>=max(a*c,a*d,b*c,b*d)
    x=J.var(I(F(1,2)),0);z=J.var(I(F(1,3)),1)
    ident=(1+x+z)*(1+x+z).inv()
    for ij in IND:
        exact=SCALE if ij==(0,0) else 0
        assert ident.c[ij].lo<=exact<=ident.c[ij].hi
    v=(1+x*x+z*z).sqrt();back=v*v-(1+x*x+z*z)
    assert all(a.lo<=0<=a.hi for a in back.c.values())
    # At the equatorial center the original G-integral gives E22 density zero?
    # No such assumption is made. Only the exact pole q=0 check is used.
    q,n2,n4=kernel(F(0),F(0),F(1,2),F(1,2),F(0),F(0),1,F(2,7))
    assert q.lo==q.hi==0
    assert all(a.lo<=0<=a.hi for a in n2) # j(0)=0.
    return 'primitive_and_jet_checks_pass'

def run():
    print(checks(),flush=True)
    results={'contract':CONTRACT,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'contract_sha256':hashlib.sha256((ROOT/'contract.json').read_bytes()).hexdigest(),'cases':[]}
    for case in CONTRACT['cases']:
        start=time.monotonic();ll,lh=map(F,case['lambda']);zl,zh=map(F,case['z']);qcap=F(case['q_cap'])
        rows=[];total=F(0);midtotal=F(0);curvtotal=F(0);tailtotal=F(0)
        cells=CONTRACT['u_cells'];h=F(1,cells)
        for eps in (-1,1):
            for j in range(cells):
                a,b=F(j,cells),F(j+1,cells);m=(a+b)/2
                qm,nm,_=kernel(m,m,ll,lh,zl,zh,eps,qcap)
                qc,_,nc=kernel(a,b,ll,lh,zl,zh,eps,qcap)
                im,fm,tm,_=moment(nm,4,qm);ic,fc,tc,_=moment(nc,6,qc)
                mid=h*F(fm.lo,SCALE);curv=h**3/24*F(fc.lo,SCALE)
                tail=h*F(tm,SCALE)+h**3/24*F(tc,SCALE)
                low=mid+curv-tail
                total+=low;midtotal+=mid;curvtotal+=curv;tailtotal+=tail
                rows.append({'epsilon':eps,'cell':j,'u':[str(a),str(b)],'midpoint_q':qm.rec(),
                   'cell_q':qc.rec(),'N2_midpoint':[v.rec() for v in nm],'N4_cell':[v.rec() for v in nc],
                   'midpoint_bound':im.rec(),'curvature_bound':ic.rec(),
                   'finite_midpoint_contribution':str(mid),'finite_curvature_contribution':str(curv),
                   'tail_loss':str(tail),'lower_contribution':str(low)})
                if (j+1)%8==0:print(case['name'],eps,j+1,'of',cells,flush=True)
        out={'name':case['name'],'lower':str(total),'finite_midpoint_sum':str(midtotal),
             'finite_curvature_sum':str(curvtotal),'tail_loss':str(tailtotal),
             'meets_minus_400':total>=-400,'elapsed_seconds':time.monotonic()-start,'records':rows}
        results['cases'].append(out)
        (ROOT/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
        print('RESULT',case['name'],'lower_reference',float(total),'mid',float(midtotal),
              'curv',float(curvtotal),'tail',float(tailtotal),'meets_minus_400',total>=-400,flush=True)
    return results
if __name__=='__main__':run()

