---
title: 'The BACCO Simulation Project: A baryonification emulator with Neural Networks'

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here
# and it will be replaced with their full name and linked to their profile.
authors:
  - admin
  - Raul Angulo 
  - Sergio Contreras 
  - Lurdes Ondaro-Mallea
  - Marcos Pellejero-Ibañez
  - Matteo Zennaro 


date: '2020-11-30T00:00:00Z'

# Schedule page publish date (NOT publication's date).
publishDate: '2023-01-01T00:00:00Z'

# Publication type.
# Accepts a single type but formatted as a YAML list (for Hugo requirements).
# Enter a publication type from the CSL standard.
publication_types: ['article-journal']

# Publication name and optional abbreviated publication name.
publication: In Monthly Notices of the Royal Astronomical Society
publication_short: MNRAS

abstract: We present a neural-network emulator for baryonic effects in the non-linear matter power spectrum. We calibrate this emulator using more than 50, 000 measurements in a 15-dimensional parameters space, varying cosmology and baryonic physics. Baryonic physics is described through a baryonification algorithm, that has been shown to accurately capture the relevant effects on the power spectrum and bispectrum in stateof-the-art hydrodynamical simulations. Cosmological parameters are sampled using a cosmology-rescaling approach including massive neutrinos and dynamical dark energy. The specific quantity we emulate is the ratio between matter power spectrum with baryons and gravity-only, and we estimate the overall precision of the emulator to be 1 − 2%, at all scales 0.01 < k < 5h Mpc−1 , and redshifts 0 < z < 1.5. We also obtain an accuracy of 1 − 2%, when testing the emulator against a collection of 74 different cosmological hydrodynamical simulations and their respective gravity-only counterparts. We show also that only one baryonic parameter, namely Mc, which set the gas fraction retained per halo mass, is enough to have accurate and realistic predictions of the baryonic feedback at a given epoch. Our emulator will become publicly available in http://www.dipc.org/bacco.

# Summary. An optional shortened abstract.
summary: We introduce a powerful neural-network emulator that precisely predicts how baryons reshape the cosmic matter power spectrum across cosmologies and feedback models. Trained on over 50,000 simulations, it achieves 1–2% accuracy and reveals that a single key parameter, that captures the essence of baryonic effects—bringing unprecedented speed and precision to cosmological modeling.

tags:
  - Cosmology, Baryons, Simulations , Machine Learning

# Display this page in the Featured widget?
featured: true

# Standard identifiers for auto-linking
hugoblox:
  ids:
    doi: 10.1093/mnras/staa1478 

# Custom links
links:
  - type: preprint
    provider: arxiv
    id: 2011.15018
  - type: code
    url: https://bitbucket.org/rangulo/baccoemu/src/master/
  - type: video
    url: https://www.youtube.com/watch?v=hIXDmuQ25zM&t=1927s


# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
image:
  caption: 'Upper panles: Baryonic impact on the matter power spectrum at z = 0, defined as S(k) = PHydro/PGro, as measaured in hydrodynamical simulations. The solid line represents the best-fitting models otained with our emulator. Lower panels: ratio between hydrodynamical simulations and our model, considering 7, 3, and 1 free parameters'
  focal_point: ''
  preview_only: false

---
