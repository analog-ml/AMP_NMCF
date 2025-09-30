You: 
Here are ready-to-run SPICE netlists (ngspice / HSPICE-compatible) you can drop into your simulator to do a VGS → ID characterization. I provide a simple NMOS test and a PMOS test, with small VDS (50 mV) for the *linear-region* gm/ID-style characterization and a note how to switch to saturation if you want. Change device W/L, model params or VGS range to match your process.

---

# NMOS — VGS / ID sweep (linear-region, VDS = 50 mV)

```pgsql
* NMOS VGS-ID characterization (linear region)
* Run with: ngspice nmos_vgs_id.sp or HSPICE compatible

.options nomod post
.temp 27

* DC supply that sets Vds (drain to source). Positive drain, source at 0.
VDS nd 0 DC 0.05        ; VDS = 50 mV (linear region)

* Gate sweep source (will be swept by .dc)
VG ng 0 DC 0

* MOSFET: Mname Drain Gate Source Bulk Model L=W=
M1 nd ng 0 0 nmos L=1u W=10u

* Simple level=1 model (replace with foundry BSIM model for accuracy)
.model nmos NMOS (level=1 VTO=0.7 KP=50u GAMMA=0.0 PHI=0.6)

* Sweep gate from 0 -> 1.8 V in 10 mV steps
.dc VG 0 1.8 0.01

* Print the drain-source current through VDS and node voltages
.print dc I(VDS) V(ng) V(nd)

.end
```

Notes:

-   `I(VDS)` is the current through the VDS voltage source (positive = flowing into the source of the voltage source). In many SPICE flavors drain current may show as negative depending on sign convention — check your simulator.
    
-   Use small `VDS` (e.g., 50 mV) to measure the channel-current vs. VGS in the *linear* region for gm/ID work. For saturation use `VDS = 0.5V` (or ~VDD) to measure saturation ID.
    

---

# PMOS — VGS / ID sweep (linear-region, VDS = -50 mV)

```pgsql
* PMOS VGS-ID characterization (linear region)
.options nomod post
.temp 27

* For PMOS use negative polarity supplies/values
VDSp pd 0 DC -0.05      ; VDS = -50 mV (drain to source)
VGp pg 0 DC 0

* PMOS device: drain gate source bulk (bulk at 0)
M1p pd pg 0 0 pmos L=1u W=10u

.model pmos PMOS (level=1 VTO=-0.7 KP=20u GAMMA=0.0 PHI=0.6)

* Sweep gate from 0 -> -1.8 V
.dc VGp 0 -1.8 -0.01

.print dc I(VDSp) V(pg) V(pd)

.end
```

---

# Helpful tips & quick extracts

-   To use a real foundry model: replace the `.model ...` lines with your foundry `.include bsim`/`.model` block. For ngspice you can also use `.include foundry.sp`.
    
-   To measure the absolute drain current in A regardless of sign, you can post-process the printed current (|I(VDS)|).
    
-   To extract threshold/Ids:
    
    -   Find the VGS where ID crosses a target (e.g., 100 µA) with `.measure` or by exporting the DC table.
        
    -   Example (ngspice/HSPICE style `.measure` for DC):  
        `.measure dc Id_at_vgs param I(VDS)` — this records the current for each sweep point; you can then parse the output or use `.meas` find commands if your SPICE supports them.
        
-   To compute gm/ID at each point: run the sweep with two close VG values and compute derivative `gm ≈ ΔID / ΔVG` or use numerical differentiation in post-processing (Python, Excel).
    
-   If you want *saturation* VGS-ID curves, set `VDS` to a large value (e.g., 0.5 V or VDD) instead of 50 mV.
    
-   Adjust `W` and `L` to your device size. W/L heavily affects ID and the shape of the curve.
    

