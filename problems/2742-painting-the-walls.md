# 2742. Painting the Walls

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/painting-the-walls/>  
- **NeetCode:** <https://neetcode.io/problems/painting-the-walls>  
- **Video:** <https://www.youtube.com/watch?v=qMZJunF5UaI>  

[← Back to index](../INDEX.md)

## 1. Recursion

We have a paid painter and a free painter working simultaneously. The paid painter takes `time[i]` to paint wall `i` and costs `cost[i]`. The free painter paints one wall per unit time at no cost, but can only work while the paid painter is busy.

The key insight is that when the paid painter paints wall `i`, the free painter can paint `time[i]` walls during that period. So assigning wall `i` to the paid painter effectively handles `1 + time[i]` walls total.

We use recursion to decide for each wall: either pay to paint it (and let the free painter handle `time[i]` additional walls), or skip it (hoping the free painter will handle it later).

```cpp
class Solution {
public:
    int paintWalls(vector<int>& cost, vector<int>& time) {
        return dfs(cost, time, 0, cost.size());
    }

private:
    int dfs(vector<int>& cost, vector<int>& time, int i, int remain) {
        if (remain <= 0) {
            return 0;
        }
        if (i == cost.size()) {
            return INT_MAX;
        }

        int paint = dfs(cost, time, i + 1, remain - 1 - time[i]);
        if (paint != INT_MAX) paint += cost[i];

        int skip = dfs(cost, time, i + 1, remain);
        return min(paint, skip);
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems. The state `(i, remain)` can be reached through different paths, and we recompute the same results multiple times.

By caching results in a memoization table, we ensure each unique state is computed only once. The table has dimensions `n x (n + 1)` since `remain` ranges from 0 to n.

```cpp
class Solution {
    vector<vector<int>> dp;

public:
    int paintWalls(vector<int>& cost, vector<int>& time) {
        dp.assign(cost.size(), vector<int>(cost.size() + 1, -1));
        return dfs(cost, time, 0, cost.size());
    }

private:
    int dfs(vector<int>& cost, vector<int>& time, int i, int remain) {
        if (remain <= 0) {
            return 0;
        }
        if (i == cost.size()) {
            return INT_MAX;
        }
        if (dp[i][remain] != -1) {
            return dp[i][remain];
        }

        int paint = dfs(cost, time, i + 1, remain - 1 - time[i]);
        if (paint != INT_MAX) paint += cost[i];

        int skip = dfs(cost, time, i + 1, remain);
        return dp[i][remain] = min(paint, skip);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Dynamic Programming (Bottom-Up)

We can convert the top-down solution to bottom-up by filling the DP table iteratively. Starting from the last wall and working backward, we compute the minimum cost for each state.

The recurrence relation remains the same: for each wall, we either pay to paint it or skip it, taking the minimum cost.

```cpp
class Solution {
public:
    int paintWalls(vector<int>& cost, vector<int>& time) {
        int n = cost.size();
        vector<vector<int>> dp(n + 1, vector<int>(n + 2, 0));

        for (int remain = 1; remain <= n; remain++) {
            dp[n][remain] = INT_MAX;
        }

        for (int i = n - 1; i >= 0; i--) {
            for (int remain = 1; remain <= n; remain++) {
                int paint = dp[i + 1][max(remain - 1 - time[i], 0)];
                if (paint !=  INT_MAX) paint += cost[i];

                int skip = dp[i + 1][remain];
                dp[i][remain] = min(paint, skip);
            }
        }

        return dp[0][n];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 4. Dynamic Programming (Space Optimized)

Notice that this problem resembles a 0/1 knapsack. Each wall is an item with a cost and a benefit (how many walls it covers). We need to cover exactly `n` walls with minimum total cost.

We can optimize space by using a 1D array. The key is to iterate `remain` in reverse order so that we do not overwrite values we still need in the current iteration.

```cpp
class Solution {
public:
    int paintWalls(vector<int>& cost, vector<int>& time) {
        int n = cost.size();
        vector<int> dp(n + 2, INT_MAX);
        dp[0] = 0;

        for (int i = 0; i < n; i++) {
            for (int remain = n; remain > 0; remain--) {
                int paint = dp[max(remain - 1 - time[i], 0)];
                if (paint != INT_MAX) paint += cost[i];
                dp[remain] = min(paint, dp[remain]);
            }
        }

        return dp[n];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$
