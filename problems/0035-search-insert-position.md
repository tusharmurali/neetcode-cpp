# 35. Search Insert Position

- **Difficulty:** Easy  
- **Pattern:** Binary Search  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/search-insert-position/>  
- **NeetCode:** <https://neetcode.io/problems/search-insert-position>  
- **Video:** <https://www.youtube.com/watch?v=K-RYzDZkzCI>  

[← Back to index](../INDEX.md)

## 1. Linear Search

We scan the array from left to right looking for the first element that is greater than or equal to the target. If we find such an element, that index is where the target either exists or should be inserted. If no element qualifies, the target belongs at the end.

```cpp
class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        for (int i = 0; i < nums.size(); i++) {
            if (nums[i] >= target) {
                return i;
            }
        }
        return nums.size();
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 2. Binary Search - I

Since the array is sorted, we can use binary search to find the target in logarithmic time. We track the potential insertion point as we search. Whenever we find an element greater than the target, we update our answer and continue searching left for a potentially smaller valid index.

```cpp
class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        int res = nums.size();
        int l = 0, r = nums.size() - 1;
        while (l <= r) {
            int mid = (l + r) / 2;
            if (nums[mid] == target) {
                return mid;
            }
            if (nums[mid] > target) {
                res = mid;
                r = mid - 1;
            } else {
                l = mid + 1;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$ extra space.

## 3. Binary Search - II

A cleaner observation: when binary search ends without finding the target, the left pointer `l` naturally lands on the correct insertion position. This happens because `l` always moves past elements smaller than the target, stopping exactly where the target should go.

```cpp
class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        int l = 0, r = nums.size() - 1;
        while (l <= r) {
            int mid = (l + r) / 2;
            if (nums[mid] == target) {
                return mid;
            }
            if (nums[mid] > target) {
                r = mid - 1;
            } else {
                l = mid + 1;
            }
        }
        return l;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$ extra space.

## 4. Binary Search (Lower Bound)

This is the classic lower bound algorithm. We find the smallest index where the element is greater than or equal to the target. By using `l < r` as the condition and setting `r = m` when `nums[m] >= target`, we converge on the lower bound without needing a separate result variable.

```cpp
class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        int l = 0, r = nums.size();
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

## 5. Built-In Binary Search Function

Most languages provide a built-in binary search or lower bound function. These functions return the index where the target is found or the position where it should be inserted to maintain sorted order. Using these avoids reimplementing binary search.

```cpp
class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        return lower_bound(nums.begin(), nums.end(), target) - nums.begin();
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0035-search-insert-position.cpp` in the NeetCode repo)

```cpp
/*
    Given a sorted array of distinct integers and a target value, return the index if the target is found. 
    If not, return the index where it would be if it were inserted in order.

    Ex.
    Input: nums = [1,3,5,6], target = 5
    Output: 2

    1.- Find the number in the middle of the vector.
    2.- Takes a part (first or second), depending on whether or not the target is greater than the middel.
    3.- Change the current left or right part.
    3.- Do this process until the left exceeds the right.

    Time: O(log n)
    Space: O(1)
*/

class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        int left = 0;
        int right = nums.size() - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (nums[mid] < target)
                left = mid + 1;
            else
                right = mid - 1;
        }
        return left;
    }
};
```
