---
title: Media
summary: Pictures, videos and animations from my research — cosmological simulations of the large-scale structure of the Universe and the baryonification method.
date: 2026-09-24
hide_date: true
reading_time: false
show_date_updated: false
share: false
profile: false
toc: false

# Shown under every item. Web versions and sizes come from manifest.json (scripts/make_web_media.py).
media_license: '[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — free to reuse for non-commercial purposes, with credit: *Giovanni Aricò*'
---

Visualisations from my research: cosmological simulations of the large-scale structure of the Universe and the baryonification method to include baryons on top of the dark matter distribution. Light versions are shown here; the full-quality originals can be downloaded with the button under each item. Feel free to use them in talks, articles and outreach, with credit.

{{< media-nav >}}

{{< media-item
    id="nenya-composite-zoom"
    title="From the cosmic web to a galaxy cluster"
    alt="Matter distribution in the BACCO Nenya simulation: the full 512 Mpc/h box, with three successive zoom-ins onto its most massive galaxy cluster."
    note="The simulation was run on MareNostrum 5 at the Barcelona Supercomputing Center. We acknowledge the Red Española de Supercomputación (RES) for supporting the generation of the simulations through project AECT-2025-2-0044."
>}}
The matter distribution in **Nenya**, one of the BACCO simulations: an N-body simulation of a cubic volume 512 Mpc/*h* on a side, evolved with 1536³ particles using the Gadget code. The large panel shows the whole box, where matter is arranged in the cosmic web of filaments, knots and voids. The three insets zoom in progressively (see the scale bars) on the most massive galaxy cluster in the simulation, until its substructures become visible.

Open the image in the deep-zoom viewer to explore all 4096 × 4096 pixels.
{{< /media-item >}}

{{< media-item
    id="nenya-orbit-dive"
    title="A dive into the most massive cluster"
    alt="Animation: the camera orbits the Nenya simulation box, then dives through the cosmic web into its most massive galaxy cluster."
    note="The simulation was run on MareNostrum 5 at the Barcelona Supercomputing Center. We acknowledge the Red Española de Supercomputación (RES) for supporting the generation of the simulations through project AECT-2025-2-0044."
>}}
A fly-through of the same Nenya simulation (512 Mpc/*h* box, 1536³ particles, Gadget N-body code). The camera first circles the entire simulated volume, then plunges through the cosmic web towards the most massive galaxy cluster in the box.
{{< /media-item >}}

{{< media-item
    id="baryonification"
    title="Baryonification, step by step"
    alt="Animation of the baryonification algorithm on a single halo: density and cumulative-mass profiles of the gravity-only, galaxy, gas and baryonified components, and the resulting radial displacement of the particles."
>}}
Gravity-only N-body simulations accurately capture the dark matter distribution, but do not consider baryonic processes and astrophysics: gas condensing into galaxies, gas outflows from supermassive black holes accretion and supernovae explosions. **Baryonification** adds these effects in post-processing. For each halo, it models the density profiles of galaxies, gas and dark matter; comparing the resulting cumulative mass profile with the gravity-only one tells how far the two distributions are. Particles inside halos are then displaced in a radial way accordingly: inwards to build the central galaxy, outwards where gas is expelled, at a negligible computational cost. The animation follows these steps for a single halo. On the upper panels the density (left) and cumulative mass (right) profiles are shown, whereas in the bottom panel a halo slice is shown in logarithmic scale. The effects of baryons are exaggerated for visualisation purposes.

The algorithm is described in [Aricò et al. 2020, MNRAS 495, 4800](https://doi.org/10.1093/mnras/staa1478) ([arXiv:1911.08471](https://arxiv.org/abs/1911.08471)); see also [its page on this site]({{< relref "/publications/bcm" >}}). It was later extended to gas pressure and the thermal Sunyaev–Zel'dovich effect in [Aricò & Angulo 2024]({{< relref "/publications/baryonification_sz" >}}).
{{< /media-item >}}

{{< media-item
    id="periodic-boundary-conditions"
    title="Periodic boundary conditions"
    alt="Animation of a cosmological simulation box: particles start on a regular lattice and cluster under gravity; a red particle leaves through one face of the box and re-enters from the opposite one, while the box is shown repeated in a 3 × 3 × 3 grid of identical copies."
>}}
A cosmological simulation follows a finite cubic volume, so what happens at its edges? The initial conditions are set on a regular lattice of particles, which are displaced with Lagrangian perturbation theory; the particles then move according to Newtonian gravity. **Follow the red particle**: when it passes through one side of the box, it reappears on the opposite side. This is what *periodic boundary conditions* mean: the box is tiled in an infinite, self-repeating grid of identical copies of itself (only the nearest ones are drawn here), so a particle leaving one box is replaced by its own image entering from the neighbouring one.
{{< /media-item >}}

{{< media-item
    id="rescaling-four-acts"
    title="Turning one universe into another"
    alt="Film in four acts: two simulated universes with 20% and 60% matter grow from the same initial pattern; their density fluctuations are compared scale by scale; stretching lengths by 3 and going back to redshift 2 makes the matter-rich universe match the other one, filament by filament."
    note="Dark-matter-only particle-mesh simulations with 512³ particles and Zel'dovich initial conditions; Ω<sub>m</sub> = 0.2, σ<sub>8</sub> = 0.80 (1000 Mpc/*h* box) and Ω<sub>m</sub> = 0.6, σ<sub>8</sub> = 0.94 (333 Mpc/*h* box)."
>}}
Two simulated universes start from exactly the same random pattern. In one, matter makes up 20% of the cosmic budget (Ω<sub>m</sub> = 0.2, the rest is dark energy); in the other, 60%. The second box is three times smaller, and is drawn to scale. Gravity then builds the cosmic web, and by today the matter-rich universe is far lumpier. **Can one be turned into the other?**

The film shows the *cosmology-rescaling* method of [Angulo & White (2010)](https://arxiv.org/abs/0912.4277) in four acts: the two boxes evolve; their lumpiness is compared scale by scale through σ(*R*), the typical density contrast on a scale *R*; the two curves are matched by **stretching every length** of the Ω<sub>m</sub> = 0.6 universe by a factor 3 and **going back in time** to the moment (redshift *z* = 2) when its fluctuations were still small enough; finally, the same two steps are applied to the simulation itself. Slide across the last frame: it is the same cosmic web, filament by filament, with pixel-by-pixel differences of about 1%. This is one of the ideas behind the fast emulators of the [BACCO project]({{< relref "/resources/baccoemu" >}}): a handful of simulations can be turned into many cosmologies.
{{< /media-item >}}

{{< media-item
    id="rescaling-three-universes"
    title="How to change the cosmology of your simulation"
    alt="Three simulated boxes side by side: a 20%-matter universe, an 80%-matter universe of the same size, and a four times smaller 80%-matter box that, stretched four times and seen at redshift 2, becomes the twin of the first."
    note="Dark-matter-only particle-mesh simulations with 512³ particles and Zel'dovich initial conditions; Ω<sub>m</sub> = 0.2, σ<sub>8</sub> = 0.80 (1000 Mpc/*h* box) and Ω<sub>m</sub> = 0.8, σ<sub>8</sub> = 0.75 (1000 and 250 Mpc/*h* boxes)."
>}}
Two simulations, same random seed, same box size, same moment in time: the only difference is **how much metter there is in the universe**, 20% or 80% (Ω<sub>m</sub> = 0.2 and 0.8). More matter gives a finer, more evolved cosmic web. Then a third box appears, with Ω<sub>m</sub> = 0.8 again but four times smaller (250 Mpc/*h*), drawn to scale. Stretched ×4 and seen at an earlier time (*z* = 2), it becomes the twin of the Ω<sub>m</sub> = 0.2 universe. Gravity does not know about cosmology, it only cares how clumpy (linear) matter is, scale by scale.
{{< /media-item >}}

{{< media-item
    id="zeldovich-displacement"
    title="Zel'dovich displacement to picture Zel'dovich"
    alt="Animation: a cosmological simulation starts from a uniform distribution of matter; gravity builds the cosmic web, and by today the dark matter draws a portrait of Yakov B. Zel'dovich."
    note="Dark-matter-only particle-mesh simulation with 512³ particles in a 1000 Mpc/*h* box (Ω<sub>m</sub> = 0.2, σ<sub>8</sub> = 0.80), Zel'dovich initial conditions at *z* = 5. Shown: a 60 Mpc/*h* slab, then the projection through the whole box."
>}}
Every cosmological simulation starts in the same way: particles placed on a regular grid are nudged by the **Zel'dovich approximation**, which moves each of them along a straight line, by an amount that grows with the density fluctuations. Usually these initial displacements are drawn at random, with the statistics of the early Universe. Here the large-scale part was **computed backwards** instead: which displacement field, once gravity has worked from redshift 5 to today, ends up drawing a picture? The smaller scales are still random, so the face is made of filaments, knots and voids, like the real cosmic web. The result is a portrait of Yakov B. Zel'dovich (1914–1987), drawn by gravity and started with his own approximation.

How it is done: the designed displacement changes only across the image, so its evolution is a two-dimensional problem. It is found with optimal transport (how to move matter from a uniform grid to the picture at the least cost), followed by a few rounds of "shooting": run the simulation, compare the final density with the picture, correct the initial displacement, repeat. Notice that the portrait is already faintly visible at early times: it is hidden in the initial conditions.
{{< /media-item >}}

{{< media-item
    id="folding-explainer"
    title="Folding the box: small-scale power with a small FFT"
    badge="Work in progress"
    alt="Explainer animation: a simulation slab with a 16 × 16 Fourier mesh, the Fourier modes the mesh can see, and the measured power spectrum; the box is folded two, four and eight times, and each fold extends the measurement to smaller scales."
    note="Projected 20 Mpc/*h* slab of a 512³ particle-mesh simulation (Ω<sub>m</sub> = 0.1, *z* = 0). Method: [Jenkins et al. (1998)](https://arxiv.org/abs/astro-ph/9709010); [Colombi et al. (2009)](https://arxiv.org/abs/0811.0313). This animation is still being developed."
>}}
The **power spectrum** *P*(*k*) measures how much structure there is on each scale. It is computed with a fast Fourier transform (FFT) on a mesh, and a coarse mesh is blind to scales smaller than its cells (beyond its *Nyquist frequency*). **Folding** gets around this without a bigger mesh: cut the box into 2 × 2 pieces (2 × 2 × 2 in 3D) and stack them on top of each other. Only the waves that fit a whole number of times into the smaller box survive, so the same 16 × 16 mesh now reaches twice as far in *k*. Fold again (×4, ×8), keep each measurement only where it is reliable, and stitch them together: the full spectrum, down to small scales, from a tiny FFT.
{{< /media-item >}}
