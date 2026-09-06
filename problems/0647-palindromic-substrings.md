# 647. Palindromic Substrings

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/palindromic-substrings/>  
- **NeetCode:** <https://neetcode.io/problems/palindromic-substrings>  
- **Video:** <https://www.youtube.com/watch?v=4RACzI5-du8>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A substring is **palindromic** if it reads the same forwards and backwards.

The brute-force idea is simple:

- Generate **all possible substrings**
- For each substring, **check if it is a palindrome**
- Count how many substrings satisfy this condition

To check a palindrome, use **two pointers**:

- One starting from the left
- One starting from the right
- Move inward while characters match

If the pointers cross (or meet), the substring is a palindrome.

```cpp
class Solution {
public:
    int countSubstrings(string s) {
        int res = 0;

        for (int i = 0; i < s.size(); i++) {
            for (int j = i; j < s.size(); j++) {
                int l = i, r = j;
                while (l < r && s[l] == s[r]) {
                    l++;
                    r--;
                }
                res += (l >= r);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(1)$

## 2. Dynamic Programming

A substring `s[i..j]` is **palindromic** if:

- The end characters match: `s[i] == s[j]`
- The inside substring `s[i+1..j-1]` is also a palindrome
  (or the length is ≤ 2, which is always a palindrome if ends match)

So instead of re-checking characters every time, we **reuse previous results**:

- Store whether a substring is palindromic in a DP table
- Build solutions for longer substrings using shorter ones

```cpp
class Solution {
public:
    int countSubstrings(string s) {
        int res = 0, n = s.length();
        vector<vector<bool>> dp(n, vector<bool>(n, false));

        for (int i = n - 1; i >= 0; i--) {
            for (int j = i; j < n; j++) {
                if (s[i] == s[j] &&
                    (j - i <= 2 || dp[i + 1][j - 1])) {

                    dp[i][j] = true;
                    res++;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Two Pointers

Every palindrome has a **center**:

- For **odd-length** palindromes, the center is a single character
- For **even-length** palindromes, the center is between two characters

Instead of checking all substrings, we:

- Fix a center
- Expand **outwards** as long as characters match
- Each successful expansion forms **one palindrome**

This way, we count palindromes directly while expanding.

```cpp
class Solution {
public:
    int countSubstrings(string s) {
        int res = 0;

        for (int i = 0; i < s.size(); i++) {
            // odd length
            int l = i, r = i;
            while (l >= 0 && r < s.size() &&
                   s[l] == s[r]) {
                res++;
                l--;
                r++;
            }

            // even length
            l = i;
            r = i + 1;
            while (l >= 0 && r < s.size() &&
                   s[l] == s[r]) {
                res++;
                l--;
                r++;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 4. Two Pointers (Optimal)

Every palindromic substring can be identified by **expanding from its center**.

There are only **two possible centers** for any palindrome:

1. A **single character** → odd-length palindromes
2. The **gap between two characters** → even-length palindromes

Instead of duplicating logic for both cases, we extract the expansion logic into a helper function (`countPali`).  
This keeps the solution **clean, reusable, and optimal**.

For each index `i`, we:

- Count palindromes centered at `(i, i)`
- Count palindromes centered at `(i, i + 1)`

Each successful expansion corresponds to **one valid palindrome**.

```cpp
class Solution {
public:
    int countSubstrings(string s) {
        int res = 0;
        for (int i = 0; i < s.size(); i++) {
            res += countPali(s, i, i);
            res += countPali(s, i, i + 1);
        }
        return res;
    }

private:
    int countPali(string s, int l, int r) {
        int res = 0;
        while (l >= 0 && r < s.size() && s[l] == s[r]) {
            res++;
            l--;
            r++;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 5. Manacher's Algorithm

The “expand around center” idea is great, but it can redo the same comparisons many times, making it `O(n^2)`.

**Manacher’s Algorithm** speeds this up to **O(n)** by using two tricks:

1. **Normalize odd/even palindromes**
    - Insert a separator like `#` between characters:  
      `"abba"` → `"#a#b#b#a#"`
    - Now every palindrome in this new string has an **odd-length center**, so we only handle one case.

2. **Reuse information using a “current best palindrome window”**
    - Maintain a palindrome window `[l, r]` (the farthest-reaching palindrome found so far).
    - For a new position `i` inside `[l, r]`, we know its **mirror position** `mirror = l + (r - i)`.
    - The palindrome radius at `i` can be **at least** the smaller of:
        - how much space remains inside the window (`r - i`)
        - the palindrome radius at `mirror` (`p[mirror]`)
    - Then we try to expand further only if possible.

This avoids repeated expansions and ensures total work is linear.

```cpp
class Solution {
public:
    vector<int> manacher(string& s) {
        if (!s.size()) return {};
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

    int countSubstrings(string s) {
        vector<int> p = manacher(s);
        int res = 0;
        for (int i : p) {
            res += (i + 1) / 2;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0647-palindromic-substrings.cpp` in the NeetCode repo)

```cpp
/*
    Given a string, return # of palindromic substrings in it
    Ex. s = "babad" -> "bab", s = "cbbd" -> "bb"

    2 pointers, middle out, check both odd & even sized strings

    Time: O(n^2)
    Space: O(1)
*/

class Solution {
public:
    int countSubstrings(string s) {
        int result = 0;
        
        for (int i = 0; i < s.size(); i++) {
            middleOut(s, i, i, result);
            middleOut(s, i, i + 1, result);
        }
        
        return result;
    }
private:
    void middleOut(string s, int i, int j, int& result) {
        while (i >= 0 && j < s.size() && s[i] == s[j]) {
            result++;
            i--;
            j++;
        }
    }
};
```
