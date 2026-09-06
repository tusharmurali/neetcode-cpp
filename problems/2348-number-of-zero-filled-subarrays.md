# 2348. Number of Zero-Filled Subarrays

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-zero-filled-subarrays/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-zero-filled-subarrays>  
- **Video:** <https://www.youtube.com/watch?v=G-EWVGCcL_w>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to check every possible subarray and count those filled entirely with zeros. For each starting index, we extend the subarray as long as we keep seeing zeros, incrementing our count for each valid zero-filled subarray we find.

```cpp
class Solution {
public:
    long long zeroFilledSubarray(vector<int>& nums) {
        long long res = 0;
        for (int i = 0; i < nums.size(); i++) {
            for (int j = i; j < nums.size(); j++) {
                if (nums[j] != 0) break;
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

## 2. Count Consecutive Zeros - I

Instead of checking every subarray, we can be smarter by processing consecutive groups of zeros. When we find a sequence of `k` consecutive zeros, the number of zero-filled subarrays within that sequence is `1 + 2 + ... + k`.

We can compute this incrementally: as we extend a run of zeros by one element, we add the current run length to our total. For example, if we have seen `3` zeros so far and see a `4`th, we add `4` to the count (representing the `4` new subarrays ending at this position).

```cpp
class Solution {
public:
    long long zeroFilledSubarray(vector<int>& nums) {
        long long res = 0;
        int i = 0;
        while (i < nums.size()) {
            long long count = 0;
            while (i < nums.size() && nums[i] == 0) {
                count++;
                i++;
                res += count;
            }
            i++;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Count Consecutive Zeros - II

This is a cleaner version of the previous approach using a single loop. We maintain a running count of consecutive zeros. Each time we see a zero, we increment the count and add it to our result. Each time we see a non-zero, we reset the count to `0`.

The key insight remains the same: when we are at the `k`-th consecutive zero, there are exactly `k` new zero-filled subarrays ending at this position (subarrays of length `1`, `2`, ..., `k`).

```cpp
class Solution {
public:
    long long zeroFilledSubarray(vector<int>& nums) {
        long long res = 0;
        int count = 0;

        for (int& num : nums) {
            if (num == 0) {
                count++;
            } else {
                count = 0;
            }
            res += count;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 4. Count Consecutive Zeros (Math)

Instead of adding incrementally during each run of zeros, we can use the mathematical formula directly. A sequence of `k` consecutive zeros contains exactly `k * (k + 1) / 2` zero-filled subarrays (the sum of `1 + 2 + ... + k`).

We scan through the array, counting the length of each consecutive zero sequence. When a sequence ends (we hit a non-zero or reach the end), we apply the formula to add all subarrays from that sequence at once.

```cpp
class Solution {
public:
    long long zeroFilledSubarray(vector<int>& nums) {
        long long res = 0, count = 0;
        for (int num : nums) {
            if (num == 0) {
                count++;
            } else {
                res += count * (count + 1) / 2;
                count = 0;
            }
        }
        res += count * (count + 1) / 2;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/2348-number-of-zero-filled-subarrays.cpp` in the NeetCode repo)

```cpp
/*
    Given an integer array nums, return the number of subarrays filled with 0.
    A subarray is a contiguous non-empty sequence of elements within an array.

    Ex. Input: nums = [1,3,0,0,2,0,0,4]
          Output: 6
	  Explanation: 
	  There are 4 occurrences of [0] as a subarray.
	  There are 2 occurrences of [0,0] as a subarray.
	  There is no occurrence of a subarray with a size more than 2 filled with 0. Therefore, we return 6.

    Time  : O(N)
    Space : O(1) 
*/

class Solution {
public:
    long long zeroFilledSubarray(vector<int>& nums) {
        long long res = 0, count = 0;
        for (int i = 0; i < nums.size(); i++) {
            if (nums[i]) {
                res += (count * (count + 1)) / 2;
                count = 0;
            } else 
                ++count;
        }
        res += (count * (count + 1)) / 2;
        return res;
    }
};
```
