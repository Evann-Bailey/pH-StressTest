# pH-StressTest

> **A 4-part stress-testing framework benchmarking structural AI (EGNN) vs. classical biophysics (PROPKA, Hydride-Jax) under geometric and topological degradation.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Summary

Modern structural bioinformatics relies heavily on two distinct paradigms: **classical/empirical physics tools** (e.g., PROPKA, Hydride-Jax) that compute properties via explicit local geometric dependencies, and **structural deep learning models** (ex. Equivariant Graph Neural Networks / pHoptNN) that map 3D molecular graphs into latent vector representations.

This repository provides an experimental framework for stress-testing these tools. By subjecting macromolecular structures (such as Concanavalin A, PDB: `1C57`) to controlled spatial, directional, topological and fragmentation perturbations, this benchmark isolates:
1. **The exact breaking points** where classical empirical lookup tables and distance thresholds fail or crash.
2. **The resilience and latent feature drift** ($\Delta\text{pH}$) in structural EGNNs when surface electrostatics, coordinates and topology are altered.

---

## Benchmark Framework (The 4 Stress Tests)

> **Core Objective:** Evaluate how classical biophysics and machine learning models handle progressive structural degradation across four distinct physical axes.

* **Stress-Strain Curve (Isotropic Noise)**
  * **Perturbation:** Random 3D Gaussian noise ($\sigma = 0.0\text{--}2.0\,\text{Å}$) applied universally across Cartesian coordinates.
  * **Focus:** Identifies the mathematical breaking point where latent vector spaces in Equivariant GNNs filter out noise better than rigid point-distance empirical lookups.

* **Directional Noise ($X, Y, Z$ Single-Axis Noise)**
  * **Perturbation:** Spatial noise restricted to a single Cartesian axis ($\sigma_x, \sigma_y,$ or $\sigma_z$).
  * **Focus:** Isolates Ångström-level sensitivity along individual axes to evaluate how asymmetric resolution (common in Cryo-EM and NMR) decouples empirical lookup tables.

* **Uniformity Scale (Uniform Topological Scaling)**
  * **Perturbation:** Uniform outward scaling of the coordinate matrix ($1\%, 2\%, 5\%, \dots$) relative to the structural centroid.
  * **Focus:** Tests topological vs. distance rigidity. Preserves 3D protein topology while stretching bond lengths out of equilibrium to test hard-coded physical bounds against relational graphs.

* **Structural Memory Loss & Shell Fragmentation**
  * **Perturbation:** Layer-by-layer radial residue peeling from the protein exterior toward the hydrophobic core ($0\%$ to $70\%$).
  * **Focus:** Measures how progressive loss of surface titratable charges (Asp, Glu, Lys, Arg) causes catastrophic software crashes in empirical engines while demonstrating Equivariant GNN stability.

---

## Key Results: Multi-Scale Response to Structural Perturbation

### Comparative Model Trajectories

| Analytical Scale | Paradigm & Tool | Failure Mode / Behavior | Physical Explanation |
| :--- | :--- | :--- | :--- |
| **Micro-Scale** | **PROPKA** *(Empirical)* | **Fatal Execution Crashes** | Hard-coded distance thresholds and lookup tables fail completely under coordinate shift ($\sigma \ge 1.75\,\text{Å}$) or severe shell stripping ($>50\%$), throwing execution exceptions or `NaN` outputs. |
| **Micro-Scale** | **Hydride** *(Geometric)* | **Linear Coordinate Error** | Distance-based hydrogen placement experiences localized distance error at boundary layers, scaling predictably with geometry loss. |
| **Macro-Scale** | **pHoptNN** *(Deep Learning GNN)* | **Near-Zero Predictive Drift** | Equivariant graph representations prove immune to catastrophic execution failure, demonstrating graceful degradation and minimal prediction shift ($\vert{}\Delta\text{pH}\vert{} \approx 0.0$) across extreme noise regimes. |

### Summary of Model Robustness

1. **Rule-Based Fragility (PROPKA & Hydride):**
   * Classical tools rely on strict geometric constraints. Noise or truncation breaks expected distance matrices, leading to execution failures or severe exponential error propagation.
2. **AI Geometric Resilience (pHoptNN GNN):**
   * Message-passing architectures over relational node embeddings preserve global spatial invariants, allowing structural ML models to maintain reliable predictions even on heavily noisy or incomplete experimental structures.

---

## Quick Start & Installation

### 1. Environment Setup
Clone the repository and recreate the Conda environment:

``bash
git clone [https://github.com/YOUR_USERNAME/Benchmarking-Stress-Struc-Perturb-.git](https://github.com/YOUR_USERNAME/pH-StressTest.git)
cd ph-StressTest

# Create and activate environment from environment.yml
conda env create -f environment.yml
conda activate stress_strain_env
## Repository Structure

```text
ph-StressTest/
├── README.md                          <-- Master project overview & documentation
├── environment.yml                    <-- Conda environment export (stress_strain_env)
├── data/
│   ├── raw/                           <-- Baseline input files (1c57.pdb)
│   └── outputs/                       <-- Calculated prediction tables and CSV logs
├── figures/                           <-- Saved high-resolution benchmark plots (.png)
├── notebooks/                         <-- Modular Jupyter Notebooks for each phase
│   ├── Stress_Strain_NoiseFail.ipynb
│   ├── DirectionalNoise.ipynb
│   ├── Memory_Loss.ipynb
│   └── Uniform-Scale.ipynb
└── src/                               <-- Core Python utility modules
    ├── __init__.py
    ├── peeling.py                     <-- Residue-level peeling & water-stripping logic
    └── phoptnn_interface.py           <-- Wrapped model execution pipeline


    ├── peeling.py                 <-- Residue-level peeling & water-stripping logic
    └── phoptnn_interface.py       <-- Wrapped model execution pipeline
