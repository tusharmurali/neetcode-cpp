# 455. Assign Cookies

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/assign-cookies/>  
- **NeetCode:** <https://neetcode.io/problems/assign-cookies>  
- **Video:** <https://www.youtube.com/watch?v=JW8fgvoxPTg>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each child, we want to find the smallest cookie that can satisfy them. Using the smallest sufficient cookie for each child leaves larger cookies available for greedier children. We iterate through children, and for each one, scan all cookies to find the smallest one that works. Once a cookie is used, we mark it as unavailable.

```cpp
class Solution {
public:
    int findContentChildren(vector<int>& g, vector<int>& s) {
        sort(s.begin(), s.end());
        int res = 0;

        for (int i : g) {
            int minIdx = -1;
            for (int j = 0; j < s.size(); j++) {
                if (s[j] < i) continue;

                if (minIdx == -1 || s[minIdx] > s[j]) {
                    minIdx = j;
                }
            }

            if (minIdx != -1) {
                s[minIdx] = -1;
                res++;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m + m \log m)$
- Space complexity: $O(1)$ or $O(m)$ depending on the sorting algorithm.

> Where $n$ is the size of the array $g$ and $m$ is the size of the array $s$.

## 2. Two Pointers - I

If both arrays are sorted, we can use two pointers to match children with cookies efficiently. Start with the least greedy child. If the current cookie is too small, move to the next larger cookie. Once we find a cookie that works, both pointers advance. This greedy matching ensures we never waste a cookie on a child who could be satisfied with a smaller one.

```cpp
class Solution {
public:
    int findContentChildren(vector<int>& g, vector<int>& s) {
        sort(g.begin(), g.end());
        sort(s.begin(), s.end());

        int i = 0, j = 0;
        while (i < g.size()) {
            while (j < s.size() && g[i] > s[j]) {
                j++;
            }
            if (j == s.size()) break;
            i++;
            j++;
        }
        return i;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n + m \log m)$
- Space complexity: $O(1)$ or $O(n + m)$ depending on the sorting algorithm.

> Where $n$ is the size of the array $g$ and $m$ is the size of the array $s$.

## 3. Two Pointers - II

This is a cleaner version of the two-pointer approach. We iterate through cookies one by one. For each cookie, if it can satisfy the current child, we move to the next child. Either way, we move to the next cookie. The key insight is that once a child is satisfied, we never revisit them, and we never skip a potentially useful cookie.

```cpp
class Solution {
public:
    int findContentChildren(vector<int>& g, vector<int>& s) {
        sort(g.begin(), g.end());
        sort(s.begin(), s.end());

        int i = 0;
        for (int j = 0; i < g.size() && j < s.size(); j++) {
            if (g[i] <= s[j]) i++;
        }
        return i;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n + m \log m)$
- Space complexity: $O(1)$ or $O(n + m)$ depending on the sorting algorithm.

> Where $n$ is the size of the array $g$ and $m$ is the size of the array $s$.
