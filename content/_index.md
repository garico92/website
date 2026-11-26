---
# Leave the homepage title empty to use the site title
title: ''
date: 2022-10-24
type: landing

design:
  # Default section spacing
  spacing: '4rem'
  background:
    # Video background — file must live in assets/media/.
    # Rendered by layouts/_partials/hooks/body-end/video-background.html
    video:
      filename: "lss.mp4"
    image_darken: 0.55        # 0..1 dark overlay for readability
    text_color_light: true    # lightens body text for contrast on the video

# Blocks: layouts/_partials/hbx/blocks/<name>/block.html (styles at the end of assets/css/custom.css)
sections:
  - block: profile-hero
    content:
      username: admin
      eyebrow: Cosmology · Large-scale structure · Simulations
      text: |
        I am a computational cosmologist. I study the nature of **dark matter** and **dark energy**, test **General Relativity** on the largest scales, and model how **galaxy formation** reshapes the distribution of matter in the Universe.

        I build non-linear models that combine cosmological simulations, astrophysical models and machine learning, and use them in Bayesian analyses of multi-wavelength surveys such as **Euclid** and the **Dark Energy Survey**. Feel free to reach out!
      buttons:
        - { text: Download CV, url: uploads/Arico_CV.pdf, icon: arrow-down-tray, primary: true }
        - { text: Publications, url: publications/, icon: document-text }
        - { text: Get in touch, url: 'mailto:arico@bo.infn.it', icon: envelope }
      stats: true

  - block: research-themes
    id: research
    content:
      eyebrow: What I work on
      title: Research
      subtitle: Four threads that run through my work, from simulations to survey data.
      items:
        - title: Baryons in the cosmic web
          text: Gas cooling, star formation and feedback from supernovae and black holes move matter around, up to scales that weak-lensing surveys measure. With the **baryonification** method I paint these effects on top of gravity-only simulations, at a negligible cost — now also for gas pressure and the thermal Sunyaev–Zel'dovich effect.
          image: { page: /media, resource: baryonification_poster.webp, fit: contain }
          links:
            - { text: The method, page: /publications/bcm }
            - { text: tSZ extension, page: /publications/baryonification_sz }
            - { text: Animation, url: 'media/#baryonification' }
        - title: Emulators & machine learning
          text: Neural networks trained on suites of simulations predict the non-linear matter power spectrum, its baryonic suppression and higher-order statistics in milliseconds, across cosmologies including massive neutrinos and dynamical dark energy. They are public in **BACCOemu**; a newer one predicts baryonic effects on the matter bispectrum for Euclid.
          image: { page: /resources/baccoemu, resource: featured.jpg, fit: contain }
          links:
            - { text: BACCOemu, page: /resources/baccoemu }
            - { text: Paper, page: /publications/baryonification_emulator }
        - title: Cosmic shear & multi-probe analyses
          text: Small scales of weak-lensing data are usually thrown away. Modelling them with emulators and baryonification, I analysed **DES Y3** cosmic shear down to small scales, constraining cosmology and baryons at once. In **Euclid** I co-lead the key project on baryonic physics with DR1 data.
          image: { page: /publications/desy3_analysis, resource: featured.jpg, fit: contain }
          links:
            - { text: DES Y3 analysis, page: /publications/desy3_analysis }
            - { text: All papers, url: publications/ }
        - title: Cosmological simulations
          text: I run and analyse large N-body simulations — the BACCO project, the 72-million-core-hour Euclid Emulator 3 suite, and new runs on **MareNostrum 5** — and use cosmology-rescaling to turn one simulated universe into another.
          image: { page: /media, resource: nenya-composite-zoom_1600.webp }
          links:
            - { text: Pictures & films, url: media/ }
            - { text: Lecture on simulations, page: /resources/lecture_colours }

  - block: news
    id: news
    content:
      eyebrow: News
      title: Latest
      count: 6
      talks: 5

  - block: featured-pubs
    id: publications
    content:
      eyebrow: Papers
      title: Selected publications
      subtitle: A few papers with a summary on this site. The [complete list](publications/) has all of them, with arXiv, journal and ADS links.
      count: 4
      archive: { text: All publications, link: publications/ }

  - block: talk-videos        # layouts/_partials/hbx/blocks/talk-videos/block.html
    id: talks
    content:
      eyebrow: Talks
      title: Recorded talks
      subtitle: Seminars and conference talks — click to play here.
      count: 3
      archive:
        text: All talks & videos
        link: talks/

  - block: media-teaser
    id: media
    content:
      eyebrow: Media
      title: From my simulations
      subtitle: Short films made from my N-body simulations. They play here; the [Media page](media/) has the descriptions, downloads and a deep-zoom picture. Free to use with credit.
      ids: nenya-orbit-dive, rescaling-four-acts, baryonification, zeldovich-displacement
      more: { text: Pictures and films, link: media/ }

  - block: resource-cards
    id: resources
    content:
      eyebrow: Resources
      title: Code, lectures & slides
      count: 4
      archive: { text: All resources, link: resources/ }
---
