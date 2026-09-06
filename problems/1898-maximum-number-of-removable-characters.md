# 1898. Maximum Number of Removable Characters

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-number-of-removable-characters/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-number-of-removable-characters>  
- **Video:** <https://www.youtube.com/watch?v=NMP3nRPyX5g>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We want to find the maximum number of characters we can remove from `s` (in the order given by `removable`) while keeping `p` as a subsequence of `s`.

The simplest approach is to remove characters one at a time. After each removal, check if `p` is still a subsequence. Once `p` is no longer a subsequence, stop and return the count of successful removals.

```cpp
class Solution {
public:
    int maximumRemovals(string s, string p, vector<int>& removable) {
        int n = s.size(), m = p.size();
        unordered_set<int> marked;
        int res = 0;

        for (int removeIdx : removable) {
            marked.insert(removeIdx);

            int sIdx = 0, pIdx = 0;
            while (pIdx < m && sIdx < n) {
                if (marked.find(sIdx) == marked.end() && s[sIdx] == p[pIdx]) {
                    pIdx++;
                }
                sIdx++;
            }

            if (pIdx != m) break;
            res++;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(k * (n + m))$
- Space complexity: $O(k)$

> Where $n$ and $m$ are the lengths of the given strings $s$ and $p$ respectively. $k$ is the size of the array $removable$.

## 2. Binary Search + Hash Set

If removing the first `k` characters still allows `p` to be a subsequence, then removing fewer than `k` characters will also work. Conversely, if removing `k` characters breaks the subsequence property, removing more will certainly break it too.

This monotonic property makes binary search applicable. We search for the largest `k` such that after removing `removable[0..k]`, `p` remains a subsequence.

```cpp
class Solution {
public:
    int maximumRemovals(string s, string p, vector<int>& removable) {
        int res = 0, l = 0, r = removable.size() - 1;

        while (l <= r) {
            int m = (l + r) / 2;
            unordered_set<int> removed(removable.begin(), removable.begin() + m + 1);

            if (isSubseq(s, p, removed)) {
                res = max(res, m + 1);
                l = m + 1;
            } else {
                r = m - 1;
            }
        }

        return res;
    }

private:
    bool isSubseq(string& s, string& subseq, unordered_set<int>& removed) {
        int i1 = 0, i2 = 0;
        while (i1 < s.size() && i2 < subseq.size()) {
            if (removed.count(i1) || s[i1] != subseq[i2]) {
                i1++;
                continue;
            }
            i1++;
            i2++;
        }
        return i2 == subseq.size();
    }
};
```

**Complexity**

- Time complexity: $O((n + m) * \log k)$
- Space complexity: $O(k)$

> Where $n$ and $m$ are the lengths of the given strings $s$ and $p$ respectively. $k$ is the size of the array $removable$.

## 3. Binary Search

Instead of using a hash set to track removed indices (which adds overhead), we can directly modify the string by replacing removed characters with a placeholder character (like `'#'`). This avoids hash lookups during the subsequence check.

The binary search logic remains the same, but the subsequence check becomes simpler since we just compare characters, skipping any `'#'` naturally by checking for equality.

```cpp
class Solution {
public:
    int maximumRemovals(string s, string p, vector<int>& removable) {
        int l = 0, r = removable.size();
        int n = s.size(), m = p.size();

        while (l < r) {
            int mid = l + (r - l) / 2;
            string tmpS = s;

            for (int i = 0; i <= mid; i++) {
                tmpS[removable[i]] = '#';
            }

            if (isSubseq(tmpS, p)) {
                l = mid + 1;
            } else {
                r = mid;
            }
        }

        return l;
    }

private:
    bool isSubseq(const string& s, const string& p) {
        int i1 = 0, i2 = 0, n = s.size(), m = p.size();

        while (i1 < n && i2 < m) {
            if (s[i1] == p[i2]) {
                i2++;
            }
            i1++;
        }
        return i2 == m;
    }
};
```

**Complexity**

- Time complexity: $O((n + m) * \log k)$
- Space complexity: $O(n)$

> Where $n$ and $m$ are the lengths of the given strings $s$ and $p$ respectively. $k$ is the size of the array $removable$.
