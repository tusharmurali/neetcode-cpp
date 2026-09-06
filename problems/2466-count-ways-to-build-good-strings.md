# 2466. Count Ways to Build Good Strings

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-ways-to-build-good-strings/>  
- **NeetCode:** <https://neetcode.io/problems/count-ways-to-build-good-strings>  
- **Video:** <https://www.youtube.com/watch?v=JKpVHG2mhbk>  

[← Back to index](../INDEX.md)

## 1. Recursion

We can think of building a string as making a series of choices. At each step, we either append `zero` number of `'0'`s or `one` number of `'1'`s. The recursion naturally explores all possible combinations by branching at each decision point. A string is "good" when its length falls within the range `[low, high]`, so we count it whenever we reach a valid length.

```cpp
class Solution {
public:
    int countGoodStrings(int low, int high, int zero, int one) {
        const int mod = 1e9 + 7;

        function<int(int)> dfs = [&](int length) {
            if (length > high) return 0;
            int res = (length >= low) ? 1 : 0;
            res = (res + dfs(length + zero)) % mod;
            res = (res + dfs(length + one)) % mod;
            return res;
        };

        return dfs(0);
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

> Where $n$ is equal to the given $high$ value.

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems because we may reach the same string length through different paths. For example, adding `zero` then `one` might give the same length as adding `one` then `zero`. Memoization stores the result for each length we have already computed, avoiding redundant calculations.

```cpp
class Solution {
    const int mod = 1e9 + 7;
    vector<int> dp;

public:
    int countGoodStrings(int low, int high, int zero, int one) {
        dp.assign(high + 1, -1);
        return dfs(low, high, zero, one, 0);
    }

private:
    int dfs(int low, int high, int zero, int one, int length) {
        if (length > high) return 0;
        if (dp[length] != -1) return dp[length];
        dp[length] = (length >= low) ? 1 : 0;
        dp[length] = (dp[length] + dfs(low, high, zero, one, length + zero)) % mod;
        dp[length] = (dp[length] + dfs(low, high, zero, one, length + one)) % mod;
        return dp[length];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is equal to the given $high$ value.

## 3. Dynamic Programming (Bottom-Up)

Instead of starting from length `0` and recursing forward, we can build the solution iteratively. For each length `i`, the number of ways to reach it equals the ways to reach length `i - zero` (then add zeros) plus the ways to reach length `i - one` (then add ones). This is similar to the classic coin change problem where we count combinations.

```cpp
class Solution {
public:
    int countGoodStrings(int low, int high, int zero, int one) {
        vector<int> dp(high + 1);
        int mod = 1e9 + 7, res = 0;
        dp[0] = 1;

        for (int i = 1; i <= high; i++) {
            if (i >= zero) dp[i] = (dp[i] + dp[i - zero]) % mod;
            if (i >= one) dp[i] = (dp[i] + dp[i - one]) % mod;
            if (i >= low) res = (res + dp[i]) % mod;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is equal to the given $high$ value.
