# 189. Rotate Array

- **Difficulty:** Medium  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/rotate-array/>  
- **NeetCode:** <https://neetcode.io/problems/rotate-array>  
- **Video:** <https://www.youtube.com/watch?v=BHr381Guz3Y>  
- **Video approach:** 4. Using Reverse  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest way to rotate an array by `k` positions is to perform `k` single rotations. In each rotation, we save the last element, shift every element one position to the right, and place the saved element at the front. This mimics the physical act of rotating items in a line. While straightforward, this approach is slow because we repeat the entire shift process `k` times.

```cpp
class Solution {
public:
    void rotate(vector<int>& nums, int k) {
        int n = nums.size();
        k %= n;
        while (k > 0) {
            int tmp = nums[n - 1];
            for (int i = n - 1; i > 0; i--) {
                nums[i] = nums[i - 1];
            }
            nums[0] = tmp;
            k--;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(1)$ extra space.

## 2. Extra Space

Instead of repeatedly shifting elements, we can directly compute the final position of each element. If an element is at index `i`, after rotation it will be at index `(i + k) % n`. By using a temporary array to store the rotated result, we can place each element in its correct position in a single pass, then copy everything back.

```cpp
class Solution {
public:
    void rotate(vector<int>& nums, int k) {
        int n = nums.size();
        vector<int> tmp(n);
        for (int i = 0; i < n; i++) {
            tmp[(i + k) % n] = nums[i];
        }
        for (int i = 0; i < n; i++) {
            nums[i] = tmp[i];
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ extra space.

## 3. Cyclic Traversal

We can rotate in-place by following cycles. Starting from any position, we move the element to its destination, then move the displaced element to its destination, and so on until we return to the starting position. If the cycle doesn't cover all elements (which happens when `n` and `k` share a common divisor), we start a new cycle from the next position. This ensures every element is moved exactly once.

```cpp
class Solution {
public:
    void rotate(vector<int>& nums, int k) {
        int n = nums.size();
        k %= n;
        int count = 0;

        for (int start = 0; count < n; start++) {
            int current = start;
            int prev = nums[start];
            do {
                int nextIdx = (current + k) % n;
                int temp = nums[nextIdx];
                nums[nextIdx] = prev;
                prev = temp;
                current = nextIdx;
                count++;
            } while (start != current);
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 4. Using Reverse ▶ video

A clever observation: rotating an array by `k` is equivalent to moving the last `k` elements to the front. We can achieve this with three reversals. First, reverse the entire array. Now the last `k` elements are at the front, but in reverse order. Reverse the first `k` elements to fix their order. Finally, reverse the remaining elements to restore their original order.

```cpp
class Solution {
public:
    void rotate(vector<int>& nums, int k) {
        int n = nums.size();
        k %= n;

        reverse(nums, 0, n - 1);
        reverse(nums, 0, k - 1);
        reverse(nums, k, n - 1);
    }

private:
    void reverse(vector<int>& nums, int l, int r) {
        while (l < r) {
            swap(nums[l], nums[r]);
            l++;
            r--;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 5. One Liner

Many languages provide built-in ways to slice and concatenate arrays. We can simply take the last `k` elements and prepend them to the rest of the array. This leverages language features to express the rotation concisely, though under the hood it may use extra space.

```cpp

class Solution {
public:
    void rotate(vector<int>& nums, int k) {
        std::rotate(nums.begin(), nums.end() - (k % nums.size()), nums.end());
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the language.

## Standalone solution file (`cpp/0189-rotate-array.cpp` in the NeetCode repo)

```cpp
/*
    Given an array, rotate the array to the right by k steps, where k is non-negative.
    Ex. 
    Input: nums = [1,2,3,4,5,6,7], k = 3 
    Output: [5,6,7,1,2,3,4]

    1.- To avoid problems with the size of the vector we use the remainder of a division.
    2.- Reverse the entire vector.
    3.- Reverse the parts you want to obtain the result.

    Time: O(1)
    Space: O(1)
*/

class Solution {
public:
    void rotate(vector<int>& nums, int k) {
        k %= nums.size();
        reverse(nums.begin(), nums.end());
        reverse(nums.begin(), nums.begin() + k);
        reverse(nums.begin() + k, nums.end());
    }
};
```
