# -*- coding: utf-8 -*-
"""512-bit analytic all-level certificate for w, D, e and Duhamel tails."""
import json
from pathlib import Path
from flint import arb, ctx

ctx.prec = 512
A = arb
HERE = Path(__file__).resolve().parent

delta=A("4.669201609102990671853"); d2=delta**2; d4=delta**4
AU0=A("0.414037999086273"); t=A("4.7911"); s8=t/delta**8
K=A("284"); M3=A("1834"); nh=A("6.331193600692640")
q2=A("111.550905120798913")
nDT=A("22.19"); nDT2=A("193.63")
rho=A("7.5e-4"); linf=A("1.104854250319780")
L1=nDT+K*rho; L2=nDT2+2*nDT*K*rho+(K*rho)**2
lKrh=linf*K*rho
pperp=A("2.808542"); Cs=A("5.495835"); mu=A("0.35")

def up(x): return x.upper()
def lo(x): return x.lower()
def us(x): return str(up(x))
def ls(x): return str(lo(x))

# Lemma W.  At pair boundaries w<=C0*s^2; at the intermediate step
# w<=C1*s^2.  A pair can only start with s<=s8/delta.
C0=A("1000"); C1=A("1280"); sp=s8/delta
first_single_coeff=(K*nh**2/2)/d2
one_coeff=(nDT*C0+K*(nh+C0*sp)**2/2)/d2
c1_unscaled=nDT*C0+K*(nh+C0*sp)**2/2
pair_coeff=(nDT2*C0+nDT*K*(nh+C0*sp)**2/2+
            K*(delta*nh+c1_unscaled*sp)**2/2)/d4
w_invariant=(up(first_single_coeff)<=C0 and up(one_coeff)<=C1 and up(pair_coeff)<=C0)

# With C1 valid at every step, Q_j<=QCOEF*s_j^2.  Summing every possible
# reverse distance r=0,1,... gives a genuine infinite Duhamel series.
QCOEF=(q2+K*nh*C1*s8+K*C1**2*s8**2/2+
       M3*(nh+C1*s8)**3*s8/6)
ratioP=mu/d2
kernel_sum=pperp+Cs*ratioP/(1-ratioP)
P_ALL=QCOEF*s8**2*kernel_sum
P_TARGET=A("3e-7")

# Lemma DE. Same-parity level increments satisfy V_{n+2}<=B V_n,
# B=[[q,0],[c,p]], because Phi(s/delta^2)<=Phi(s)/delta^4.
q=L2/d4; p=1/d2; c=lKrh*(delta+L1)/d4

def Phi(s): return q2*s*s+M3*nh**3*s**3/6

def exit_de(k):
    n=k-7; s=t/delta**(k+1); D=Phi(s); e=linf*D; j=0
    if n%2:
        e=delta*e+lKrh*D; D=L1*D; j=1
    while j<n:
        e=delta**2*e+lKrh*(delta+L1)*D; D=L2*D; j+=2
    return D,e

finite=[]; Dstar=A(0); estar=A(0); kD=kE=None
for k in range(8,502):
    D,e=exit_de(k); finite.append((k,D,e))
    if up(D)>up(Dstar):Dstar,kD=D,k
    if up(e)>up(estar):estar,kE=e,k

tail_rows={}
for k0 in (500,501):
    D0,e0=exit_de(k0)
    Dsum=D0*q/(1-q)
    esum=e0*p/(1-p)+c*D0/((1-p)*(1-q))
    tail_rows[str(k0)]={
      "D_at_base_upper":us(D0),"e_at_base_upper":us(e0),
      "sum_D_same_parity_after_base_upper":us(Dsum),
      "sum_e_same_parity_after_base_upper":us(esum),
      "therefore_each_later_D_upper":us(Dsum),
      "therefore_each_later_e_upper":us(esum)}

payload={
 "precision_bits":512,
 "w_pair_invariant":{
   "C0_pair_boundary":"1000","C1_intermediate":"1280",
   "first_single_coeff_upper":us(first_single_coeff),
   "intermediate_coeff_upper":us(one_coeff),
   "pair_output_coeff_upper":us(pair_coeff),"pass":bool(w_invariant)},
 "duhamel_all_levels":{
   "Qcoef_upper":us(QCOEF),"geometric_ratio_mu_over_delta2_upper":us(ratioP),
   "kernel_sum_upper":us(kernel_sum),"P_all_levels_upper":us(P_ALL),
   "target":"3e-7","pass":bool(up(P_ALL)<=P_TARGET)},
 "DE_geometric_matrix":{
   "q_L2_over_delta4_upper":us(q),"p_delta_minus2_upper":us(p),
   "c_offdiag_upper":us(c),"spectral_radius_upper":us(q if up(q)>=up(p) else p),
   "finite_checked":"k=8..501","D_star_upper":us(Dstar),"D_star_k":kD,
   "e_star_upper":us(estar),"e_star_k":kE,"tails_after_500_501":tail_rows,
   "pass":bool(up(q)<1 and up(p)<1)},
 "all_pass":bool(w_invariant and up(P_ALL)<=P_TARGET and up(q)<1 and up(p)<1)}
(HERE/"level_tail_certificate.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
with (HERE/"level_tail_certificate.log").open("w",encoding="utf-8") as f:
    lines=[
      "PREC=512",
      "W: first<=%s <=1000; intermediate<=%s <=1280; pair<=%s <=1000; pass=%s"%(us(first_single_coeff),us(one_coeff),us(pair_coeff),w_invariant),
      "Duhamel: Qcoef<=%s ratio<=%s P_all<=%s <=3e-7 pass=%s"%(us(QCOEF),us(ratioP),us(P_ALL),up(P_ALL)<=P_TARGET),
      "DE: q<=%s p<=%s c<=%s D*<=%s(k=%s) e*<=%s(k=%s)"%(us(q),us(p),us(c),us(Dstar),kD,us(estar),kE),
      "tail even after 500: sumD<=%s sumE<=%s"%(tail_rows['500']['sum_D_same_parity_after_base_upper'],tail_rows['500']['sum_e_same_parity_after_base_upper']),
      "tail odd after 501: sumD<=%s sumE<=%s"%(tail_rows['501']['sum_D_same_parity_after_base_upper'],tail_rows['501']['sum_e_same_parity_after_base_upper']),
      "ALL_PASS=%s"%payload["all_pass"]]
    f.write("\n".join(lines)+"\n");print("\n".join(lines))
if not payload["all_pass"]:raise SystemExit(1)
