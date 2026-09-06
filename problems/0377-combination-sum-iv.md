# 377. Combination Sum IV

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/combination-sum-iv/>  
- **NeetCode:** <https://neetcode.io/problems/combination-sum-iv>  
- **Video:** <https://www.youtube.com/watch?v=dw2nMCxG0ik>  

[← Back to index](../INDEX.md)

## 1. Recursion

We need to count all possible combinations (with different orderings counted separately) that sum to the target. At each step, we can pick any number from the array and subtract it from our remaining sum. This naturally leads to a recursive approach where we try every number at each position.

```cpp
class Solution {
public:
    int combinationSum4(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        return dfs(nums, target);
    }

    int dfs(vector<int>& nums, int total) {
        if (total == 0) {
            return 1;
        }

        int res = 0;
        for (int num : nums) {
            if (total < num) {
                break;
            }
            res += dfs(nums, total - num);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ t)$
- Space complexity: $O(t)$

> Where $n$ is the size of the array $nums$ and $t$ is the given target.

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems since the same remaining total can be reached through different paths. By caching results for each total value, we avoid redundant computations. This memoization transforms exponential time complexity into polynomial.

```cpp
class Solution {
private:
    unordered_map<int, int> memo;

public:
    int combinationSum4(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        memo[0] = 1;
        return dfs(nums, target);
    }

    int dfs(vector<int>& nums, int total) {
        if (memo.count(total)) {
            return memo[total];
        }

        int res = 0;
        for (int num : nums) {
            if (total < num) {
                break;
            }
            res += dfs(nums, total - num);
        }
        memo[total] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * t)$
- Space complexity: $O(t)$

> Where $n$ is the size of the array $nums$ and $t$ is the given target.

## 3. Dynamic Programming (Bottom-Up) - I

Instead of working backwards from the target, we can build up the solution by computing the number of ways to reach each sum from 0 to target. For each sum, we check all numbers in the array and add the ways to reach the sum minus that number.

```cpp
class Solution {
public:
    int combinationSum4(vector<int>& nums, int target) {
        unordered_map<int, long long> dp;
        dp[0] = 1;

        for (int total = 1; total <= target; total++) {
            dp[total] = 0;
            for (int num : nums) {
                if (total >= num) {
                    dp[total] += dp[total - num];
                }
            }
            if (dp[total] > INT_MAX) {
                dp[total] = 0;
            }
        }
        return dp[target];
    }
};
```

**Complexity**

- Time complexity: $O(n * t)$
- Space complexity: $O(t)$

> Where $n$ is the size of the array $nums$ and $t$ is the given target.

## 4. Dynamic Programming (Bottom-Up) - II

We can also work backwards from the target. Starting at the target, each number represents how many ways we can reach the target from that sum. When we subtract a number from the current total, we propagate the count to the resulting sum.

```cpp
class Solution {
public:
    int combinationSum4(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        unordered_map<int, int> dp;
        dp[target] = 1;

        for (int total = target; total > 0; total--) {
            if (dp[total] == -1) continue;
            for (auto& num : nums) {
                if (total < num) break;
                if (dp[total - num] + 0LL + dp[total] > INT_MAX) {
                    dp[total - num] = -1;
                    break;
                }
                dp[total - num] += dp[total];
            }
        }
        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n * t)$
- Space complexity: $O(t)$

> Where $n$ is the size of the array $nums$ and $t$ is the given target.

## Standalone solution file (`cpp/0377-combination-sum-iv.cpp` in the NeetCode repo)

```cpp
/*
    Given an array of distinct integers nums and a target integer 'target', 
    return the number of possible combinations that add up to target.
    
    Ex. nums = [1,2,3] target = 4
    Possible Combinations: (1,1,1,1) (1,1,2) (1,2,1) (1,3) (2,1,1,)
    (2,2) (3,1). 
    So, total number of combinations possible is 7.

    Time: O(n * m)
    Space: O(m)
*/

class Solution {
public:
    int combinationSum4(vector<int>& nums, int target) {
    sort(nums.begin(), nums.end());
    vector<unsigned int> dp(target+1, 0);
    dp[0] = 1;
    for(int total=1; total<=target; total++) {
        for(int i=0; i<nums.size(); i++) {
            if(nums[i] <= total) dp[total] += dp[total - nums[i]];
            else break;
        }
    }
    return dp[target];
    }
};
```
