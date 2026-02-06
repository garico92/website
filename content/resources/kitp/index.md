---
title: 'Simultaneous Constraints on Cosmology and Astrophysics with Multi-Wavelength Observations'

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here
# and it will be replaced with their full name and linked to their profile.
authors:
  - admin

date: '2026-02-06T00:00:00Z'

# Schedule page publish date (NOT publication's date).
publishDate: '2026-02-06T00:00:00Z'

# Publication type.
# Accepts a single type but formatted as a YAML list (for Hugo requirements).
# Enter a publication type from the CSL standard.
publication_types: ['speech']

abstract: Modern cosmological surveys are specifically designed to characterise the dark energy equation of state and dark matter power spectrum, and place tight constraints on the neutrino mass. Unfortunately, a large part of the data is currently discarded because of the lack of robust theoretical modelling on small scales. The main uncertainties are associated with baryonic physics and galaxy formation. In my talk, I will introduce a novel hybrid framework, capable of optimally analysing the incoming sky surveys, leveraging a hybrid approach that mixes post-processed N-body simulations and machine learning. The post-processed baryonification technique allows the accurate and fast prediction of multiple cosmic fields in a wide range of astrophysical scenarios, by flexibly painting galaxies and gas on top of the dark matter. Artificial neural networks are used to train fast emulators of 2pt and higher-order statistics as a function of cosmological and astrophysical scenarios. The emulators can be seamlessly embedded in a Bayesian pipeline for multi-probe analyses, which can include cosmic shear, galaxy clustering, diffuse X-ray, thermal Sunyaev-Zel’dovich effect and their cross-correlation.

summary: Video and slides of the talk at New Synergies in Multi-Probe Cosmology conference, Kavli Institute for Theoretical Physics (KITP), Santa Barbara, California. 

design:
  # Default section spacing
  spacing: '6rem'
  background:
    image: 
      filename: "sim.png"
    image_darken: 1   # optional: dark overlay for readability (0–1)
    image_parallax: true # optional: parallax scrolling
    text_color_light: false # makes text white for contrast


tags:
  - Cosmology
  - Baryons

# Display this page in the Featured widget?
featured: true


# Custom links
links:
  - type: slides
    url: https://online.kitp.ucsb.edu/online/cmblss-c26/arico/
  - type: conference
    url: https://www.kitp.ucsb.edu/activities/cmblss-c26



# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
image:
  caption: ''
  focal_point: ''
  preview_only: false

---
