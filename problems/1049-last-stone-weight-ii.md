# 1049. Last Stone Weight II

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/last-stone-weight-ii/>  
- **NeetCode:** <https://neetcode.io/problems/last-stone-weight-ii>  
- **Video:** <https://www.youtube.com/watch?v=gdXkkmzvR3c>  
- **Video approach:** 2. Dynamic Programming (Top-Down)  

[← Back to index](../INDEX.md)

## 1. Recursion

The key insight is that smashing stones is equivalent to partitioning them into two groups and finding the minimum difference between their sums. When two stones collide, the result is the absolute difference of their weights. If we think of assigning a positive or negative sign to each stone, the final result is the absolute value of the sum. This transforms the problem into finding a subset with sum as close to half the total as possible.

```cpp
class Solution {
public:
    int lastStoneWeightII(vector<int>& stones) {
        int stoneSum = accumulate(stones.begin(), stones.end(), 0);
        int target = (stoneSum + 1) / 2;
        return dfs(0, 0, stones, stoneSum, target);
    }

private:
    int dfs(int i, int total, const vector<int>& stones, int stoneSum, int target) {
        if (total >= target || i == stones.size()) {
            return abs(total - (stoneSum - total));
        }
        return min(
            dfs(i + 1, total, stones, stoneSum, target),
            dfs(i + 1, total + stones[i], stones, stoneSum, target)
        );
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(min(n, m))$ for recursion stack.

> Where $n$ is the number of stones and $m$ is the sum of the weights of the stones.

## 2. Dynamic Programming (Top-Down) ▶ video

The recursive solution recomputes the same subproblems many times. For example, reaching a total of `10` using stones at different indices might happen through multiple paths. By caching results based on the current index and running total, we avoid redundant work and speed up the solution significantly.

```cpp
class Solution {
private:
    vector<vector<int>> dp;

public:
    int lastStoneWeightII(vector<int>& stones) {
        int stoneSum = accumulate(stones.begin(), stones.end(), 0);
        int target = (stoneSum + 1) / 2;
        dp = vector<vector<int>>(stones.size(), vector<int>(target + 1, -1));
        return dfs(0, 0, stones, stoneSum, target);
    }

private:
    int dfs(int i, int total, const vector<int>& stones, int stoneSum, int target) {
        if (total >= target || i == stones.size()) {
            return abs(total - (stoneSum - total));
        }
        if (dp[i][total] != -1) {
            return dp[i][total];
        }

        dp[i][total] = min(
            dfs(i + 1, total, stones, stoneSum, target),
            dfs(i + 1, total + stones[i], stones, stoneSum, target)
        );
        return dp[i][total];
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ is the number of stones and $m$ is the sum of the weights of the stones.

## 3. Dynamic Programming (Bottom-Up)

Instead of working recursively from the first stone forward, we can build up solutions iteratively. We create a 2D table where `dp[i][t]` represents the maximum sum achievable using the first `i` stones without exceeding capacity `t`. This is essentially a 0/1 knapsack problem where we want to pack stones into a knapsack of capacity `target` to maximize the total weight.

```cpp
class Solution {
public:
    int lastStoneWeightII(vector<int>& stones) {
        int stoneSum = accumulate(stones.begin(), stones.end(), 0);
        int target = stoneSum / 2;
        int n = stones.size();

        vector<vector<int>> dp(n + 1, vector<int>(target + 1, 0));

        for (int i = 1; i <= n; i++) {
            for (int t = 0; t <= target; t++) {
                if (t >= stones[i - 1]) {
                    dp[i][t] = max(dp[i - 1][t], dp[i - 1][t - stones[i - 1]] + stones[i - 1]);
                } else {
                    dp[i][t] = dp[i - 1][t];
                }
            }
        }

        return stoneSum - 2 * dp[n][target];
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ is the number of stones and $m$ is the sum of the weights of the stones.

## 4. Dynamic Programming (Space Optimized)

Looking at the bottom-up solution, each row only depends on the previous row. This means we don't need to store the entire 2D table. A single 1D array is sufficient if we iterate through capacities in reverse order to avoid overwriting values we still need.

```cpp
class Solution {
public:
    int lastStoneWeightII(vector<int>& stones) {
        int stoneSum = accumulate(stones.begin(), stones.end(), 0);
        int target = stoneSum / 2;
        vector<int> dp(target + 1, 0);

        for (int stone : stones) {
            for (int t = target; t >= stone; t--) {
                dp[t] = max(dp[t], dp[t - stone] + stone);
            }
        }

        return stoneSum - 2 * dp[target];
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(m)$

> Where $n$ is the number of stones and $m$ is the sum of the weights of the stones.

## 5. Dynamic Programming (Hash Set)

Instead of tracking the maximum achievable sum at each capacity, we can simply track which sums are reachable. A hash set stores all possible subset sums. For each stone, we generate new reachable sums by adding the stone's weight to existing sums. The answer is the largest reachable sum that doesn't exceed `target`.

```cpp
class Solution {
public:
    int lastStoneWeightII(vector<int>& stones) {
        int stoneSum = accumulate(stones.begin(), stones.end(), 0);
        int target = stoneSum / 2;

        unordered_set<int> dp = {0};

        for (int& stone : stones) {
            unordered_set<int> newDp(dp);
            for (int val : dp) {
                if (val + stone == target) {
                    return stoneSum - 2 * target;
                }
                if (val + stone < target) {
                    newDp.insert(val + stone);
                }
            }
            dp = newDp;
        }

        int maxVal = 0;
        for (int val : dp) {
            maxVal = max(maxVal, val);
        }

        return stoneSum - 2 * maxVal;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(m)$

> Where $n$ is the number of stones and $m$ is the sum of the weights of the stones.

## 6. Dynamic Programming (Bitset)

A bitset can represent reachable sums more compactly than a hash set. Each bit position represents whether that sum is achievable. Shifting the bitset left by a stone's weight and OR-ing with the original efficiently computes all new reachable sums in a single operation.

```cpp
class Solution {
public:
    int lastStoneWeightII(vector<int>& stones) {
        int stoneSum = accumulate(stones.begin(), stones.end(), 0);
        int target = stoneSum / 2;
        bitset<3001> dp;
        dp[0] = true;

        for (int stone : stones) {
            dp |= (dp << stone);
        }

        for (int t = target; t >= 0; --t) {
            if (dp[t]) {
                return stoneSum - 2 * t;
            }
        }
        return 0;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(m)$

> Where $n$ is the number of stones and $m$ is the sum of the weights of the stones.
