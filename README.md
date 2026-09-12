# Algorithms | From Intuition to Code

A visual, interactive algorithms course by Allan Allemand.

This repository is ready for GitHub Pages. It currently contains:

- a complete course landing page;
- a full first chapter on sorting;
- interactive visualizers for insertion sort, merge sort, and quicksort;
- correctness arguments, complexity summaries, exercises, and revealable answers;
- responsive layouts for desktop and mobile;
- MathJax support for mathematical notation.

## Publish on GitHub Pages

1. Create a new GitHub repository, for example `algorithms`.
2. Upload all files from this folder to the repository root.
3. Open `Settings → Pages`.
4. Under `Build and deployment`, choose `Deploy from a branch`.
5. Select the `main` branch and `/ (root)`.
6. Save.

Your site will appear at:

`https://YOUR-USERNAME.github.io/algorithms/`

If you instead use a repository named exactly `YOUR-USERNAME.github.io`, the site will be published at the root domain.

## Structure

```text
algorithms-course/
├── index.html
├── sorting.html
├── assets/
│   ├── app.js
│   ├── styles.css
│   └── favicon.svg
├── .nojekyll
└── README.md
```

The project deliberately uses plain HTML/CSS/JavaScript so it works on GitHub Pages without a build system.

## Suggested next chapters

Binary Search, Two Pointers, Prefix Sums, Hashing, Stacks & Queues, Trees & Heaps, Graphs, DSU, Greedy Algorithms, Dynamic Programming, and Strings.
