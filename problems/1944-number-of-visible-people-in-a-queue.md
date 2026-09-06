# 1944. Number of Visible People in a Queue

- **Difficulty:** Hard  
- **Pattern:** Stack  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-visible-people-in-a-queue/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-visible-people-in-a-queue>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each person in the queue, we want to count how many people they can see to their right. Person `i` can see person `j` if there's no one taller than both of them standing in between. We track the maximum height seen so far as we scan rightward. If the minimum of the current person's height and the person we're checking is greater than the max height between them, they can see each other.

```cpp
class Solution {
public:
    vector<int> canSeePersonsCount(vector<int>& heights) {
        int n = heights.size();
        vector<int> res(n);
        for (int i = 0; i < n; i++) {
            int maxi = 0, cnt = 0;
            for (int j = i + 1; j < n; j++) {
                if (min(heights[i], heights[j]) > maxi) {
                    cnt++;
                }
                maxi = max(maxi, heights[j]);
            }
            res[i] = cnt;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$ for the output array.

## 2. Stack - I

A monotonic decreasing stack helps us efficiently find visibility relationships. As we iterate left to right, we pop people who are shorter than the current person since they can now see this taller person as their last visible person. The person remaining on top of the stack (if any) can also see the current person since nothing blocks their view.

```cpp
class Solution {
public:
    vector<int> canSeePersonsCount(vector<int>& heights) {
        int n = heights.size();
        vector<int> res(n);
        stack<int> st;
        for (int i = 0; i < n; i++) {
            int h = heights[i];
            while (!st.empty() && heights[st.top()] < h) {
                res[st.top()]++;
                st.pop();
            }
            if (!st.empty()) {
                res[st.top()]++;
            }
            st.push(i);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Stack - II

We can also solve this by iterating from right to left. For each person, we count how many people they can see by popping shorter people from the stack (each popped person is visible). If someone taller remains on the stack after popping, that person is also visible since nothing blocks the view.

```cpp
class Solution {
public:
    vector<int> canSeePersonsCount(vector<int>& heights) {
        int n = heights.size();
        vector<int> res(n, 0);
        stack<int> st;

        for (int i = n - 1; i >= 0; --i) {
            while (!st.empty() && st.top() < heights[i]) {
                st.pop();
                res[i]++;
            }
            if (!st.empty()) {
                res[i]++;
            }
            st.push(heights[i]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
