<div align="center">

# Advanced & Parallel Programming

**Parallel Mandelbrot generator in C with OpenMP · Expression tree interpreter in Python**

![C](https://img.shields.io/badge/C-OpenMP-A8B9CC?logo=c&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)

*University projects — Advanced & Parallel Programming · University of Trieste (UniTS)*

</div>

---

## Projects

### 1. Mandelbrot Set Generator — C + OpenMP

Parallel computation of the Mandelbrot fractal over a pixel grid, written to a PGM grayscale image.

**Key techniques**
- `#pragma omp parallel for collapse(2)` over the full pixel grid
- Logarithmic colour mapping for smooth gradient output
- Custom PGM image writer (`pgm.c`)

**Build & run**

```bash
cd mandelbrot
make
./main output.pgm 1000 800
# args: <output file> <max iterations> <image height (must be even)>
```

> Requires GCC with OpenMP support. On macOS use `brew install libomp`.

**Quick Start (Docker)**

```bash
docker compose up --build
# output.pgm is written inside the container; mount a volume to retrieve it:
docker run --rm -v $(pwd)/out:/out mandelbrot-img ./main /out/output.pgm 1000 800
```

---

### 2. Expression Tree Interpreter — Python

A stack-based parser and evaluator for arithmetic expressions, implemented as a full AST class hierarchy.

**Key features**
- Custom `Stack` with typed exceptions (`EmptyStackException`, `IndexOutOfBoundsException`, …)
- `Expression` class hierarchy: literals, variables, binary operators, array access
- `from_program()` class method — parses token sequences into an AST
- Fully self-contained, no external dependencies

**Run**

```bash
python expression-tree/expr.py
```

---

## Project Structure

```
.
├── mandelbrot/
│   ├── main.c          # Entry point — arg parsing, OpenMP loop, PGM output
│   ├── mandelbrot.c/h  # Complex Mandelbrot iteration
│   ├── pgm.c/h         # PGM image writer
│   └── Makefile
├── expression-tree/
│   └── expr.py         # Stack, AST nodes, parser (~600 lines)
├── Dockerfile
├── docker-compose.yml
└── .gitignore
```

---

## Tech Stack

`C (C11)` · `OpenMP` · `GCC` · `Python 3.11` · `Docker`
