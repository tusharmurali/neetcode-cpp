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

## 2. Dynamic Programming

For each position `i`, we can compute how many valid substrings end at that position. If the character at position `i` matches the previous character, the count equals the previous count plus `1` (we extend all previous substrings and add one new single-character substring). Otherwise, only the single character itself forms a valid substring. The total is the sum across all positions.

```cpp
class Solution {
public:
    int countLetters(string s) {
        vector<int> substrings(s.length());
        int total = 1;
        substrings[0] = 1;

        for (int i = 1; i < s.length(); i++) {
            if (s[i] == s[i - 1]) {
                substrings[i] = substrings[i - 1] + 1;
            } else {
                substrings[i] = 1;
            }

            total += substrings[i];
        }

        return total;
    }
};
```

**Complexity**

- Time complexity: $O(N)$

- Space complexity: $O(N)$

>  Where $N$ is the length of the input string `s`.

## 3. Dynamic Programming (Optimized)

Since we only need the previous value to compute the current one, we can optimize space by using a single variable instead of an array. This variable (`count`) tracks the count of valid substrings ending at the current position.

```cpp
class Solution {
public:
    int countLetters(string s) {
        int total = 1, count = 1;

        for (int i = 1; i < s.length(); i++) {
            if (s[i] == s[i-1]) {
                count++;
            } else {
                count = 1;
            }
            total += count;
        }

        return total;
    }
};
```

**Complexity**

- Time complexity: $O(N)$

- Space complexity: $O(1)$ constant space

>  Where $N$ is the length of the input string `s`.
