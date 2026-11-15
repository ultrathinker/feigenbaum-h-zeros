# -*- coding: utf-8 -*-
"""Probe: measure affine image radius R vs |c| of denominator x_{2^m} over
arc disks, to choose N (arc count) so that the arg-variation bound
2*arcsin(R/|c|) < pi/2 holds. Throwaway exploration, NOT a deliverable."""
import math, sys
from pathlib import Path
import flint

ROOT = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")
sys.path.insert(0, str(ROOT / "w35" / "x4_walk_sonnet"))
import x4_common as xc

flint.ctx.prec = 200
A = flint.arb
C = flint.acb

# minimal affine algebra, S=1 (u is the only symbol)
K = 1
ZERO_ACB = flint.acb(0)
ZERO_ARB = flint.arb(0)

def mag_ub(z): return z.abs_upper()
def mag_lb(z): return z.abs_lower()

class AF:
    __slots__=('c','a','r')
    def __init__(self,c,a,r): self.c=c; self.a=a; self.r=r

def l1(vec):
    s=ZERO_ARB
    for v in vec: s=s+mag_ub(v)
    return s
def af_const(c): return AF(c,[ZERO_ACB],ZERO_ARB)
def af_add(x,y): return AF(x.c+y.c,[x.a[0]+y.a[0]],x.r+y.r)
def af_add_const(x,k): return AF(x.c+k,x.a,x.r)
def af_scale_const(x,k): return AF(x.c*k,[x.a[0]*k],x.r*mag_ub(k))
def af_mul(x,y):
    return AF(x.c*y.c,[x.c*y.a[0]+y.c*x.a[0]],
              l1(x.a)*l1(y.a)+mag_ub(x.c)*y.r+mag_ub(y.c)*x.r+l1(x.a)*y.r+l1(y.a)*x.r+x.r*y.r)
def af_horner(coeffs,w):
    b=af_const(ZERO_ACB)
    for k in range(len(coeffs)-1,-1,-1):
        b=af_mul(b,w); b=af_add(b,coeffs[k])
    return b
def af_abs_lower(x): return mag_lb(x.c)-l1(x.a)-x.r

# build G1/H1 carrying g/h coefficient uncertainty as remainder r (cert_slice base style)
G1=[AF(xc.tc_g[k],[ZERO_ACB],flint.arb(xc.RHO_G)) for k in range(xc.M)]
H1=[AF(xc.tc_h[k],[ZERO_ACB],flint.arb(xc.RHO_H)) for k in range(xc.M)]
INV_R=flint.acb(1)/flint.acb(xc.r_disc)

def dsdu(m):
    delta_af=AF(xc.DELTA_pt,[flint.acb(xc.RHO_D) if False else ZERO_ACB],flint.arb(xc.RHO_D))
    # delta^{-m} with delta uncertainty as remainder
    dm=delta_af
    for _ in range(m-1): dm=af_mul(dm,delta_af)
    inv,q=af_recip_local(dm)
    return af_scale_const(inv,xc.AU0)

def af_recip_local(y):
    cy_lo=mag_lb(y.c); rho=l1(y.a)+y.r
    if cy_lo<=ZERO_ARB or not(rho<cy_lo): return None,rho/cy_lo
    q=rho/cy_lo; invc=flint.acb(1)/y.c
    return AF(invc,[-y.a[0]*invc*invc],y.r/(cy_lo*cy_lo)+(q*q/(1-q))/cy_lo),q

def orbit_den_arc(u_mid, rho_arc, m):
    """Affine orbit over arc disk, return x_{2^m} affine form."""
    s_af=af_mul(dsdu(m), AF(u_mid,[flint.acb(rho_arc)],ZERO_ARB))
    lev_den=1<<m; lev_num=1<<(m+1)
    x=af_const(ZERO_ACB); xden=None
    for n in range(lev_num):
        xx=af_add_const(af_mul(x,x),flint.acb(-1))
        w=af_scale_const(xx,INV_R)
        rz= (mag_ub(w.c)+l1(w.a)+w.r)
        if not(rz<1): raise RuntimeError(f"domain rz={rz} at n={n}")
        vg=af_horner(G1,w); vh=af_horner(H1,w)
        x=af_add(vg,af_mul(vh,s_af))
        if n+1==lev_den: xden=x
    return xden

def probe(label,cre,cim,rho,m):
    uc=C(A(str(cre)),A(str(cim)))
    rho=A(str(rho))
    print(f"\n=== {label}  uc=({cre},{cim}) rho={rho} m={m} ===")
    for N in [32]:
        worst_ratio=0.0; worst_R=0.0; worst_clo=float('inf'); worst_darg=0.0; dom_ok=True
        for j in range(N):
            th_lo=2*math.pi*j/N; th_hi=2*math.pi*(j+1)/N
            th_mid=0.5*(th_lo+th_hi)
            umc=uc+rho*(C(math.cos(th_mid),math.sin(th_mid)))
            rho_arc=2*float(rho)*math.sin((th_hi-th_lo)/4)*(1+1e-9)+0.01
            try:
                xd=orbit_den_arc(umc,flint.arb(repr(rho_arc)),m)
            except RuntimeError as e:
                dom_ok=False; break
            clo=float(mag_lb(xd.c)); R=float(l1(xd.a)+xd.r)
            ablo=float(af_abs_lower(xd))
            ratio=R/clo if clo>0 else float('inf')
            import math as _m
            darg=2*_m.asin(min(1.0,ratio)) if ratio<=1 else float('inf')
            if ratio>worst_ratio: worst_ratio=ratio
            if R>worst_R: worst_R=R
            if clo<worst_clo: worst_clo=clo
            if darg>worst_darg: worst_darg=darg
        print(f"  N={N:3d} dom_ok={dom_ok} worst_R/c|={worst_ratio:.4f} worst_R={worst_R:.3e} "
              f"min|c|={worst_clo:.3e} worst_darg={worst_darg:.4f} (need <{math.pi/2:.4f})")

probe("Z40","8.36818444963026","3.42161554921713","0.1",7)
