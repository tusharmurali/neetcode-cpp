# 256. Paint House

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/paint-house/>  
- **NeetCode:** <https://neetcode.io/problems/paint-house>  
- **Video:** <https://www.youtube.com/watch?v=-w67-4tnH5U>  

[← Back to index](../INDEX.md)

## 1. Recursion

We need to paint each house with one of three colors such that no two adjacent houses have the same color. The most natural way to approach this is to consider each house in order and try all valid color choices.

For each house, we pick a color different from the previous house, add its cost, and recurse to the next house. By exploring all possible valid combinations, we can find the minimum total cost. This brute force approach considers every valid painting configuration.

```cpp
class Solution {
private:
    vector<vector<int>> costs;
    int n;

    int dfs(int i, int prevColor) {
        if (i == n) {
            return 0;
        }

        int res = INT_MAX;
        for (int c = 0; c < 3; c++) {
            if (c == prevColor) {
                continue;
            }
            res = min(res, costs[i][c] + dfs(i + 1, c));
        }
        return res;
    }

public:
    int minCost(vector<vector<int>>& costs) {
        this->costs = costs;
        this->n = costs.size();
        return dfs(0, -1);
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The recursive solution recomputes the same subproblems many times. For example, computing the minimum cost to paint houses 2 through n starting with color 0 might be calculated multiple times from different paths.

We can use memoization to store results for each unique state `(house index, previous color)`. When we encounter the same state again, we simply return the cached result instead of recomputing it.

```cpp
class Solution {
public:
    vector<vector<int>> dp;
    vector<vector<int>> costs;

    int minCost(vector<vector<int>>& costs) {
        int n = costs.size();
        this->costs = costs;
        dp.assign(n, vector<int>(4, -1));
        return dfs(0, -1);
    }

private:
    int dfs(int i, int prevColor) {
        if (i == costs.size()) {
            return 0;
        }
        if (dp[i][prevColor + 1] != -1) {
            return dp[i][prevColor + 1];
        }

        int res = INT_MAX;
        for (int c = 0; c < 3; c++) {
            if (c == prevColor) continue;
            res = min(res, costs[i][c] + dfs(i + 1, c));
        }

        return dp[i][prevColor + 1] = res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Instead of working top-down with recursion, we can build up the solution iteratively. For each house, we compute the minimum cost to paint it with each color, considering that we must have painted the previous house with a different color.

The key insight is that the minimum cost to paint house `i` with color `c` equals `costs[i][c]` plus the minimum of the costs from the previous house painted with the other two colors.

```cpp
class Solution {
public:
    int minCost(vector<vector<int>>& costs) {
        int n = costs.size();
        if (n == 0) return 0;

        vector<vector<int>> dp(n, vector<int>(3, 0));
        for (int c = 0; c < 3; c++) {
            dp[0][c] = costs[0][c];
        }

        for (int i = 1; i < n; i++) {
            for (int c = 0; c < 3; c++) {
                dp[i][c] = costs[i][c] +
                           min(dp[i - 1][(c + 1) % 3], dp[i - 1][(c + 2) % 3]);
            }
        }

        return min({dp[n - 1][0], dp[n - 1][1], dp[n - 1][2]});
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized)

Looking at the bottom-up solution, we notice that computing the DP values for house `i` only requires the values from house `i-1`. We do not need to keep track of all previous houses.

This means we can reduce space from O(n) to O(1) by only storing the costs for the previous house. We maintain three variables representing the minimum costs ending with each color and update them as we process each house.

```cpp
class Solution {
public:
    int minCost(vector<vector<int>>& costs) {
        int dp0 = 0, dp1 = 0, dp2 = 0;

        for (const auto& cost : costs) {
            int newDp0 = cost[0] + min(dp1, dp2);
            int newDp1 = cost[1] + min(dp0, dp2);
            int newDp2 = cost[2] + min(dp0, dp1);
            dp0 = newDp0;
            dp1 = newDp1;
            dp2 = newDp2;
        }

        return min({dp0, dp1, dp2});
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
