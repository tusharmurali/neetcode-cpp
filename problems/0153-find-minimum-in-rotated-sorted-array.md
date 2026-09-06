# 153. Find Minimum In Rotated Sorted Array

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/>  
- **NeetCode:** <https://neetcode.io/problems/find-minimum-in-rotated-sorted-array>  
- **Video:** <https://www.youtube.com/watch?v=nIVW4P8b1VA>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A rotated sorted array still contains all its original values, just shifted.  
So the simplest way to find the minimum is to **look at every element and pick the smallest one**.  
This requires no special logic and works in all cases, but it is not the most efficient.

```cpp
class Solution {
public:
    int findMin(vector<int>& nums) {
        return *min_element(nums.begin(), nums.end());
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Binary Search

A rotated sorted array has one special property:  
**one part is always sorted, and the other part contains the rotation (and the minimum element).**

We can use binary search to identify which side is sorted:

- If the left half is sorted, then the minimum cannot be there, so we search the right half.
- If the right half is sorted, then the minimum must be in the left half (or at the midpoint).

This lets us eliminate half of the array each time and quickly narrow down to the smallest value.

```cpp
class Solution {
public:
    int findMin(vector<int> &nums) {
        int res = nums[0];
        int l = 0;
        int r = nums.size() - 1;

        while (l <= r) {
            if (nums[l] < nums[r]) {
                res = min(res, nums[l]);
                break;
            }
            int m = l + (r - l) / 2;
            res = min(res, nums[m]);

            if (nums[m] >= nums[l]) {
                l = m + 1;
            } else {
                r = m - 1;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 3. Binary Search (Lower Bound)

In a rotated sorted array, the minimum element is the **first element of the rotated portion**.  
Using binary search, we compare the middle value with the rightmost value:

- If `nums[mid] < nums[right]`, then the minimum lies **in the left half (including `mid`)**.
- Otherwise, the minimum lies **in the right half (excluding `mid`)**.

This behaves exactly like finding a **lower bound**, gradually shrinking the search space until only the minimum remains.

```cpp
class Solution {
public:
    int findMin(vector<int>& nums) {
        int l = 0, r = nums.size() - 1;
        while (l < r) {
            int m = l + (r - l) / 2;
            if (nums[m] < nums[r]) {
                r = m;
            } else {
                l = m + 1;
            }
        }
        return nums[l];
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0153-find-minimum-in-rotated-sorted-array.cpp` in the NeetCode repo)

```cpp
/*
 * @lc app=leetcode id=153 lang=cpp
 *
 * [153] Find Minimum in Rotated Sorted Array
 */

// @lc code=start
class Solution {
public:
    int findMin(vector<int> &nums) {
        int l = 0;
        int r = nums.size() - 1;
        int res = nums[0];
        while (l <= r) {
            int mid = (r - l) / 2 + l;
            if (nums[mid] >= res) {
                l = mid + 1;
            } else {
                r = mid - 1;
            }
            res = std::min(nums[mid], res);
        }
        return res;
    }
};
// @lc code=end
```
