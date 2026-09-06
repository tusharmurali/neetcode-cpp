# 525. Contiguous Array

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/contiguous-array/>  
- **NeetCode:** <https://neetcode.io/problems/contiguous-array>  
- **Video:** <https://www.youtube.com/watch?v=agB1LyObUNE>  
- **Video approach:** 3. Hash Map (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach is to check every possible subarray and count the number of zeros and ones in each. When we find a subarray where the count of zeros equals the count of ones, we have found a valid contiguous array. We keep track of the maximum length among all valid subarrays.

```cpp
class Solution {
public:
    int findMaxLength(vector<int>& nums) {
        int n = nums.size(), res = 0;

        for (int i = 0; i < n; i++) {
            int zeros = 0, ones = 0;
            for (int j = i; j < n; j++) {
                if (nums[j] == 1) {
                    ones++;
                } else {
                    zeros++;
                }
                if (ones == zeros && res < (j - i + 1)) {
                    res = j - i + 1;
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

## 2. Array

Instead of counting zeros and ones separately, we can treat zeros as `-1` and ones as `+1`. When we compute a running sum, any subarray with equal zeros and ones will have a sum of `0`. More importantly, if the running sum at index `i` equals the running sum at index `j`, then the subarray from `i+1` to `j` has equal zeros and ones. We use an array to store the first occurrence of each possible running sum value.

```cpp
class Solution {
public:
    int findMaxLength(vector<int>& nums) {
        int n = nums.size(), res = 0, count = 0;
        vector<int> diffIndex(2 * n + 1, -2);
        diffIndex[n] = -1;

        for (int i = 0; i < n; i++) {
            count += nums[i] == 1 ? 1 : -1;
            if (diffIndex[count + n] != -2) {
                res = max(res, i - diffIndex[count + n]);
            } else {
                diffIndex[count + n] = i;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Hash Map ▶ video

This approach uses the same logic as the array solution but replaces the fixed-size array with a hash map. The key insight remains the same: if the difference between ones and zeros at two different indices is the same, the subarray between them contains equal zeros and ones. A hash map provides more flexibility and can be more memory-efficient when the array is sparse or when we want cleaner code.

```cpp
class Solution {
public:
    int findMaxLength(vector<int>& nums) {
        int zero = 0, one = 0, res = 0;
        unordered_map<int, int> diffIndex;

        for (int i = 0; i < nums.size(); i++) {
            if (nums[i] == 0) {
                zero++;
            } else {
                one++;
            }

            int diff = one - zero;
            if (diffIndex.find(diff) == diffIndex.end()) {
                diffIndex[diff] = i;
            }

            if (one == zero) {
                res = one + zero;
            } else {
                res = max(res, i - diffIndex[diff]);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
