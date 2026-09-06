# 57. Insert Interval

- **Difficulty:** Medium  
- **Pattern:** Intervals  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/insert-interval/>  
- **NeetCode:** <https://neetcode.io/problems/insert-new-interval>  
- **Video:** <https://www.youtube.com/watch?v=A8NUOmlwOlM>  
- **Video approach:** 3. Greedy  

[← Back to index](../INDEX.md)

## 1. Linear Search

We are given a list of **non-overlapping intervals sorted by start time**, and we need to insert `newInterval` into the list while keeping the result sorted and non-overlapping.

Since the intervals are already sorted, we can process them in one pass and split the work into three simple parts:

1. **Intervals completely before** `newInterval`
    - These do not overlap, so we can add them directly to the result.

2. **Intervals that overlap** with `newInterval`
    - While there is overlap, we merge them by expanding `newInterval`:
        - new start = minimum of starts
        - new end = maximum of ends

3. **Intervals completely after** the merged `newInterval`
    - These also do not overlap, so we add them directly.

This way, we only scan the list once and merge exactly when needed.

```cpp
class Solution {
public:
    vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
        int n = intervals.size(), i = 0;
        vector<vector<int>> res;

        while (i < n && intervals[i][1] < newInterval[0]) {
            res.push_back(intervals[i]);
            i++;
        }

        while (i < n && newInterval[1] >= intervals[i][0]) {
            newInterval[0] = min(newInterval[0], intervals[i][0]);
            newInterval[1] = max(newInterval[1], intervals[i][1]);
            i++;
        }
        res.push_back(newInterval);

        while (i < n) {
            res.push_back(intervals[i]);
            i++;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output list.

## 2. Binary Search

We are given a list of **non-overlapping intervals sorted by start time**, and we want to insert `newInterval` while keeping the final list sorted and merged.

A simple idea is:

1. Use **binary search** to find the correct position where `newInterval` should be inserted based on its start time.
2. After inserting, the list is still sorted by start time.
3. Then we do a normal **merge intervals** pass:
    - if the current interval does not overlap the last interval in the result, append it
    - otherwise merge them by extending the end

Binary search helps us avoid scanning from the beginning just to find the insertion position.

```cpp
class Solution {
public:
    vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
        if (intervals.empty()) {
            return {newInterval};
        }

        int n = intervals.size();
        int target = newInterval[0];
        int left = 0, right = n - 1;

        while (left <= right) {
            int mid = (left + right) / 2;
            if (intervals[mid][0] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        intervals.insert(intervals.begin() + left, newInterval);

        vector<vector<int>> res;
        for (const auto& interval : intervals) {
            if (res.empty() || res.back()[1] < interval[0]) {
                res.push_back(interval);
            } else {
                res.back()[1] = max(res.back()[1], interval[1]);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output list.

## 3. Greedy ▶ video

We are inserting `newInterval` into a list of **sorted, non-overlapping intervals** and want the final result to remain sorted and non-overlapping.

A greedy approach works because as we scan from left to right, every interval falls into one of three cases relative to `newInterval`:

1. **Completely after `newInterval`**
    - If `newInterval` ends before the current interval starts, there will be no overlap with any later interval either.
    - So we can safely place `newInterval` here and return the answer immediately.

2. **Completely before `newInterval`**
    - If the current interval ends before `newInterval` starts, it can be added to the result unchanged.

3. **Overlapping with `newInterval`**
    - If they overlap, we merge them by expanding `newInterval` to cover both ranges.

By continuously merging when needed and stopping early when `newInterval` is placed, we solve it in one pass.

```cpp
class Solution {
public:
    vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
        vector<vector<int>> res;
        int newStart = newInterval[0];
        int newEnd = newInterval[1];
        int n = intervals.size();
        for (int i = 0; i < n; i++) {
            if (intervals[i][0] > newEnd) {
                res.push_back(newInterval);
                copy(intervals.begin() + i, intervals.end(), back_inserter(res));
                return res;
            } else if (intervals[i][1] < newStart) {
                res.push_back(intervals[i]);
            } else {
                newInterval[0] = min(newInterval[0], intervals[i][0]);
                newInterval[1] = max(newInterval[1], intervals[i][1]);
            }
        }
        res.push_back(newInterval);
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output list.

## Standalone solution file (`cpp/0057-insert-interval.cpp` in the NeetCode repo)

```cpp
/*
    Given array of non-overlapping intervals & a new interval, insert & merge if necessary
    Ex. intervals = [[1,3],[6,9]], newInterval = [2,5] -> [[1,5],[6,9]]

    To merge: while intervals are still overlapping the new one, take the larger bounds

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
        vector<vector<int>> ans;
        int newStart = newInterval[0];
        int newEnd = newInterval[1];
        int n = intervals.size();
        for (int i = 0; i < n; i++) {
            // Case 1: Non overlapping interval
            // If new interval is before the current interval
            if (intervals[i][0] > newEnd) {
                ans.push_back(newInterval);
                copy(intervals.begin() + i, intervals.end(), back_inserter(ans));
                return ans;
            }
            // If new interval is after the current interval
            else if (intervals[i][1] < newStart) {
                ans.push_back(intervals[i]);
            }
            // Case 2: Overlapping interval
            else {
                newInterval[0] = min(newInterval[0], intervals[i][0]);
                newInterval[1] = max(newInterval[1], intervals[i][1]);
            }
        }
        ans.push_back(newInterval);
        return ans;
    }
};
```
