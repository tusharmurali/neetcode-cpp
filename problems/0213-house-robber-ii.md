# 213. House Robber II

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/house-robber-ii/>  
- **NeetCode:** <https://neetcode.io/problems/house-robber-ii>  
- **Video:** <https://www.youtube.com/watch?v=rWAJCfYYOvM>  
- **Video approach:** 4. Dynamic Programming (Space Optimized)  

[← Back to index](../INDEX.md)

## 1. Recursion

This is **House Robber II**, where houses are in a **circle**.  
So the **first and last house cannot both be robbed**.

To handle the circular constraint, we split the problem into **two linear cases**:

1. **Rob from house `0` to `n-2`** (exclude last house)
2. **Rob from house `1` to `n-1`** (exclude first house)

The recursive function explores:

- **Skip the current house**
- **Rob the current house** and jump two steps ahead

A flag is used to ensure that **if the first house is robbed, the last house is not allowed**.

Finally, we take the **maximum result from the two cases**.

```cpp
class Solution {
public:
    int rob(vector<int>& nums) {
        if (nums.size() == 1) return nums[0];
        return max(dfs(0, true, nums), dfs(1, false, nums));
    }

private:
    int dfs(int i, bool flag, vector<int>& nums) {
        if (i >= nums.size() || (flag && i == nums.size() - 1))
            return 0;

        return max(dfs(i + 1, flag, nums),
                   nums[i] + dfs(i + 2, flag || i == 0, nums));
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

This is **House Robber II (circular houses)** with **Top-Down DP**.

Because houses form a **circle**, the **first and last houses cannot both be robbed**.  
We handle this by tracking a **flag** that tells us whether the **first house was robbed**.

At each house, we have two choices:

- **Skip the house**
- **Rob the house** (then skip the next one)

Memoization is used so each state `(index, flag)` is solved only once.

```cpp
class Solution {
    vector<vector<int>> memo;

public:
    int rob(vector<int>& nums) {
        if (nums.size() == 1) return nums[0];

        memo.resize(nums.size(), vector<int>(2, -1));
        return max(dfs(0, 1, nums), dfs(1, 0, nums));
    }

private:
    int dfs(int i, int flag, vector<int>& nums) {
        if (i >= nums.size() || (flag == 1 && i == nums.size() - 1))
            return 0;
        if (memo[i][flag] != -1)
            return memo[i][flag];
        memo[i][flag] = max(dfs(i + 1, flag, nums),
                        nums[i] + dfs(i + 2, flag | (i == 0 ? 1 : 0), nums));
        return memo[i][flag];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

This is **House Robber II (circular houses)** solved using **Bottom-Up Dynamic Programming**.

Because houses are in a **circle**, you **cannot rob both the first and last house**.  
So we split the problem into **two linear cases**:

- Rob houses from **index 1 to n-1** (exclude first house)
- Rob houses from **index 0 to n-2** (exclude last house)

Each case becomes the normal **House Robber I** problem.

```cpp
class Solution {
public:
    int rob(std::vector<int>& nums) {
        if (nums.size() == 1) return nums[0];

        return max(helper(vector<int>(nums.begin() + 1, nums.end())),
                        helper(vector<int>(nums.begin(), nums.end() - 1)));
    }

    int helper(vector<int> nums) {
        if (nums.empty()) return 0;
        if (nums.size() == 1) return nums[0];

        vector<int> dp(nums.size());
        dp[0] = nums[0];
        dp[1] = max(nums[0], nums[1]);

        for (int i = 2; i < nums.size(); i++) {
            dp[i] = max(dp[i - 1], nums[i] + dp[i - 2]);
        }

        return dp.back();
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized) ▶ video

This is **House Robber II**, where houses are arranged in a **circle**.  
Because of the circular setup, **you cannot rob both the first and last house**.

To handle this, split the problem into **two linear subproblems**:

1. Rob houses **excluding the first house**.
2. Rob houses **excluding the last house**.

Each subproblem becomes the classic **House Robber I**, which can be solved using **two variables** instead of a full DP array.

```cpp
class Solution {
public:
    int rob(vector<int>& nums) {
        vector<int> nums1(nums.begin() + 1, nums.end());
        vector<int> nums2(nums.begin(), nums.end() - 1);
        return max(nums[0],
               max(helper(nums1), helper(nums2)));
    }

private:
    int helper(vector<int>& nums) {
        int rob1 = 0, rob2 = 0;
        for (int num : nums) {
            int newRob = max(rob1 + num, rob2);
            rob1 = rob2;
            rob2 = newRob;
        }
        return rob2;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0213-house-robber-ii.cpp` in the NeetCode repo)

```cpp
/*
    Given int array in a circle, return max amount can rob (can't rob adj houses)
    Ex. nums = [2,3,2] -> 3, can't rob house 1 & 3 b/c circular adj, so rob 2

    Recursion w/ memo -> DP, rob either 2 away + here, or 1 away, try both ranges
    Recurrence relation: robFrom[i] = max(robFrom[i-2] + nums[i], robFrom[i-1])

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        
        if (n == 1) {
            return nums[0];
        }
        
        int range1 = robber(nums, 0, n - 2);
        int range2 = robber(nums, 1, n - 1);
        
        return max(range1, range2);
    }
private:
    int robber(vector<int>& nums, int start, int end) {
        int prev = 0;
        int curr = 0;
        int next = 0;
        
        for (int i = start; i <= end; i++) {
            next = max(prev + nums[i], curr);
            prev = curr;
            curr = next;
        }
        
        return curr;
    }
};
```
