# 2251. Number of Flowers in Full Bloom

- **Difficulty:** Hard  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-flowers-in-full-bloom/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-flowers-in-full-bloom>  
- **Video:** <https://www.youtube.com/watch?v=zY3Uty9IwvY>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to check each person's arrival time against every flower's bloom period. A flower is visible to a person if the arrival time falls within the flower's start and end times (inclusive). We count all such flowers for each person.

```cpp
class Solution {
public:
    vector<int> fullBloomFlowers(vector<vector<int>>& flowers, vector<int>& people) {
        int m = people.size();
        vector<int> res(m);

        for (int i = 0; i < m; i++) {
            int count = 0;
            for (auto& flower : flowers) {
                if (flower[0] <= people[i] && people[i] <= flower[1]) {
                    count++;
                }
            }
            res[i] = count;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m)$ for the output array.

> Where $n$ is the size of the array $flowers$, and $m$ is the size of the array $people$.

## 2. Two Min-Heaps

Instead of checking every flower for every person, we can process people in sorted order of their arrival times. By using two min-heaps (one for start times, one for end times), we can efficiently track how many flowers have started blooming and how many have finished. The difference gives us the count of flowers currently in bloom.

```cpp
class Solution {
public:
    vector<int> fullBloomFlowers(vector<vector<int>>& flowers, vector<int>& people) {
        int m = people.size();
        vector<int> res(m);

        vector<pair<int, int>> sortedPeople;
        for (int i = 0; i < m; i++) {
            sortedPeople.push_back({people[i], i});
        }
        sort(sortedPeople.begin(), sortedPeople.end());

        priority_queue<int, vector<int>, greater<int>> startHeap, endHeap;
        for (const auto& f : flowers) {
            startHeap.push(f[0]);
            endHeap.push(f[1]);
        }

        int count = 0;
        for (const auto& person : sortedPeople) {
            int p = person.first, index = person.second;

            while (!startHeap.empty() && startHeap.top() <= p) {
                startHeap.pop();
                count++;
            }
            while (!endHeap.empty() && endHeap.top() < p) {
                endHeap.pop();
                count--;
            }

            res[index] = count;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m \log m + n \log n)$
- Space complexity: $O(m + n)$

> Where $n$ is the size of the array $flowers$, and $m$ is the size of the array $people$.

## 3. Min-Heap

We can optimize the two-heap approach by sorting the flowers by start time and using only one heap for end times. As we process each person, we push end times of flowers that have started blooming onto the heap. Then we remove flowers that have finished blooming. The heap size represents the current bloom count.

```cpp
class Solution {
public:
    vector<int> fullBloomFlowers(vector<vector<int>>& flowers, vector<int>& people) {
        int m = people.size();
        vector<int> res(m);
        vector<pair<int, int>> indexedPeople;

        for (int i = 0; i < m; i++) {
            indexedPeople.emplace_back(people[i], i);
        }
        sort(indexedPeople.begin(), indexedPeople.end());
        sort(flowers.begin(), flowers.end());

        priority_queue<int, vector<int>, greater<int>> endHeap;
        int j = 0, n = flowers.size();

        for (auto [p, index] : indexedPeople) {
            while (j < n && flowers[j][0] <= p) {
                endHeap.push(flowers[j][1]);
                j++;
            }
            while (!endHeap.empty() && endHeap.top() < p) {
                endHeap.pop();
            }
            res[index] = endHeap.size();
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m \log m + n \log n)$
- Space complexity: $O(m + n)$

> Where $n$ is the size of the array $flowers$, and $m$ is the size of the array $people$.

## 4. Sorting + Two Pointers

Rather than using heaps, we can separate the start and end times into two sorted arrays. By sorting people by arrival time and using two pointers to traverse the start and end arrays, we can efficiently count how many flowers have started minus how many have ended at each person's arrival time.

```cpp
class Solution {
public:
    vector<int> fullBloomFlowers(vector<vector<int>>& flowers, vector<int>& people) {
        int m = people.size();
        vector<int> res(m), start, end;
        for (auto& f : flowers) {
            start.push_back(f[0]);
            end.push_back(f[1]);
        }

        sort(start.begin(), start.end());
        sort(end.begin(), end.end());

        int count = 0, i = 0, j = 0;
        vector<pair<int, int>> peopleIndex;
        for (int k = 0; k < m; k++) {
            peopleIndex.emplace_back(people[k], k);
        }
        sort(peopleIndex.begin(), peopleIndex.end());

        for (auto& [p, index] : peopleIndex) {
            while (i < start.size() && start[i] <= p) {
                count++;
                i++;
            }
            while (j < end.size() && end[j] < p) {
                count--;
                j++;
            }
            res[index] = count;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m \log m + n \log n)$
- Space complexity: $O(m + n)$

> Where $n$ is the size of the array $flowers$, and $m$ is the size of the array $people$.

## 5. Line Sweep

The line sweep technique treats flower blooms as events on a timeline. Each flower creates two events: a `+1` at its start time and a `-1` at one past its end time. By processing these events in order alongside sorted queries, we maintain a running `count` of blooming flowers at any point in time.

```cpp
class Solution {
public:
    vector<int> fullBloomFlowers(vector<vector<int>>& flowers, vector<int>& people) {
        vector<pair<int, int>> events;
        for (auto& f : flowers) {
            events.emplace_back(f[0], 1);
            events.emplace_back(f[1] + 1, -1);
        }

        sort(events.begin(), events.end());
        vector<pair<int, int>> queries;
        for (int i = 0; i < people.size(); i++) {
            queries.emplace_back(people[i], i);
        }

        sort(queries.begin(), queries.end());
        vector<int> res(people.size());
        int count = 0, j = 0;

        for (auto& [time, index] : queries) {
            while (j < events.size() && events[j].first <= time) {
                count += events[j++].second;
            }
            res[index] = count;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m \log m + n \log n)$
- Space complexity: $O(m + n)$

> Where $n$ is the size of the array $flowers$, and $m$ is the size of the array $people$.
