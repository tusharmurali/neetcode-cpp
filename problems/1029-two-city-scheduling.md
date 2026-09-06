# 1029. Two City Scheduling

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/two-city-scheduling/>  
- **NeetCode:** <https://neetcode.io/problems/two-city-scheduling>  
- **Video:** <https://www.youtube.com/watch?v=d-B_gk_gJtQ>  

[← Back to index](../INDEX.md)

## 1. Recursion

We need to send exactly `n` people to city A and `n` people to city B, minimizing total cost. For each person, we have two choices: send them to A or B. We can explore all possible assignments using recursion, tracking how many slots remain for each city.

```cpp
class Solution {
public:
    int twoCitySchedCost(vector<vector<int>>& costs) {
        int n = costs.size() / 2;
        return dfs(costs, 0, n, n);
    }

private:
    int dfs(vector<vector<int>>& costs, int i, int aCount, int bCount) {
        if (i == costs.size()) {
            return 0;
        }

        int res = INT_MAX;
        if (aCount > 0) {
            res = costs[i][0] + dfs(costs, i + 1, aCount - 1, bCount);
        }

        if (bCount > 0) {
            res = min(res, costs[i][1] + dfs(costs, i + 1, aCount, bCount - 1));
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ N)$
- Space complexity: $O(N)$ for recursion stack.

> Where $N$ is the size of the array $costs$.

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems because the same state (remaining slots for A and B) can be reached through different paths. We can use memoization to cache results and avoid redundant computation.

```cpp
class Solution {
public:
    vector<vector<int>> dp;

    int twoCitySchedCost(vector<vector<int>>& costs) {
        int n = costs.size() / 2;
        dp = vector<vector<int>>(n + 1, vector<int>(n + 1, -1));
        return dfs(costs, 0, n, n);
    }

private:
    int dfs(vector<vector<int>>& costs, int i, int aCount, int bCount) {
        if (i == costs.size()) {
            return 0;
        }
        if (dp[aCount][bCount] != -1) {
            return dp[aCount][bCount];
        }

        int res = INT_MAX;
        if (aCount > 0) {
            res = costs[i][0] + dfs(costs, i + 1, aCount - 1, bCount);
        }
        if (bCount > 0) {
            res = min(res, costs[i][1] + dfs(costs, i + 1, aCount, bCount - 1));
        }

        dp[aCount][bCount] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

> Where $n$ is the half of the size of the array $costs$.

## 3. Dynamic Programming (Bottom-Up)

Instead of recursion with memoization, we can build the solution iteratively. We fill a table where `dp[aCount][bCount]` represents the minimum cost to assign the first `aCount + bCount` people such that `aCount` go to city A and `bCount` go to city B.

```cpp
class Solution {
public:
    int twoCitySchedCost(vector<vector<int>>& costs) {
        int n = costs.size() / 2;
        vector<vector<int>> dp(n + 1, vector<int>(n + 1));

        for (int aCount = 0; aCount <= n; aCount++) {
            for (int bCount = 0; bCount <= n; bCount++) {
                int i = aCount + bCount;
                if (i == 0) continue;

                dp[aCount][bCount] = INT_MAX;
                if (aCount > 0) {
                    dp[aCount][bCount] = min(dp[aCount][bCount], dp[aCount - 1][bCount] + costs[i - 1][0]);
                }
                if (bCount > 0) {
                    dp[aCount][bCount] = min(dp[aCount][bCount], dp[aCount][bCount - 1] + costs[i - 1][1]);
                }
            }
        }

        return dp[n][n];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

> Where $n$ is the half of the size of the array $costs$.

## 4. Dynamic Programming (Space Optimized)

Looking at the bottom-up recurrence, each cell `dp[aCount][bCount]` only depends on `dp[aCount-1][bCount]` and `dp[aCount][bCount-1]`. We can reduce space by using a 1D array and carefully updating it in the right order.

```cpp
class Solution {
public:
    int twoCitySchedCost(vector<vector<int>>& costs) {
        int n = costs.size() / 2;
        vector<int> dp(n + 1, 0);

        for (int aCount = 0; aCount <= n; aCount++) {
            for (int bCount = 0; bCount <= n; bCount++) {
                int i = aCount + bCount;
                if (i == 0) continue;

                int tmp = dp[bCount];
                dp[bCount] = INT_MAX;
                if (aCount > 0) {
                    dp[bCount] = min(dp[bCount], tmp + costs[i - 1][0]);
                }
                if (bCount > 0) {
                    dp[bCount] = min(dp[bCount], dp[bCount - 1] + costs[i - 1][1]);
                }
            }
        }

        return dp[n];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

> Where $n$ is the half of the size of the array $costs$.

## 5. Greedy

For each person, the "cost difference" `cost[B] - cost[A]` tells us how much extra we pay to send them to city B instead of A. A negative difference means B is cheaper. If we sort by this difference, the first half of people have the smallest (most negative) differences, meaning they benefit most from going to city B.

```cpp
class Solution {
public:
    int twoCitySchedCost(vector<vector<int>>& costs) {
        vector<vector<int>> diffs;
        for (auto& cost : costs) {
            diffs.push_back({cost[1] - cost[0], cost[0], cost[1]});
        }

        sort(diffs.begin(), diffs.end());

        int res = 0;
        for (int i = 0; i < diffs.size(); i++) {
            if (i < diffs.size() / 2) {
                res += diffs[i][2];
            } else {
                res += diffs[i][1];
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 6. Greedy (Optimal)

We can simplify the greedy approach by sorting the original array directly by `cost[B] - cost[A]` without creating extra tuples. After sorting, the first `n` entries favor city B, and the last `n` favor city A.

```cpp
class Solution {
public:
    int twoCitySchedCost(vector<vector<int>>& costs) {
        sort(costs.begin(), costs.end(), [](const auto& a, const auto& b) {
            return (a[1] - a[0]) < (b[1] - b[0]);
        });

        int n = costs.size() / 2, res = 0;
        for (int i = 0; i < n; i++) {
            res += costs[i][1] + costs[i + n][0];
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.
