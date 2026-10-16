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
