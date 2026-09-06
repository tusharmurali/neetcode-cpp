# 1834. Single Threaded CPU

- **Difficulty:** Medium  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/single-threaded-cpu/>  
- **NeetCode:** <https://neetcode.io/problems/single-threaded-cpu>  
- **Video:** <https://www.youtube.com/watch?v=RR1n-d4oYqE>  
- **Video approach:** 2. Sorting + Min-Heap  

[← Back to index](../INDEX.md)

## 1. Two Min-Heaps

A single-threaded CPU processes one task at a time. At any moment, we need to know which tasks are available (enqueue time has passed) and pick the one with the shortest processing time. A min-heap efficiently gives us the task with minimum processing time among available tasks. We use two heaps: one for pending tasks (sorted by enqueue time) and one for available tasks (sorted by processing time, then by index).

```cpp
class Solution {
public:
    vector<int> getOrder(vector<vector<int>>& tasks) {
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> available;
        priority_queue<array<int, 3>, vector<array<int, 3>>, greater<>> pending;

        int n = tasks.size();
        for (int i = 0; i < n; ++i) {
            pending.push({tasks[i][0], tasks[i][1], i});
        }

        vector<int> res;
        long long time = 0;
        while (!pending.empty() || !available.empty()) {
            while (!pending.empty() && pending.top()[0] <= time) {
                auto [enqueueTime, processTime, index] = pending.top();
                pending.pop();
                available.push({processTime, index});
            }

            if (available.empty()) {
                time = pending.top()[0];
                continue;
            }

            auto [processTime, index] = available.top();
            available.pop();
            time += processTime;
            res.push_back(index);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Sorting + Min-Heap ▶ video

Instead of using two heaps, we can sort the tasks by enqueue time first. This allows us to iterate through tasks in order and add them to the available heap as they become ready. We only need one heap for available tasks, simplifying the implementation while maintaining the same logic.

```cpp
class Solution {
public:
    vector<int> getOrder(vector<vector<int>>& tasks) {
        int n = tasks.size();
        for (int i = 0; i < n; ++i) {
            tasks[i].push_back(i);
        }
        sort(tasks.begin(), tasks.end());

        vector<int> res;
        priority_queue<array<int, 2>, vector<array<int, 2>>, greater<>> minHeap;

        int i = 0;
        long long time = tasks[0][0];
        while (!minHeap.empty() || i < n) {
            while (i < n && time >= tasks[i][0]) {
                minHeap.push({tasks[i][1], tasks[i][2]});
                i++;
            }
            if (minHeap.empty()) {
                time = tasks[i][0];
            } else {
                auto [procTime, index] = minHeap.top();
                minHeap.pop();
                time += procTime;
                res.push_back(index);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Sorting + Min-Heap (Optimal)

This solution optimizes memory by not modifying the original tasks array. Instead of copying task data, we sort an array of indices by enqueue time. The heap stores only indices and uses the original tasks array for comparisons. This approach is more memory efficient while maintaining the same time complexity.

```cpp
// C++ Solution
class Solution {
public:
    vector<int> getOrder(vector<vector<int>>& tasks) {
        int n = tasks.size();
        vector<int> indices(n);
        iota(indices.begin(), indices.end(), 0);

        sort(indices.begin(), indices.end(), [&](int a, int b) {
            return tasks[a][0] < tasks[b][0] ||
                   (tasks[a][0] == tasks[b][0] && a < b);
        });

        auto comp = [&](int a, int b) {
            return tasks[a][1] > tasks[b][1] ||
                   (tasks[a][1] == tasks[b][1] && a > b);
        };
        priority_queue<int, vector<int>, decltype(comp)> minHeap(comp);

        vector<int> result;
        long long time = 0;
        int i = 0;

        while (!minHeap.empty() || i < n) {
            while (i < n && tasks[indices[i]][0] <= time) {
                minHeap.push(indices[i]);
                i++;
            }

            if (minHeap.empty()) {
                time = tasks[indices[i]][0];
            } else {
                int nextIndex = minHeap.top();
                minHeap.pop();
                time += tasks[nextIndex][1];
                result.push_back(nextIndex);
            }
        }

        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$
