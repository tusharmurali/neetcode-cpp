# 88. Merge Sorted Array

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/merge-sorted-array/>  
- **NeetCode:** <https://neetcode.io/problems/merge-sorted-array>  
- **Video:** <https://www.youtube.com/watch?v=P1Ic85RarKY>  
- **Video approach:** 3. Three Pointers Without Extra Space - I  

[← Back to index](../INDEX.md)

## 1. Sorting

The simplest approach is to copy all elements from `nums2` into the empty slots at the end of `nums1`, then sort the entire array. Since `nums1` has enough space allocated for both arrays, we can place `nums2`'s elements starting at index `m`. After sorting, the merged result is in sorted order.

```cpp
class Solution {
public:
    void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        for (int i = 0; i < n; i++) {
            nums1[i + m] = nums2[i];
        }
        sort(nums1.begin(), nums1.end());
    }
};
```

**Complexity**

- Time complexity: $O((m + n) \log (m + n))$
- Space complexity: $O(1)$ or $O(m + n)$ depending on the sorting algorithm.

> Where $m$ and $n$ represent the number of elements in the arrays $nums1$ and $nums2$, respectively.

## 2. Three Pointers With Extra Space

Since both arrays are already sorted, we can merge them in linear time using the standard merge technique from merge sort. However, if we write directly into `nums1` from the front, we risk overwriting elements we still need. To avoid this, we first copy the original elements of `nums1` to a temporary array, then merge from both sources into `nums1`.

```cpp
class Solution {
public:
    void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        vector<int> nums1Copy(nums1.begin(), nums1.begin() + m);
        int idx = 0, i = 0, j = 0;

        while (idx < m + n) {
            if (j >= n || (i < m && nums1Copy[i] <= nums2[j])) {
                nums1[idx++] = nums1Copy[i++];
            } else {
                nums1[idx++] = nums2[j++];
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(m)$

> Where $m$ and $n$ represent the number of elements in the arrays $nums1$ and $nums2$, respectively.

## 3. Three Pointers Without Extra Space - I ▶ video

The key insight is that `nums1` has empty space at the end. If we fill from the back instead of the front, we never overwrite elements we still need. By comparing the largest remaining elements from both arrays and placing the larger one at the current end position, we can merge in place without extra space.

```cpp
class Solution {
public:
    void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        int last = m + n - 1;

        // Merge in reverse order
        while (m > 0 && n > 0) {
            if (nums1[m - 1] > nums2[n - 1]) {
                nums1[last] = nums1[m - 1];
                m--;
            } else {
                nums1[last] = nums2[n - 1];
                n--;
            }
            last--;
        }

        // Fill nums1 with leftover nums2 elements
        while (n > 0) {
            nums1[last] = nums2[n - 1];
            n--;
            last--;
        }
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(1)$ extra space.

> Where $m$ and $n$ represent the number of elements in the arrays $nums1$ and $nums2$, respectively.

## 4. Three Pointers Without Extra Space - II

This is a cleaner version of the previous approach. We observe that once all elements from `nums2` are placed, the remaining elements of `nums1` are already in their correct positions. So we only need to loop while `j >= 0`. This simplifies the logic and removes the need for a separate cleanup loop.

```cpp
class Solution {
public:
    void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        int last = m + n - 1;
        int i = m - 1, j = n - 1;

        while (j >= 0) {
            if (i >= 0 && nums1[i] > nums2[j]) {
                nums1[last--] = nums1[i--];
            } else {
                nums1[last--] = nums2[j--];
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(1)$ extra space.

> Where $m$ and $n$ represent the number of elements in the arrays $nums1$ and $nums2$, respectively.

## Standalone solution file (`cpp/0088-merge-sorted-array.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        int j=0;
        int i=0;
        if(n==0) return;
        if(m==0)
        {  
         for(int i = 0; i < n; i++){
                nums1[i] = nums2[i];
            } return;
        } 
        while(i<m)
        {
            if(nums1[i]>nums2[j])
            {
                swap(nums1[i],nums2[j]);
                sort(nums2.begin(),nums2.end());
            }
            i++;
        }
        j=0;
        while(i<m+n)
        {
            nums1[i] = nums2[j];
            j++;
            i++;
        }
        
    }
};
```
