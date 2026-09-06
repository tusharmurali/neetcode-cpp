# 435. Non Overlapping Intervals

- **Difficulty:** Medium  
- **Pattern:** Intervals  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/non-overlapping-intervals/>  
- **NeetCode:** <https://neetcode.io/problems/non-overlapping-intervals>  
- **Video:** <https://www.youtube.com/watch?v=nONCGxWoUfM>  
- **Video approach:** 5. Greedy (Sort By Start)  

[← Back to index](../INDEX.md)

## 1. Recursion

We want to remove the minimum number of intervals so that the remaining intervals **do not overlap**.

A helpful way to think about this is:

- instead of directly counting removals, we can try to keep as many non-overlapping intervals as possible
- if we know the maximum number of intervals we can keep without overlap, then:
    - `minimum removals = total intervals - maximum kept`

To make decisions, we sort the intervals by start time and use recursion to explore two choices at each interval:

1. **Skip** the current interval
2. **Take** the current interval (only if it does not overlap with the previously taken interval)

The recursive function represents:
**"What is the maximum number of non-overlapping intervals we can keep starting from index `i`, given that the last chosen interval is `prev`?"**

```cpp
class Solution {
public:
    int eraseOverlapIntervals(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end());
        return intervals.size() - dfs(intervals, 0, -1);
    }

private:
    int dfs(const vector<vector<int>>& intervals, int i, int prev) {
        if (i == intervals.size()) return 0;
        int res = dfs(intervals, i + 1, prev);
        if (prev == -1 || intervals[prev][1] <= intervals[i][0]) {
            res = max(res, 1 + dfs(intervals, i + 1, i));
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

We want to remove the minimum number of intervals so that the remaining intervals **do not overlap**.

A common trick is to flip the problem:

- instead of counting removals directly, find the **maximum number of non-overlapping intervals** we can keep
- then:
    - `minimum removals = total intervals - maximum kept`

This solution sorts intervals by **end time**. After that, for any interval `i`, the next interval we choose must start **at or after** `intervals[i][1]`.

We define a DP state that answers:
**"If we choose interval `i` as part of our set, what is the maximum number of non-overlapping intervals we can take starting from `i`?"**

The result for an index depends on future indices, and many states repeat, so we use memoization.

```cpp
class Solution {
public:
    int eraseOverlapIntervals(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end(), [](auto& a, auto& b) {
            return a[1] < b[1];
        });
        int n = intervals.size();
        vector<int> memo(n, -1);

        int maxNonOverlapping = dfs(intervals, 0, memo);
        return n - maxNonOverlapping;
    }

