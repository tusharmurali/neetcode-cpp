# 26. Remove Duplicates From Sorted Array

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/remove-duplicates-from-sorted-array/>  
- **NeetCode:** <https://neetcode.io/problems/remove-duplicates-from-sorted-array>  
- **Video:** <https://www.youtube.com/watch?v=DEJAZBq0FDA>  
- **Video approach:** 3. Two Pointers - II  

[← Back to index](../INDEX.md)

## 1. Sorted Set

A set automatically removes duplicates, and a sorted set maintains order. We insert all elements into a sorted set, then copy the unique elements back to the original array. This approach is simple but uses extra space and doesn't take advantage of the array already being sorted.

```cpp
class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        set<int> unique(nums.begin(), nums.end());
        int i = 0;
        for (int num : unique) {
            nums[i++] = num;
        }
        return unique.size();
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Two Pointers - I

Since the array is sorted, duplicates are adjacent. We use two pointers: one (`l`) marks where to place the next unique element, and another (`r`) scans through the array. When `r` finds a new value (different from what's at `l`), we copy it to position `l` and advance both pointers. This modifies the array in-place.

```cpp
class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        int n = nums.size(), l = 0, r = 0;
        while (r < n) {
            nums[l] = nums[r];
            while (r < n && nums[r] == nums[l]) {
                r++;
            }
            l++;
        }
        return l;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Two Pointers - II ▶ video

A more elegant approach: we compare each element with its predecessor. Since duplicates are consecutive in a sorted array, an element is unique if it differs from the one before it. We maintain a write pointer that only advances when we find a new unique value.

```cpp
class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        int l = 1;
        for (int r = 1; r < nums.size(); r++) {
            if (nums[r] != nums[r - 1]) {
                nums[l++] = nums[r];
            }
        }
        return l;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0026-remove-duplicates-from-sorted-array.cpp` in the NeetCode repo)

```cpp
int removeDuplicates(int* nums, int numsSize){
    int indx = 1;
    
    for(int i = 1; i < numsSize; i++){
        if(nums[i] != nums[i-1]){
            nums[indx] = nums[i];
            indx++;
        }
    }
    return indx;
}
```
