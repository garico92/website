---
# Leave the homepage title empty to use the site title
title: ''
date: 2022-10-24
type: landing

design:
  # Default section spacing
  spacing: '6rem'
  background:
    image: 
      filename: "sim.png"
    image_darken: 1   # optional: dark overlay for readability (0–1)
    image_parallax: true # optional: parallax scrolling
    text_color_light: true # makes text white for contrast

sections:
  - block: resume-biography-3
    content:
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: admin
      text: ''
      # Show a call-to-action button under your biography? (optional)
      button:
        text: Download CV
        url: https://drive.google.com/file/d/1V-aCVBPsB-IDIA41RHm67a5p_Lzw83Wc/view?usp=sharing
      headings:
        about: ''
        education: ''
        interests: ''
    design:
      # Apply a gradient background
      #css_class: hbx-bg-gradient
      # Avatar customization
      avatar:
        size: large # Options: small (150px), medium (200px, default), large (320px), xl (400px), xxl (500px)
        shape: circle # Options: circle (default), square, rounded
  - block: markdown
    content:
      title: '📚 My Research'
      subtitle: ''
      text: |-
        I aim to answer fundamental questions such as the nature of dark matter and dark energy, the validity of General Relativity at the largest scale of the Universe, and the physics of the formation of galaxies. To do so, I analyse multi-wavelength maps of the large-scale structure of the Universe using Bayesian inference. I optimise the extraction of information by developing new non-linear methods, which combine cosmological simulations, theoretical models of astrophysics, and machine learning techniques.

        Feel free to reach out! 😃
    design:
      columns: '1'
  - block: collection
    id: publications
    content:
      title: Publications
      filters:
        folders:
          - publications
        featured_only: true
    design:
      view: article-grid
      columns: 2
  - block: collection
    content:
      title: Recent Publications
      text: ''
      filters:
        folders:
          - publications
        exclude_featured: false
    design:
      view: citation
  - block: collection
    id: talks
    content:
      title: Talks
      filters:
        folders:
          - events
    design:
      view: article-grid
      columns: 3
  - block: collection
    id: resources
    content:
      title: Resources
      filters:
        folders:
          - resources
    design:
      # Choose a layout view
      view: card
      # Reduce spacing
      spacing:
        padding: [0, 0, 0, 0]
---
