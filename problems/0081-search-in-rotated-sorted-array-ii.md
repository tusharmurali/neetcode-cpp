# 81. Search In Rotated Sorted Array II

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/search-in-rotated-sorted-array-ii/>  
- **NeetCode:** <https://neetcode.io/problems/search-in-rotated-sorted-array-ii>  
- **Video:** <https://www.youtube.com/watch?v=oUnF7o88_Xc>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach is to scan every element until we find the target. This ignores the sorted structure but guarantees correctness. Since we only need to know if the target exists, we return immediately upon finding it.

```cpp
class Solution {
public:
    bool search(vector<int>& nums, int target) {
        for (int& num : nums) {
            if (num == target) {
                return true;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Binary Search

A rotated sorted array with duplicates still has a useful property: at least one half (left or right of `mid`) is always sorted. We can determine which half is sorted and check if the target lies within that range. The tricky case is when `nums[l] == nums[m]`, which means we cannot tell which side is sorted. In this case, we simply increment `l` to skip the duplicate and try again.

```cpp
class Solution {
public:
    bool search(vector<int>& nums, int target) {
        int l = 0, r = nums.size() - 1;

        while (l <= r) {
            int m = l + (r - l) / 2;

            if (nums[m] == target) {
                return true;
            }

            if (nums[l] < nums[m]) { // Left portion
                if (nums[l] <= target && target < nums[m]) {
                    r = m - 1;
                } else {
                    l = m + 1;
                }
            } else if (nums[l] > nums[m]) { // Right portion
                if (nums[m] < target && target <= nums[r]) {
                    l = m + 1;
                } else {
                    r = m - 1;
                }
            } else {
                l++;
            }
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$ in average case, $O(n)$ in worst case.
- Space complexity: $O(1)$
