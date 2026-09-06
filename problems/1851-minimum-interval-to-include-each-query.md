# 1851. Minimum Interval to Include Each Query

- **Difficulty:** Hard  
- **Pattern:** Intervals  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/minimum-interval-to-include-each-query/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-interval-including-query>  
- **Video:** <https://www.youtube.com/watch?v=5hQ5WWW5awQ>  
- **Video approach:** 3. Min Heap  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each query value `q`, we want to find the **smallest interval length** among all intervals `[l, r]` that **contain** `q` (meaning `l <= q <= r`).
If no interval contains `q`, we return `-1`.

The brute force idea is very direct:

- handle queries one by one
- for a query, scan through every interval
- whenever an interval covers the query, compute its length `r - l + 1`
- keep the minimum length seen

```cpp
class Solution {
public:
    vector<int> minInterval(vector<vector<int>>& intervals, vector<int>& queries) {
        vector<int> res;
        for (int q : queries) {
            int cur = -1;
            for (auto& interval : intervals) {
                int l = interval[0], r = interval[1];
                if (l <= q && q <= r) {
                    if (cur == -1 || (r - l + 1) < cur) {
                        cur = r - l + 1;
                    }
                }
            }
            res.push_back(cur);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(m)$ space for the output array.

> Where $m$ is the length of the array $queries$ and $n$ is the length of the array $intervals$.

## 2. Sweep Line Algorithm

For each query value `q`, we want the length of the **smallest interval** `[l, r]` that contains `q` (`l <= q <= r`). If none exists, the answer is `-1`.

A sweep line approach processes everything (interval starts, interval ends, and queries) in **sorted order of time**.  
While sweeping from left to right, we maintain a data structure of “currently active intervals” (intervals that have started but have not ended yet).  
For a query time `q`, the answer is simply the **smallest interval length among the active intervals**.

To get that smallest length quickly, we use a **min-heap** ordered by interval size.

Because intervals can end later, we also need a way to remove expired intervals:

- when an interval ends, we mark it as inactive
- when answering a query, we pop inactive intervals from the heap until the top is active

```cpp
class Solution {
public:
    vector<int> minInterval(vector<vector<int>>& intervals, vector<int>& queries) {
        vector<vector<int>> events;
        // Create events for intervals
        for (int i = 0; i < intervals.size(); i++) {
            events.push_back({intervals[i][0], 0, intervals[i][1] - intervals[i][0] + 1, i});
            events.push_back({intervals[i][1], 2, intervals[i][1] - intervals[i][0] + 1, i});
        }

        // Create events for queries
        for (int i = 0; i < queries.size(); i++) {
            events.push_back({queries[i], 1, i});
        }

        // Sort by time and type (end before query)
        sort(events.begin(), events.end(), [](const vector<int>& a, const vector<int>& b) {
            return a[0] == b[0] ? a[1] < b[1] : a[0] < b[0];
        });

        vector<int> ans(queries.size(), -1);
        // Min heap storing [size, index]
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        vector<bool> inactive(intervals.size(), false);

        for (const auto& event : events) {
            if (event[1] == 0) { // Interval start
                pq.push({event[2], event[3]});
            } else if (event[1] == 2) { // Interval end
                inactive[event[3]] = true;
            } else { // Query
                int queryIdx = event[2];
                while (!pq.empty() && inactive[pq.top().second]) {
                    pq.pop();
                }
                if (!pq.empty()) {
                    ans[queryIdx] = pq.top().first;
                }
            }
        }

        return ans;
    }
};
```

**Complexity**

- Time complexity: $O((n + m) \log (n + m))$
- Space complexity: $O(n + m)$

> Where $m$ is the length of the array $queries$ and $n$ is the length of the array $intervals$.

## 3. Min Heap ▶ video

For each query `q`, we want the **length of the smallest interval** `[l, r]` such that
`l ≤ q ≤ r`. If no interval covers `q`, the answer is `-1`.

A very efficient way to do this is:

- process queries in **sorted order**
- as queries increase, we **add intervals whose start ≤ q**
- among those active intervals, remove any that end before `q`
- the smallest valid interval is always at the **top of a min heap**

The heap is ordered by **interval length**, so the smallest covering interval is easy to find.

```cpp
class Solution {
public:
    vector<int> minInterval(vector<vector<int>>& intervals, vector<int>& queries) {
        // Sort intervals based on the start value
        sort(intervals.begin(), intervals.end(), [](auto& a, auto& b) {
            return a[0] < b[0];
        });

        vector<int> sortedQueries = queries;
        sort(sortedQueries.begin(), sortedQueries.end());
        map<int, int> res;

        auto cmp = [](const vector<int>& a, const vector<int>& b) {
            return a[0] > b[0] || (a[0] == b[0] && a[1] > b[1]);
        };
        priority_queue<vector<int>, vector<vector<int>>, decltype(cmp)> minHeap(cmp);

        int i = 0;
        for (int q : sortedQueries) {
            while (i < intervals.size() && intervals[i][0] <= q) {
                int l = intervals[i][0];
                int r = intervals[i][1];
                minHeap.push({r - l + 1, r});
                i++;
            }

            while (!minHeap.empty() && minHeap.top()[1] < q) {
                minHeap.pop();
            }

            res[q] = minHeap.empty() ? -1 : minHeap.top()[0];
        }

        vector<int> result(queries.size());
        for (int j = 0; j < queries.size(); j++) {
            result[j] = res[queries[j]];
        }
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n + m \log m)$
- Space complexity: $O(n + m)$

> Where $m$ is the length of the array $queries$ and $n$ is the length of the array $intervals$.

## 4. Min Segment Tree (Lazy Propagation)

For each query `q`, we need the length of the **smallest interval** `[l, r]` such that `l <= q <= r`.  
If no interval covers `q`, the answer is `-1`.

This solution treats the number line as a set of **discrete important points** (all interval endpoints and all queries).  
Then it uses a **segment tree** that supports:

- **Range update**: “For every point covered by this interval, the best (minimum) interval length might become smaller.”
- **Point query**: “At this query point, what is the minimum interval length that covers it?”

Since many intervals update large ranges, we use **lazy propagation** to apply updates efficiently without touching every point in the range.

Because coordinates can be large, we first do **coordinate compression**:

- map every unique coordinate to a compact index `0..M-1`
- this allows the segment tree to work on a small index range

```cpp
class SegmentTree {
public:
    int n;
    vector<int> tree;
    vector<int> lazy;

    SegmentTree(int N) {
        this->n = N;
        tree.assign(4 * N, INT_MAX);
        lazy.assign(4 * N, INT_MAX);
    }

    void propagate(int treeidx, int lo, int hi) {
        if (lazy[treeidx] != INT_MAX) {
            tree[treeidx] = min(tree[treeidx], lazy[treeidx]);
            if (lo != hi) {
                lazy[2 * treeidx + 1] = min(lazy[2 * treeidx + 1], lazy[treeidx]);
                lazy[2 * treeidx + 2] = min(lazy[2 * treeidx + 2], lazy[treeidx]);
            }
            lazy[treeidx] = INT_MAX;
        }
    }

    void update(int treeidx, int lo, int hi, int left, int right, int val) {
        propagate(treeidx, lo, hi);

        if (lo > right || hi < left) return;

        if (lo >= left && hi <= right) {
            lazy[treeidx] = min(lazy[treeidx], val);
            propagate(treeidx, lo, hi);
            return;
        }

        int mid = (lo + hi) / 2;
        update(2 * treeidx + 1, lo, mid, left, right, val);
        update(2 * treeidx + 2, mid + 1, hi, left, right, val);

        tree[treeidx] = min(tree[2 * treeidx + 1], tree[2 * treeidx + 2]);
    }

    int query(int treeidx, int lo, int hi, int idx) {
        propagate(treeidx, lo, hi);
        if (lo == hi) return tree[treeidx];

        int mid = (lo + hi) / 2;
        if (idx <= mid) return query(2 * treeidx + 1, lo, mid, idx);
        else return query(2 * treeidx + 2, mid + 1, hi, idx);
    }

    void update(int left, int right, int val) {
        update(0, 0, n - 1, left, right, val);
    }

    int query(int idx) {
        return query(0, 0, n - 1, idx);
    }
};

class Solution {
public:
    vector<int> minInterval(vector<vector<int>>& intervals, vector<int>& queries) {
        vector<int> points;

        for (const auto& interval : intervals) {
            points.push_back(interval[0]);
            points.push_back(interval[1]);
        }
        for (int q : queries) {
            points.push_back(q);
        }

        sort(points.begin(), points.end());
        points.erase(unique(points.begin(), points.end()), points.end());

        // compress the coordinates
        unordered_map<int, int> compress;
        for (int i = 0; i < points.size(); ++i) {
            compress[points[i]] = i;
        }

        SegmentTree segTree(points.size());

        for (const auto& interval : intervals) {
            int start = compress[interval[0]];
            int end = compress[interval[1]];
            int len = interval[1] - interval[0] + 1;
            segTree.update(start, end, len);
        }

        vector<int> ans;
        for (int q : queries) {
            int idx = compress[q];
            int res = segTree.query(idx);
            ans.push_back(res == INT_MAX ? -1 : res);
        }

        return ans;
    }
};
```

**Complexity**

- Time complexity: $O((n + m)\log k)$
- Space complexity:
    - $O(k)$ extra space.
    - $O(m)$ space for the output array.

> Where $m$ is the length of the array $queries$, $n$ is the length of the array $intervals$ and $k$ is the number of unique points.

## Standalone solution file (`cpp/1851-minimum-interval-to-include-each-query.cpp` in the NeetCode repo)

```cpp
/*
    Given intervals array & queries array, ans to a query is min interval containing it
    Ex. intervals = [[1,4],[2,4],[3,6],[4,4]], queries = [2,3,4,5] -> [3,3,1,4]

    Min heap & sort by size of intervals, top will be min size, 

    Time: O(n log n + q log q) -> n = number of intervals, q = number of queries
    Space: O(n + q)
*/

class Solution {
public:
    vector<int> minInterval(vector<vector<int>>& intervals, vector<int>& queries) {
        vector<int> sortedQueries = queries;
        
        // [size of interval, end of interval]
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        // {query -> size of interval}
        unordered_map<int, int> m;
        
        // also need only valid intervals so sort by start time & sort queries
        sort(intervals.begin(), intervals.end());
        sort(sortedQueries.begin(), sortedQueries.end());
        
        vector<int> result;
        
        int i = 0;
        for (int j = 0; j < sortedQueries.size(); j++) {
            int query = sortedQueries[j];
            
            while (i < intervals.size() && intervals[i][0] <= query) {
                int left = intervals[i][0];
                int right = intervals[i][1];
                pq.push({right - left + 1, right});
                i++;
            }
            
            while (!pq.empty() && pq.top().second < query) {
                pq.pop();
            }
            
            if (!pq.empty()) {
                m[query] = pq.top().first;
            } else {
                m[query] = -1;
            }
        }
        
        for (int j = 0; j < queries.size(); j++) {
            result.push_back(m[queries[j]]);
        }
        return result;
    }
};
```
