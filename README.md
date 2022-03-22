# Browian Dynamics 
(BOAP algorithm: *BJ Leimkuhler and C Matthews Appl. Math. Res. eXpress 2013, 34–56 (2013); J. Chem. Phys. 138, 174102 (2013)*)

![Simulation](./sim_G0.5_T1.0_N10_F1.0_dt0.005.gif)

<br>

<!-- $$
\dot{p}=-\gamma p + \sigma\dot{w}
$$ --> 

<div align="center"><img style="background: white;" src="svg\4DqKy5PaJk.svg"></div>

where:
1. <!-- $\gamma p$ --> <img style="transform: translateY(0.1em); background: white;" src="svg\F0ta9KDBiZ.svg">  is the friction force. It simulates the effect of the bath (solvent) on the system.
2. <!-- $\sigma \dot{w}$ --> <img style="transform: translateY(0.1em); background: white;" src="svg\BtGT0Mblt8.svg"> is the random force, which is represented by the derivate of a Wiener process $\bold{w}$">.
3. <!-- $\sigma =\sqrt{2\gamma m k_B T}$ --> <img style="transform: translateY(0.1em); background: white;" src="svg\9qnAURm6Si.svg"> governs the strenght of the random force (it is related to the friction coefficient via the fluctuation-dissipation theorem)
<!-- $dp=-\gamma p dt +\sigma dw$ --> <img style="transform: translateY(0.1em); background: white;" src="svg\kXz0wb5NL3.svg">

With solution:

<!-- $$
p\left(t+\delta t \right) = \exp(-\gamma\delta t)p\left(t \right) + \sqrt{1-\exp(-2\gamma\delta t)}\sqrt{m k_B T} G
$$ --> 

<div align="center"><img style="background: white;" src="svg\xjz8y3RP62.svg"></div>

