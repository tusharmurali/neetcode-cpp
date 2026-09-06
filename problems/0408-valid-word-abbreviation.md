# 408. Valid Word Abbreviation

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/valid-word-abbreviation/>  
- **NeetCode:** <https://neetcode.io/problems/valid-word-abbreviation>  
- **Video:** <https://www.youtube.com/watch?v=m7U90fpD2j0>  

[← Back to index](../INDEX.md)

## 1. Two Pointers

We need to verify that the abbreviation correctly represents the word. The abbreviation contains letters and numbers, where numbers indicate how many characters to skip. We use two pointers to traverse both strings simultaneously. When we see a letter in the abbreviation, it must match the current character in the word. When we see a number, we parse the full number and skip that many characters in the word. A leading zero in any number makes the abbreviation invalid.

```cpp
class Solution {
public:
    bool validWordAbbreviation(string word, string abbr) {
        int n = word.length(), m = abbr.length();
        int i = 0, j = 0;

        while (i < n && j < m) {
            if (abbr[j] == '0') return false;

            if (isalpha(abbr[j])) {
                if (word[i] == abbr[j]) {
                    i++; j++;
                } else {
                    return false;
                }
            } else {
                int subLen = 0;
                while (j < m && isdigit(abbr[j])) {
                    subLen = subLen * 10 + (abbr[j] - '0');
                    j++;
                }
                i += subLen;
            }
        }

        return i == n && j == m;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(1)$

> Where $n$ and $m$ are the lengths of the strings $word$ and $abbr$, respectively.
