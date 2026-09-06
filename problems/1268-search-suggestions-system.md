# 1268. Search Suggestions System

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/search-suggestions-system/>  
- **NeetCode:** <https://neetcode.io/problems/search-suggestions-system>  
- **Video:** <https://www.youtube.com/watch?v=D4T2N0yAr20>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each prefix of the search word, we need to find up to three products that match that prefix in lexicographical order. By sorting products first, we guarantee that the first matching products we encounter are the lexicographically smallest. We then scan through all products for each prefix, collecting up to three matches.

```cpp
class Solution {
public:
    vector<vector<string>> suggestedProducts(vector<string>& products, string searchWord) {
        vector<vector<string>> res;
        int m = searchWord.size();
        sort(products.begin(), products.end());

        for (int i = 0; i < m; i++) {
            vector<string> cur;
            for (const string& w : products) {
                if (w.size() <= i) continue;

                bool flag = true;
                for (int j = 0; j <= i; j++) {
                    if (w[j] != searchWord[j]) {
                        flag = false;
                        break;
                    }
                }

                if (flag) {
                    cur.push_back(w);
                    if (cur.size() == 3) break;
                }
            }

            if (cur.empty()) {
                while (i < m) {
                    res.push_back({});
                    i++;
                }
                break;
            }

            res.push_back(cur);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n + m * n)$
- Space complexity:
    - $O(n)$ or $O(1)$ space for the sorting algorithm.
    - $O(m * w)$ space for the output array.

> Where $n$ is the total number of characters in the string array $products$, $m$ is the length of the string $searchWord$, and $w$ is the average length of each word in the given string array.

## 2. Sorting + Binary Search

Once products are sorted, all products sharing a prefix form a contiguous block. Instead of scanning all products for each prefix, we use binary search to find where this block starts. Since the prefix grows character by character, the start position can only move forward, so we keep track of it across iterations.

```cpp
class Solution {
public:
    vector<vector<string>> suggestedProducts(vector<string>& products, string searchWord) {
        vector<vector<string>> res;
        int m = searchWord.size();
        sort(products.begin(), products.end());

        string prefix = "";
        int start = 0;

        for (int i = 0; i < m; i++) {
            prefix += searchWord[i];
            start = binarySearch(products, prefix, start);

            vector<string> cur;
            for (int j = start; j < min(start + 3, (int)products.size()); j++) {
                if (products[j].substr(0, prefix.size()) == prefix) {
                    cur.push_back(products[j]);
                } else {
                    break;
                }
            }

            res.push_back(cur);
        }

        return res;
    }

private:
    int binarySearch(vector<string>& products, string target, int start) {
        int l = start, r = products.size();
        while (l < r) {
            int mid = l + (r - l) / 2;
            if (products[mid] >= target) {
                r = mid;
            } else {
                l = mid + 1;
            }
        }
        return l;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n + m * w * \log N)$
- Space complexity:
    - $O(n)$ or $O(1)$ space for the sorting algorithm.
    - $O(m * w)$ space for the output array.

> Where $n$ is the total number of characters in the string array $products$, $N$ is the size of the array $products$, $m$ is the length of the string $searchWord$, and $w$ is the average length of each word in the given string array.

## 3. Sorting + Binary Search (Built-In Function)

This approach is identical to the previous one, but uses built-in binary search functions provided by the language. Functions like `bisect_left` in Python or `lower_bound` in C++ handle the binary search logic, making the code cleaner and less error-prone.

```cpp
class Solution {
public:
    vector<vector<string>> suggestedProducts(vector<string>& products, string searchWord) {
        vector<vector<string>> res;
        int m = searchWord.size();
        sort(products.begin(), products.end());

        string prefix = "";
        int start = 0;
        for (int i = 0; i < m; i++) {
            prefix += searchWord[i];
            start = lower_bound(products.begin() + start, products.end(), prefix) - products.begin();

            vector<string> cur;
            for (int j = start; j < min(start + 3, (int)products.size()); j++) {
                if (products[j].find(prefix) == 0) {
                    cur.push_back(products[j]);
                } else {
                    break;
                }
            }

            res.push_back(cur);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n + m * w * \log N)$
- Space complexity:
    - $O(n)$ or $O(1)$ space for the sorting algorithm.
    - $O(m * w)$ space for the output array.

> Where $n$ is the total number of characters in the string array $products$, $N$ is the size of the array $products$, $m$ is the length of the string $searchWord$, and $w$ is the average length of each word in the given string array.

## 4. Sorting + Two Pointers

Instead of binary searching for each prefix, we maintain a window `[l, r]` of valid products. As we process each character of the search word, we shrink the window by moving `l` forward past products that do not match at position `i`, and moving `r` backward past products that do not match. The first up to 3 products in the remaining window are our suggestions.

```cpp
class Solution {
public:
    vector<vector<string>> suggestedProducts(vector<string>& products, string searchWord) {
        vector<vector<string>> res;
        sort(products.begin(), products.end());

        int l = 0, r = products.size() - 1;
        for (int i = 0; i < searchWord.size(); i++) {
            char c = searchWord[i];

            while (l <= r && (products[l].size() <= i || products[l][i] != c)) {
                l++;
            }
            while (l <= r && (products[r].size() <= i || products[r][i] != c)) {
                r--;
            }

            vector<string> cur;
            int remain = r - l + 1;
            for (int j = 0; j < min(3, remain); j++) {
                cur.push_back(products[l + j]);
            }

            res.push_back(cur);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n + m * w + N)$
- Space complexity:
    - $O(n)$ or $O(1)$ space for the sorting algorithm.
    - $O(m * w)$ space for the output array.

> Where $n$ is the total number of characters in the string array $products$, $N$ is the size of the array $products$, $m$ is the length of the string $searchWord$, and $w$ is the average length of each word in the given string array.
