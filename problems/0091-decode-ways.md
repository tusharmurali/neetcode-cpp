# 91. Decode Ways

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/decode-ways/>  
- **NeetCode:** <https://neetcode.io/problems/decode-ways>  
- **Video:** <https://www.youtube.com/watch?v=6aEyTjOwlJU>  
- **Video approach:** 2. Dynamic Programming (Top-Down)  

[← Back to index](../INDEX.md)

## 1. Recursion

Each digit (or pair of digits) in the string can be mapped to a letter:

- `"1"` → `"A"`, `"2"` → `"B"`, …, `"26"` → `"Z"`

At any index `i`, you only have **two possible decoding choices**:

1. **Take one digit** (`s[i]`) → valid if it’s not `'0'`
2. **Take two digits** (`s[i:i+2]`) → valid if it forms a number between `10` and `26`

So the problem naturally breaks into **subproblems**:

> “How many ways can I decode the substring starting at index `i`?”

This leads directly to a recursive structure.

Key base ideas:

- If you reach the end of the string → **1 valid decoding**
- If a substring starts with `'0'` → **0 ways** (invalid)
- Otherwise, sum the ways from:
    - decoding one digit
    - decoding two digits (if valid)

```cpp
class Solution {
public:
    int dfs(int i, string& s) {
        if (i == s.size()) return 1;
        if (s[i] == '0') return 0;

        int res = dfs(i + 1, s);
        if (i < s.size() - 1) {
            if (s[i] == '1' ||
               (s[i] == '2' && s[i + 1] < '7')) {
                res += dfs(i + 2, s);
            }
        }
        return res;
    }

    int numDecodings(string s) {
        return dfs(0, s);
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down) ▶ video

This is the same decoding logic as the recursive approach, but with **memoization** to avoid recomputing the same subproblems.

Observation:

- While decoding, the same index `i` is reached multiple times.
- The number of ways to decode `s[i:]` **never changes**, so we can store it once and reuse it.

So instead of recalculating:

> “How many ways can I decode from index `i`?”

we **cache the answer** the first time we compute it.

This converts the exponential recursion into linear time.

```cpp
class Solution {
public:
    int numDecodings(string s) {
        unordered_map<int, int> dp;
        dp[s.size()] = 1;
        return dfs(s, 0, dp);
    }

private:
    int dfs(string s, int i, unordered_map<int, int>& dp) {
        if (dp.count(i)) {
            return dp[i];
        }
        if (s[i] == '0') {
            return 0;
        }

        int res = dfs(s, i + 1, dp);
        if (i + 1 < s.size() && (s[i] == '1' ||
            s[i] == '2' && s[i + 1] < '7')) {
            res += dfs(s, i + 2, dp);
        }
        dp[i] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

This is the **iterative version** of the decoding logic.

Instead of asking:

> “How many ways can I decode starting at index `i`?”

recursively, we **build the answer from the back**.

Key idea:

- Let `dp[i]` = number of ways to decode the substring `s[i:]`
- The answer we want is `dp[0]`
- Each position depends only on the next **one** or **two** positions → perfect for bottom-up DP

```cpp
class Solution {
public:
    int numDecodings(string s) {
        vector<int> dp(s.size() + 1);
        dp[s.size()] = 1;
        for (int i = s.size() - 1; i >= 0; i--) {
            if (s[i] == '0') {
                dp[i] = 0;
            } else {
                dp[i] = dp[i + 1];
                if (i + 1 < s.size() && (s[i] == '1' ||
                    s[i] == '2' && s[i + 1] < '7')) {
                    dp[i] += dp[i + 2];
                }
            }
        }
        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized)

This is the **space-optimized version** of bottom-up DP.

From the bottom-up approach, we know:

- `dp[i]` depends **only on** `dp[i+1]` and `dp[i+2]`
- So we don’t need an entire DP array

We just keep:

- `dp1` → ways to decode from `i + 1`
- `dp2` → ways to decode from `i + 2`

At each index `i`, we compute the current answer using these two values, then **shift them forward**.

```cpp
class Solution {
public:
    int numDecodings(string s) {
        int dp = 0, dp2 = 0;
        int dp1 = 1;
        for (int i = s.size() - 1; i >= 0; i--) {
            if (s[i] == '0') {
                dp = 0;
            } else {
                dp = dp1;
                if (i + 1 < s.size() && (s[i] == '1' ||
                    s[i] == '2' && s[i + 1] < '7')) {
                    dp += dp2;
                }
            }
            dp2 = dp1;
            dp1 = dp;
            dp = 0;
        }
        return dp1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0091-decode-ways.cpp` in the NeetCode repo)

```cpp
/*
    Given a string w/ only digits, return # ways to decode it (letter -> digit)
    Ex. s = "12" -> 2 (AB 1 2 or L 12), s = "226" -> 3 (2 26 or 22 6 or 2 2 6)

    DP: At each digit, check validity of ones & tens, if valid add to # ways
    Recurrence relation: dp[i] += dp[i-1] (if valid) + dp[i-2] (if valid)

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    int numDecodings(string s) {
        if (s[0] == '0') {
            return 0;
        }
        
        int n = s.size();
        
        vector<int> dp(n + 1);
        dp[0] = 1;
        dp[1] = 1;
        
        for (int i = 2; i <= n; i++) {
            int ones = stoi(s.substr(i - 1, 1));
            if (ones >= 1 && ones <= 9) {
                dp[i] += dp[i - 1];
            }
            int tens = stoi(s.substr(i - 2, 2));
            if (tens >= 10 && tens <= 26) {
                dp[i] += dp[i - 2];
            }
        }
        
        return dp[n];
    }
};
```
