# 34. Find First And Last Position of Element In Sorted Array

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/>  
- **NeetCode:** <https://neetcode.io/problems/find-first-and-last-position-of-element-in-sorted-array>  
- **Video:** <https://www.youtube.com/watch?v=4sQL7R5ySUU>  

[← Back to index](../INDEX.md)

## 1. Brute Force

Since the array is sorted, all occurrences of the target will be consecutive. We can scan through the array once, recording the first and last positions where we encounter the target. The first time we see the target, we set both the start and end to that index. For subsequent matches, we only update the end position.

```cpp
class Solution {
public:
    vector<int> searchRange(vector<int>& nums, int target) {
        vector<int> res = {-1, -1};

        for (int i = 0; i < nums.size(); i++) {
            if (nums[i] == target) {
                if (res[0] == -1) {
                    res[0] = res[1] = i;
                } else {
                    res[1] = i;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Binary Search - I

Binary search can find any occurrence of the target in O(log n) time, but we need both the first and last occurrences. The key insight is that when we find the target, instead of returning immediately, we continue searching. For the leftmost occurrence, we search the left half after finding a match. For the rightmost, we search the right half. This gives us two separate binary searches with a bias parameter.

```cpp
class Solution {
public:
    vector<int> searchRange(vector<int>& nums, int target) {
        int left = binarySearch(nums, target, true);
        int right = binarySearch(nums, target, false);
        return {left, right};
    }

private:
    int binarySearch(vector<int>& nums, int target, bool leftBias) {
        int l = 0, r = nums.size() - 1, i = -1;
        while (l <= r) {
            int m = (l + r) / 2;
            if (target > nums[m]) {
                l = m + 1;
            } else if (target < nums[m]) {
                r = m - 1;
            } else {
                i = m;
                if (leftBias) {
                    r = m - 1;
                } else {
                    l = m + 1;
                }
            }
        }
        return i;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 3. Binary Search - II

We can use a single style of binary search that finds the insertion point for a value. The insertion point for `target` gives us the first occurrence (if it exists). The insertion point for `target + 1` gives us one past the last occurrence. This approach uses the standard lower-bound binary search pattern, which finds the smallest index where `nums[index] >= target`.

```cpp
class Solution {
public:
    vector<int> searchRange(vector<int>& nums, int target) {
        int n = nums.size();

        int start = binarySearch(nums, target, n);
        if (start == n || nums[start] != target) {
            return {-1, -1};
        }

        return {start, binarySearch(nums, target + 1, n) - 1};
    }

private:
    int binarySearch(vector<int>& nums, int target, int n) {
        int l = 0, r = n;
        while (l < r) {
            int m = l + (r - l) / 2;
            if (nums[m] >= target) {
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

## 4. In-Built Function

Most programming languages provide built-in functions for binary search that find lower and upper bounds. These functions are optimized and well-tested, making them a practical choice when available. The lower bound gives the first occurrence, and the upper bound (minus one) gives the last occurrence.

```cpp
class Solution {
public:
    vector<int> searchRange(vector<int>& nums, int target) {
        int left = lower_bound(nums.begin(), nums.end(), target) - nums.begin();
        if (left == nums.size() || nums[left] != target) {
            return {-1, -1};
        }

        int right = upper_bound(nums.begin(), nums.end(), target) - nums.begin() - 1;
        return {left, right};
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0034-find-first-and-last-position-of-element-in-sorted-array.cpp` in the NeetCode repo)

```cpp
/*
    Given an array of integers nums sorted in non-decreasing order, find the starting and ending position of a given target value.
    Ex. nums = [5,7,7,8,8,10], target = 8 -> [3, 4] (start position is 3, end position is 4)

    Use binary search, firstly binary search left endpoint, then binary search right endpoint.

    Time: O(log n)
    Space: O(1)
*/

class Solution {
public:
    vector<int> searchRange(vector<int>& nums, int target) {
        if (nums.empty()) return {-1, -1};
        int l = 0, r = nums.size() - 1;
        while (l < r) {
            int mid = l + r >> 1;
            if (nums[mid] >= target) r = mid;
            else l = mid + 1;
        }
        if (nums[l] != target) return {-1, -1};
        int left = l;

        l = 0, r = nums.size() - 1;
        while (l < r) {
            int mid = l + r + 1ll >> 1;
            if (nums[mid] <= target) l = mid;
            else r = mid - 1;
        }
        return {left, r};
    }
};
```
