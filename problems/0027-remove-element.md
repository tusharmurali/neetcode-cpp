# 27. Remove Element

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/remove-element/>  
- **NeetCode:** <https://neetcode.io/problems/remove-element>  
- **Video:** <https://www.youtube.com/watch?v=Pcd1ii9P9ZI>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest way to remove elements is to collect all the values we want to keep into a separate list.
We iterate through the array, skip any element that matches the target value, and store the rest.
Then we copy everything back into the original array.
This works but uses extra space proportional to the input size.

```cpp
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        vector<int> tmp;
        for (int num : nums) {
            if (num != val) {
                tmp.push_back(num);
            }
        }
        for (int i = 0; i < tmp.size(); i++) {
            nums[i] = tmp[i];
        }
        return tmp.size();
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Two Pointers - I

Instead of using extra space, we can overwrite unwanted elements in place.
We use a write pointer `k` that tracks where the next valid element should go.
As we scan through the array, whenever we find an element that is not equal to `val`, we write it at position `k` and move `k` forward.
At the end, everything before index `k` contains valid elements.

```cpp
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int k = 0;
        for (int i = 0; i < nums.size(); i++) {
            if (nums[i] != val) {
                nums[k++] = nums[i];
            }
        }
        return k;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Two Pointers - II

When there are few elements to remove, the previous approach does unnecessary copying.
Instead, we can swap unwanted elements with elements from the end of the array.
When we encounter the target value, we replace it with the last element and shrink the valid range by one.
This minimizes write operations when removals are rare.

```cpp
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int i = 0, n = nums.size();
        while (i < n) {
            if (nums[i] == val) {
                nums[i] = nums[--n];
            } else {
                i++;
            }
        }
        return n;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0027-remove-element.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int n=nums.size();
        int count=0;
        for(int i=0;i<n;i++)
        {
            if(nums[i]!=val)
            {
                swap(nums[i],nums[count]);
                count++;
            }
        }
        
        return count;
    }
};
```
