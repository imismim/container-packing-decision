# PackCont — Bin Packing Algorithm Analyzer

A Django web application for solving and comparing **bin packing problem** algorithms. Built as a laboratory project for studying mathematical methods and operations research under uncertainty.

---

## Features

### Four Bin Packing Algorithms

Each algorithm is run in both **unsorted** and **pre-sorted** (descending) modes:

| Algorithm | Description | Complexity |
|-----------|-------------|------------|
| **NFA** (Next Fit) | Places each item in the current container; opens a new one if it doesn't fit | O(n) |
| **FFA** (First Fit) | Places each item in the first container where it fits | O(n²) |
| **WFA** (Worst Fit) | Places each item in the container with the most remaining space | O(n²) |
| **BFA** (Best Fit) | Places each item in the container with the least remaining space that still fits | O(n²) |

### Multi-Dataset Comparison

- Accepts up to **3 independent item sets** (Items 1, 2, 3) as input
- Runs all algorithms on each dataset individually and on the **combined dataset** (Items 1+2+3)
- Displays the **analytical minimum** containers (theoretical lower bound: `⌈sum / capacity⌉`) for comparison

### 30 Predefined Variants

- Select from **Variant 1–30** for reproducible, preset test cases
- Built-in **Test** variant for quick verification
- **Custom input** mode (`variant-enter`) for entering your own item weights and container capacity

### Performance Metrics

- Tracks and displays the **total operation count** for each algorithm run, including sorting overhead (O(n log n))
- Enables direct comparison of computational complexity across approaches

### Visual Results

- HTML tables showing container-to-item mappings (rows = containers, columns = item indices)
- Separate result tabs for each dataset and the combined dataset
- Side-by-side comparison of unsorted vs. sorted performance

---

## Tech Stack

- **Backend**: Django 6.0.3, Python 3.13
- **Frontend**: Bootstrap 5.3.3
- **Static files**: WhiteNoise
- **Production server**: Gunicorn

---

## Getting Started

**macOS / Linux**
```bash
cd packcont
python -m venv .venv
source .venv/bin/activate
pip install django
python manage.py runserver
```

**Windows**
```bat
cd packcont
python -m venv .venv
.venv\Scripts\activate
pip install django
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and select a variant or enter custom data.

---

## Deploy to Heroku

> Requires [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and a free Heroku account.

```bash
cd packcont                          # directory with manage.py and Procfile

heroku login
heroku create your-app-name

heroku config:set SECRET_KEY='your-strong-secret-key'
heroku config:set ALLOWED_HOSTS='your-app-name.herokuapp.com'

git init                             # if not already a git repo
git add .
git commit -m "initial deploy"

heroku git:remote -a your-app-name
git push heroku main

heroku open
```

No database migrations are required — the app stores no data.

---

## URL Structure

| URL | Description |
|-----|-------------|
| `/` | Variant selection page |
| `/variant-1/` … `/variant-30/` | Predefined test variants |
| `/variant-test/` | Quick test variant |
| `/variant-enter/` | Custom input |
