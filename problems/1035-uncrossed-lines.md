# 1035. Uncrossed Lines

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/uncrossed-lines/>  
- **NeetCode:** <https://neetcode.io/problems/uncrossed-lines>  
- **Video:** <https://www.youtube.com/watch?v=mnJF4vJ7GyE>  

[← Back to index](../INDEX.md)

## 1. Recursion

This problem is essentially finding the longest common subsequence (LCS) between two arrays. We can draw a line between `nums1[i]` and `nums2[j]` only if they have the same value. Lines cannot cross, which means if we connect `nums1[i]` to `nums2[j]`, we can only connect elements after index `i` in `nums1` to elements after index `j` in `nums2`.

At each position, we have two choices: if the current elements match, we draw a line and move both pointers forward. If they don't match, we try skipping an element from either array and take the maximum result.

```cpp
class Solution {
public:
    int dfs(vector<int>& nums1, vector<int>& nums2, int i, int j) {
        if (i == nums1.size() || j == nums2.size()) return 0;

        if (nums1[i] == nums2[j]) {
            return 1 + dfs(nums1, nums2, i + 1, j + 1);
        }
        return max(dfs(nums1, nums2, i, j + 1), dfs(nums1, nums2, i + 1, j));
    }

    int maxUncrossedLines(vector<int>& nums1, vector<int>& nums2) {
        return dfs(nums1, nums2, 0, 0);
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ {n + m})$
- Space complexity: $O(n + m)$ for recursion stack.

> Where $n$ and $m$ are the sizes of the arrays $nums1$ and $nums2$ respectively.

## 2. Dynamic Programming (Top-Down)

The recursive solution recomputes many subproblems. For example, `dfs(2, 3)` might be called multiple times through different paths. We can use memoization to store results of subproblems and avoid redundant calculations.

```cpp
class Solution {
public:
    int maxUncrossedLines(vector<int>& nums1, vector<int>& nums2) {
        int n = nums1.size(), m = nums2.size();
        vector<vector<int>> dp(n, vector<int>(m, -1));

        return dfs(0, 0, nums1, nums2, dp);
    }

private:
    int dfs(int i, int j, vector<int>& nums1, vector<int>& nums2, vector<vector<int>>& dp) {
        if (i == nums1.size() || j == nums2.size()) {
            return 0;
        }

        if (dp[i][j] != -1) {
            return dp[i][j];
        }

        if (nums1[i] == nums2[j]) {
            dp[i][j] = 1 + dfs(i + 1, j + 1, nums1, nums2, dp);
        } else {
            dp[i][j] = max(dfs(i, j + 1, nums1, nums2, dp), dfs(i + 1, j, nums1, nums2, dp));
        }

        return dp[i][j];
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ and $m$ are the sizes of the arrays $nums1$ and $nums2$ respectively.

## 3. Dynamic Programming (Bottom-Up)

Instead of recursion with memoization, we can build the solution iteratively. We define `dp[i][j]` as the maximum number of uncrossed lines using `nums1[0..i-1]` and `nums2[0..j-1]`. By filling this table row by row, we avoid recursion overhead.

```cpp
class Solution {
public:
    int maxUncrossedLines(vector<int>& nums1, vector<int>& nums2) {
        int n = nums1.size(), m = nums2.size();
        vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (nums1[i] == nums2[j]) {
                    dp[i + 1][j + 1] = 1 + dp[i][j];
                } else {
                    dp[i + 1][j + 1] = max(dp[i][j + 1], dp[i + 1][j]);
                }
            }
        }

        return dp[n][m];
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ and $m$ are the sizes of the arrays $nums1$ and $nums2$ respectively.

## 4. Dynamic Programming (Space Optimized)

Notice that each row of the `dp` table only depends on the previous row. We can reduce space complexity by keeping only two rows: the `prev` row and the current `dp` row being computed.

```cpp
class Solution {
public:
    int maxUncrossedLines(vector<int>& nums1, vector<int>& nums2) {
        vector<int> prev(nums2.size() + 1, 0);

        for (int i = 0; i < nums1.size(); i++) {
            vector<int> dp(nums2.size() + 1, 0);
            for (int j = 0; j < nums2.size(); j++) {
                if (nums1[i] == nums2[j]) {
                    dp[j + 1] = 1 + prev[j];
                } else {
                    dp[j + 1] = max(dp[j], prev[j + 1]);
                }
            }
            prev = dp;
        }

        return prev[nums2.size()];
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(m)$

> Where $n$ and $m$ are the sizes of the arrays $nums1$ and $nums2$ respectively.

## 5. Dynamic Programming (Optimal)

We can further optimize by using a single array and a variable to track the diagonal value from the previous iteration. This requires careful handling to avoid overwriting values we still need.

```cpp
class Solution {
public:
    int maxUncrossedLines(vector<int>& nums1, vector<int>& nums2) {
        int n = nums1.size(), m = nums2.size();
        if (m > n) {
            swap(nums1, nums2);
            swap(n, m);
        }

        vector<int> dp(m + 1, 0);

        for (int i = 0; i < n; i++) {
            int prev = 0;
            for (int j = 0; j < m; j++) {
                int temp = dp[j + 1];
                if (nums1[i] == nums2[j]) {
                    dp[j + 1] = 1 + prev;
                } else {
                    dp[j + 1] = max(dp[j + 1], dp[j]);
                }
                prev = temp;
            }
        }

        return dp[m];
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(min(n, m))$

> Where $n$ and $m$ are the sizes of the arrays $nums1$ and $nums2$ respectively.
