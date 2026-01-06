---
title: "Deep Learning for Accelerated MRI Reconstruction"
shortTitle: "Accelerated MRI"
description: "Developing novel deep learning methods to accelerate MRI acquisition while maintaining diagnostic image quality, enabling faster scans and improved patient comfort."
status: active
startDate: 2022-01-15
topics:
  - MRI
  - deep learning
  - image reconstruction
  - compressed sensing
featuredImage: "../../assets/images/projects/mri-placeholder.svg"
investigators:
  - sarah-chen
  - emily-zhang
funding:
  - agency: NIH
    grantNumber: R01-EB029xxx
  - agency: NSF
    grantNumber: CAREER-2134xxx
featured: true
order: 1
draft: false
---

## Overview

Magnetic Resonance Imaging (MRI) is a powerful diagnostic tool, but long scan times limit its accessibility and patient comfort. This project develops deep learning approaches that enable high-quality imaging from significantly undersampled data, reducing scan times by 4-8x.

## Research Goals

1. **Physics-Informed Networks**: Develop neural network architectures that incorporate MRI physics constraints
2. **Self-Supervised Learning**: Train models without requiring fully-sampled ground truth data
3. **Real-Time Reconstruction**: Enable on-scanner reconstruction for immediate clinical feedback

## Methods

We combine unrolled optimization networks with learned regularizers, leveraging both the forward model of MRI acquisition and data-driven priors learned from large imaging datasets.

## Impact

Our methods have been validated on clinical datasets and are being translated to clinical practice in collaboration with partner hospitals.
