# 974. Subarray Sums Divisible by K

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/subarray-sums-divisible-by-k/>  
- **NeetCode:** <https://neetcode.io/problems/subarray-sums-divisible-by-k>  
- **Video:** <https://www.youtube.com/watch?v=bcXy-T4Sc3E>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach checks every possible subarray. For each starting index, we extend the subarray one element at a time, keeping a running sum. If the sum is divisible by `k` (i.e., `sum % k == 0`), we count it.

```cpp
class Solution {
public:
    int subarraysDivByK(vector<int>& nums, int k) {
        int n = nums.size(), res = 0;

        for (int i = 0; i < n; i++) {
            int curSum = 0;
            for (int j = i; j < n; j++) {
                curSum += nums[j];
                if (curSum % k == 0) {
                    res++;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Prefix Sum + Hash Map

If two prefix sums have the same remainder when divided by `k`, their difference is divisible by `k`. So the subarray between those two positions has a sum divisible by `k`. We use a hash map to count how many times each remainder has appeared. For each new prefix sum, we check how many previous prefix sums share the same remainder.

```cpp
class Solution {
public:
    int subarraysDivByK(vector<int>& nums, int k) {
        int prefixSum = 0, res = 0;
        unordered_map<int, int> prefixCnt;
        prefixCnt[0] = 1;

        for (int n : nums) {
            prefixSum += n;
            int remain = prefixSum % k;
            if (remain < 0) remain += k;

            res += prefixCnt[remain];
            prefixCnt[remain]++;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(k)$

## 3. Prefix Sum + Array

Since remainders when dividing by `k` are always in the range `[0, k-1]`, we can use a fixed-size array instead of a hash map. This gives slightly better constant factors. We also handle negative numbers by adding `k` to the modulo result, ensuring all remainders are non-negative.

```cpp
class Solution {
public:
    int subarraysDivByK(vector<int>& nums, int k) {
        vector<int> count(k, 0);
        count[0] = 1;
        int prefix = 0, res = 0;

        for (int num : nums) {
            prefix = (prefix + num % k + k) % k;
            res += count[prefix];
            count[prefix]++;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + k)$
- Space complexity: $O(k)$
