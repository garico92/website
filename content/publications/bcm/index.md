---
design:
  # Default section spacing
  spacing: '6rem'
  background:
    image: 
      filename: "sim.png"
    image_darken: 1   # optional: dark overlay for readability (0–1)
    image_parallax: true # optional: parallax scrolling
    text_color_light: false # makes text white for contrast
title: 'Modelling the large scale structure of the Universe as a function of cosmology and baryonic physics'

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here
# and it will be replaced with their full name and linked to their profile.
authors:
  - admin
  - Raul Angulo 
  - Carlos Hernández-Monteagudo
  - Sergio Contreras 
  - Matteo Zennaro 
  - Lurdes Ondaro-Mallea
  - Marcos Pellejero-Ibañez
  - Yetli Rosas-Guevara


date: '2020-07-05T00:00:00Z'

# Schedule page publish date (NOT publication's date).
publishDate: '2025-07-01T00:00:00Z'

# Publication type.
# Accepts a single type but formatted as a YAML list (for Hugo requirements).
# Enter a publication type from the CSL standard.
publication_types: ['article-journal']

# Publication name and optional abbreviated publication name.
publication: In Monthly Notices of the Royal Astronomical Society
publication_short: MNRAS

abstract: We present and test a framework that models the 3D distribution of mass in the universe as a function of cosmological and astrophysical parameters. Our approach combines two different techniques; a rescaling algorithm that modifies the cosmology of gravity-only N-body simulations, and a 'baryonification' algorithm that mimics the effects of astrophysical processes induced by baryons, such as star formation and active galactic nuclei (AGN) feedback. We show how this approach can accurately reproduce the effects of baryons on the matter power spectrum of various state-of-the-art hydrodynamical simulations (EAGLE, Illustris, Illustris-TNG, Horizon-AGN, and OWLS, Cosmo-OWLS and BAHAMAS), to better than 1 per cent from very large down to small, highly non-linear, scales (  k∼5hMpc−1 ), and from z = 0 up to z ∼ 2. We highlight that, because of the heavy optimization of our algorithms, we can obtain these predictions for arbitrary baryonic models and cosmology (including massive neutrinos and dynamical dark energy models) with an almost negligible CPU cost. With these tools in hand, we explore the degeneracies between cosmological and astrophysical parameters in the non-linear mass power spectrum. Our findings suggest that after marginalizing over baryonic physics, cosmological constraints inferred from weak gravitational lensing should be moderately degraded.

# Summary. An optional shortened abstract.
summary: We present a fast framework that models the Universe’s 3D mass distribution by combining rescaled N-body simulations with a baryonification algorithm, accurately reproducing baryonic effects on the matter power spectrum. This enables efficient exploration of cosmological and astrophysical parameter degeneracies for weak lensing studies.

tags:
  - Cosmology, Baryons, Simulations

# Display this page in the Featured widget?
featured: true

# Standard identifiers for auto-linking
hugoblox:
  ids:
    doi: 10.1093/mnras/stab1911

# Custom links
links:
  - type: preprint
    provider: arxiv
    id: 1911.08471
  - type: code
    url: https://bitbucket.org/rangulo/baccoemu/src/master/
  - type: video
    url: https://www.youtube.com/watch?v=hIXDmuQ25zM&t=1927s


# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
image:
  caption: 'Modifications to the matter power spectrum at z = 0 caused by baryons, S(k) ≡ P/PGrO. Each panel varies one of the four free parameters of the baryon correction model (Mc , η, β, M1) while keeping the other three fixed at their fiducial value.'
  focal_point: ''
  preview_only: false

---
