---
title: "An example journal article"
authors:
- admin
- Raul Angulo
date: "2024-06-03T00:00:00Z"

# Schedule page publish date (NOT publication's date).
publishDate: "2024-06-10T00:00:00Z"

# Publication type.
# Accepts a single type but formatted as a YAML list (for Hugo requirements).
# Enter a publication type from the CSL standard.
publication_types: ["article-journal"]

# Publication name and optional abbreviated publication name.
publication: "Astronomy & Astrophysics"
publication_short: "A&A"

abstract: Baryonification algorithms model the impact of galaxy formation and feedback on the matter field in gravity-only simulations by adopting physically motivated parametric prescriptions. In this paper, we extend these models to describe gas temperature and pressure, allowing for a self-consistent modelling of the thermal Sunyaev-Zel'dovich effect, weak gravitational lensing, and their cross-correlation, down to small scales. We validate our approach by showing that it can simultaneously reproduce the electron pressure, gas, stellar, and dark matter power spectra as measured in all BAHAMAS hydrodynamical simulations. Specifically, with only two additional free parameters, we can fit the electron pressure auto- and cross-power spectra at 10% while reproducing the suppression in the matter power spectrum induced by baryons at the per cent level, for different active galactic nuclei (AGN) feedback strengths in BAHAMAS. Furthermore, we reproduce BAHAMAS convergence and thermal Sunyaev Zel'dovich angular power spectra within 1% and 10% accuracy, respectively, down to ℓ = 5000. When used jointly with cosmological rescaling algorithms, the baryonification presented here allows for a fast and accurate exploration of cosmological and astrophysical scenarios. Therefore, it can be employed to create mock catalogues, lightcones, and large training sets for emulators aimed at interpreting forthcoming multi-wavelength observations of the large-scale structure of the Universe.

# Summary. An optional shortened abstract.
summary: We designed an enhanced baryonification model that captures not only how galaxy formation shapes matter but also how it heats and pressurizes gas — unlocking realistic predictions for lensing and the thermal Sunyaev-Zel’dovich effect. With just two extra parameters, it matches state-of-the-art hydrodynamical simulations at percent-level precision, paving the way for fast, accurate modeling of the Universe’s small-scale structure.

tags:
- Cosmology, Baryons
featured: false

hugoblox:
  ids:
    arxiv: 2406.01672

links:
  - type: pdf
    url: https://arxiv.org/pdf/2406.01672
  - type: code
    url: https://github.com/HugoBlox/hugo-blox-builder

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
image:
  caption: 'Cosmic density fields obtained by applying our baryonification to an N-body simulation: dark matter, galaxies, bound gas in hydrostatic equilibrium, and gas ejected by AGN feedback'
  focal_point: ""
  preview_only: false
---
