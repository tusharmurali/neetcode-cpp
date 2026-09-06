# 33. Search In Rotated Sorted Array

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/search-in-rotated-sorted-array/>  
- **NeetCode:** <https://neetcode.io/problems/find-target-in-rotated-sorted-array>  
- **Video:** <https://www.youtube.com/watch?v=U8XENwh8Oy8>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest way to search for a value in an array is to **check every element one by one**.  
If we find the target, we return its index.  
If we reach the end without finding it, the target is not present.

This method always works, but it's not efficient for large arrays.

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        for (int i = 0; i < nums.size(); i++) {
            if (nums[i] == target) {
                return i;
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Binary Search

A rotated sorted array is basically two sorted subarrays joined together.  
So the idea is:

1. **Find the pivot** — the index of the smallest element.  
   This tells us where the rotation happened.

2. After finding the pivot, the array becomes:
   - A sorted left half  
   - A sorted right half  

3. Now we can perform a **normal binary search** on the correct half where the target could lie.

By combining these two binary searches, we efficiently find the target in logarithmic time.

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int l = 0, r = nums.size() - 1;

        while (l < r) {
            int m = (l + r) / 2;
            if (nums[m] > nums[r]) {
                l = m + 1;
            } else {
                r = m;
            }
        }

        int pivot = l;

        int result = binarySearch(nums, target, 0, pivot - 1);
        if (result != -1) {
            return result;
        }

        return binarySearch(nums, target, pivot, nums.size() - 1);
    }

    int binarySearch(vector<int>& nums, int target, int left, int right) {
        while (left <= right) {
            int mid = (left + right) / 2;
            if (nums[mid] == target) {
                return mid;
            } else if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 3. Binary Search (Two Pass)

A rotated sorted array is really two sorted arrays stuck together.  
So we break the problem into **two simple binary searches**:

1. **First binary search**:  
   Find the pivot — the index of the smallest element.  
   This tells us where the array was rotated.

2. **Second binary search**:  
   Decide which sorted half may contain the target,  
   then run a standard binary search only on that half.

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int l = 0, r = nums.size() - 1;

        while (l < r) {
            int m = (l + r) / 2;
            if (nums[m] > nums[r]) {
                l = m + 1;
            } else {
                r = m;
            }
        }

        int pivot = l;
        l = 0;
        r = nums.size() - 1;

        if (target >= nums[pivot] && target <= nums[r]) {
            l = pivot;
        } else {
            r = pivot - 1;
        }

        while (l <= r) {
            int m = (l + r) / 2;
            if (nums[m] == target) {
                return m;
            } else if (nums[m] < target) {
                l = m + 1;
            } else {
                r = m - 1;
            }
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 4. Binary Search (One Pass)

```cpp
class Solution {
public:
    int search(std::vector<int>& nums, int target) {
        int l = 0, r = nums.size() - 1;

        while (l <= r) {
            int mid = (l + r) / 2;
            if (target == nums[mid]) {
                return mid;
            }

            if (nums[l] <= nums[mid]) {
                if (target > nums[mid] || target < nums[l]) {
                    l = mid + 1;
                } else {
                    r = mid - 1;
                }
            } else {
                if (target < nums[mid] || target > nums[r]) {
                    r = mid - 1;
                } else {
                    l = mid + 1;
                }
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0033-search-in-rotated-sorted-array.cpp` in the NeetCode repo)

```cpp
/*
    Given array after some possible rotation, find if target is in nums
    Ex. nums = [4,5,6,7,0,1,2] target = 0 -> 4 (value 0 is at index 4)

    Modified binary search, if low <= mid left sorted, else right sorted

    Time: O(log n)
    Space: O(1)
*/

class Solution {
public:
    int search(vector<int>& nums, int target) {
        int low = 0;
        int high = nums.size() - 1;
        
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] == target) {
                return mid;
            }
            if (nums[low] <= nums[mid]) {
                if (nums[low] <= target && target <= nums[mid]) {
                    high = mid - 1;
                } else {
                    low = mid + 1;
                }
            } else {
                if (nums[mid] <= target && target <= nums[high]) {
                    low = mid + 1;
                } else {
                    high = mid - 1;
                }
            }
        }
        
        return -1;
    }
};
```
