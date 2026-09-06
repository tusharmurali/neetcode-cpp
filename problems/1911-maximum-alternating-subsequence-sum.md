# 1911. Maximum Alternating Subsequence Sum

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-alternating-subsequence-sum/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-alternating-subsequence-sum>  
- **Video:** <https://www.youtube.com/watch?v=4v42XOuU1XA>  

[← Back to index](../INDEX.md)

## 1. Recursion

An alternating subsequence sum adds elements at even positions and subtracts elements at odd positions. At each index, we have two choices: include the current element in our subsequence or skip it. If we include it, the sign depends on whether we are at an even or odd position in our chosen subsequence.

The recursive approach explores both choices at every index and tracks whether the next element we pick would be at an even or odd position.

```cpp
class Solution {
public:
    long long maxAlternatingSum(vector<int>& nums) {
        return dfs(nums, 0, true);
    }

private:
    long long dfs(vector<int>& nums, int i, bool even) {
        if (i == nums.size()) {
            return 0;
        }
        long long total = even ? nums[i] : -nums[i];
        return max(total + dfs(nums, i + 1, !even), dfs(nums, i + 1, even));
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems. The state `(i, even)` can be reached multiple times through different paths, so we can cache results to avoid redundant computation.

Since there are `n` possible indices and `2` possible parity states, we have `O(n)` unique states. Memoizing these transforms the exponential time complexity into linear.

```cpp
class Solution {
    vector<vector<long long>> dp;

public:
    long long maxAlternatingSum(vector<int>& nums) {
        dp.assign(nums.size(), vector<long long>(2, -1));
        return dfs(nums, 0, true);
    }

private:
    long long dfs(vector<int>& nums, int i, bool even) {
        if (i == nums.size()) {
            return 0;
        }
        if (dp[i][even] != -1) {
            return dp[i][even];
        }
        long long total = even ? nums[i] : -nums[i];
        dp[i][even] = max(total + dfs(nums, i + 1, !even), dfs(nums, i + 1, even));
        return dp[i][even];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

We can convert the top-down approach to bottom-up by filling the DP table iteratively. For each position, we track two values: the maximum alternating sum if the next element we pick would be at an even position, and the maximum if it would be at an odd position.

Working backwards from the end of the array, we compute these values based on the two choices at each position (pick or skip).

```cpp
class Solution {
public:
    long long maxAlternatingSum(vector<int>& nums) {
        int n = nums.size();
        vector<vector<long long>> dp(n + 1, vector<long long>(2, 0)); // dp[i][0] -> odd, dp[i][1] -> even

        for (int i = n - 1; i >= 0; i--) {
            dp[i][1] = max(nums[i] + dp[i + 1][0], dp[i + 1][1]); // even
            dp[i][0] = max(-nums[i] + dp[i + 1][1], dp[i + 1][0]); // odd
        }

        return dp[0][1];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized)

Notice that each state only depends on the state at the next index. We do not need the entire DP table; just two variables suffice to track the best even-position sum and odd-position sum for the suffix starting at the current index.

This reduces space from O(n) to O(1) while maintaining the same logic.

```cpp
class Solution {
public:
    long long maxAlternatingSum(vector<int>& nums) {
        long long sumEven = 0, sumOdd = 0;

        for (int i = nums.size() - 1; i >= 0; i--) {
            long long tmpEven = max(nums[i] + sumOdd, sumEven);
            long long tmpOdd = max(-nums[i] + sumEven, sumOdd);
            sumEven = tmpEven;
            sumOdd = tmpOdd;
        }

        return sumEven;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/1911-maximum-alternating-subsequence-sum.cpp` in the NeetCode repo)

```cpp
/*
Given an array nums, return the maximum alternating sum of any subsequence of nums (after reindexing the elements of the subsequence).
The alternating sum of a 0-indexed array is defined as the sum of the elements at even indices minus the sum of the elements at odd indices.
For example, the alternating sum of [4,2,5,3] is (4 + 5) - (2 + 3) = 4.

Example. Let nums = [6,2,1,2,4,5].
         The subsequence {6,1,5} can be choosen which gives maximum alternating sum of (6 + 5) - 1 = 10, which is the optimal solution in this case.
	 So we return 10 as our answer.



Time: O(n)
Space: O(1)

*/


class Solution {
public:
    long long maxAlternatingSum(vector<int>& nums) {
        long long even = 0, odd = 0, tmpEven, tmpOdd;
        for(int i=nums.size()-1; i>=0; i--) {
            tmpEven = max(odd + nums[i], even);
            tmpOdd = max(even - nums[i], odd);
            even = tmpEven;
            odd = tmpOdd;
        }
        return even;
    }
};
```
