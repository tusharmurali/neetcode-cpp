# 1685. Sum of Absolute Differences in a Sorted Array

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/sum-of-absolute-differences-in-a-sorted-array/>  
- **NeetCode:** <https://neetcode.io/problems/sum-of-absolute-differences-in-a-sorted-array>  
- **Video:** <https://www.youtube.com/watch?v=3nkc-e66JmA>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each element, we need to compute the sum of absolute differences with all other elements. Since we need every pair, the straightforward approach is to iterate through every element and compute the difference with every other element, summing them up.

```cpp
class Solution {
public:
    vector<int> getSumAbsoluteDifferences(vector<int>& nums) {
        int n = nums.size();
        vector<int> res;

        for (int i = 0; i < n; i++) {
            int sum = 0;
            for (int j = 0; j < n; j++) {
                sum += abs(nums[i] - nums[j]);
            }
            res.push_back(sum);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$ for the output array.

## 2. Prefix & Suffix Sums (Extra Space)

Since the array is sorted, we can remove the absolute value operation. For element at index `i`, all elements to its left are smaller (so we subtract them from `nums[i]`) and all elements to its right are larger (so we subtract `nums[i]` from them). Using prefix and suffix sums, we can compute these contributions efficiently without iterating through every pair.

```cpp
class Solution {
public:
    vector<int> getSumAbsoluteDifferences(vector<int>& nums) {
        int n = nums.size();
        vector<int> prefixSum(n, 0), suffixSum(n, 0), res(n, 0);

        prefixSum[0] = nums[0];
        for (int i = 1; i < n; i++) {
            prefixSum[i] = prefixSum[i - 1] + nums[i];
        }

        suffixSum[n - 1] = nums[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            suffixSum[i] = suffixSum[i + 1] + nums[i];
        }

        for (int i = 0; i < n; i++) {
            int leftSum = i > 0 ? (i * nums[i] - prefixSum[i - 1]) : 0;
            int rightSum = i < n - 1 ? (suffixSum[i + 1] - (n - i - 1) * nums[i]) : 0;
            res[i] = leftSum + rightSum;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Prefix & Suffix Sums

We can reduce space by reusing the result array to store suffix sums initially, then computing the final result in a single pass. We first fill the result array with suffix sums, then iterate from left to right, computing the answer for each position while building the prefix sum on the fly.

```cpp
class Solution {
public:
    vector<int> getSumAbsoluteDifferences(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n, 0);

        res[n - 1] = nums[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            res[i] = res[i + 1] + nums[i];
        }

        int prefixSum = 0;
        for (int i = 0; i < n; i++) {
            int leftSum = i * nums[i] - prefixSum;
            int rightSum = i < n - 1 ? (res[i + 1] - (n - i - 1) * nums[i]) : 0;
            res[i] = leftSum + rightSum;
            prefixSum += nums[i];
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for the output array.

## 4. Prefix & Suffix Sums (Optimal)

Instead of precomputing a suffix sum array, we can compute both prefix and suffix sums on the fly. We start by computing the total sum, then as we iterate through the array, we maintain a running prefix sum and derive the suffix sum by subtracting from the total. This eliminates the need for a separate preprocessing pass.

```cpp
class Solution {
public:
    vector<int> getSumAbsoluteDifferences(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n, 0);

        int totalSum = 0, prefixSum = 0;
        for (int& num : nums) {
            totalSum += num;
        }

        for (int i = 0; i < n; i++) {
            totalSum -= nums[i];
            int leftSum = i * nums[i] - prefixSum;
            int rightSum = totalSum - (n - i - 1) * nums[i];
            res[i] = leftSum + rightSum;
            prefixSum += nums[i];
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for the output array.
