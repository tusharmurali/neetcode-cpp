# 905. Sort Array by Parity

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/sort-array-by-parity/>  
- **NeetCode:** <https://neetcode.io/problems/sort-array-by-parity>  
- **Video:** <https://www.youtube.com/watch?v=QC4c9fyr8As>  

[← Back to index](../INDEX.md)

## 1. Sorting

We want all even numbers before odd numbers. By treating the parity (even/odd) as a sort key, we can leverage a built-in sort. Even numbers have parity 0, odd numbers have parity 1, so sorting by parity naturally places evens first.

```cpp
class Solution {
public:
    vector<int> sortArrayByParity(vector<int>& nums) {
        sort(nums.begin(), nums.end(), [&](int& a, int& b) {
            return (a & 1) < (b & 1);
        });
        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Array

Instead of sorting, we can separate elements into two groups in a single pass. Collect all even numbers in one list and all odd numbers in another, then concatenate them. This avoids the overhead of comparison-based sorting.

```cpp
class Solution {
public:
    vector<int> sortArrayByParity(vector<int>& nums) {
        vector<int> even, odd;

        for (int& num : nums) {
            if (num & 1) {
                odd.push_back(num);
            } else {
                even.push_back(num);
            }
        }

        int idx = 0;
        for (int& e : even) {
            nums[idx++] = e;
        }
        for (int& o : odd) {
            nums[idx++] = o;
        }

        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Two Pointers - I

We can partition the array in-place using two pointers at opposite ends. The left pointer finds odd numbers that need to move right, and the right pointer marks where odd numbers should go. When we find an odd number on the left, we swap it with whatever is on the right, effectively pushing odd numbers to the end.

```cpp
class Solution {
public:
    vector<int> sortArrayByParity(vector<int>& nums) {
        int i = 0, j = nums.size() - 1;
        while (i < j) {
            if ((nums[i] & 1) == 1) {
                swap(nums[i], nums[j]);
                j--;
            } else {
                i++;
            }
        }
        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 4. Two Pointers - II

This approach uses a slow and fast pointer moving in the same direction. The slow pointer `l` tracks where the next even number should be placed. The fast pointer `r` scans through the array. Whenever we find an even number, we swap it to position `l` and advance `l`. This collects all even numbers at the front.

```cpp
class Solution {
public:
    vector<int> sortArrayByParity(vector<int>& nums) {
        for (int l = 0, r = 0; r < nums.size(); r++) {
            if (nums[r] % 2 == 0) {
                swap(nums[l], nums[r]);
                l++;
            }
        }
        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
