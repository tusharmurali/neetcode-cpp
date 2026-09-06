# 2369. Check if There is a Valid Partition For The Array

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/check-if-there-is-a-valid-partition-for-the-array/>  
- **NeetCode:** <https://neetcode.io/problems/check-if-there-is-a-valid-partition-for-the-array>  
- **Video:** <https://www.youtube.com/watch?v=OxXPiwWFdTI>  

[← Back to index](../INDEX.md)

## 1. Recursion

We need to partition the array into subarrays where each subarray is either two equal elements, three equal elements, or three consecutive increasing elements. At each position, we can try taking 2 or 3 elements if they form a valid pattern, then recursively check if the remainder can also be validly partitioned.

```cpp
class Solution {
public:
    bool validPartition(vector<int>& nums) {
        return dfs(nums, 0);
    }

private:
    bool dfs(vector<int>& nums, int i) {
        if (i == nums.size()) return true;

        bool res = false;
        if (i < nums.size() - 1 && nums[i] == nums[i + 1]) {
            res = dfs(nums, i + 2);
        }
        if (i < nums.size() - 2) {
            if ((nums[i] == nums[i + 1] && nums[i + 1] == nums[i + 2]) ||
                (nums[i] + 1 == nums[i + 1] && nums[i + 1] + 1 == nums[i + 2])) {
                res = res || dfs(nums, i + 3);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems because we might reach the same index through different partition choices. By memoizing results for each starting index, we avoid redundant computations. Once we compute whether a valid partition exists from index `i`, we store it and reuse it.

```cpp
class Solution {
public:
    unordered_map<int, bool> memo;

    bool validPartition(vector<int>& nums) {
        return dfs(nums, 0);
    }

private:
    bool dfs(vector<int>& nums, int i) {
        if (i == nums.size()) return true;
        if (memo.count(i)) return memo[i];

        bool res = false;
        if (i < nums.size() - 1 && nums[i] == nums[i + 1]) {
            res = dfs(nums, i + 2);
        }
        if (i < nums.size() - 2) {
            if ((nums[i] == nums[i + 1] && nums[i + 1] == nums[i + 2]) ||
                (nums[i] + 1 == nums[i + 1] && nums[i + 1] + 1 == nums[i + 2])) {
                res = res || dfs(nums, i + 3);
            }
        }

        return memo[i] = res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Instead of starting from the beginning and recursing forward, we can build our solution from the ground up. We define `dp[i]` as whether the first `i` elements can be validly partitioned. We iterate through the array and for each position, check if we can extend a valid partition by adding a valid 2-element or 3-element subarray.

```cpp
class Solution {
public:
    bool validPartition(vector<int>& nums) {
        vector<bool> dp(nums.size() + 1, false);
        dp[0] = true;

        for (int i = 2; i <= nums.size(); i++) {
            if (nums[i - 1] == nums[i - 2]) {
                dp[i] = dp[i] || dp[i - 2];
            }
            if (i > 2 && ((nums[i - 1] == nums[i - 2] && nums[i - 2] == nums[i - 3]) ||
                          (nums[i - 3] + 1 == nums[i - 2] && nums[i - 2] + 1 == nums[i - 1]))) {
                dp[i] = dp[i] || dp[i - 3];
            }
        }

        return dp[nums.size()];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized)

Since each DP state only depends on the previous three states (`dp[i-1]`, `dp[i-2]`, `dp[i-3]`), we do not need to store the entire DP array. We can use just three variables and rotate them as we iterate through the array from right to left.

```cpp
class Solution {
public:
    bool validPartition(vector<int>& nums) {
        bool dp[3] = {false, true, true};

        for (int i = nums.size() - 2; i >= 0; --i) {
            bool dp1 = dp[0];
            if (nums[i] == nums[i + 1] && dp[1]) {
                dp[0] = true;
            } else if (i < nums.size() - 2 && dp[2] &&
                      ((nums[i] == nums[i + 1] && nums[i] == nums[i + 2]) ||
                      (nums[i] + 1 == nums[i + 1] && nums[i + 1] == nums[i + 2] - 1))) {
                dp[0] = true;
            } else {
                dp[0] = false;
            }
            dp[2] = dp[1];
            dp[1] = dp1;
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
