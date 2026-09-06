# 977. Squares of a Sorted Array

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/squares-of-a-sorted-array/>  
- **NeetCode:** <https://neetcode.io/problems/squares-of-a-sorted-array>  
- **Video:** <https://www.youtube.com/watch?v=FPCZsG_AkUg>  

[← Back to index](../INDEX.md)

## 1. Sorting

The straightforward approach is to square each element first and then sort the result. While the original array is sorted, squaring can change the order since negative numbers become positive. For example, `[-4, -1, 0, 3]` becomes `[16, 1, 0, 9]` after squaring, which needs to be sorted to `[0, 1, 9, 16]`.

```cpp
class Solution {
public:
    vector<int> sortedSquares(vector<int>& nums) {
        for (int i = 0; i < nums.size(); i++) {
            nums[i] *= nums[i];
        }
        sort(nums.begin(), nums.end());
        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Two Pointers - I

Since the input array is sorted, the largest squares will be at either end (the most negative or most positive values). By using two pointers at both ends, we can compare absolute values and always pick the larger square. This builds the result in descending order, which we then reverse.

```cpp
class Solution {
public:
    vector<int> sortedSquares(vector<int>& nums) {
        int l = 0, r = nums.size() - 1;
        vector<int> res;

        while (l <= r) {
            if (nums[l] * nums[l] > nums[r] * nums[r]) {
                res.push_back(nums[l] * nums[l]);
                l++;
            } else {
                res.push_back(nums[r] * nums[r]);
                r--;
            }
        }

        reverse(res.begin(), res.end());
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for the output array.

## 3. Two Pointers - II

This is an optimization of the previous approach that avoids the final reversal step. Instead of building the result from smallest to largest and reversing, we fill the result array from the end to the beginning. We still use two pointers to compare the absolute values at both ends, but we place each square directly in its final position.

```cpp
class Solution {
public:
    vector<int> sortedSquares(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n);
        int l = 0, r = n - 1, resIndex = n - 1;

        while (l <= r) {
            if (abs(nums[l]) > abs(nums[r])) {
                res[resIndex] = nums[l] * nums[l];
                l++;
            } else {
                res[resIndex] = nums[r] * nums[r];
                r--;
            }
            resIndex--;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for the output array.

## Standalone solution file (`cpp/0977-squares-of-a-sorted-array.cpp` in the NeetCode repo)

```cpp
/*
    Given an integer array nums sorted in non-decreasing order, return 
    an array of the squares of each number sorted in non-decreasing order.

    Ex. 
    Input: nums = [-4,-1,0,3,10]
    Output: [0,1,9,16,100]

    1.- Multiply each number of the nums by themselves.
    2.- Use the sort function to sort the vector.

    Time: O(NlogN) 
    Space: O(N)
*/

class Solution {
public:
    vector<int> sortedSquares(vector<int>& nums) {
        for (int& i : nums)
            i *= i;
        sort(nums.begin(), nums.end());
        return nums;
    }
};
```
