# 1768. Merge Strings Alternately

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/merge-strings-alternately/>  
- **NeetCode:** <https://neetcode.io/problems/merge-strings-alternately>  
- **Video:** <https://www.youtube.com/watch?v=LECWOvTo-Sc>  

[← Back to index](../INDEX.md)

## 1. Two Pointers - I

We want to interleave characters from both strings, taking one from each in turn. Using two pointers, we can walk through both strings simultaneously. While both strings have characters remaining, we append one from each. Once one string is exhausted, we append whatever remains from the other string.

```cpp
class Solution {
public:
    string mergeAlternately(string word1, string word2) {
        string res;
        int i = 0, j = 0;
        while (i < word1.size() && j < word2.size()) {
            res += word1[i++];
            res += word2[j++];
        }
        res += word1.substr(i);
        res += word2.substr(j);
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$ for the output string.

> Where $n$ and $m$ are the lengths of the strings $word1$ and $word2$ respectively.

## 2. Two Pointers - II

Instead of handling the remaining characters separately after the main loop, we can continue the loop as long as either string has characters left. In each iteration, we check if each pointer is still valid before appending. This approach handles unequal length strings naturally within a single loop.

```cpp
class Solution {
public:
    string mergeAlternately(string word1, string word2) {
        int n = word1.size(), m = word2.size();
        string res;
        int i = 0, j = 0;
        while (i < n || j < m) {
            if (i < n) res += word1[i++];
            if (j < m) res += word2[j++];
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$ for the output string.

> Where $n$ and $m$ are the lengths of the strings $word1$ and $word2$ respectively.

## 3. One Pointer

Since we always process characters at the same index from both strings in each iteration, we can simplify to a single index variable. We iterate up to the length of the longer string, and for each index, we add the character from each string if that index is valid.

```cpp
class Solution {
public:
    string mergeAlternately(string word1, string word2) {
        int n = word1.size(), m = word2.size();
        string res;
        for (int i = 0; i < n || i < m; i++) {
            if (i < n) {
                res += word1[i];
            }
            if (i < m) {
                res += word2[i];
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$ for the output string.

> Where $n$ and $m$ are the lengths of the strings $word1$ and $word2$ respectively.

## Standalone solution file (`cpp/1768-merge-strings-alternately.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    string mergeAlternately(string word1, string word2)
    {
        int i=0;
        string final="";

        while(i < word1.size() && i < word2.size())
            final = final + word1[i] + word2[i++];

        while(i < word1.size())
            final += word1[i++];
        while(i < word2.size())
            final += word2[i++];

        return final;
    }
};
```
