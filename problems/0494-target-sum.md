# 494. Target Sum

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/target-sum/>  
- **NeetCode:** <https://neetcode.io/problems/target-sum>  
- **Video:** <https://www.youtube.com/watch?v=dwMOrl85Xes>  

[← Back to index](../INDEX.md)

## 1. Recursion

This problem asks us to count how many different ways we can assign a `+` or `-` sign to each number so that the final sum equals the target.

At every index, we have **two independent choices**:
- add the current number to the total
- subtract the current number from the total

Using recursion, we try all possible sign assignments.  
The recursive function represents:
**"How many ways can we reach the target starting from index `i` with the current sum `total`?"**

When all numbers are processed, we simply check whether the accumulated sum equals the target.

```cpp
class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        return backtrack(0, 0, nums, target);
    }

    int backtrack(int i, int total, vector<int>& nums, int target) {
        if (i == nums.size()) {
            return total == target;
        }
        return backtrack(i + 1, total + nums[i], nums, target) +
               backtrack(i + 1, total - nums[i], nums, target);
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

This problem asks us to count the number of ways to assign a `+` or `-` sign to each number so that the final sum equals the target.

The recursive solution tries all possible sign combinations, but many subproblems repeat. To avoid recomputing the same states, we use **top-down dynamic programming (memoization)**.

Each state is uniquely defined by:
- the current index `i`
- the current accumulated sum `total`

The recursive function answers the question:
**"How many ways can we reach the target starting from index `i` with the current sum `total`?"**

By caching results for each state, we significantly improve efficiency.

```cpp
class Solution {
    vector<vector<int>> dp;
    int totalSum;

public:
    int findTargetSumWays(vector<int>& nums, int target) {
        totalSum = accumulate(nums.begin(), nums.end(), 0);
        dp = vector<vector<int>>(nums.size(), vector<int>(2 * totalSum + 1, INT_MIN));
        return backtrack(0, 0, nums, target);
    }

    int backtrack(int i, int total, vector<int>& nums, int target) {
        if (i == nums.size()) {
            return total == target;
        }
        if (dp[i][total + totalSum] != INT_MIN) {
            return dp[i][total + totalSum];
        }
        dp[i][total + totalSum] = backtrack(i + 1, total + nums[i], nums, target) +
                                  backtrack(i + 1, total - nums[i], nums, target);
        return dp[i][total + totalSum];
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ is the length of the array $nums$ and $m$ is the sum of all the elements in the array.

## 3. Dynamic Programming (Bottom-Up)

We need to count how many ways we can assign a `+` or `-` sign to each number so that the final sum equals the target.

Instead of using recursion, we can solve this using **bottom-up dynamic programming**, where we build solutions step by step as we process each number.

At each position, we keep track of:
- all possible sums we can form
- how many ways each sum can be formed

As we move forward, each existing sum can branch into two new sums by adding or subtracting the current number.

```cpp
class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        int n = nums.size();
        vector<unordered_map<int, int>> dp(n + 1);
        dp[0][0] = 1;

        for (int i = 0; i < n; i++) {
            for (auto &p : dp[i]) {
                dp[i + 1][p.first + nums[i]] += p.second;
                dp[i + 1][p.first - nums[i]] += p.second;
            }
        }
        return dp[n][target];
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ is the length of the array $nums$ and $m$ is the sum of all the elements in the array.

## 4. Dynamic Programming (Space Optimized)

We want to count the number of ways to assign `+` and `-` signs to the numbers so that their final sum equals the target.

In the bottom-up DP approach, we used a separate data structure for each index. However, at each step, the new states depend **only on the previous step**, not on all earlier steps.

This means we can **reuse a single data structure** to keep track of all possible sums and how many ways each sum can be formed, updating it as we process each number.

```cpp
class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        unordered_map<int, int> dp;
        dp[0] = 1;

        for (int num : nums) {
            unordered_map<int, int> nextDp;
            for (auto& entry : dp) {
                int total = entry.first;
                int count = entry.second;
                nextDp[total + num] += count;
                nextDp[total - num] += count;
            }
            dp = nextDp;
        }
        return dp[target];
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(m)$

> Where $n$ is the length of the array $nums$ and $m$ is the sum of all the elements in the array.

## Standalone solution file (`cpp/0494-target-sum.cpp` in the NeetCode repo)

```cpp
/*
    Given int array & a target, want to build expressions w/ '+' & '-'
    Return number of different expressions that evaluates to target

    Recursion w/ memoization, cache on (index, total), which stores # ways
    If total ever reaches the target, return 1 (this is a way), else 0

    Time: O(n x target)
    Space: O(n x target)
*/

class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        return backtrack(nums, target, 0, 0);
    }
private:
    // {(index, total) -> # of ways}
    map<pair<int, int>, int> dp;
    
    int backtrack(vector<int>& nums, int target, int i, int total) {
        if (i == nums.size()) {
            return total == target ? 1 : 0;
        }
        if (dp.find({i, total}) != dp.end()) {
            return dp[{i, total}];
        }
        
        dp[{i, total}] = backtrack(nums, target, i + 1, total + nums[i])
                       + backtrack(nums, target, i + 1, total - nums[i]);
        
        return dp[{i, total}];
    }
};
```
