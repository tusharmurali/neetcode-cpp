# 1903. Largest Odd Number in String

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/largest-odd-number-in-string/>  
- **NeetCode:** <https://neetcode.io/problems/largest-odd-number-in-string>  
- **Video:** <https://www.youtube.com/watch?v=svuPjFAUeDE>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A number is odd if and only if its last digit is odd (1, 3, 5, 7, or 9). To find the largest odd substring, we could check every possible substring. However, since we want the largest value, we need to consider both length (longer is generally larger) and numeric value (for equal lengths, compare digit by digit).

The brute force approach generates all substrings ending with an odd digit and tracks the maximum one found.

```cpp
class Solution {
public:
    string largestOddNumber(string num) {
        string res = "";
        int n = num.size();

        for (int i = 0; i < n; i++) {
            for (int j = i; j < n; j++) {
                int onesDigit = num[j] - '0';
                if (onesDigit & 1) {
                    string cur = num.substr(i, j - i + 1);
                    if (res.size() < cur.size() ||
                       (res.size() == cur.size() && res < cur)) {
                        res = cur;
                    }
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(n)$

## 2. Find The Rightmost Odd Digit

The largest odd substring must start from the beginning of the string (to maximize length and leading digits) and end at the rightmost odd digit. Why? Because starting from index 0 gives us the largest possible prefix, and we just need to find where to cut it off to make it odd.

By scanning from right to left, we find the first (rightmost) odd digit and return the prefix up to and including that position.

```cpp
class Solution {
public:
    string largestOddNumber(string num) {
        for (int i = num.size() - 1; i >= 0; i--) {
            if ((num[i] - '0') % 2 == 1) {
                return num.substr(0, i + 1);
            }
        }
        return "";
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ for the output string.
