# 1526. Minimum Number of Increments on Subarrays to Form a Target Array

- **Difficulty:** Hard  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-number-of-increments-on-subarrays-to-form-a-target-array/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-number-of-increments-on-subarrays-to-form-a-target-array>  
- **Video:** <https://www.youtube.com/watch?v=84mt0YWJd1w>  

[← Back to index](../INDEX.md)

## 1. Simulation

Think of building the target array as painting horizontal layers. Each operation increments a contiguous subarray by `1`, which is like painting one layer. We can recursively find the minimum element in a range, paint up to that height, then solve the left and right portions independently.

The minimum element acts as a "floor" that separates the problem into independent subproblems. We paint `min_value - current_height` layers across the whole range, then recursively handle the regions to the left and right of the minimum.

```cpp
class Solution {
public:
    int minNumberOperations(vector<int>& target) {
        return rec(target, 0, target.size() - 1, 0);
    }

private:
    int rec(vector<int>& target, int l, int r, int h) {
        if (l > r) return 0;

        int minIdx = l;
        for (int i = l + 1; i <= r; i++) {
            if (target[i] < target[minIdx]) {
                minIdx = i;
            }
        }

        int res = target[minIdx] - h;
        res += rec(target, l, minIdx - 1, target[minIdx]);
        res += rec(target, minIdx + 1, r, target[minIdx]);

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Segment Tree

The simulation approach is slow because finding the minimum in each range takes O(n) time. A segment tree allows O(log `n`) range minimum queries, speeding up the overall algorithm.

The logic remains the same: divide at the minimum, but now we query the segment tree instead of scanning linearly. This reduces the total time from O(n^2) to O(n log `n`).

```cpp
class SegmentTree {
public:
    int n;
    vector<int> A, tree;
    const int INF = INT_MAX;

    SegmentTree(vector<int>& arr) {
        A = arr;
        n = arr.size();
        while (__builtin_popcount(n) != 1) {
            A.push_back(INF);
            n++;
        }
        tree.resize(2 * n);
        build();
    }

    void build() {
        for (int i = 0; i < n; ++i) {
            tree[n + i] = i;
        }
        for (int j = n - 1; j >= 1; --j) {
            int a = tree[j << 1], b = tree[(j << 1) | 1];
            tree[j] = A[a] <= A[b] ? a : b;
        }
    }

    int query(int ql, int qh) {
        return _query(1, 0, n - 1, ql, qh);
    }

    int _query(int node, int l, int h, int ql, int qh) {
        if (ql > h || qh < l) return -1;
        if (l >= ql && h <= qh) return tree[node];
        int mid = (l + h) >> 1;
        int a = _query(node << 1, l, mid, ql, qh);
        int b = _query((node << 1) | 1, mid + 1, h, ql, qh);
        if (a == -1) return b;
        if (b == -1) return a;
        return A[a] <= A[b] ? a : b;
    }
};

class Solution {
public:
    int minNumberOperations(vector<int>& target) {
        SegmentTree seg(target);
        return rec(0, target.size() - 1, 0, target, seg);
    }

    int rec(int l, int r, int h, vector<int>& target, SegmentTree& seg) {
        if (l > r) return 0;
        int minIdx = seg.query(l, r);
        int res = target[minIdx] - h;
        res += rec(l, minIdx - 1, target[minIdx], target, seg);
        res += rec(minIdx + 1, r, target[minIdx], target, seg);
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Greedy

Consider how we would paint the array left to right. At the first element, we need `target[0]` operations to build it from `0`. For each subsequent element, if it is taller than the previous one, we need additional operations to "extend" our brush strokes upward. If it is shorter or equal, the existing strokes can simply continue or stop.

The key insight: we only need new operations when the height increases. The total count is the first element plus the sum of all positive increases between consecutive elements.

```cpp
class Solution {
public:
    int minNumberOperations(vector<int>& target) {
        int res = target[0];
        for (int i = 1; i < target.size(); i++) {
            res += max(target[i] - target[i - 1], 0);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
