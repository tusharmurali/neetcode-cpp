# 926. Flip String to Monotone Increasing

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/flip-string-to-monotone-increasing/>  
- **NeetCode:** <https://neetcode.io/problems/flip-string-to-monotone-increasing>  
- **Video:** <https://www.youtube.com/watch?v=tMq9z5k3umQ>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

A monotone increasing binary string consists of some number of 0s followed by some number of 1s. At each position, we need to decide whether to keep the character as is or flip it. The key insight is that we can track whether we are still in the "all zeros" portion or have transitioned to the "all ones" portion.

If we are still allowed to have zeros (`mono = true`), we can either keep a `0` or flip a `1` to `0`, or we can transition to the ones portion. Once we commit to having only 1s, any `0` we encounter must be flipped. This recursive structure with memoization efficiently explores all valid ways to partition the string.

```cpp
class Solution {
public:
    int minFlipsMonoIncr(string s) {
        int n = s.length();
        vector<vector<int>> dp(n, vector<int>(2, -1));
        return dfs(0, 1, s, dp);
    }

private:
    int dfs(int i, int mono, const string& s, vector<vector<int>>& dp) {
        if (i == s.length()) return 0;
        if (dp[i][mono] != -1) return dp[i][mono];

        if (mono == 1 && s[i] == '0') {
            dp[i][mono] = min(1 + dfs(i + 1, 0, s, dp), dfs(i + 1, mono, s, dp));
        } else if (mono == 1 && s[i] == '1') {
            dp[i][mono] = min(1 + dfs(i + 1, mono, s, dp), dfs(i + 1, 0, s, dp));
        } else if (mono == 0 && s[i] == '1') {
            dp[i][mono] = dfs(i + 1, mono, s, dp);
        } else {
            dp[i][mono] = 1 + dfs(i + 1, mono, s, dp);
        }
        return dp[i][mono];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Bottom-Up)

Instead of recursion, we can iterate through the string from right to left and build up the solution. For each position, we track the minimum flips needed if that position and everything after it should be all `1`s versus if we are still in the flexible zone where `0`s are allowed.

Processing from right to left lets us use already-computed results for positions ahead of the current one. The state transitions mirror the top-down approach but avoid recursion overhead.

```cpp
class Solution {
public:
    int minFlipsMonoIncr(string s) {
        int n = s.size();
        vector<vector<int>> dp(n + 1, vector<int>(2, 0));

        for (int i = n - 1; i >= 0; i--) {
            if (s[i] == '0') {
                dp[i][1] = min(1 + dp[i + 1][0], dp[i + 1][1]);
                dp[i][0] = 1 + dp[i + 1][0];
            } else { // s[i] == '1'
                dp[i][1] = min(1 + dp[i + 1][1], dp[i + 1][0]);
                dp[i][0] = dp[i + 1][0];
            }
        }

        return dp[0][1];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Space Optimized)

The bottom-up solution only needs the DP values from the next position to compute the current position. This means we do not need an entire 2D array; just two variables suffice.

By maintaining only the previous row's values, we reduce space from O(n) to O(1) while preserving the same logic.

```cpp
class Solution {
public:
    int minFlipsMonoIncr(string s) {
        vector<int> dp(2, 0);

        for (int i = s.length() - 1; i >= 0; i--) {
            int newDp1, newDp0;
            if (s[i] == '0') {
                newDp1 = min(1 + dp[0], dp[1]);
                newDp0 = dp[0] + 1;
            } else { // s[i] == '1'
                newDp1 = min(1 + dp[1], dp[0]);
                newDp0 = dp[0];
            }

            dp[1] = newDp1;
            dp[0] = newDp0;
        }

        return dp[1];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 4. Prefix & Suffix Arrays

A monotone increasing string is all `0`s followed by all `1`s. We can think of the string as being split at some index: everything before is `0`, everything after is `1`. For each possible split point, we need to flip all `1`s on the left to `0` and all `0`s on the right to `1`.

Precomputing prefix counts of `1`s and suffix counts of `0`s lets us evaluate each split point in O(1) time. The answer is the minimum sum across all split points.

```cpp
class Solution {
public:
    int minFlipsMonoIncr(string s) {
        int n = s.size();
        vector<int> leftOnes(n + 1, 0), rightZeros(n + 1, 0);

        for (int i = 0; i < n; i++) {
            leftOnes[i + 1] = leftOnes[i] + (s[i] == '1' ? 1 : 0);
        }

        for (int i = n - 1; i >= 0; i--) {
            rightZeros[i] = rightZeros[i + 1] + (s[i] == '0' ? 1 : 0);
        }

        int res = INT_MAX;
        for (int i = 0; i <= n; i++) {
            res = min(res, leftOnes[i] + rightZeros[i]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 5. Dynamic Programming (Optimal)

We can solve this problem in a single pass by maintaining a running count of `1`s seen so far and the minimum flips needed. When we see a `1`, it might need to be flipped later if we decide that position should be `0`. When we see a `0`, we can either flip it to `1` (incrementing our flip count) or flip all previous `1`s to `0`.

The key insight is that the minimum flips at any position equals the minimum of: (1) flipping this `0` plus the previous minimum, or (2) flipping all `1`s seen so far to `0`s.

```cpp
class Solution {
public:
    int minFlipsMonoIncr(string s) {
        int res = 0, cntOne = 0;
        for (char& c : s) {
            if (c == '1') {
                cntOne++;
            } else {
                res = min(res + 1, cntOne);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
