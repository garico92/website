---
title: 'Disentangle'

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here
# and it will be replaced with their full name and linked to their profile.
authors:
  - admin
  - Raul Angulo 
  - Matteo Zennaro 
  - Marcos Pellejero-Ibañez


date: '2020-11-30T00:00:00Z'

# Schedule page publish date (NOT publication's date).
publishDate: '2023-01-01T00:00:00Z'

# Publication type.
# Accepts a single type but formatted as a YAML list (for Hugo requirements).
# Enter a publication type from the CSL standard.
publication_types: ['software']

# Publication name and optional abbreviated publication name.
publication:  Astrophysics Source Code Library

abstract: BACCOemu provides a collection of emulators for large-scale structure statistics over a wide range of cosmologies. The emulators provide fast predictions for the linear cold- and total-matter power spectrum, the nonlinear cold-matter power spectrum, and the modifications to the cold-matter power spectrum caused by baryonic physics in a wide cosmological parameter space, including dynamical dark energy and massive neutrinos.

# Summary. An optional shortened abstract.
summary: BACCOemu is a software library providing neural-network emulators for cosmological large-scale structure statistics.

tags:
  - Cosmology, Baryons, Simulations , Machine Learning

# Display this page in the Featured widget?
featured: true

# Standard identifiers for auto-linking
hugoblox:
  ids:
    doi: 2023ascl.soft07010A

# Custom links
links:
  - type: preprint
    provider: arxiv
    id: 2011.15018
  - type: code
    url: https://bitbucket.org/rangulo/baccoemu/src/master/
  - type: documentation
    url: https://baccoemu.readthedocs.io/en/latest/#installation



# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
image:
  caption: 'Upper panles: Baryonic impact on the matter power spectrum at z = 0, defined as S(k) = PHydro/PGro, as measaured in hydrodynamical simulations. The solid line represents the best-fitting models otained with our emulator. Lower panels: ratio between hydrodynamical simulations and our model, considering 7, 3, and 1 free parameters'
  focal_point: ''
  preview_only: false

---
