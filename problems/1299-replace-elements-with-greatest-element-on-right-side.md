# 1299. Replace Elements With Greatest Element On Right Side

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/replace-elements-with-greatest-element-on-right-side/>  
- **NeetCode:** <https://neetcode.io/problems/replace-elements-with-greatest-element-on-right-side>  
- **Video:** <https://www.youtube.com/watch?v=ZHjKhUjcsaU>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each element at index `i`, we need to find the maximum value among all elements to its right. The most straightforward approach is to scan every element to the right for each position using index `j`. The last element has no elements to its right, so it becomes `-1`.

```cpp
class Solution {
public:
    vector<int> replaceElements(vector<int>& arr) {
        int n = arr.size();
        vector<int> ans(n);
        for (int i = 0; i < n; ++i) {
            int rightMax = -1;
            for (int j = i + 1; j < n; ++j) {
                rightMax = max(rightMax, arr[j]);
            }
            ans[i] = rightMax;
        }
        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

> The output array is not counted towards space complexity, as the [standard convention](https://en.wikipedia.org/wiki/DSPACE) measures only auxiliary working space.

## 2. Suffix Max

By traversing right to left, we can maintain a running maximum of all elements seen so far in `rightMax`. When we visit position `i`, the current running maximum represents the greatest element to the right of `i`. We then update `rightMax` to include `arr[i]` for the next iteration. This eliminates redundant scanning.

```cpp
class Solution {
public:
    vector<int> replaceElements(vector<int>& arr) {
        int n = arr.size();
        vector<int> ans(n);
        int rightMax = -1;
        for (int i = n - 1; i >= 0; --i) {
            ans[i] = rightMax;
            rightMax = max(rightMax, arr[i]);
        }
        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

> The output array is not counted towards space complexity, as the [standard convention](https://en.wikipedia.org/wiki/DSPACE) measures only auxiliary working space.

## Standalone solution file (`cpp/1299-replace-elements-with-greatest-element-on-right-side.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    vector<int> replaceElements(vector<int>& arr) {
    // O(N) Time Complexity , O(1) Space complexity
      int n = arr.size();
      int maxSoFar = arr[n-1];
      arr[n-1] = -1;
      
      for(int i=n-2;i>=0;i--)
      {
        int temp = maxSoFar;
        if(maxSoFar < arr[i]) maxSoFar = arr[i];
        arr[i] = temp;
      }
      return arr;
    }
};
```
