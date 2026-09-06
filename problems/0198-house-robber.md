# 198. House Robber

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/house-robber/>  
- **NeetCode:** <https://neetcode.io/problems/house-robber>  
- **Video:** <https://www.youtube.com/watch?v=73r3KWiEvyk>  

[← Back to index](../INDEX.md)

## 1. Recursion

At every house, you have **two choices**:

- **Skip** the current house → move to the next house.
- **Rob** the current house → take its money and skip the next house.

The goal is to choose the option that gives the **maximum total money**.
Recursion tries **both choices at each index** and returns the best result.

```cpp
class Solution {
public:
    int rob(vector<int>& nums) {
        return dfs(nums, 0);
    }

    int dfs(vector<int>& nums, int i) {
        if (i >= nums.size()) {
            return 0;
        }
        return max(dfs(nums, i + 1),
                   nums[i] + dfs(nums, i + 2));
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

The recursive solution recomputes the same subproblems many times.
To optimize this, we **store the result for each index** once it’s computed.

At every house `i`, you still have **two choices**:

- Skip the house → go to `i + 1`
- Rob the house → take `nums[i]` and go to `i + 2`

Using **memoization**, each index is solved only once.

```cpp
class Solution {
public:
    vector<int> memo;

    int rob(vector<int>& nums) {
        memo.resize(nums.size(), -1);
        return dfs(nums, 0);
    }

    int dfs(vector<int>& nums, int i) {
        if (i >= nums.size()) {
            return 0;
        }
        if (memo[i] != -1) {
            return memo[i];
        }
        memo[i] = max(dfs(nums, i + 1),
                    nums[i] + dfs(nums, i + 2));
        return memo[i];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Instead of deciding recursively, we **build the answer step by step**.

For each house `i`, the maximum money we can have depends on:

- **Not robbing it** → same money as `i - 1`
- **Robbing it** → money at `i` + best up to `i - 2`

We choose the **better of the two** at every step.

```cpp
class Solution {
public:
    int rob(vector<int>& nums) {
        if (nums.empty()) return 0;
        if (nums.size() == 1) return nums[0];

        vector<int> dp(nums.size());
        dp[0] = nums[0];
        dp[1] = max(nums[0], nums[1]);

        for (int i = 2; i < nums.size(); i++) {
            dp[i] = max(dp[i - 1], nums[i] + dp[i - 2]);
        }

        return dp[nums.size() - 1];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized)

We don’t actually need a full DP array.

At any house, we only care about:

- the **best result up to the previous house**
- the **best result up to the house before that**

So instead of storing everything, we just keep **two variables** and update them as we move forward.

For each house:

- Either **skip it** → keep previous best
- Or **rob it** → current money + best from two steps back  
  Pick the maximum.

```cpp
class Solution {
public:
    int rob(vector<int>& nums) {
        int rob1 = 0, rob2 = 0;

        for (int num : nums) {
            int temp = max(num + rob1, rob2);
            rob1 = rob2;
            rob2 = temp;
        }
        return rob2;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0198-house-robber.cpp` in the NeetCode repo)

```cpp
/*
    Given int array, return max amount can rob (can't rob adjacent houses)
    Ex. nums = [1,2,3,1] -> 4, rob house 1 then house 3: 1 + 3 = 4

    Recursion w/ memoization -> DP, rob either 2 away + here, or 1 away
    Recurrence relation: robFrom[i] = max(robFrom[i-2] + nums[i], robFrom[i-1])

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int rob(vector<int>& nums) {
        int prev = 0;
        int curr = 0;
        int next = 0;
        
        for (int i = 0; i < nums.size(); i++) {
            next = max(prev + nums[i], curr);
            prev = curr;
            curr = next;
        }
        
        return curr;
    }
};
```
