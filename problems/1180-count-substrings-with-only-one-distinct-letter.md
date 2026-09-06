# 1180. Count Substrings with Only One Distinct Letter

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-substrings-with-only-one-distinct-letter/>  
- **NeetCode:** <https://neetcode.io/problems/count-substrings-with-only-one-distinct-letter>  

[← Back to index](../INDEX.md)

## 1. Arithmetic Sequence

The string can be split into consecutive groups of identical characters. For each group of length `L`, the number of substrings containing only that character follows the arithmetic sequence formula: `1 + 2 + 3 + ... + L = L*(L+1)/2`. We scan through the string, identify each group, and sum up the contributions.

```cpp
class Solution {
public:
    int countLetters(string s) {
        int total = 0;
        for (int left = 0, right = 0; right <= s.length(); right++) {
            if (right == s.length() || s[left] != s[right]) {
                int lenSubstring = right - left;
                // more details about the sum of the arithmetic sequence:
                // https://en.wikipedia.org/wiki/Arithmetic_progression#Sum
                total += (1 + lenSubstring) * lenSubstring / 2;
                left = right;
            }
        }

        return total;
    }
};
```

**Complexity**

- Time complexity: $O(N)$

- Space complexity: $O(1)$ constant space

> Where $N$ is the length of the input string `s`.
