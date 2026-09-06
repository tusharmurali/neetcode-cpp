# 2270. Number of Ways to Split Array

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-ways-to-split-array/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-ways-to-split-array>  
- **Video:** <https://www.youtube.com/watch?v=JK_zuiNYJOQ>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A valid split at index `i` means the sum of elements from `0` to `i` is at least as large as the sum from `i+1` to the end. The straightforward approach is to compute both sums for every possible split point by iterating through the relevant portions of the array each time.

```cpp
class Solution {
public:
    int waysToSplitArray(vector<int>& nums) {
        int n = nums.size();
        int res = 0;

        for (int i = 0; i < n - 1; i++) {
            long long leftSum = 0;
            for (int j = 0; j <= i; j++) {
                leftSum += nums[j];
            }

            long long rightSum = 0;
            for (int j = i + 1; j < n; j++) {
                rightSum += nums[j];
            }

            if (leftSum >= rightSum) {
                res++;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Prefix Sum

Recomputing sums from scratch for each split is wasteful. By precomputing a prefix sum array, we can find the sum of any subarray in constant time. The left sum up to index `i` is `prefix[i]`, and the right sum is `prefix[n] - prefix[i]`.

```cpp
class Solution {
public:
    int waysToSplitArray(vector<int>& nums) {
        int n = nums.size();
        vector<long long> prefix(n + 1, 0);

        for (int i = 0; i < n; i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }

        int res = 0;
        for (int i = 1; i < n; i++) {
            long long left = prefix[i];
            long long right = prefix[n] - prefix[i];
            if (left >= right) {
                res++;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Prefix Sum (Optimal)

We don't need to store the entire prefix sum array. Instead, we can maintain a running left sum and right sum. Start with `right` as the total, then shift elements from right to left as we iterate through possible split points.

```cpp
class Solution {
public:
    int waysToSplitArray(vector<int>& nums) {
        long long right = 0, left = 0;
        for (int num : nums) {
            right += num;
        }

        int res = 0;
        for (int i = 0; i < nums.size() - 1; i++) {
            left += nums[i];
            right -= nums[i];
            if (left >= right) {
                res++;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
