# NeetCode C++ Desk

One page for working through the NeetCode 150 / 250 in C++. Search a problem, open it on LeetCode, and see every approach NeetCode teaches, from brute force to optimal, with the C++ code, a short intuition, and the time and space complexity. Copy a solution with one click. Tick problems off as you go.

**Live site:** https://tusharmurali.com/neetcode-cpp/



## What it does

- **Every list.** Blind 75, NeetCode 150, NeetCode 250, or all 700+ problems NeetCode has written up, grouped by pattern in the site's order.
- **Every C++ approach.** Tabs per approach, in NeetCode's order. "Show all" stacks them for comparison. The standalone file from NeetCode's repo is included as a final tab when one exists.
- **Links that matter.** LeetCode, NeetCode (free for the LeetCode Premium ones), and the video walkthrough.
- **Progress.** Solved marks with a progress bar per list and per pattern. Saved in your browser. Export and import as JSON to move between devices.
- **Keyboard.** `/` search, `↑` `↓` or `j` `k` move, `Enter` opens on LeetCode, `1`–`9` picks an approach, `a` shows all, `x` toggles solved.
- **Direct links.** `#1` opens Two Sum, `#217` opens Contains Duplicate.
- **Light and dark.** Follows your system, with a manual toggle.

The whole site is a single `index.html` with the data inlined. Download it and it works offline.

## Also in this repo

- `problems/` has one markdown file per problem with the same content, for reading on GitHub or grepping locally. `INDEX.md` links them all.
- `data.json` is the same data in machine-readable form.

## How it's built

`build.py` pulls the problem list (with NeetCode's own slugs and list membership) from neetcode.io, clones NeetCode's MIT-licensed [solutions repo](https://github.com/neetcode-gh/leetcode), parses the C++ tab of every approach in every article, and renders `template.html` into `index.html`.

```sh
python3 build.py            # fresh build, needs network
python3 build.py --offline  # re-render from .cache/ after editing template.html
```

A GitHub Action rebuilds the site every Monday and commits if NeetCode added or changed anything.

## Credits and license

All problems, explanations, and solutions belong to [NeetCode](https://neetcode.io). They are redistributed here under the MIT license of [neetcode-gh/leetcode](https://github.com/neetcode-gh/leetcode). This project is not affiliated with NeetCode or LeetCode. If you find it useful, NeetCode's courses and Pro plan are how the author gets paid.

The build script and page template in this repo are also MIT licensed. See `LICENSE`.
