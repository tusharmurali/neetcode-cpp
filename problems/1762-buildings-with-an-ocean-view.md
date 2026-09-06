# 1762. Buildings With an Ocean View

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/buildings-with-an-ocean-view/>  
- **NeetCode:** <https://neetcode.io/problems/buildings-with-an-ocean-view>  
- **Video:** <https://www.youtube.com/watch?v=ntzA9LS8kLM>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A building has an ocean view if no building to its right is taller or equal in height. The ocean is to the right of all buildings. The simplest approach is to check each building individually: for every building, scan all buildings to its right and see if any of them block the view.

```cpp
class Solution {
public:
    vector<int> findBuildings(vector<int>& heights) {
        int n = heights.size();
        vector<int> res;

        for (int i = 0; i < n; i++) {
            bool flag = true;
            for (int j = i + 1; j < n; j++) {
                if (heights[i] <= heights[j]) {
                    flag = false;
                    break;
                }
            }
            if (flag) res.push_back(i);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$ for the output array.

## 2. Monotonic Stack

We can use a monotonic decreasing stack to efficiently track buildings with ocean views. As we scan from left to right, whenever we encounter a building that is taller than or equal to the building at the top of the stack, the stack building loses its ocean view (because this new building blocks it). We pop such buildings and push the current one. The remaining buildings in the stack at the end all have ocean views.

```cpp
class Solution {
public:
    vector<int> findBuildings(vector<int>& heights) {
        vector<int> stack;

        for (int i = 0; i < heights.size(); i++) {
            while (!stack.empty() && heights[stack.back()] <= heights[i]) {
                stack.pop_back();
            }
            stack.push_back(i);
        }

        return stack;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Greedy

The most elegant approach is to scan from right to left. A building has an ocean view if it is strictly taller than every building to its right. We only need to track the maximum height seen so far as we traverse from the rightmost building toward the left.

```cpp
class Solution {
public:
    vector<int> findBuildings(vector<int>& heights) {
        vector<int> res;
        int n = heights.size();
        res.push_back(n - 1);

        for (int i = n - 2; i >= 0; i--) {
            if (heights[i] > heights[res.back()]) {
                res.push_back(i);
            }
        }

        reverse(res.begin(), res.end());
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ for the output array.
