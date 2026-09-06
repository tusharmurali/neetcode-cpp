# 253. Meeting Rooms II

- **Difficulty:** Medium  
- **Pattern:** Intervals  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/meeting-rooms-ii/>  
- **NeetCode:** <https://neetcode.io/problems/meeting-schedule-ii>  
- **Video:** <https://www.youtube.com/watch?v=FdzJmTCVyJU>  

[← Back to index](../INDEX.md)

## 1. Min Heap

We want to find the **minimum number of meeting rooms** required so that no meetings overlap.

A useful way to think about this is:

- each meeting needs a room from its start time to its end time
- if a meeting starts **after or at the same time** another meeting ends, they can share the **same room**
- otherwise, we need a **new room**

To efficiently track room availability, we use a **min heap**:

- the heap stores the **end times** of meetings currently occupying rooms
- the smallest end time is always at the top, representing the room that frees up the earliest

As we process meetings in order of start time:

- if the earliest-ending meeting finishes before the current one starts, we can reuse that room
- otherwise, we must allocate a new room

The maximum size the heap reaches is the number of rooms needed.

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
    int minMeetingRooms(vector<Interval>& intervals) {
        sort(intervals.begin(), intervals.end(), [](auto& a, auto& b) {
            return a.start < b.start;
        });
        priority_queue<int, vector<int>, greater<int>> minHeap;
        for (const auto& interval : intervals) {
            if (!minHeap.empty() && minHeap.top() <= interval.start) {
                minHeap.pop();
            }
            minHeap.push(interval.end);
        }
        return minHeap.size();
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Sweep Line Algorithm

We want to find the **minimum number of meeting rooms** needed so that no meetings overlap.

Instead of assigning rooms directly, we can look at the problem as a **timeline**:

- every meeting **starts** at a certain time
- every meeting **ends** at a certain time

At any point in time, the number of rooms required is simply:

> the number of meetings happening at that moment

The sweep line technique helps us track how this number changes over time by processing all start and end events in order.

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
    int minMeetingRooms(vector<Interval>& intervals) {
        map<int, int> mp;
        for (auto& i : intervals) {
            mp[i.start]++;
            mp[i.end]--;
        }
        int prev = 0, res = 0;
        for (auto& [key, value] : mp) {
            prev += value;
            res = max(res, prev);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Two Pointers

We want to find the **minimum number of meeting rooms** required so that no meetings overlap.

Instead of tracking whole intervals, we can separate the problem into two simpler timelines:

- one list of **all start times**
- one list of **all end times**

If we process these timelines in order:

- whenever a meeting **starts before another one ends**, we need a **new room**
- whenever a meeting **ends before or at the same time another starts**, a room becomes **free**

By moving two pointers over the sorted start and end times, we can track how many meetings are happening at the same time.

The maximum number of simultaneous meetings at any moment is exactly the number of rooms we need.

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
    int minMeetingRooms(vector<Interval>& intervals) {
        vector<int> start, end;

        for (const auto& i : intervals) {
            start.push_back(i.start);
            end.push_back(i.end);
        }

        sort(start.begin(), start.end());
        sort(end.begin(), end.end());

        int res = 0, count = 0, s = 0, e = 0;
        while (s < intervals.size()) {
            if (start[s] < end[e]) {
                s++;
                count++;
            } else {
                e++;
                count--;
            }
            res = max(res, count);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Greedy

We want to find the **minimum number of meeting rooms** required so that no meetings overlap.

Instead of thinking in terms of rooms directly, we can think in terms of **events on a timeline**:

- when a meeting **starts**, we need **one more room**
- when a meeting **ends**, one room is **freed**

So the problem reduces to:

> What is the **maximum number of meetings happening at the same time**?

If we track how the number of active meetings changes over time, the maximum value we ever reach is exactly the number of rooms we need.

This greedy approach works by:

- converting each meeting into two events (start and end)
- sorting all events by time
- sweeping from left to right while counting active meetings

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
    int minMeetingRooms(vector<Interval>& intervals) {
        vector<pair<int, int>> time;
        for (const auto& i : intervals) {
            time.push_back({i.start, 1});
            time.push_back({i.end, -1});
        }

        sort(time.begin(), time.end(), [](auto& a, auto& b) {
            return a.first == b.first ? a.second < b.second : a.first < b.first;
        });

        int res = 0, count = 0;
        for (const auto& t : time) {
            count += t.second;
            res = max(res, count);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0253-meeting-rooms-ii.cpp` in the NeetCode repo)

```cpp
/*
    Given array of time intervals, determine min # of meeting rooms required
    Ex. intervals = [[0,30],[5,10],[15,20]] -> 2

    Min heap for earliest end times, most overlap will be heap size

    Time: O(n log n)
    Space: O(n)
*/

class Solution {
public:
    int minMeetingRooms(vector<vector<int>>& intervals) {
        // sort intervals by start time
        sort(intervals.begin(), intervals.end());
        
        // min heap to track min end time of merged intervals
        priority_queue<int, vector<int>, greater<int>> pq;
        pq.push(intervals[0][1]);
        
        for (int i = 1; i < intervals.size(); i++) {
            // compare curr start w/ earliest end time, if no overlap then pop
            if (intervals[i][0] >= pq.top()) {
                pq.pop();
            }
            // add new room (will replace/be same size if above was true)
            pq.push(intervals[i][1]);
        }
        
        return pq.size();
    }
};
```
