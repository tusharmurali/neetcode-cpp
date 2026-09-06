# 1578. Minimum Time To Make Rope Colorful

- **Difficulty:** Medium  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-time-to-make-rope-colorful/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-time-to-make-rope-colorful>  
- **Video:** <https://www.youtube.com/watch?v=9_9jwd2DHMU>  

[← Back to index](../INDEX.md)

## 1. Two Pointers - I

The goal is to remove consecutive balloons of the same color such that no two adjacent balloons share a color. When we find a group of consecutive same-colored balloons, we need to keep exactly one and remove the rest. To minimize the total removal time, we should keep the balloon with the highest removal cost and remove all others.

```cpp
class Solution {
public:
    int minCost(string colors, vector<int>& neededTime) {
        int n = neededTime.size();
        int res = 0, i = 0;
        while (i < n) {
            int j = i, maxi = 0, curr = 0;
            while (j < n && colors[j] == colors[i]) {
                maxi = max(maxi, neededTime[j]);
                curr += neededTime[j];
                j++;
            }
            res += curr - maxi;
            i = j;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 2. Two Pointers - II

Instead of finding entire groups at once, we can process pairs of adjacent balloons. When two adjacent balloons have the same color, we remove the one with smaller removal time. We keep a pointer `l` to track the balloon we're keeping, and compare it with each new balloon at position `r`.

```cpp
class Solution {
public:
    int minCost(string colors, vector<int>& neededTime) {
        int l = 0, res = 0;
        for (int r = 1; r < colors.size(); r++) {
            if (colors[l] == colors[r]) {
                if (neededTime[l] < neededTime[r]) {
                    res += neededTime[l];
                    l = r;
                } else {
                    res += neededTime[r];
                }
            } else {
                l = r;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 3. Two Pointers - III

We can simplify the logic further by tracking the maximum removal time seen so far in the current group of same-colored balloons. For each balloon, we add the minimum of the current maximum and the current balloon's time to the result, then update the maximum. When we encounter a different color, we reset the maximum to `0`.

```cpp
class Solution {
public:
    int minCost(string colors, vector<int>& neededTime) {
        int res = 0, maxi = 0;
        for (int i = 0; i < colors.size(); i++) {
            if (i > 0 && colors[i] != colors[i - 1]) {
                maxi = 0;
            }
            res += min(maxi, neededTime[i]);
            maxi = max(maxi, neededTime[i]);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/1578-minimum-time-to-make-rope-colorful.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int minCost(string colors, vector<int>& neededTime) {
        int left = 0, time = 0;
        for (int right = 1; right < colors.size(); ++right) {
            if (colors[left] == colors[right]) {
                if (neededTime[left] < neededTime[right]) {
                    time += neededTime[left];
                    left = right;
                } 
                else {
                    time += neededTime[right];
                }
            } 
            else {
                left = right;
            }
        }
        return time;
    }
};
```
