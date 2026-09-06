# 56. Merge Intervals

- **Difficulty:** Medium  
- **Pattern:** Intervals  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/merge-intervals/>  
- **NeetCode:** <https://neetcode.io/problems/merge-intervals>  
- **Video:** <https://www.youtube.com/watch?v=44H3cEC2fFM>  

[← Back to index](../INDEX.md)

## 1. Sorting

We are given a list of intervals, and some of them may **overlap**.
The goal is to merge all overlapping intervals so that the final list contains only **non-overlapping intervals**, covering the same ranges.

A natural way to approach this is:

- if intervals are processed in **sorted order by start time**, then
- any overlap can only happen with the **most recently added interval**

So after sorting:

- we keep track of the last merged interval
- if the current interval overlaps with it, we merge them
- otherwise, we start a new interval

```cpp
class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end());
        vector<vector<int>> output;
        output.push_back(intervals[0]);

        for (auto& interval : intervals) {
            int start = interval[0];
            int end = interval[1];
            int lastEnd = output.back()[1];

            if (start <= lastEnd) {
                output.back()[1] = max(lastEnd, end);
            } else {
                output.push_back({start, end});
            }
        }
        return output;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity:
    - $O(1)$ or $O(n)$ space depending on the sorting algorithm.
    - $O(n)$ for the output list.

## 2. Sweep Line Algorithm

This approach treats each interval as a pair of **events** on a number line:

- an interval **starts** at `start`
- an interval **ends** at `end`

Instead of merging intervals directly, we track **how many intervals are currently active** as we move from left to right along the number line.

The key idea:

- when the number of active intervals goes from `0 → positive`, a merged interval **starts**
- when it goes from `positive → 0`, a merged interval **ends**

By recording how the count changes at each boundary and sweeping through them in order, we can reconstruct all merged intervals.

```cpp
class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        map<int, int> mp;
        for (const auto& interval : intervals) {
            mp[interval[0]]++;
            mp[interval[1]]--;
        }

        vector<vector<int>> res;
        vector<int> interval;
        int have = 0;
        for (const auto& [i, count] : mp) {
            if (interval.empty()) {
                interval.push_back(i);
            }
            have += count;
            if (have == 0) {
                interval.push_back(i);
                res.push_back(interval);
                interval.clear();
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Greedy

We want to merge all overlapping intervals so the result contains only **non-overlapping ranges**.

This solution uses a greedy idea with an auxiliary array:

- For every possible start point `start`, we record the **farthest end** of any interval that begins at `start`
- Then we scan from left to right, maintaining the farthest point we must still cover (`have`)

While scanning:

- if we see an interval starting at position `i`, we may need to extend our current merged interval’s end to include it
- once our scan index reaches the farthest required end, we can safely close the current merged interval

So the scan behaves like:

- “start a merged interval when we first see coverage”
- “keep extending its end while overlaps exist”
- “close it when we finish the coverage”

```cpp
class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        int max_val = 0;
        for (const auto& interval : intervals) {
            max_val = max(interval[0], max_val);
        }

        vector<int> mp(max_val + 1, 0);
        for (const auto& interval : intervals) {
            int start = interval[0];
            int end = interval[1];
            mp[start] = max(end + 1, mp[start]);
        }

        vector<vector<int>> res;
        int have = -1;
        int intervalStart = -1;
        for (int i = 0; i < mp.size(); i++) {
            if (mp[i] != 0) {
                if (intervalStart == -1) intervalStart = i;
                have = max(mp[i] - 1, have);
            }
            if (have == i) {
                res.push_back({intervalStart, have});
                have = -1;
                intervalStart = -1;
            }
        }

        if (intervalStart != -1) {
            res.push_back({intervalStart, have});
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n)$

> Where $n$ is the length of the array and $m$ is the maximum start value among all the intervals.

## Standalone solution file (`cpp/0056-merge-intervals.cpp` in the NeetCode repo)

```cpp
/*
    Given an array of intervals, merge all overlapping intervals
    Ex. intervals = [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]]

    Sort by earliest start time, merge overlapping intervals (take longer end time)

    Time: O(n log n)
    Space: O(n)
*/

class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        int n = intervals.size();
        if (n == 1) {
            return intervals;
        }
        
        sort(intervals.begin(), intervals.end(), [](const auto& a, const auto& b) {
           return a[0] < b[0]; 
        });
        
        vector<vector<int>> result;
        
        int i = 0;
        while (i < n - 1) {
            if (intervals[i][1] >= intervals[i+1][0]) {
                intervals[i+1][0] = intervals[i][0];
                intervals[i+1][1] = max(intervals[i][1], intervals[i+1][1]);
            } else {
                result.push_back(intervals[i]);
            }
            i++;
        }
        result.push_back(intervals[i]);
        
        return result;
    }
};
```
