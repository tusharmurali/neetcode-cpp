# 11. Container With Most Water

- **Difficulty:** Medium  
- **Pattern:** Two Pointers  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/container-with-most-water/>  
- **NeetCode:** <https://neetcode.io/problems/max-water-container>  
- **Video:** <https://www.youtube.com/watch?v=UuiTKBwPgAo>  
- **Video approach:** 2. Two Pointers  

[← Back to index](../INDEX.md)

## 1. Brute Force

We try every possible pair of lines and compute the area they form.  
For each pair `(i, j)`, the height of the container is the shorter of the two lines, and the width is the distance between them.  
By checking all pairs, we are guaranteed to find the maximum area.

```cpp
class Solution {
public:
    int maxArea(vector<int>& heights) {
        int res = 0;
        for (int i = 0; i < heights.size(); i++) {
            for (int j = i + 1; j < heights.size(); j++) {
                res = max(res, min(heights[i], heights[j]) * (j - i));
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Two Pointers ▶ video

Using two pointers lets us efficiently search for the maximum area without checking every pair.  
We start with the widest container (left at start, right at end).  
The height is limited by the shorter line, so to potentially increase the area, we must move the pointer at the shorter line inward.  
Moving the taller line never helps because it keeps the height the same but reduces the width.  
By always moving the shorter side, we explore all meaningful possibilities.

```cpp
class Solution {
public:
    int maxArea(vector<int>& heights) {
        int l = 0;
        int r = heights.size() - 1;
        int res = 0;

        while (l < r) {
            int area = min(heights[l], heights[r]) * (r - l);
            res = max(res, area);

            if (heights[l] <= heights[r]) {
                l++;
            } else {
                r--;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0011-container-with-most-water.cpp` in the NeetCode repo)

```cpp
/*
    Given array of heights, find max water container can store
    Ex. height = [1,8,6,2,5,4,8,3,7] -> 49, (8 - 1) x min(8, 7)

    2 pointers outside in, greedily iterate pointer w/ lower height

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int maxArea(vector<int>& height) {
        int i = 0;
        int j = height.size() - 1;
        
        int curr = 0;
        int result = 0;
        
        while (i < j) {
            curr = (j - i) * min(height[i], height[j]);
            result = max(result, curr);
            
            if (height[i] <= height[j]) {
                i++;
            } else {
                j--;
            }
        }
        
        return result;
    }
};
```
