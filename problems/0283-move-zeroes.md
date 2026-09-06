# 283. Move Zeroes

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/move-zeroes/>  
- **NeetCode:** <https://neetcode.io/problems/move-zeroes>  
- **Video:** <https://www.youtube.com/watch?v=aayNRwUN3Do>  

[← Back to index](../INDEX.md)

## 1. Extra Space

The simplest approach is to separate non-zero elements from zeros using extra storage. We collect all non-zero elements first, then write them back to the original array, filling the remaining positions with zeros. This guarantees the relative order of non-zero elements is preserved.

```cpp
class Solution {
public:
    void moveZeroes(vector<int>& nums) {
        vector<int> tmp;
        for (int num : nums) {
            if (num != 0) {
                tmp.push_back(num);
            }
        }

        for (int i = 0; i < nums.size(); ++i) {
            if (i < tmp.size()) {
                nums[i] = tmp[i];
            } else {
                nums[i] = 0;
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Two Pointers (Two Pass)

We can avoid extra space by overwriting the array in place. Use a left pointer to track where the next non-zero element should go. As we scan with a right pointer, each non-zero element gets copied to the left pointer's position. After the first pass, all non-zero elements are at the front in order. A second pass fills the remaining positions with zeros.

```cpp
class Solution {
public:
    void moveZeroes(vector<int>& nums) {
        int l = 0;
        for (int r = 0; r < nums.size(); r++) {
            if (nums[r] != 0) {
                nums[l++] = nums[r];
            }
        }

        while (l < nums.size()) {
            nums[l++] = 0;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Two Pointers (One Pass)

Instead of copying values and then filling zeros separately, we can swap elements in a single pass. The left pointer marks the boundary between processed non-zero elements and unprocessed elements. When we encounter a non-zero element with the right pointer, we swap it with the element at the left pointer. This naturally pushes `0` to the right while keeping non-zero elements in their relative order.

```cpp
class Solution {
public:
    void moveZeroes(vector<int>& nums) {
        for (int l = 0, r = 0; r < nums.size(); r++) {
            if (nums[r]) {
                swap(nums[l++], nums[r]);
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0283-move-zeroes.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    void moveZeroes(vector<int>& nums) {
        int left = 0;

        for(int i = 0; i < nums.size(); i++){
            if(nums[i] != 0){
                nums[left++] = nums[i];
            }
        }

        for(left; left < nums.size(); left ++){
            nums[left] = 0;
        }
    }
};
```
