# 239. Sliding Window Maximum

- **Difficulty:** Hard  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/sliding-window-maximum/>  
- **NeetCode:** <https://neetcode.io/problems/sliding-window-maximum>  
- **Video:** <https://www.youtube.com/watch?v=DfljaUwZsOk>  
- **Video approach:** 5. Deque  

[← Back to index](../INDEX.md)

## 1. Brute Force

For every possible window of size `k`, we simply look at all `k` elements and pick the maximum.  
We slide the window one step at a time, and each time we scan all elements inside it to find the max.  
This method is very easy to understand but slow, because we repeatedly re-scan many of the same elements.

```cpp
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        vector<int> output;
        int n = nums.size();

        for (int i = 0; i <= n - k; i++) {
            int maxi = nums[i];
            for (int j = i; j < i + k; j++) {
                maxi = max(maxi, nums[j]);
            }
            output.push_back(maxi);
        }

        return output;
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n - k + 1)$ space for the output array.

> Where $n$ is the length of the array and $k$ is the size of the window.

## 2. Segment Tree

The brute-force solution recomputes the maximum for every window by scanning all `k` elements each time, which is slow.  
A **Segment Tree** helps us answer “what is the maximum in this range?” much faster after some preprocessing.

Think of the segment tree as a special structure built on top of the array where:

- Each node stores the **maximum** of a segment (range) of the array.
- The root stores the maximum of the whole array.
- Its children store the maximum of left half and right half, and so on.

Once we build this tree:

- We can query the maximum for any range `[L, R]` (our sliding window) in `O(log n)` time.
- We just slide the window and ask the segment tree for the max in each range.

So the process is:
**build once → query many times efficiently.**

```cpp
class SegmentTree {
public:
    int n;
    vector<int> tree;

    SegmentTree(int N, vector<int>& A) {
        this->n = N;
        while (__builtin_popcount(n) != 1) {
            n++;
        }
        build(N, A);
    }

    void build(int N, vector<int>& A) {
        tree.resize(2 * n, INT_MIN);
        for (int i = 0; i < N; i++) {
            tree[n + i] = A[i];
        }
        for (int i = n - 1; i > 0; --i) {
            tree[i] = max(tree[i << 1], tree[i << 1 | 1]);
        }
    }

    int query(int l, int r) {
        int res = INT_MIN;
        for (l += n, r += n + 1; l < r; l >>= 1, r >>= 1) {
            if (l & 1) res = max(res, tree[l++]);
            if (r & 1) res = max(res, tree[--r]);
        }
        return res;
    }
};

class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        int n = nums.size();
        SegmentTree segTree(n, nums);
        vector<int> output;
        for (int i = 0; i <= n - k; i++) {
            output.push_back(segTree.query(i, i + k - 1));
        }
        return output;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Heap

We want to quickly get the maximum value inside a sliding window that moves across the array.  
A **max-heap** is perfect for this because it always lets us access the largest element instantly.

As we slide the window:

- We keep inserting new elements into the heap.
- Some old elements will fall out of the left side of the window.
- If the largest element in the heap is no longer inside the window, we remove it.
- The top of the heap always represents the current maximum for the window.

This way, we efficiently maintain the maximum even as the window moves.

```cpp
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        priority_queue<pair<int, int>> heap;
        vector<int> output;
        for (int i = 0; i < nums.size(); i++) {
            heap.push({nums[i], i});
            if (i >= k - 1) {
                while (heap.top().second <= i - k) {
                    heap.pop();
                }
                output.push_back(heap.top().first);
            }
        }
        return output;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming

Instead of recalculating the maximum for each sliding window, we can preprocess the array so that every window’s maximum can be answered in **O(1)** time.

We divide the array into blocks of size `k`.  
Within each block, we build:

- a **leftMax** array: left-to-right maximums inside each block
- a **rightMax** array: right-to-left maximums inside each block

For any sliding window:

- its left part falls inside some block, so the maximum for that region is in `rightMax[i]`
- its right part falls inside a block, so the maximum is in `leftMax[i + k - 1]`

The true window maximum is the larger of those two.  
This lets us compute each window's maximum instantly.

```cpp
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        int n = nums.size();
        vector<int> leftMax(n);
        vector<int> rightMax(n);

        leftMax[0] = nums[0];
        rightMax[n - 1] = nums[n - 1];

        for (int i = 1; i < n; i++) {
            if (i % k == 0) {
                leftMax[i] = nums[i];
            } else {
                leftMax[i] = max(leftMax[i - 1], nums[i]);
            }

            if ((n - 1 - i) % k == 0) {
                rightMax[n - 1 - i] = nums[n - 1 - i];
            } else {
                rightMax[n - 1 - i] = max(rightMax[n - i], nums[n - 1 - i]);
            }
        }

        vector<int> output(n - k + 1);

        for (int i = 0; i < n - k + 1; i++) {
            output[i] = max(leftMax[i + k - 1], rightMax[i]);
        }

        return output;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 5. Deque ▶ video

A deque helps us efficiently track the maximum inside the sliding window.  
The key idea is to keep the deque storing **indices** of elements in **decreasing order of their values**.  
This guarantees that:

- The **front** of the deque always holds the index of the current window’s maximum.
- Smaller elements behind a bigger one are useless (they can never become the max later),  
  so we remove them when pushing a new number.
- If the element at the front falls out of the window, we remove it.

By maintaining this structure, each element is added and removed at most once, giving an optimal solution.

```cpp
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        int n = nums.size();
        vector<int> output(n - k + 1);
        deque<int> q;
        int l = 0, r = 0;

        while (r < n) {
            while (!q.empty() && nums[q.back()] < nums[r]) {
                q.pop_back();
            }
            q.push_back(r);

            if (l > q.front()) {
                q.pop_front();
            }

            if ((r + 1) >= k) {
                output[l] = nums[q.front()];
                l++;
            }
            r++;
        }

        return output;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0239-sliding-window-maximum.cpp` in the NeetCode repo)

```cpp
/*
    Given int array & sliding window size k, return max sliding window
    Ex. nums = [1,3,-1,-3,5,3,6,7] k = 3 -> [3,3,5,5,6,7]

    Sliding window deque, ensure monotonic decr, leftmost largest

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        deque<int> dq;
        vector<int> result;
        
        int i = 0;
        int j = 0;
        
        while (j < nums.size()) {
            while (!dq.empty() && nums[dq.back()] < nums[j]) {
                dq.pop_back();
            }
            dq.push_back(j);
            
            if (i > dq.front()) {
                dq.pop_front();
            }
            
            if (j + 1 >= k) {
                result.push_back(nums[dq.front()]);
                i++;
            }
            j++;
        }
        
        return result;
    }
};
```