private:
    int dfs(const vector<vector<int>>& intervals, int i, vector<int>& memo) {
        if (i >= intervals.size()) return 0;
        if (memo[i] != -1) return memo[i];

        int res = 1;
        for (int j = i + 1; j < intervals.size(); j++) {
            if (intervals[i][1] <= intervals[j][0]) {
                res = max(res, 1 + dfs(intervals, j, memo));
            }
        }
        memo[i] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

We want to remove the minimum number of intervals so that the remaining intervals **do not overlap**.

A useful trick is to instead find the **maximum number of non-overlapping intervals** we can keep.
Once we know that:

- `minimum removals = total intervals - maximum kept`

After sorting intervals by **end time**, we can build a DP array where:

- `dp[i]` = the maximum number of non-overlapping intervals we can keep **ending at interval `i`** (meaning interval `i` is included)

To compute `dp[i]`, we look at all earlier intervals `j < i`:

- if interval `j` ends before interval `i` starts, they can both be kept
- so we can extend the chain: `1 + dp[j]`

```cpp
class Solution {
public:
    int eraseOverlapIntervals(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end(), [](auto& a, auto& b) {
            return a[1] < b[1];
        });
        int n = intervals.size();
        vector<int> dp(n, 0);

        for (int i = 0; i < n; i++) {
            dp[i] = 1;
            for (int j = 0; j < i; j++) {
                if (intervals[j][1] <= intervals[i][0]) {
                    dp[i] = max(dp[i], 1 + dp[j]);
                }
            }
        }

        int maxNonOverlapping = *max_element(dp.begin(), dp.end());
        return n - maxNonOverlapping;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Binary Search)

We want to remove the minimum number of intervals so that the remaining intervals **do not overlap**.

A common trick is to flip the goal:

- instead of counting removals directly, find the **maximum number of non-overlapping intervals** we can keep
- then:
    - `minimum removals = total intervals - maximum kept`

After sorting intervals by **end time**, consider interval `i`:

- we have two choices:
    1. **skip** interval `i` → keep the best answer up to `i - 1`
    2. **take** interval `i` → then we must take it after the last interval that ends
       before `intervals[i][0]`

The slow part is finding that "previous compatible interval".
Because the intervals are sorted by end time, we can find it using **binary search**.

We maintain:

- `dp[i]` = maximum number of non-overlapping intervals we can keep using intervals `0..i`

```cpp
class Solution {
public:
    int eraseOverlapIntervals(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end(), [](auto& a, auto& b) {
            return a[1] < b[1];
        });
        int n = intervals.size();
        vector<int> dp(n);
        dp[0] = 1;

        for (int i = 1; i < n; i++) {
            int idx = bs(i, intervals[i][0], intervals);
            if (idx == 0) {
                dp[i] = dp[i - 1];
            } else {
                dp[i] = max(dp[i - 1], 1 + dp[idx - 1]);
            }
        }
        return n - dp[n - 1];
    }

    int bs(int r, int target, vector<vector<int>>& intervals) {
        int l = 0;
        while (l < r) {
            int m = (l + r) >> 1;
            if (intervals[m][1] <= target) {
                l = m + 1;
            } else {
                r = m;
            }
        }
        return l;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 5. Greedy (Sort By Start) ▶ video

We want to remove the **minimum number of intervals** so that the remaining intervals **do not overlap**.

A greedy strategy works well here. After sorting intervals by their **start time**, we process them from left to right and always keep the interval that ends **earlier** when an overlap occurs.

Why this works:

- When two intervals overlap, keeping the one with the **smaller end time** leaves more room for future intervals
- Removing the interval with the larger end is always the better choice, because keeping it would block more upcoming intervals

So instead of choosing which interval to keep globally, we make a **local greedy decision** whenever an overlap happens.

```cpp
class Solution {
public:
    int eraseOverlapIntervals(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end());
        int res = 0;
        int prevEnd = intervals[0][1];

        for (int i = 1; i < intervals.size(); i++) {
            int start = intervals[i][0];
            int end = intervals[i][1];
            if (start >= prevEnd) {
                prevEnd = end;
            } else {
                res++;
                prevEnd = min(end, prevEnd);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 6. Greedy (Sort By End)

We want to remove the **minimum number of intervals** so that the remaining intervals **do not overlap**.

A very clean greedy idea is to always **keep the interval that ends earliest**.
Why? Because an interval that ends earlier leaves more room for future intervals, reducing the chance of overlap later.

So instead of deciding which intervals to remove directly, we:

- sort all intervals by their **end time**
- walk through them from left to right
- keep track of the end of the last interval we decided to keep

Whenever we see an overlap:

- we **remove the current interval**
- because it ends later than the one we already kept (due to sorting)

This greedy choice is optimal and ensures the maximum number of intervals are kept.

```cpp
class Solution {
public:
    int eraseOverlapIntervals(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end(), [](auto& a, auto& b) {
            return a[1] < b[1];
        });
        int res = 0;
        int prevEnd = intervals[0][1];

        for (int i = 1; i < intervals.size(); i++) {
            int start = intervals[i][0];
            int end = intervals[i][1];
            if (start < prevEnd) {
                res++;
            } else {
                prevEnd = end;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## Standalone solution file (`cpp/0435-non-overlapping-intervals.cpp` in the NeetCode repo)

```cpp
/*
    Given array of intervals, return min # of intervals to remove for all non-overlapping
    Ex. intervals = [[1,2],[1,3],[2,3],[3,4]] -> 1, remove [1,3] for all non-overlapping

    Remove interval w/ longer end point, since will always overlap more or = vs shorter one

    Time: O(n log n)
    Space: O(1)
*/

class Solution {
public:
    int eraseOverlapIntervals(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end());
        int prevEnd = intervals[0][1];
        int count = 0;
        for (int i = 1; i < intervals.size(); i++) {
            if (prevEnd > intervals[i][0]) {
                count++;
                prevEnd = min(prevEnd, intervals[i][1]);
            } else {
                prevEnd = intervals[i][1];
            }
        }
        return count;
    }
};
```
