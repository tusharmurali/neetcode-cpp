# 474. Ones and Zeroes

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/ones-and-zeroes/>  
- **NeetCode:** <https://neetcode.io/problems/ones-and-zeroes>  
- **Video:** <https://www.youtube.com/watch?v=miZ3qV04b1g>  

[← Back to index](../INDEX.md)

## 1. Recursion

This problem is a variant of the 0/1 knapsack problem with two constraints instead of one. For each binary string, we must decide whether to include it in our subset or not.

We can try all possible combinations by exploring two branches at each string: include it (if we have enough zeros and ones remaining) or skip it. The goal is to maximize the count of strings we can include while staying within the budget of `m` zeros and `n` ones.

```cpp
class Solution {
public:
    int findMaxForm(vector<string>& strs, int m, int n) {
        vector<vector<int>> arr(strs.size(), vector<int>(2));
        for (int i = 0; i < strs.size(); i++) {
            for (char c : strs[i]) {
                arr[i][c - '0']++;
            }
        }
        return dfs(0, m, n, arr);
    }

private:
    int dfs(int i, int m, int n, vector<vector<int>>& arr) {
        if (i == arr.size()) {
            return 0;
        }

        int res = dfs(i + 1, m, n, arr);
        if (m >= arr[i][0] && n >= arr[i][1]) {
            res = max(res, 1 + dfs(i + 1, m - arr[i][0], n - arr[i][1], arr));
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ N)$
- Space complexity: $O(N)$ for recursion stack.

> Where $N$ represents the number of binary strings, and $m$ and $n$ are the maximum allowable counts of zeros and ones, respectively.

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems. The same state `(i, m, n)` can be reached through different paths, leading to redundant computations.

We add memoization to cache results for each unique state. The state is defined by three variables: the current string index, remaining zeros budget, and remaining ones budget. Once we compute the answer for a state, we store it and return immediately on future calls.

```cpp
class Solution {
private:
    vector<vector<vector<int>>> dp;
    vector<vector<int>> arr;

public:
    int findMaxForm(vector<string>& strs, int m, int n) {
        arr = vector<vector<int>>(strs.size(), vector<int>(2));
        for (int i = 0; i < strs.size(); i++) {
            for (char c : strs[i]) {
                arr[i][c - '0']++;
            }
        }

        dp = vector<vector<vector<int>>>(strs.size(), vector<vector<int>>(m + 1, vector<int>(n + 1, -1)));
        return dfs(0, m, n);
    }

private:
    int dfs(int i, int m, int n) {
        if (i == arr.size()) {
            return 0;
        }
        if (m == 0 && n == 0) {
            return 0;
        }
        if (dp[i][m][n] != -1) {
            return dp[i][m][n];
        }

        int res = dfs(i + 1, m, n);
        if (m >= arr[i][0] && n >= arr[i][1]) {
            res = max(res, 1 + dfs(i + 1, m - arr[i][0], n - arr[i][1]));
        }
        dp[i][m][n] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n * N)$
- Space complexity: $O(m * n * N)$

> Where $N$ represents the number of binary strings, and $m$ and $n$ are the maximum allowable counts of zeros and ones, respectively.

## 3. Dynamic Programming (Bottom-Up)

We can convert the top-down approach to bottom-up by building the solution iteratively. We process strings one by one and, for each combination of remaining zeros and ones budget, compute the maximum strings achievable.

The DP table `dp[i][j][k]` represents the maximum strings from the first `i` strings using at most `j` zeros and `k` ones.

```cpp
class Solution {
public:
    int findMaxForm(vector<string>& strs, int m, int n) {
        vector<vector<int>> arr(strs.size(), vector<int>(2));
        for (int i = 0; i < strs.size(); i++) {
            for (char c : strs[i]) {
                arr[i][c - '0']++;
            }
        }

        vector<vector<vector<int>>> dp(strs.size() + 1, vector<vector<int>>(m + 1, vector<int>(n + 1, 0)));

        for (int i = 1; i <= strs.size(); i++) {
            for (int j = 0; j <= m; j++) {
                for (int k = 0; k <= n; k++) {
                    dp[i][j][k] = dp[i - 1][j][k];
                    if (j >= arr[i - 1][0] && k >= arr[i - 1][1]) {
                        dp[i][j][k] = max(dp[i][j][k], 1 + dp[i - 1][j - arr[i - 1][0]][k - arr[i - 1][1]]);
                    }
                }
            }
        }

        return dp[strs.size()][m][n];
    }
};
```

**Complexity**

- Time complexity: $O(m * n * N)$
- Space complexity: $O(m * n * N)$

> Where $N$ represents the number of binary strings, and $m$ and $n$ are the maximum allowable counts of zeros and ones, respectively.

## 4. Dynamic Programming (Space Optimized)

Notice that when computing `dp[i]`, we only need values from `dp[i-1]`. This means we can reduce the 3D table to a 2D table.

The key trick is to iterate the budgets in reverse order. When we update `dp[j][k]`, we need the old values of `dp[j-zeros][k-ones]`. By iterating backward, we ensure these values have not been overwritten yet in the current iteration.

```cpp
class Solution {
public:
    int findMaxForm(vector<string>& strs, int m, int n) {
        vector<vector<int>> arr(strs.size(), vector<int>(2));
        for (int i = 0; i < strs.size(); i++) {
            for (char c : strs[i]) {
                arr[i][c - '0']++;
            }
        }

        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));

        for (const auto& pair : arr) {
            int zeros = pair[0], ones = pair[1];
            for (int j = m; j >= zeros; j--) {
                for (int k = n; k >= ones; k--) {
                    dp[j][k] = max(dp[j][k], 1 + dp[j - zeros][k - ones]);
                }
            }
        }

        return dp[m][n];
    }
};
```

**Complexity**

- Time complexity: $O(m * n * N)$
- Space complexity: $O(m * n + N)$

> Where $N$ represents the number of binary strings, and $m$ and $n$ are the maximum allowable counts of zeros and ones, respectively.

## Standalone solution file (`cpp/0474-ones-and-zeroes.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int rec(vector<pair<int, int>>& oz, int i, int m, int n, vector<vector<vector<int>>>& dp)
    {
        if (i >= oz.size())
            return 0;

        if (oz[i].first > m || oz[i].second > n)
            return rec(oz, i + 1, m, n, dp);
        
        if (dp[i][m][n] != -1)
            return dp[i][m][n];
        
        int take = 1 + rec(oz, i + 1, m - oz[i].first, n - oz[i].second, dp);
        int notTake = rec(oz, i + 1, m, n, dp);

        return dp[i][m][n] = max(take, notTake);
    }
    int findMaxForm(vector<string>& strs, int m, int n) {
        vector<pair<int, int>> oz(strs.size());
        vector<vector<vector<int>>> dp (strs.size() + 1, vector<vector<int>>(m + 1, vector<int> (n + 1, -1)));

        for (int i = 0; i < strs.size(); i++)
        {
            int one = 0, zero = 0;
            for (int j = 0; j < strs[i].size(); j++)
            {
                if (strs[i][j] == '1')
                    one++;
                else
                    zero++;
            }
            oz[i] = {zero, one};
        }
        
        return rec(oz, 0, m, n, dp);
    }
};
```
