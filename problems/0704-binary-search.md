# 704. Binary Search

- **Difficulty:** Easy  
- **Pattern:** Binary Search  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/binary-search/>  
- **NeetCode:** <https://neetcode.io/problems/binary-search>  
- **Video:** <https://www.youtube.com/watch?v=s4DPM8ct1pI>  
- **Video approach:** 2. Iterative Binary Search  

[← Back to index](../INDEX.md)

## 1. Recursive Binary Search

Binary search works by repeatedly cutting the search space in half.  
Instead of scanning the entire array, we check the **middle element**:

- If it’s the target → return the index.
- If the target is larger → search only in the right half.
- If the target is smaller → search only in the left half.

The recursive version simply expresses this idea as a function that keeps calling itself on the appropriate half until the target is found or the range becomes invalid.

```cpp
class Solution {
public:
    int binary_search(int l, int r, vector<int>& nums, int target){
        if (l > r) return -1;
        int m = l + (r - l) / 2;

        if (nums[m] == target) return m;
        return ((nums[m] < target) ?
                binary_search(m + 1, r, nums, target) :
                binary_search(l, m - 1, nums, target));
    }

    int search(vector<int>& nums, int target) {
        return binary_search(0, nums.size() - 1, nums, target);
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(\log n)$

## 2. Iterative Binary Search ▶ video

Binary search checks the middle element of a sorted array and decides which half to discard.  
Instead of using recursion, the iterative approach keeps shrinking the search range using a loop.  
We adjust the left and right pointers until we either find the target or the pointers cross, meaning the target isn’t present.

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int l = 0, r = nums.size() - 1;

        while (l <= r) {
            int m = l + ((r - l) / 2);
            if (nums[m] > target) {
                r = m - 1;
            } else if (nums[m] < target) {
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

## 3. Upper Bound

Upper bound binary search finds the **first index where a value greater than the target appears**.  
Once we know that position, the actual target—if it exists—must be right before it.  
So instead of directly searching for the target, we search for the boundary where values stop being ≤ target.  
Then we simply check whether the element just before that boundary is the target.

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int l = 0, r = nums.size();

        while (l < r) {
            int m = l + (r - l) / 2;
            if (nums[m] > target) {
                r = m;
            } else {
                l = m + 1;
            }
        }
        return (l > 0 && nums[l - 1] == target) ? l - 1 : -1;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 4. Lower Bound

Lower bound binary search finds the **first index where a value is greater than or equal to the target**.  
This means if the target exists in the array, this lower-bound index will point exactly to its first occurrence.  
So instead of directly searching for equality, we search for the **leftmost position** where the target _could_ appear, then verify it.

This approach is especially useful for sorted arrays because it avoids overshooting and naturally handles duplicates.

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int l = 0, r = nums.size();

        while (l < r) {
            int m = l + (r - l) / 2;
            if (nums[m] >= target) {
                r = m;
            } else {
                l = m + 1;
            }
        }
        return (l < nums.size() && nums[l] == target) ? l : -1;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 5. Built-In Function

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        auto it = lower_bound(nums.begin(), nums.end(), target);
        return (it != nums.end() && *it == target) ? it - nums.begin() : -1;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0704-binary-search.cpp` in the NeetCode repo)

```cpp
/*
    Given sorted int array, search for a target value
    Ex. nums = [-1,0,3,5,9,12], target = 9 -> 4 (index)

    Since array is sorted, perform binary search

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
            if (nums[mid] < target) {
                low = mid + 1;
            } else if (nums[mid] > target) {
                high = mid - 1;
            } else {
                return mid;
            }
        }
        
        return -1;
    }
};
```
