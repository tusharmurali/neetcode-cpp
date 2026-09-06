# 1533. Find the Index of the Large Integer

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-the-index-of-the-large-integer/>  
- **NeetCode:** <https://neetcode.io/problems/find-the-index-of-the-large-integer>  

[← Back to index](../INDEX.md)

## 1. Binary Search

We need to find the index of the largest element, but we can only compare subarray sums, not individual elements. The key observation is that if we split the array into two equal halves and compare their sums, the half containing the largest element will have a greater sum (since all other elements are identical). This naturally leads to binary search: we repeatedly halve the search space based on which half has the larger sum.

```cpp
class Solution {
public:
    int getIndex(ArrayReader &reader) {
        int left = 0;
        int length = reader.length();
        
        while (length > 1) {
            length /= 2;
            int cmp = reader.compareSub(
                left, 
                left + length - 1, 
                left + length,
                left + length + length - 1
            );
            
            if (cmp == 0) {
                return left + length + length;
            }
            if (cmp < 0) {
                left += length;
            }
        }
        
        return left;
    }
};
```

**Complexity**

- Time complexity: $O(\log N)$
- Space complexity: $O(1)$ constant space

>  Where $N$ is the length of the internal array.
