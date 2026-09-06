# 1094. Car Pooling

- **Difficulty:** Medium  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/car-pooling/>  
- **NeetCode:** <https://neetcode.io/problems/car-pooling>  
- **Video:** <https://www.youtube.com/watch?v=08sn_w4LWEE>  

[← Back to index](../INDEX.md)

## 1. Brute Force

At each pickup location, we need to know how many passengers are currently in the car. We can sort trips by their start location and for each trip, check all previous trips that have not yet dropped off their passengers. If the total exceeds capacity at any point, carpooling is not possible.

```cpp
class Solution {
public:
    bool carPooling(vector<vector<int>>& trips, int capacity) {
        sort(trips.begin(), trips.end(), [](const vector<int>& a, const vector<int>& b) {
            return a[1] < b[1];
        });

        for (int i = 0; i < trips.size(); i++) {
            int curPass = trips[i][0];
            for (int j = 0; j < i; j++) {
                if (trips[j][2] > trips[i][1]) {
                    curPass += trips[j][0];
                }
            }
            if (curPass > capacity) {
                return false;
            }
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Min-Heap

When we process trips in order of pickup time, we only care about trips whose passengers are still in the car. A min-heap ordered by drop-off time lets us efficiently remove all trips whose passengers have already been dropped off before the current pickup. This way, we maintain a running count of current passengers.

```cpp
class Solution {
public:
    bool carPooling(vector<vector<int>>& trips, int capacity) {
        sort(trips.begin(), trips.end(), [](const vector<int>& a, const vector<int>& b) {
            return a[1] < b[1];
        });

        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> minHeap; // [end, numPassengers]
        int curPass = 0;

        for (const auto& trip : trips) {
            int numPass = trip[0], start = trip[1], end = trip[2];

            while (!minHeap.empty() && minHeap.top().first <= start) {
                curPass -= minHeap.top().second;
                minHeap.pop();
            }

            curPass += numPass;
            if (curPass > capacity) {
                return false;
            }

            minHeap.emplace(end, numPass);
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Line Sweep - I

Think of each trip as two events: passengers getting on at the start and passengers getting off at the end. By treating pickups as positive changes and drop-offs as negative changes, we can process all events in sorted order. At any point, if the cumulative passenger count exceeds capacity, the answer is false.

```cpp
class Solution {
public:
    bool carPooling(vector<vector<int>>& trips, int capacity) {
        vector<pair<int, int>> points;
        for (const auto& trip : trips) {
            int passengers = trip[0], start = trip[1], end = trip[2];
            points.emplace_back(start, passengers);
            points.emplace_back(end, -passengers);
        }

        sort(points.begin(), points.end(), [](const pair<int, int>& a, const pair<int, int>& b) {
            return a.first == b.first ? a.second < b.second : a.first < b.first;
        });

        int curPass = 0;
        for (const auto& point : points) {
            curPass += point.second;
            if (curPass > capacity) {
                return false;
            }
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Line Sweep - II

Instead of sorting events, we can use an array where each index represents a location on the route. We record passenger changes at each location: add passengers at pickup points and subtract at drop-off points. A single pass through this array gives us the passenger count at each location.

```cpp
class Solution {
public:
    bool carPooling(vector<vector<int>>& trips, int capacity) {
        int L = INT_MAX, R = INT_MIN;
        for (const auto& trip : trips) {
            L = min(L, trip[1]);
            R = max(R, trip[2]);
        }

        int N = R - L + 1;
        vector<int> passChange(N + 1, 0);
        for (const auto& trip : trips) {
            passChange[trip[1] - L] += trip[0];
            passChange[trip[2] - L] -= trip[0];
        }

        int curPass = 0;
        for (int change : passChange) {
            curPass += change;
            if (curPass > capacity) {
                return false;
            }
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n + N)$
- Space complexity: $O(N)$

> Where $n$ is the size of the array $trips$ and $N$ is the difference between the rightmost location and the leftmost location.

## Standalone solution file (`cpp/1094-car-pooling.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    bool carPooling(vector<vector<int>>& trips, int capacity) {
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> minHeap;
        for (int i=0; i<trips.size(); ++i) {
            int numPassengers=trips[i][0], from=trips[i][1], to=trips[i][2];
            minHeap.push({from, numPassengers});
            minHeap.push({to, -numPassengers});
        }

        int currCapacity = 0;
        while (!minHeap.empty()) {
            int currTime = minHeap.top().first;
            while (!minHeap.empty() and minHeap.top().first == currTime) {
                auto [time, numPassengers] = minHeap.top();
                minHeap.pop();
                currCapacity += numPassengers;
            }
            if (currCapacity > capacity)
                return false;
        }

        return true;
    }
};
```
