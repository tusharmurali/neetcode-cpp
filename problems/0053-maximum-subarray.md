# 53. Maximum Subarray

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/maximum-subarray/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-subarray>  
- **Video:** <https://www.youtube.com/watch?v=5WZl3MMT0Eg>  
- **Video approach:** 6. Kadane's Algorithm  

[← Back to index](../INDEX.md)

## 1. Brute Force

This problem asks us to find the **maximum sum of any contiguous subarray**.

The most straightforward way to think about this is:

- try **every possible subarray**
- calculate its sum
- keep track of the maximum sum we see

A subarray is defined by a start index `i` and an end index `j`.
By fixing `i` and expanding `j` to the right, we can compute the sum of all subarrays that start at `i`.

This approach is easy to understand and works well for learning, but it is not efficient for large inputs.

```cpp
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int n = nums.size(), res = nums[0];
        for (int i = 0; i < n; i++) {
            int cur = 0;
            for (int j = i; j < n; j++) {
                cur += nums[j];
                res = max(res, cur);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Recursion

We want the **maximum sum of a contiguous subarray**.

Using recursion, we can think of the problem as making a decision at each index:

- either we **haven’t started** a subarray yet
- or we are **already inside** a subarray and can choose whether to continue it or stop

The recursive function keeps track of this using a flag:

- `flag = False` - we have not started a subarray yet
- `flag = True` - we are currently building a subarray

The function answers the question:  
**“What is the maximum subarray sum we can get starting from index `i`, given whether we are already inside a subarray or not?”**

By exploring both possibilities at every step, the recursion eventually finds the best contiguous subarray.

```cpp
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        return dfs(nums, 0, false);
    }

private:
    int dfs(vector<int>& nums, int i, bool flag) {
        if (i == nums.size() - 1) return flag ? max(0, nums[i]) : nums[i];
        if (flag) return max(0, nums[i] + dfs(nums, i + 1, true));
        return max(dfs(nums, i + 1, false),
                   nums[i] + dfs(nums, i + 1, true));
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Top-Down)

We want to find the **maximum sum of a contiguous subarray**.

In the recursive solution, we modeled the problem using two states:

- we have **not started** a subarray yet
- we are **already inside** a subarray

However, plain recursion repeats the same computations many times.  
To optimize this, we use **top-down dynamic programming (memoization)**.

Each state is uniquely identified by:

- `i`: the current index in the array
- `flag`: whether a subarray has already started (`True`) or not (`False`).

The function answers:  
**“What is the maximum subarray sum we can get starting from index `i`, given whether a subarray is already in progress?”**

By storing results for each `(i, flag)` state, we avoid recomputing them.

```cpp
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        vector<array<int, 2>> memo(nums.size());
        vector<array<bool, 2>> seen(nums.size(), {false, false});
        return dfs(nums, 0, false, memo, seen);
    }

private:
    int dfs(vector<int>& nums, int i, bool flag,
            vector<array<int, 2>>& memo, vector<array<bool, 2>>& seen) {
        if (i == nums.size() - 1) return flag ? max(0, nums[i]) : nums[i];
        int f = flag ? 1 : 0;
        if (seen[i][f]) return memo[i][f];
        if (flag)
            memo[i][f] = max(0, nums[i] + dfs(nums, i + 1, true, memo, seen));
        else
            memo[i][f] = max(dfs(nums, i + 1, false, memo, seen),
                             nums[i] + dfs(nums, i + 1, true, memo, seen));
        seen[i][f] = true;
        return memo[i][f];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Bottom-Up)

We want the **maximum sum of a contiguous subarray**.

From the recursive and top-down DP solutions, we observed two useful states:

- the best subarray sum **starting exactly at index `i`**
- the best subarray sum **starting at or after index `i`**

Instead of recursion, we can compute these values iteratively using **bottom-up dynamic programming**.

At each index, we decide:

- whether to start a new subarray at the current element
- or extend a subarray from the next index

By filling the DP table from right to left, all needed future values are already known.

```cpp
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int n = nums.size();
        vector<vector<int>> dp(n + 1, vector<int>(2, 0));

        dp[n - 1][1] = dp[n - 1][0] = nums[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            dp[i][1] = max(nums[i], nums[i] + dp[i + 1][1]);
            dp[i][0] = max(dp[i + 1][0], dp[i][1]);
        }

        return dp[0][0];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 5. Dynamic Programming (Space Optimized)

We want the **maximum sum of a contiguous subarray**.

At every position, we have a simple choice:

- start a new subarray at the current element
- or extend the subarray that ended at the previous index

If the sum up to the previous index is negative, extending it would only make things worse, so we start fresh at the current element.

This idea allows us to keep track of the best subarray sum ending at each index and update it in a single pass.

```cpp
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        vector<int> dp(nums);
        for (int i = 1; i < nums.size(); i++) {
            dp[i] = max(nums[i], nums[i] + dp[i - 1]);
        }
        return *max_element(dp.begin(), dp.end());
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 6. Kadane's Algorithm ▶ video

We want the **maximum sum of a contiguous subarray**.

Kadane’s Algorithm is based on one simple observation:

- if the running sum becomes negative, keeping it will only reduce the sum of any future subarray

So whenever the current sum drops below zero, we **reset** it and start a new subarray from the next element.

As we scan the array once, we keep track of:

- the best subarray sum ending at the current position
- the best subarray sum seen overall

```cpp
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int maxSub = nums[0], curSum = 0;
        for (int num : nums) {
            if (curSum < 0) {
                curSum = 0;
            }
            curSum += num;
            maxSub = max(maxSub, curSum);
        }
        return maxSub;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 7. Divide & Conquer

We want the **maximum sum of a contiguous subarray**.

Using **divide and conquer**, we split the array into two halves and solve the problem recursively.  
For any subarray `[l .. r]`, the maximum subarray must be one of these three cases:

1. Entirely in the **left half**
2. Entirely in the **right half**
3. **Crossing the middle** (includes the middle element)

The first two cases are solved recursively.  
The third case is handled by:

- taking the maximum sum extending **left** from the middle
- taking the maximum sum extending **right** from the middle
- adding both to the middle element

The recursive function represents:  
**“What is the maximum subarray sum within the range `[l .. r]`?”**

```cpp
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        return dfs(nums, 0, nums.size() - 1);
    }

private:
    int dfs(vector<int>& nums, int l, int r) {
        if (l > r) {
            return INT_MIN;
        }
        int m = (l + r) >> 1;
        int leftSum = 0, rightSum = 0, curSum = 0;
        for (int i = m - 1; i >= l; --i) {
            curSum += nums[i];
            leftSum = max(leftSum, curSum);
        }
        curSum = 0;
        for (int i = m + 1; i <= r; ++i) {
            curSum += nums[i];
            rightSum = max(rightSum, curSum);
        }
        return max(dfs(nums, l, m - 1),
                   max(dfs(nums, m + 1, r),
                       leftSum + nums[m] + rightSum));
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(\log n)$

## Standalone solution file (`cpp/0053-maximum-subarray.cpp` in the NeetCode repo)

```cpp
/*
    Given int array, find contiguous subarray w/ max sum
    Ex. nums = [-2,1,-3,4,-1,2,1,-5,4] -> 6, [4,-1,2,1]

    At each point, determine if it's better to add to curr sum or start over

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int curr = nums[0];
        int result = nums[0];
        
        for (int i = 1; i < nums.size(); i++) {
            curr = max(curr + nums[i], nums[i]);
            result = max(result, curr);
        }
        
        return result;
    }
};
```
