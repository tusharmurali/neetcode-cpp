# 252. Meeting Rooms

- **Difficulty:** Easy  
- **Pattern:** Intervals  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/meeting-rooms/>  
- **NeetCode:** <https://neetcode.io/problems/meeting-schedule>  
- **Video:** <https://www.youtube.com/watch?v=PaJxqZVPhbg>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We want to check whether a person can attend **all meetings without any overlap**.

Two meetings overlap if they share **any common time**.
For two intervals `A` and `B`, this happens when:

- the earlier ending time is **greater** than the later starting time

In a brute force approach, we simply:

- compare **every pair of meetings**
- if **any pair overlaps**, it is impossible to attend all meetings

This approach is very straightforward and easy to understand, making it ideal as a starting solution.

```cpp
/**
 * Definition of Interval:
 * class Interval {
 * public:
 *     int start, end;
 *     Interval(int start, int end) {
 *         this->start = start;
 *         this->end = end;
 *     }
 * }
 */

class Solution {
public:
    bool canAttendMeetings(vector<Interval>& intervals) {
        int n = intervals.size();
        for (int i = 0; i < n; i++) {
            Interval& A =intervals[i];
            for (int j = i + 1; j < n; j++) {
                Interval& B =intervals[j];
                if (min(A.end, B.end) > max(A.start, B.start)) {
                    return false;
                }
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Sorting

We want to determine whether a person can attend **all meetings without any overlaps**.

A key observation is:

- if meetings are sorted by their **start time**, then
- we only need to check **adjacent meetings** for overlap

Why this works:

- if two meetings overlap, they must appear next to each other after sorting by start time
- there is no need to compare every pair

So by sorting once and doing a single pass, we can efficiently detect any conflict.

```cpp
/**
 * Definition of Interval:
 * class Interval {
 * public:
 *     int start, end;
 *     Interval(int start, int end) {
 *         this->start = start;
 *         this->end = end;
 *     }
 * }
 */

class Solution {
public:
    bool canAttendMeetings(vector<Interval>& intervals) {
        sort(intervals.begin(), intervals.end(), [](auto& x, auto& y) {
            return x.start < y.start;
        });
        for (int i = 1; i < intervals.size(); ++i) {
            if (intervals[i].start < intervals[i - 1].end) {
                return false;
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## Standalone solution file (`cpp/0252-meeting-rooms.cpp` in the NeetCode repo)

```cpp
/*
    Given array of time intervals, determine if can attend all meetings
    Ex. intervals = [[0,30],[5,10],[15,20]] -> false

    Sort by start time, check adj meetings, if overlap return false

    Time: O(n log n)
    Space: O(1)
*/

class Solution {
public:
    bool canAttendMeetings(vector<vector<int>>& intervals) {
        if (intervals.empty()) {
            return true;
        }
        
        sort(intervals.begin(), intervals.end());
        for (int i = 0; i < intervals.size() - 1; i++) {
            if (intervals[i][1] > intervals[i + 1][0]) {
                return false;
            }
        }
        return true;
    }
};
```
