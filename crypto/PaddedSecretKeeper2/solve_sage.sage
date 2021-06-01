#!/usr/bin/env sage
from Crypto.Util.number import long_to_bytes as l2b
n = 23800642165490855754178829343527013065268263358621563298519117639997756879578773948017712320565918237264257437120558506856679893210135416466682587950310910796773794286455433463268863543652573507281592643029409503192425761745770696760868895657290592113056341404566294944674672807291294106736174949601885946548811783603824319104263011154866856617729352133736005537708707250423314208644022353527843872496405544403218416224519756835579277085487200485198925042088065936253046491299255105203680444279867101482097238135308102588204456256403889823041172318839274075624560964072690001161218275849380725202332126958952456314317
C1= 0x060ab072d5d56d678769282fca6694ce1aa5f21bda61db9d511cbc52383a4dcc8db066fd0a96d511becb26cb333a4d5d8a0bed0b923d55eb4c1dbf708e191662da86bae668408d39af965e87e96ba971be695ca2448d7dda21a152a425a512f86a7f4f73d9ee6cbcbb1378d2f401d99327745fc39daac63039ace85196673775f36a2ca104b82032705d00d65c4d7ade92847c7dfbce088c525581d58e8c2122e5cf5cfdc431aa977f141425305ac086929dc0c61081df01cf8396762969d3df7d7462f525898e1ce0ad16d7db0778c50b0c4bad16f59edcfc193321855dcb9e40cf9243eb8940
C2 = 0x060ab072d5d56d678769282fca6694ce1aa5f21bda61db9d511cbc52383a4dcc8db066fd0a96d511becb26cb333a4d5d8a0bed0b923d55eb4c1dbf708e191662da86bae668408d39af965f3e251e252d6603146eb277201603c3f8e0010cd2f7098bdaff74ee963611ad709a8890a45761f8aa08f7369ae20f58e27160e6076f69658714832bde6e608df18d977907690256d8b9b5df4c4d3c917dc2e67d319b73ffbd1c714d4776ec2d225bb2d6b9717ca42fee6c59131890a147382c50470eb6a7784c40ba1e5fa9d0e6dfe991837398190c3dfe9c9a7e738c46c10af304f1ab267cf354c5a5


e = 3

n1 = n

 
PRxy.<x,y> = PolynomialRing(Zmod(n1))
PRx.<xn> = PolynomialRing(Zmod(n1))
PRZZ.<xz,yz> = PolynomialRing(Zmod(n1))
 
g1 = x**e - C1
g2 = (x + y)**e - C2
 
q1 = g1.change_ring(PRZZ)
q2 = g2.change_ring(PRZZ)
 
h = q2.resultant(q1)
# need to switch to univariate polynomial ring
# because .small_roots is implemented only for univariate
h = h.univariate_polynomial() # x is hopefully eliminated
h = h.change_ring(PRx).subs(y=xn)
h = h.monic()
 
roots = h.small_roots(X=2**40, beta=0.3)
assert roots, "Failed1"
 
diff = roots[0]
if diff > 2**32:
    diff = -diff
    C1, C2 = C2, C1
print("Difference:", diff)

x = PRx.gen() # otherwise write xn
g1 = x**e - C1
g2 = (x + diff)**e - C2
 
# gcd
while g2:
    g1, g2 = g2, g1 % g2
 
g = g1.monic()
assert g.degree() == 1, "Failed 2"
 
# g = xn - msg
msg = -g[0]
# convert to str
h = hex(int(msg))[2:].rstrip("L")
h = "0" * (len(h) % 2) + h
print(h)