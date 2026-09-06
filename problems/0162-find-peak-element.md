# 162. Find Peak Element

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-peak-element/>  
- **NeetCode:** <https://neetcode.io/problems/find-peak-element>  
- **Video:** <https://www.youtube.com/watch?v=kMzJy9es7Hc>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A peak element is greater than its neighbors. Since adjacent elements are guaranteed to be different and elements outside the array are treated as negative infinity, we can scan from left to right. The first time we find an element greater than its next neighbor, we have found a peak. If no such element exists before the last index, the last element itself must be a peak (since the array keeps increasing).

```cpp
class Solution {
public:
    int findPeakElement(vector<int>& nums) {
        for (int i = 0; i < nums.size() - 1; i++) {
            if (nums[i] > nums[i + 1]) {
                return i;
            }
        }
        return nums.size() - 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Binary Search

Binary search works here because a peak must exist in any subarray. At each midpoint, if the element is smaller than its left neighbor, a peak exists on the left side. If it is smaller than its right neighbor, a peak exists on the right side. Otherwise, the midpoint itself is a peak. This property allows us to eliminate half the search space each iteration.

```cpp
class Solution {
public:
    int findPeakElement(vector<int>& nums) {
        int l = 0, r = nums.size() - 1;

        while (l <= r) {
            int m = l + (r - l) / 2;
            if (m > 0 && nums[m] < nums[m - 1]) {
                r = m - 1;
            } else if (m < nums.size() - 1 && nums[m] < nums[m + 1]) {
                l = m + 1;
            } else {
                return m;
            }
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 3. Recursive Binary Search

This is the same binary search logic implemented recursively. At each step, we compare the middle element with its right neighbor. If the middle is greater, a peak lies in the left half (including `mid`). Otherwise, a peak lies in the right half. The recursion continues until the search range narrows to a single element, which must be a peak.

```cpp
class Solution {
public:
    int findPeakElement(vector<int>& nums) {
        return binarySearch(nums, 0, nums.size() - 1);
    }

private:
    int binarySearch(vector<int>& nums, int l, int r) {
        if (l == r) {
            return l;
        }
        int m = l + (r - l) / 2;
        if (nums[m] > nums[m + 1]) {
            return binarySearch(nums, l, m);
        }
        return binarySearch(nums, m + 1, r);
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(\log n)$ for recursion stack.

## 4. Binary Search (Optimal)

We can simplify the binary search by using `l < r` as the loop condition instead of `l <= r`. This eliminates extra boundary checks. By always comparing `mid` with `mid + 1`, we ensure we move toward a peak. When `l == r`, we have found the peak without needing additional checks.

```cpp
class Solution {
public:
    int findPeakElement(vector<int>& nums) {
        int l = 0, r = nums.size() - 1;

        while (l < r) {
            int m = (l + r) >> 1;
            if (nums[m] > nums[m + 1]) {
                r = m;
            } else {
                l = m + 1;
            }
        }

        return l;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0162-find-peak-element.cpp` in the NeetCode repo)

```cpp
// Time: O(logN)
// Space: O(1)

class Solution {
public:
    int findPeakElement(vector<int>& nums) {
        int n = nums.size();

        if(n == 1) return 0;

        int left = 0, right = n - 1;
        while(left <= right) {
            int mid = left + (right-left)/2;

            if(mid > 0 && nums[mid] < nums[mid-1]) {
                right = mid - 1;
            }
            else if(mid < n-1 && nums[mid] < nums[mid+1]) {
                left = mid + 1;
            }
            else {
                return mid;
            }
        }
        return -1;
    }
};
```
