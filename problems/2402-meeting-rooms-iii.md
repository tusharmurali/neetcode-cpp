# 2402. Meeting Rooms III

- **Difficulty:** Hard  
- **Pattern:** Intervals  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/meeting-rooms-iii/>  
- **NeetCode:** <https://neetcode.io/problems/meeting-rooms-iii>  
- **Video:** <https://www.youtube.com/watch?v=2VLwjvODQbA>  

[← Back to index](../INDEX.md)

## 1. Sorting + Brute Force

Meetings must be processed in order of their start times. For each meeting, we check rooms in order from `0` to `n - 1`. If a room is free by the meeting's start time, we assign the meeting there. Otherwise, we find the room that becomes free earliest and delay the meeting until that room is available. We track how many meetings each room hosts and return the room with the most meetings, breaking ties by smallest room number.

```cpp
class Solution {
public:
    int mostBooked(int n, vector<vector<int>>& meetings) {
        sort(meetings.begin(), meetings.end());
        vector<long> rooms(n, 0); // end times of meetings in rooms
        vector<int> meetingCount(n, 0);

        for (const auto& meeting : meetings) {
            int start = meeting[0], end = meeting[1];
            int minRoom = 0;
            bool found = false;

            for (int i = 0; i < n; i++) {
                if (rooms[i] <= start) {
                    meetingCount[i]++;
                    rooms[i] = end;
                    found = true;
                    break;
                }
                if (rooms[minRoom] > rooms[i]) {
                    minRoom = i;
                }
            }

            if (found) continue;
            meetingCount[minRoom]++;
            rooms[minRoom] += end - start;
        }

        int maxIndex = 0;
        for (int i = 1; i < n; i++) {
            if (meetingCount[i] > meetingCount[maxIndex]) {
                maxIndex = i;
            }
        }
        return maxIndex;
    }
};
```

**Complexity**

- Time complexity: $O(m\log m + n * m)$
- Space complexity: $O(n)$

> Where $n$ is the number of rooms and $m$ is the number of meetings.

## 2. Two Min-Heaps

Scanning all rooms for each meeting is slow. Instead, we use two min-heaps: one for available rooms (ordered by room number) and one for rooms in use (ordered by end time, then room number). When a meeting starts, we first move all rooms whose meetings have ended back to the available heap. If available is empty, we pop the earliest-ending room, delay the meeting, and push that room back to available. Then we pop the smallest available room, assign the meeting, and push it to the used heap.

```cpp
class Solution {
public:
    int mostBooked(int n, vector<vector<int>>& meetings) {
        sort(meetings.begin(), meetings.end(), [](const vector<int>& a, const vector<int>& b) {
            return (long long)a[0] < (long long)b[0];
        });
        priority_queue<int, vector<int>, greater<int>> available;
        priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> used;
        for (int i = 0; i < n; i++) {
            available.push(i);
        }
        vector<int> count(n);

        for (const auto& meeting : meetings) {
            long long start = meeting[0];
            long long end = meeting[1];
            while (!used.empty() && used.top().first <= start) {
                int room = used.top().second;
                used.pop();
                available.push(room);
            }
            if (available.empty()) {
                auto current = used.top();
                used.pop();
                end = current.first + (end - start);
                available.push(current.second);
            }

            int room = available.top();
            available.pop();
            used.push({end, room});
            count[room]++;
        }

        int maxRoom = 0;
        for (int i = 1; i < n; i++) {
            if (count[i] > count[maxRoom]) {
                maxRoom = i;
            }
        }
        return maxRoom;
    }
};
```

**Complexity**

- Time complexity: $O(m\log m + m \log n)$
- Space complexity: $O(n)$

> Where $n$ is the number of rooms and $m$ is the number of meetings.

## 3. One Min-Heap

We can simplify to a single heap that tracks `(end_time, room)`. Initially all rooms have end time `0`. Before assigning a meeting, we update any rooms whose end time is before the meeting's start to have end time equal to the start (they become available). Then we pop the room with the smallest end time (and smallest room number on ties), assign the meeting, and push the room back with the new end time.

```cpp
class Solution {
public:
    int mostBooked(int n, vector<vector<int>>& meetings) {
        sort(meetings.begin(), meetings.end());
        priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> available;
        for (int i = 0; i < n; i++) {
            available.push({0, i});
        }
        vector<int> count(n);

        for (const auto& meeting : meetings) {
            int start = meeting[0], end = meeting[1];
            while (!available.empty() && available.top().first < start) {
                auto [end_time, room] = available.top();
                available.pop();
                available.push({start, room});
            }

            auto [end_time, room] = available.top();
            available.pop();
            available.push({end_time + (end - start), room});
            count[room]++;
        }

        return max_element(count.begin(), count.end()) - count.begin();
    }
};
```

**Complexity**

- Time complexity:
    - $O(m \log m + m \log n)$ time in average case.
    - $O(m \log m + m * n)$ time in worst case.
- Space complexity: $O(n)$

> Where $n$ is the number of rooms and $m$ is the number of meetings.
