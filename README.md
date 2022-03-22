# Browian Dynamics 
(BOAP algorithm: *BJ Leimkuhler and C Matthews Appl. Math. Res. eXpress 2013, 34–56 (2013); J. Chem. Phys. 138, 174102 (2013)*)

![Simulation](./sim_G0.5_T1.0_N10_F1.0_dt0.005.gif)


<img src="https://render.githubusercontent.com/render/math?math=\dot{p}}=-\gamma p + \sigma\dot{w}">

where:
<br>
1. <img src="https://render.githubusercontent.com/render/math?math=\gamma p"> is the friction force. It simulates the effect of the bath (solvent) on the system.
<br>
2. <img src="https://render.githubusercontent.com/render/math?math=\sigma \dot{w}"> is the random force, which is represented by the derivate of a Wiener process <img src="https://render.githubusercontent.com/render/math?math=w">.
<br>
3. <img src="https://render.githubusercontent.com/render/math?math=\sigma =\sqrt{2\gamma m k_B T}"> governs the strenght of the random force (it is related to the friction coefficient via the fluctuation-dissipation theorem)
<br>
<img src="https://render.githubusercontent.com/render/math?math=dp=-\gamma p dt +\sigma dw">

<br>

<img src="https://render.githubusercontent.com/render/math?math=\vec{p}\left(t+\delta t \right)}= \exp(-\gamma\delta t)\vec{p}\left(t \right)} + \sqrt{1-\exp(-2\gamma\delta t)}\sqrt{m k_B T} \vec{G}">

