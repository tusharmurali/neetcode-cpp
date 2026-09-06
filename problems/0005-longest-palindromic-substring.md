# 5. Longest Palindromic Substring

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/longest-palindromic-substring/>  
- **NeetCode:** <https://neetcode.io/problems/longest-palindromic-substring>  
- **Video:** <https://www.youtube.com/watch?v=XYQecbcd6_c>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A palindrome reads the same forward and backward.  
The simplest idea is to **try every possible substring** and check whether it is a palindrome, then keep the longest one found.

For each pair `(i, j)`:

- Assume `s[i:j]` is a candidate substring
- Use two pointers (`l` and `r`) to check if it’s a palindrome
- If valid and longer than the current answer, update the result

This approach is straightforward but inefficient.

```cpp
class Solution {
public:
    string longestPalindrome(string s) {
        string res = "";
        int resLen = 0;

        for (int i = 0; i < s.size(); i++) {
            for (int j = i; j < s.size(); j++) {
                int l = i, r = j;
                while (l < r && s[l] == s[r]) {
                    l++;
                    r--;
                }

                if (l >= r && resLen < (j - i + 1)) {
                    res = s.substr(i, j - i + 1);
                    resLen = j - i + 1;
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

## 2. Dynamic Programming

Instead of re-checking the same substrings again and again, we **remember** whether a substring is a palindrome.

Let:

- `dp[i][j] = true` if the substring `s[i..j]` is a palindrome.

A substring `s[i..j]` is a palindrome when:

1. The end characters match: `s[i] == s[j]`
2. And the inside part is also a palindrome: `dp[i+1][j-1]`
    - **Special small cases:** if the length is `1`, `2`, or `3` (`j - i <= 2`), then matching ends is enough because the middle is empty or a single char.

We fill `dp` from **bottom to top** (`i` from `n-1` down to `0`) so that when we compute `dp[i][j]`, the value `dp[i+1][j-1]` is already known.

While filling, we keep track of the **best (longest) palindrome** seen so far.

```cpp
class Solution {
public:
    string longestPalindrome(string s) {
        int resIdx = 0, resLen = 0;
        int n = s.size();

        vector<vector<bool>> dp(n, vector<bool>(n, false));

        for (int i = n - 1; i >= 0; i--) {
            for (int j = i; j < n; j++) {
                if (s[i] == s[j] &&
                    (j - i <= 2 || dp[i + 1][j - 1])) {

                    dp[i][j] = true;
                    if (resLen < (j - i + 1)) {
                        resIdx = i;
                        resLen = j - i + 1;
                    }
                }
            }
        }

        return s.substr(resIdx, resLen);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Two Pointers

A palindrome **expands symmetrically from its center**.

Every palindrome has one of two centers:

1. **Odd length** → a single character center (e.g. `"racecar"`)
2. **Even length** → between two characters (e.g. `"abba"`)

So instead of checking all substrings, we:

- Treat every index as a possible center
- Expand **left and right** while characters match
- Track the longest palindrome found during expansion

This avoids extra space and redundant checks.

```cpp
class Solution {
public:
    string longestPalindrome(string s) {
        int resLen = 0, resIdx = 0;

        for (int i = 0; i < s.size(); i++) {
            // odd length
            int l = i, r = i;
            while (l >= 0 && r < s.size() &&
                   s[l] == s[r]) {
                if (r - l + 1 > resLen) {
                    resIdx = l;
                    resLen = r - l + 1;
                }
                l--;
                r++;
            }

            // even length
            l = i;
            r = i + 1;
            while (l >= 0 && r < s.size() &&
                   s[l] == s[r]) {
                if (r - l + 1 > resLen) {
                    resIdx = l;
                    resLen = r - l + 1;
                }
                l--;
                r++;
            }
        }

        return s.substr(resIdx, resLen);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output string.

## 4. Manacher's Algorithm

Manacher’s Algorithm is an **optimized way to find the longest palindromic substring in linear time**.

The key ideas are:

- **Unify odd and even length palindromes** by inserting a special character (like `#`) between characters.
    - Example: `"abba"` → `"#a#b#b#a#"`
- Use **previous palindrome information** to avoid re-checking characters.
- Maintain a **current rightmost palindrome** and mirror indices to reuse results.

Instead of expanding from every center independently, Manacher’s algorithm **reuses symmetry**, making it much faster than the two-pointer approach.

```cpp
class Solution {
public:
    vector<int> manacher(string& s) {
        string t = "#" + string(1, s[0]);
        for (int i = 1; i < s.size(); ++i)
            t += "#" + string(1, s[i]);
        t += "#";
        int n = t.size();
        vector<int> p(n, 0);
        int l = 0, r = 0;
        for (int i = 0; i < n; i++) {
            p[i] = (i < r) ? min(r - i, p[l + (r - i)]) : 0;
            while (i + p[i] + 1 < n && i - p[i] - 1 >= 0 &&
                   t[i + p[i] + 1] == t[i - p[i] - 1])
                p[i]++;
            if (i + p[i] > r)
                l = i - p[i], r = i + p[i];
        }
        return p;
    }

    string longestPalindrome(string s) {
        vector<int> p = manacher(s);
        int resLen = 0, center_idx = 0;
        for (int i = 0; i < p.size(); i++) {
            if (p[i] > resLen) {
                resLen = p[i];
                center_idx = i;
            }
        }
        int resIdx = (center_idx - resLen) / 2;
        return s.substr(resIdx, resLen);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0005-longest-palindromic-substring.cpp` in the NeetCode repo)

```cpp
/*
    Given a string s, return the longest palindromic substring in s
    Ex. s = "babad" -> "bab", s = "cbbd" -> "bb"

    Expand around center, extend as far as possible, store max length

    Time: O(n^2)
    Space: O(1)
*/

class Solution {
public:
    string longestPalindrome(string s) {
        int maxStart = 0;
        int maxLength = 1;
        
        for (int i = 0; i < s.size() - 1; i++) {
            middleOut(s, i, i, maxStart, maxLength);
            middleOut(s, i, i + 1, maxStart, maxLength);
        }
        
        return s.substr(maxStart, maxLength);
    }
private:
    void middleOut(string s, int i, int j, int& maxStart, int& maxLength) {
        while (i >= 0 && j <= s.size() - 1 && s[i] == s[j]) {
            i--;
            j++;
        }
        if (j - i - 1 > maxLength) {
            maxStart = i + 1;
            maxLength = j - i - 1;
        }
    }
};
```
