# 746. Min Cost Climbing Stairs

- **Difficulty:** Easy  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/min-cost-climbing-stairs/>  
- **NeetCode:** <https://neetcode.io/problems/min-cost-climbing-stairs>  
- **Video:** <https://www.youtube.com/watch?v=ktmzAZWkEZ0>  
- **Video approach:** 4. Dynamic Programming (Space Optimized)  

[← Back to index](../INDEX.md)

## 1. Recursion

From any step, you can climb **1 or 2 steps**.
If you step on index `i`, you must **pay `cost[i]`**, then choose the cheaper path ahead.
So the problem is: **from each step, pick the minimum cost path to the top**.

```cpp
class Solution {
public:
    int minCostClimbingStairs(vector<int>& cost) {
        return min(dfs(cost, 0), dfs(cost, 1));
    }

    int dfs(vector<int>& cost, int i) {
        if (i >= cost.size()) {
            return 0;
        }
        return cost[i] + min(dfs(cost, i + 1),
                             dfs(cost, i + 2));
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

The brute force solution recomputes the same subproblems many times.
We can **optimize it by remembering results** once we compute them.

For each step `i`, the minimum cost to reach the top is:

- `cost[i]` + minimum cost from step `i+1` or `i+2`

By storing this result, we avoid repeated work.

```cpp
class Solution {
public:
    vector<int> memo;

    int minCostClimbingStairs(vector<int>& cost) {
        memo.resize(cost.size(), -1);
        return min(dfs(cost, 0), dfs(cost, 1));
    }

    int dfs(vector<int>& cost, int i) {
        if (i >= cost.size()) {
            return 0;
        }
        if (memo[i] != -1) {
            return memo[i];
        }
        memo[i] = cost[i] + min(dfs(cost, i + 1),
                                dfs(cost, i + 2));
        return memo[i];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Instead of solving the problem recursively, we build the answer **from the bottom up**.

Let `dp[i]` represent the **minimum cost to reach step `i`**.
To reach step `i`, you can:

- Come from step `i-1`, after spending `dp[i-1]` to get there, then pay `cost[i-1]`
- Come from step `i-2`, after spending `dp[i-2]` to get there, then pay `cost[i-2]`

We choose the cheaper total cost, not just the cheaper single step cost.

```cpp
class Solution {
public:
    int minCostClimbingStairs(vector<int>& cost) {
        int n = cost.size();
        vector<int> dp(n + 1);

        for (int i = 2; i <= n; i++) {
            dp[i] = min(dp[i - 1] + cost[i - 1],
                        dp[i - 2] + cost[i - 2]);
        }

        return dp[n];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized) ▶ video

At each step, you only need the **minimum cost of the next one or two steps**.
So instead of using a full DP array, we can **reuse the input array** and update it in place.

Each `cost[i]` is updated to represent:

> the minimum cost to reach the top starting from step `i`.

By the end, the answer is simply the minimum cost starting from step `0` or `1`.

```cpp
class Solution {
public:
    int minCostClimbingStairs(vector<int>& cost) {
        for (int i = cost.size() - 3; i >= 0; i--) {
            cost[i] += min(cost[i + 1], cost[i + 2]);
        }
        return min(cost[0], cost[1]);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0746-min-cost-climbing-stairs.cpp` in the NeetCode repo)

```cpp
/*
    Given cost array, ith step is cost[i], can climb 1 or 2 steps
    Return min cost to reach top floor, can start at index 0 or 1
    Ex. cost = [10,15,20] -> 15, start at idx 1, pay 15, climb 2

    Recursion w/ memoization -> DP, min cost to reach 1/2 steps below curr step
    Recurrence relation: minCost[i] = min(minCost[i-1] + cost[i-1], minCost[i-2] + cost[i-2])

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int minCostClimbingStairs(vector<int>& cost) {
        int downOne = 0;
        int downTwo = 0;
        
        for (int i = 2; i <= cost.size(); i++) {
            int temp = downOne;
            downOne = min(downOne + cost[i - 1], downTwo + cost[i - 2]);
            downTwo = temp;
        }
        
        return downOne;
    }
};
```
