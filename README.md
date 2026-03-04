<<<<<<< HEAD
# CSE4303 Project 1 — Software Rasterizer (Python)

**Goal**: Implement a CPU triangle rasterizer with edge-function coverage, supersampling (SSAA), and bilinear texture filtering.

## Quick Start
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest           # run unit tests
python src/run.py --scene data/triangles_scene.json --out out/p1.png --spp 4
```

## What to Implement
Open `src/rasterizer.py` and complete the TODOs:
- `draw_triangle` — edge tests + barycentric interpolation
- `sample_texture` — nearest + bilinear sampling
- `resolve` — average SSAA samples back to 1× framebuffer

**Optional**: Mipmapping level choice (stub provided).

Grading emphasizes **correctness**, **image quality** (AA), **engineering**, and **write‑up**.
=======
# Project-computer-Graphics
>>>>>>> 9d1b0dfa568a0ca7a460983e4576d20245bd7fc5
