# 1095. Find in Mountain Array

- **Difficulty:** Hard  
- **Pattern:** Binary Search  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/find-in-mountain-array/>  
- **NeetCode:** <https://neetcode.io/problems/find-in-mountain-array>  
- **Video:** <https://www.youtube.com/watch?v=BGgYC-YkGvc>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach is to scan through the mountain array from left to right. Since we need the minimum index, returning the first occurrence guarantees the correct answer. This works because a linear scan naturally encounters smaller indices first.

```cpp
/**
 * // This is the MountainArray's API interface.
 * // You should not implement it, or speculate about its implementation
 * class MountainArray {
 *   public:
 *     int get(int index);
 *     int length();
 * };
 */

class Solution {
public:
    int findInMountainArray(int target, MountainArray &mountainArr) {
        int n = mountainArr.length();

        for (int i = 0; i < n; i++) {
            if (mountainArr.get(i) == target) {
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

A mountain array has a peak element with strictly increasing values to its left and strictly decreasing values to its right. This structure allows us to use binary search three times: first to find the peak, then to search the ascending left portion, and finally the descending right portion. We search the left side first because we need the minimum index, and values on the left have smaller indices than equivalent values on the right.

```cpp
/**
 * // This is the MountainArray's API interface.
 * // You should not implement it, or speculate about its implementation
 * class MountainArray {
 *   public:
 *     int get(int index);
 *     int length();
 * };
 */

class Solution {
public:
    int findInMountainArray(int target, MountainArray &mountainArr) {
        int length = mountainArr.length();

        // Find Peak
        int l = 1, r = length - 2, peak = 0;
        while (l <= r) {
            int m = (l + r) / 2;
            int left = mountainArr.get(m - 1);
            int mid = mountainArr.get(m);
            int right = mountainArr.get(m + 1);
            if (left < mid && mid < right) {
                l = m + 1;
            } else if (left > mid && mid > right) {
                r = m - 1;
            } else {
                peak = m;
                break;
            }
        }

        // Search left portion
        l = 0;
        r = peak - 1;
        while (l <= r) {
            int m = (l + r) / 2;
            int val = mountainArr.get(m);
            if (val < target) {
                l = m + 1;
            } else if (val > target) {
                r = m - 1;
            } else {
                return m;
            }
        }

        // Search right portion
        l = peak;
        r = length - 1;
        while (l <= r) {
            int m = (l + r) / 2;
            int val = mountainArr.get(m);
            if (val > target) {
                l = m + 1;
            } else if (val < target) {
                r = m - 1;
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

## 3. Binary Search + Caching

The MountainArray API may have limited calls or expensive operations. During peak-finding, we query values at `mid - 1`, `mid`, and `mid + 1`, and some of these indices may be queried again in subsequent binary searches. By caching previously retrieved values, we avoid redundant API calls. This is particularly useful when the peak-finding phase overlaps with the search regions.

```cpp
/**
 * // This is the MountainArray's API interface.
 * // You should not implement it, or speculate about its implementation
 * class MountainArray {
 *   public:
 *     int get(int index);
 *     int length();
 * };
 */

class Solution {
private:
    unordered_map<int, int> cache;

    int get(int index, MountainArray &mountainArr) {
        if (cache.find(index) == cache.end()) {
            cache[index] = mountainArr.get(index);
        }
        return cache[index];
    }

    int binarySearch(int l, int r, bool ascending, int target, MountainArray &mountainArr) {
        while (l <= r) {
            int m = (l + r) >> 1;
            int val = get(m, mountainArr);
            if (val == target) {
                return m;
            }
            if (ascending == (val < target)) {
                l = m + 1;
            } else {
                r = m - 1;
            }
        }
        return -1;
    }

public:
    int findInMountainArray(int target, MountainArray &mountainArr) {
        int length = mountainArr.length();

        // Find Peak
        int l = 1, r = length - 2, peak = 0;
        while (l <= r) {
            int m = (l + r) >> 1;
            int left = get(m - 1, mountainArr);
            int mid = get(m, mountainArr);
            int right = get(m + 1, mountainArr);
            if (left < mid && mid < right) {
                l = m + 1;
            } else if (left > mid && mid > right) {
                r = m - 1;
            } else {
                peak = m;
                break;
            }
        }

        // Search left portion
        int res = binarySearch(0, peak, true, target, mountainArr);
        if (res != -1) {
            return res;
        }

        // Search right portion
        return binarySearch(peak, length - 1, false, target, mountainArr);
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(\log n)$

## Standalone solution file (`cpp/1095-find-in-mountain-array.cpp` in the NeetCode repo)

```cpp
/**
 * 
 *  Algorithm:
 *      -  The algorithm's goal is to find the minimum index at which the value "target",
 *         exist within a "MountainArray".
 *      -  It employs a binary search approach, dividing the array into ascending and 
 *         descending halves. Additionally, it identifies the peak index to determine the
 *         transition from ascending to descending.
 * 
 *  Time  Complexity: O(log n) 
 *  Space Complexity: O(1)
 * 
 */

/**
 * // This is the MountainArray's API interface.
 * // You should not implement it, or speculate about its implementation
 * class MountainArray {
 *   public:
 *     int get(int index);
 *     int length();
 * };
 */

class Solution {
public:
    int binarySearch(int& begin, int& end, const int& target, MountainArray &mountainArr)
    {
        while (begin <= end)
        {
            int mid = begin + (end-begin)/2;
            int mid_number = mountainArr.get(mid);

            if(mid_number == target)
            {
                return mid;
            }
            else if (mid_number > target)
            {
                end = --mid;
            }
            else
            {
                begin = ++mid;
            }
        }
        return -1;
    }

    int reverseBinarySearch(int& begin, int& end, const int& target, MountainArray &mountainArr)
    {
        while (begin <= end)
        {
            int mid = begin + (end-begin)/2;
            int mid_number = mountainArr.get(mid);

            if(mid_number == target)
            {
                return mid;
            }
            else if (mid_number > target)
            {
                begin = ++mid;
            }
            else
            {
                end = --mid;
            }
        }
        return -1;
    }

    int findPeakElement(int& begin, int& end, MountainArray &mountainArr)
    {
        while (begin < end)
        {
            int mid = begin + (end-begin)/2;
            if(mountainArr.get(mid) < mountainArr.get(mid+1))
            {
                begin = ++mid;
            }
            else
            {
                end = --mid;
            }
        }
        return begin;
    }

    int findInMountainArray(int target, MountainArray &mountainArr) {
        ios_base::sync_with_stdio(false);
        cin.tie(NULL);

        int begin = 0; 
        int end = mountainArr.length()-1;
        int minimum_index = 0;

        int peak_index = findPeakElement(begin, end, mountainArr);

        begin = 0; 
        end = peak_index;   
        minimum_index = binarySearch(begin, end, target, mountainArr);

        if(minimum_index != -1) return minimum_index;
        
        begin = peak_index;
        end = mountainArr.length()-1;
        minimum_index = reverseBinarySearch(begin, end, target, mountainArr);

        return minimum_index;
    }
};
```
