---
title: "DES Y3 cosmic shear down to small scales: constraints on cosmology and baryons"
authors:
- admin
date: "2023-08-07T00:00:00Z"

# Schedule page publish date (NOT publication's date).
publishDate: "2023-08-08T00:00:00Z"

# Publication type.
# Accepts a single type but formatted as a YAML list (for Hugo requirements).
# Enter a publication type from the CSL standard.
publication_types: ["article"]

# Publication name and optional abbreviated publication name.
publication: ""
publication_short: ""

abstract: We present the first analysis of cosmic shear measured in DES Y3 that employs the entire range of angular scales in the data. To achieve this, we build upon recent advances in the theoretical modelling of weak lensing provided by a combination of N-body simulations, physical models of baryonic processes, and neural networks. Specifically, we use BACCOemu to model the linear and nonlinear matter power spectrum including baryonic physics, allowing us to robustly exploit scales smaller than those used by the DES Collaboration. We show that the additional data produce cosmological parameters that are tighter but consistent with those obtained from larger scales, while also constraining the distribution of baryons. In particular, we measure the mass scale at which haloes have lost half of their gas, log Mc = 14.38+0.60-0.56 log(h−1 M⊙), and a parameter that quantifies the weighted amplitudes of the present-day matter inhomogeneities, S8 = 0.799+0.023 −0.015. Our constraint on S8 is statistically compatible with that inferred from the Planck satellite’s data at the 0.9σ level. We find instead a 1.4σ shift in comparison to that from the official DES Y3 cosmic shear, because of different choices in the modelling of intrinsic alignment, non-linearities, baryons, and lensing shear ratios. We conclude that small scales in cosmic shear data contain valuable astrophysical and cosmological information and thus should be included in standard analyses.

# Summary. An optional shortened abstract.
summary: Unlocking the hidden power of small scales, this study delivers the first full-range cosmic shear analysis of DES Y3 data—tightening cosmological constraints and revealing how baryons shape the universe. By harnessing advanced simulations and neural networks, we show that even the tiniest cosmic distortions carry crucial clues about matter distribution and fundamental physics.

tags:
- Large-scale structure of the Universe; Cosmic shear; emulators; 

featured: true

hugoblox:
  ids:
    arxiv: 2303.05537

links:
- type: preprint
  provider: arxiv
  id: 2303.05537
- type: code
  url: https://bitbucket.org/rangulo/baccoemu/src/master/
- type: dataset
  url: http://desdr-server.ncsa.illinois.edu/despublic/
- type: video
  url: https://www.youtube.com/watch?v=023dBECojxM


# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
image:
  caption: 'Constraints on baryonic physics obtained with cosmic shear, compared to several state-of-the-art hydrodynamical simulations.'
  focal_point: ""
  preview_only: false

# Associated Projects (optional).
#   Associate this publication with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `internal-project` references `content/project/internal-project/index.md`.
#   Otherwise, set `projects: []`.
projects:
- internal-project

# Slides (optional).
#   Associate this publication with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides: "example"` references `content/slides/example/index.md`.
#   Otherwise, set `slides: ""`.
slides: ""
---

This analyis was enabled by my previous work on neural networks emulators trained on baryonified N-body simulations, described [here](/publications/conference-paper/).