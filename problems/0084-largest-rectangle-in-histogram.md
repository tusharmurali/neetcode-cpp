# 84. Largest Rectangle In Histogram

- **Difficulty:** Hard  
- **Pattern:** Stack  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/largest-rectangle-in-histogram/>  
- **NeetCode:** <https://neetcode.io/problems/largest-rectangle-in-histogram>  
- **Video:** <https://www.youtube.com/watch?v=zx5Sw9130L0>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For every bar, we try to treat it as the **shortest bar** in the rectangle.  
To find how wide this rectangle can extend, we look **left** and **right** until we hit a bar shorter than the current one.  
The width between these two boundaries gives the largest rectangle where this bar is the limiting height.  
We repeat this for every bar and keep track of the maximum rectangle found.

```cpp
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        int n = heights.size();
        int maxArea = 0;

        for (int i = 0; i < n; i++) {
            int height = heights[i];

            int rightMost = i + 1;
            while (rightMost < n && heights[rightMost] >= height) {
                rightMost++;
            }

            int leftMost = i;
            while (leftMost >= 0 && heights[leftMost] >= height) {
                leftMost--;
            }

            rightMost--;
            leftMost++;
            maxArea = max(maxArea, height * (rightMost - leftMost + 1));
        }
        return maxArea;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Divide And Conquer (Segment Tree)

A large rectangle in the histogram must have some bar as its **shortest bar**.  
If we know the index of the **minimum height bar** in any range, then:

- The largest rectangle that **uses that bar as the limiting height** spans the entire range.
- Anything larger must lie **entirely on the left** or **entirely on the right** of that bar.

So we can solve the problem with a **divide and conquer** idea:

1. In a given range `[L, R]`, find the index of the smallest bar.
2. Compute:
    - The area using this bar across the whole range.
    - The best area entirely in `[L, minIndex - 1]`.
    - The best area entirely in `[minIndex + 1, R]`.
3. The answer for `[L, R]` is the maximum of those three.

To find the **index of the minimum height quickly** for any range, we use a **segment tree** built on heights. It supports “min index in range” queries in `O(log n)` time, which makes the whole divide-and-conquer efficient.

```cpp
class MinIdx_Segtree {
public:
    int n;
    const int INF = 1e9;
    vector<int> A;
    vector<int> tree;
    MinIdx_Segtree(int N, vector<int>& a) {
        this->n = N;
        this->A = a;
        while (__builtin_popcount(n) != 1) {
            A.push_back(INF);
            n++;
        }
        tree.resize(2 * n);
        build();
    }

    void build() {
        for (int i = 0; i < n; i++) {
            tree[n + i] = i;
        }
        for (int j = n - 1; j >= 1; j--) {
            int a = tree[j<<1];
            int b = tree[(j<<1) + 1];
            if(A[a]<=A[b])tree[j]=a;
            else tree[j] = b;
        }
    }

    void update(int i, int val) {
        A[i] = val;
        for (int j = (n + i) >> 1; j >= 1; j >>= 1) {
            int a = tree[j<<1];
            int b = tree[(j<<1) + 1];
            if(A[a]<=A[b])tree[j]=a;
            else tree[j] = b;
        }
    }

    int query(int ql, int qh) {
        return query(1, 0, n - 1, ql, qh);
    }

    int query(int node, int l, int h, int ql, int qh) {
        if (ql > h || qh < l) return INF;
        if (l >= ql && h <= qh) return tree[node];
        int a = query(node << 1, l, (l + h) >> 1, ql, qh);
        int b = query((node << 1) + 1, ((l + h) >> 1) + 1, h, ql, qh);
        if(a==INF)return b;
        if(b==INF)return a;
        return A[a]<=A[b]?a:b;
    }
};

