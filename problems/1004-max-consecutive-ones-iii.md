# 1004. Max Consecutive Ones III

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/max-consecutive-ones-iii/>  
- **NeetCode:** <https://neetcode.io/problems/max-consecutive-ones-iii>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to check every possible starting position and see how far we can extend while flipping at most `k` zeros. For each starting index, we move forward and count zeros. Once the count exceeds `k`, we stop and record the window length. This method explores all contiguous subarrays but performs redundant work by rescanning overlapping regions.

```cpp
class Solution {
public:
    int longestOnes(vector<int>& nums, int k) {
        int res = 0;
        for (int l = 0; l < nums.size(); l++) {
            int cnt = 0, r = l;
            while (r < nums.size()) {
                if (nums[r] == 0) {
                    if (cnt == k) break;
                    cnt++;
                }
                r++;
            }
            res = max(res, r - l);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Binary Search + Prefix Sum

We can precompute a prefix sum array that counts zeros up to each index. For any subarray from `l` to `r`, the number of zeros is simply `prefix[r + 1] - prefix[l]`. This allows us to quickly check if a window is valid (contains at most `k` zeros). For each starting position, we binary search for the farthest ending position where the zero count stays within the limit. This avoids the linear scan of the brute force approach.

```cpp
class Solution {
public:
    int longestOnes(vector<int>& nums, int k) {
        vector<int> prefix(nums.size() + 1, 0);
        for (int i = 0; i < nums.size(); ++i) {
            prefix[i + 1] = prefix[i] + (nums[i] == 0 ? 1 : 0);
        }

        int res = 0;
        for (int l = 0; l < nums.size(); ++l) {
            int low = l, high = nums.size();
            while (low < high) {
                int mid = (low + high) / 2;
                if (prefix[mid + 1] - prefix[l] <= k) {
                    low = mid + 1;
                } else {
                    high = mid;
                }
            }
            res = max(res, low - l);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Sliding Window

A sliding window provides the optimal approach. We maintain a window that can contain at most `k` zeros. As we expand the right boundary, we decrement `k` for each zero encountered. When `k` goes negative, the window has too many zeros, so we shrink from the `left` until the window is valid again. The maximum window size seen during this process is our answer. Each element is processed at most twice, yielding linear time complexity.

```cpp
class Solution {
public:
    int longestOnes(vector<int>& nums, int k) {
        int l = 0, res = 0;
        for (int r = 0; r < nums.size(); ++r) {
            k -= (nums[r] == 0 ? 1 : 0);
            while (k < 0) {
                k += (nums[l] == 0 ? 1 : 0);
                ++l;
            }
            res = max(res, r - l + 1);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
