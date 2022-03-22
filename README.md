# Browian Dynamics 
(BOAP algorithm: *BJ Leimkuhler and C Matthews Appl. Math. Res. eXpress 2013, 34–56 (2013); J. Chem. Phys. 138, 174102 (2013)*)

![Simulation](./sim_G0.5_T1.0_N10_F1.0_dt0.005.gif)


```math
\bold{\dot{p}} = -\gamma\bold{p} + \sigma \bold{\dot{w}} 
```

where:
<br>
1. $\gamma\bold{p}$ is the friction force. It simulates the effect of the bath (solvent) on the system.
<br>
2. $\sigma\bold{\dot{w}}$ is the random force, which is represented by the derivate of a Wiener process $\bold{w}$.
<br>
3. $\sigma = \sqrt{2 \gamma m k_B T}$ governs the strenght of the random force (it is related to the friction coefficient via the fluctuation-dissipation theorem)
<br>
$$
d\bold{p} = -\gamma\bold{p} dt + \sigma d\bold{w}
$$

<br>

$$
\bold{p\left(t + \delta t\right)} = \exp(-\gamma\delta t) \bold{p\left(t\right)} + \sqrt{1-\exp(-2\gamma\delta t)}\sqrt{m k_B T} \bold{G}
$$