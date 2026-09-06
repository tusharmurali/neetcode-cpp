# 42. Trapping Rain Water

- **Difficulty:** Hard  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/trapping-rain-water/>  
- **NeetCode:** <https://neetcode.io/problems/trapping-rain-water>  
- **Video:** <https://www.youtube.com/watch?v=ZI2z5pq0TqA>  
- **Video approach:** 4. Two Pointers  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each position, the water trapped above it depends on the **tallest bar to its left** and the **tallest bar to its right**.
If we know these two values, the water at index `i` is:

`min(leftMax, rightMax) - height[i]`

The brute-force method recomputes the left maximum and right maximum for every index by scanning the array each time.

```cpp
class Solution {
public:
    int trap(vector<int>& height) {
        if (height.empty()) {
            return 0;
        }
        int n = height.size();
        int res = 0;

        for (int i = 0; i < n; i++) {
            int leftMax = height[i];
            int rightMax = height[i];

            for (int j = 0; j < i; j++) {
                leftMax = max(leftMax, height[j]);
            }
            for (int j = i + 1; j < n; j++) {
                rightMax = max(rightMax, height[j]);
            }

            res += min(leftMax, rightMax) - height[i];
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Prefix & Suffix Arrays

Instead of recomputing the tallest bar to the left and right for every index, we can precompute these values once.
We build two arrays:

- `leftMax[i]` = tallest bar from the start up to index `i`
- `rightMax[i]` = tallest bar from the end up to index `i`

Once we have these, the trapped water at position `i` is simply:

`min(leftMax[i], rightMax[i]) - height[i]`

This removes the repeated work from the brute-force approach and makes the solution more efficient and easier to understand.

```cpp
class Solution {
public:
    int trap(vector<int>& height) {
        int n = height.size();
        if (n == 0) {
            return 0;
        }

        vector<int> leftMax(n);
        vector<int> rightMax(n);

        leftMax[0] = height[0];
        for (int i = 1; i < n; i++) {
            leftMax[i] = max(leftMax[i - 1], height[i]);
        }

        rightMax[n - 1] = height[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            rightMax[i] = max(rightMax[i + 1], height[i]);
        }

        int res = 0;
        for (int i = 0; i < n; i++) {
            res += min(leftMax[i], rightMax[i]) - height[i];
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Stack

The stack helps us find places where water can collect.
When we see a bar that is taller than the bar on top of the stack, it means we've found a **right wall** for a container.
The bar we pop is the **bottom**, and the new top of the stack becomes the **left wall**.
With a left wall, bottom, and right wall, we can calculate how much water fits in between.
We keep doing this as long as the current bar keeps forming valid containers.

```cpp
class Solution {
public:
    int trap(vector<int>& height) {
        if (height.empty()) {
            return 0;
        }

        stack<int> stk;
        int res = 0;

        for (int i = 0; i < height.size(); i++) {
            while (!stk.empty() && height[i] >= height[stk.top()]) {
                int mid = height[stk.top()];
                stk.pop();
                if (!stk.empty()) {
                    int right = height[i];
                    int left = height[stk.top()];
                    int h = min(right, left) - mid;
                    int w = i - stk.top() - 1;
                    res += h * w;
                }
            }
            stk.push(i);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Two Pointers ▶ video

Water at any position depends on the **shorter** wall between the left and right sides.
So if the left wall is shorter, the right wall can't help us—water is limited by the left side.
That means we safely move the **left pointer** inward and calculate how much water can be trapped there.
Similarly, if the right wall is shorter, we move the **right pointer** left.

As we move the pointers, we keep track of the highest wall seen so far on each side (`leftMax` and `rightMax`).
The water at each position is simply:

`max wall on that side – height at that position`

```cpp
class Solution {
public:
    int trap(vector<int>& height) {
        if (height.empty()) {
            return 0;
        }

        int l = 0, r = height.size() - 1;
        int leftMax = height[l], rightMax = height[r];
        int res = 0;
        while (l < r) {
            if (leftMax < rightMax) {
                l++;
                leftMax = max(leftMax, height[l]);
                res += leftMax - height[l];
            } else {
                r--;
                rightMax = max(rightMax, height[r]);
                res += rightMax - height[r];
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0042-trapping-rain-water.cpp` in the NeetCode repo)

```cpp
/*
    Given elevation map array, compute trapped water
    Ex. height = [0,1,0,2,1,0,1,3,2,1,2,1] -> 6

    2 pointers, outside in, track max left/right
    For lower max, curr only dependent on that one
    Compute height of these, iterate lower one

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int trap(vector<int>& height) {
        int i = 0;
        int j = height.size() - 1;
        
        int maxLeft = height[i];
        int maxRight = height[j];
        
        int result = 0;
        
        while (i < j) {
            if (maxLeft <= maxRight) {
                i++;
                maxLeft = max(maxLeft, height[i]);
                result += maxLeft - height[i];
            } else {
                j--;
                maxRight = max(maxRight, height[j]);
                result += maxRight - height[j];
            }
        }
        
        return result;
    }
};
```