class Solution {
public:
    int getMaxArea(vector<int>& heights, int l, int r, MinIdx_Segtree& st) {
        if (l > r) return 0;
        if (l == r) return heights[l];

        int minIdx = st.query(l, r);
        return max(max(getMaxArea(heights, l, minIdx - 1, st),
                   getMaxArea(heights, minIdx + 1, r, st)),
                   (r - l + 1) * heights[minIdx]);
    }
    int largestRectangleArea(vector<int>& heights) {
        int n = heights.size();
        MinIdx_Segtree st(n, heights);
        return getMaxArea(heights, 0, n - 1, st);
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Stack

For each bar, we want to know how far it can stretch left and right **before bumping into a shorter bar**.  
That distance tells us the widest rectangle where this bar is the limiting height.  
To efficiently find the nearest smaller bar on both sides, we use a **monotonic stack** that keeps indices of bars in increasing height order.  
This lets us compute boundaries in linear time instead of checking outward for every bar.

```cpp
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        int n = heights.size();
        vector<int> leftMost(n, -1);
        vector<int> rightMost(n, n);
        stack<int> stack;

        for (int i = 0; i < n; i++) {
            while (!stack.empty() && heights[stack.top()] >= heights[i]) {
                stack.pop();
            }
            if (!stack.empty()) {
                leftMost[i] = stack.top();
            }
            stack.push(i);
        }

        while (!stack.empty()) stack.pop();

        for (int i = n - 1; i >= 0; i--) {
            while (!stack.empty() && heights[stack.top()] >= heights[i]) {
                stack.pop();
            }
            if (!stack.empty()) {
                rightMost[i] = stack.top();
            }
            stack.push(i);
        }

        int maxArea = 0;
        for (int i = 0; i < n; i++) {
            leftMost[i] += 1;
            rightMost[i] -= 1;
            maxArea = max(maxArea, heights[i] * (rightMost[i] - leftMost[i] + 1));
        }

        return maxArea;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Stack (One Pass)

We want, for each bar, the widest area where it can act as the **shortest bar**.  
With a single pass and a stack, we can do this on the fly:

- We keep a stack of bars in **increasing height order**, each stored with the earliest index where that height can start.
- When we see a new bar that is **shorter** than the top of the stack, it means the taller bar on top can’t extend further to the right.
    - So we pop it and compute the area it could cover.
- The new shorter bar can start from as far left as the popped bar’s start index, so we reuse that index.
- After the pass, we compute areas for any bars still in the stack, extending them to the end.

Each bar is pushed and popped at most once, giving an efficient, one-pass solution.

```cpp
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        int maxArea = 0;
        stack<pair<int, int>> stack; // pair: (index, height)

        for (int i = 0; i < heights.size(); i++) {
            int start = i;
            while (!stack.empty() && stack.top().second > heights[i]) {
                pair<int, int> top = stack.top();
                int index = top.first;
                int height = top.second;
                maxArea = max(maxArea, height * (i - index));
                start = index;
                stack.pop();
            }
            stack.push({ start, heights[i] });
        }

        while (!stack.empty()) {
            int index = stack.top().first;
            int height = stack.top().second;
            maxArea = max(maxArea, height * (static_cast<int>(heights.size()) - index));
            stack.pop();
        }
        return maxArea;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 5. Stack (Optimal)

We want, for every bar, to know how wide it can stretch while still being the **shortest bar** in that rectangle.

A monotonic stack helps with this:

- We keep a stack of indices where the bar heights are in **increasing order**.
- As long as the next bar is **taller or equal**, we keep pushing indices.
- When we see a **shorter** bar, it means the bar on top of the stack can’t extend further to the right:
    - We pop it and treat it as the height of a rectangle.
    - Its width goes from the new top of the stack + 1 up to the current index − 1.

To make sure every bar eventually gets popped and processed, we run the loop one extra step with a “virtual” bar of height 0 at the end.  
Each bar is pushed and popped at most once, so this is both optimal and clean.

```cpp
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        int n = heights.size();
        int maxArea = 0;
        stack<int> stack;

        for (int i = 0; i <= n; i++) {
            while (!stack.empty() &&
                 (i == n || heights[stack.top()] >= heights[i])) {
                int height = heights[stack.top()];
                stack.pop();
                int width = stack.empty() ? i : i - stack.top() - 1;
                maxArea = max(maxArea, height * width);
            }
            stack.push(i);
        }
        return maxArea;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0084-largest-rectangle-in-histogram.cpp` in the NeetCode repo)

```cpp
/*
Given array of heights, return area of largest rectangle
Ex. heights = [2,1,5,6,2,3] -> 10 (5 x 2 at index 2 and 3)

Monotonic incr stack, if curr height lower extend back, find max area

Time: O(n)
Space: O(n)
*/

class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        // pair: [index, height]
        stack<pair<int, int>> stk;
        int result = 0;
        
        for (int i = 0; i < heights.size(); i++) {
            int start = i;
            
            while (!stk.empty() && stk.top().second > heights[i]) {
                int index = stk.top().first;
                int width = i - index;
                int height = stk.top().second;
                stk.pop();
                
                result = max(result, height * width);
                start = index;
            }
            
            stk.push({start, heights[i]});
        }
        
        while (!stk.empty()) {
            int width = heights.size() - stk.top().first;
            int height = stk.top().second;
            stk.pop();
            
            result = max(result, height * width);
        }
                          
        return result;
    }
};
```
