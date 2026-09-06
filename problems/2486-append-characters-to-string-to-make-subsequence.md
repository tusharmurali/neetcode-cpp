# 2486. Append Characters to String to Make Subsequence

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/append-characters-to-string-to-make-subsequence/>  
- **NeetCode:** <https://neetcode.io/problems/append-characters-to-string-to-make-subsequence>  
- **Video:** <https://www.youtube.com/watch?v=gKDmO8ZLRD8>  

[← Back to index](../INDEX.md)

## 1. Two Pointers

To make `t` a subsequence of `s` by appending characters, we first need to figure out how much of `t` is already a subsequence of `s`. We can greedily match characters from `t` in `s` from left to right. Once we know how many characters of `t` we can match, the remaining characters must be appended.

The greedy approach works because matching earlier characters in `s` never hurts. If a character from `t` appears multiple times in `s`, taking the first occurrence leaves more room for matching subsequent characters.

```cpp
class Solution {
public:
    int appendCharacters(string s, string t) {
        int i = 0, j = 0;

        while (i < s.length() && j < t.length()) {
            if (s[i] == t[j]) {
                i++;
                j++;
            } else {
                i++;
            }
        }
        return t.length() - j;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(1)$

> Where $n$ and $m$ are the lengths of the strings $s$ and $t$, respectively.

## 2. Index Jumping

The two-pointer approach scans `s` character by character, which can be slow if `s` is long and the characters we need are sparse. We can speed this up by precomputing where each character appears in `s`. For any position, we can instantly jump to the next occurrence of the character we need.

We build a table where `store[i][c]` tells us the nearest index at or after position `i` where character `c` appears. This lets us skip over irrelevant characters in constant time.

```cpp
class Solution {
public:
    int appendCharacters(string s, string t) {
        int n = s.length(), m = t.length();
        vector<vector<int>> store(n, vector<int>(26, n + 1));
        store[n - 1][s[n - 1] - 'a'] = n - 1;

        for (int i = n - 2; i >= 0; i--) {
            store[i] = store[i + 1];
            store[i][s[i] - 'a'] = i;
        }

        int i = 0, j = 0;
        while (i < n && j < m) {
            if (store[i][t[j] - 'a'] == n + 1) {
                break;
            }
            i = store[i][t[j] - 'a'] + 1;
            j++;
        }

        return m - j;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n)$

> Where $n$ and $m$ are the lengths of the strings $s$ and $t$, respectively.
