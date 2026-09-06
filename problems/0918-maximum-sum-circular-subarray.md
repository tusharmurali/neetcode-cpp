# 918. Maximum Sum Circular Subarray

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/maximum-sum-circular-subarray/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-sum-circular-subarray>  
- **Video:** <https://www.youtube.com/watch?v=fxT9KjakYPM>  

[← Back to index](../INDEX.md)

## 1. Brute Force

Since the array is circular, any contiguous subarray can wrap around from the end back to the beginning. The most direct approach is to try every possible starting position and extend the subarray up to the full length of the array, tracking the maximum sum found. Using modular indexing allows us to wrap around seamlessly. While simple to understand, this method is slow because it examines every possible subarray.

```cpp
class Solution {
public:
    int maxSubarraySumCircular(vector<int>& nums) {
        int n = nums.size();
        int res = nums[0];

        for (int i = 0; i < n; i++) {
            int curSum = 0;
            for (int j = i; j < i + n; j++) {
                curSum += nums[j % n];
                res = max(res, curSum);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 2. Prefix & Suffix Sums

A circular subarray with maximum sum either lies entirely within the array (no wrap), or it wraps around (takes a prefix and a suffix). For the non-wrapping case, we can use standard Kadane's algorithm. For the wrapping case, we want the best prefix ending at some index combined with the best suffix starting after that index. By precomputing the maximum suffix sum from each position, we can efficiently find the best combination of prefix and suffix sums in a single pass.

```cpp
class Solution {
public:
    int maxSubarraySumCircular(vector<int>& nums) {
        int n = nums.size();
        vector<int> rightMax(n);
        rightMax[n - 1] = nums[n - 1];
        int suffixSum = nums[n - 1];

        for (int i = n - 2; i >= 0; --i) {
            suffixSum += nums[i];
            rightMax[i] = max(rightMax[i + 1], suffixSum);
        }

        int maxSum = nums[0];
        int curMax = 0;
        int prefixSum = 0;

        for (int i = 0; i < n; ++i) {
            curMax = max(curMax, 0) + nums[i];
            maxSum = max(maxSum, curMax);
            prefixSum += nums[i];
            if (i + 1 < n) {
                maxSum = max(maxSum, prefixSum + rightMax[i + 1]);
            }
        }

        return maxSum;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Kadane's Algorithm

The maximum circular subarray sum falls into one of two cases: either the subarray does not wrap around, or it does. For the non-wrapping case, standard Kadane's algorithm finds the maximum subarray sum. For the wrapping case, if we remove a contiguous middle portion from the array, what remains is a prefix plus a suffix. Removing the minimum subarray sum leaves behind the maximum wrapping sum, which equals `total - minSubarraySum`. We take the better of these two cases, but if all elements are negative, the maximum is simply the largest single element.

```cpp
class Solution {
public:
    int maxSubarraySumCircular(vector<int>& nums) {
        int globMax = nums[0], globMin = nums[0];
        int curMax = 0, curMin = 0, total = 0;

        for (int& num : nums) {
            curMax = max(curMax + num, num);
            curMin = min(curMin + num, num);
            total += num;
            globMax = max(globMax, curMax);
            globMin = min(globMin, curMin);
        }

        return globMax > 0 ? max(globMax, total - globMin) : globMax;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
