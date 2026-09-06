# 1662. Check If Two String Arrays are Equivalent

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/check-if-two-string-arrays-are-equivalent/>  
- **NeetCode:** <https://neetcode.io/problems/check-if-two-string-arrays-are-equivalent>  
- **Video:** <https://www.youtube.com/watch?v=ejBwc2oE7ck>  

[← Back to index](../INDEX.md)

## 1. Concatenate Strings

The simplest approach is to concatenate all strings in each array into a single string, then compare the two resulting strings. If they match character by character, the arrays represent the same string.

```cpp
class Solution {
public:
    bool arrayStringsAreEqual(vector<string>& word1, vector<string>& word2) {
        string str1 = accumulate(word1.begin(), word1.end(), string());
        string str2 = accumulate(word2.begin(), word2.end(), string());
        return str1 == str2;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$

> Where $n$ and $m$ are the total number of characters in both the arrays $word1$ and $word2$, respectively.

## 2. Concatenate Strings Of One Array

We can reduce space usage by only concatenating one of the arrays. We then iterate through the second array character by character, comparing each character against the concatenated string. This way, we only build one full string instead of two.

```cpp
class Solution {
public:
    bool arrayStringsAreEqual(vector<string>& word1, vector<string>& word2) {
        string s1 = "";
        for (string w : word1) s1 += w;

        int i = 0;
        for (string w : word2) {
            for (char c : w) {
                if (i == s1.length() || s1[i] != c) return false;
                i++;
            }
        }
        return i == s1.length();
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n)$

> Where $n$ and $m$ are the total number of characters in both the arrays $word1$ and $word2$, respectively.

## 3. Two Pointers

We can avoid creating any concatenated strings by using four pointers: two to track which string we are currently in (one for each array), and two to track the character position within those strings. We compare characters one at a time, advancing through both arrays simultaneously.

```cpp
class Solution {
public:
    bool arrayStringsAreEqual(vector<string>& word1, vector<string>& word2) {
        int w1 = 0, w2 = 0; // Index of word
        int i = 0, j = 0;   // Index of character

        while (w1 < word1.size() && w2 < word2.size()) {
            if (word1[w1][i] != word2[w2][j]) {
                return false;
            }

            i++;
            j++;

            if (i == word1[w1].size()) {
                w1++;
                i = 0;
            }
            if (j == word2[w2].size()) {
                w2++;
                j = 0;
            }
        }
        return w1 == word1.size() && w2 == word2.size();
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(1)$ extra space.

> Where $n$ and $m$ are the total number of characters in both the arrays $word1$ and $word2$, respectively.
