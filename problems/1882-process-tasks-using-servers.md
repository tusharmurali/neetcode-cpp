# 1882. Process Tasks Using Servers

- **Difficulty:** Medium  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/process-tasks-using-servers/>  
- **NeetCode:** <https://neetcode.io/problems/process-tasks-using-servers>  
- **Video:** <https://www.youtube.com/watch?v=XKA22PecuMQ>  

[← Back to index](../INDEX.md)

## 1. Brute Force (Simulation)

We simulate the process step by step. For each task, we advance `time` to when the task becomes available, mark all servers that have finished as available, then pick the best available server (lowest weight, then lowest index). If no server is free, we wait until the earliest one finishes. This direct simulation is easy to understand but slow due to repeated linear scans.

```cpp
class Solution {
public:
    vector<int> assignTasks(vector<int>& servers, vector<int>& tasks) {
        int n = servers.size(), m = tasks.size();
        vector<bool> available(n, true);
        vector<int> finishTime(n, 0), res(m);
        int time = 0;

        for (int t = 0; t < m; t++) {
            time = max(time, t);

            for (int i = 0; i < n; i++) {
                if (finishTime[i] <= time) {
                    available[i] = true;
                }
            }

            if (!any_of(available.begin(), available.end(), [](bool v) { return v; })) {
                time = *min_element(finishTime.begin(), finishTime.end());
                for (int i = 0; i < n; i++) {
                    if (finishTime[i] <= time) {
                        available[i] = true;
                    }
                }
            }

            int minIdx = -1;
            for (int i = 0; i < n; i++) {
                if (available[i] && (minIdx == -1 || servers[i] < servers[minIdx] ||
                    (servers[i] == servers[minIdx] && i < minIdx))) {
                    minIdx = i;
                }
            }

            res[t] = minIdx;
            available[minIdx] = false;
            finishTime[minIdx] = time + tasks[t];
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity:
    - $O(n)$ extra space.
    - $O(m)$ space for the output array.

> Where $m$ is the number of tasks and $n$ is the number of servers.

## 2. Two Min-Heaps - I

Using two heaps makes server selection efficient. One heap holds available servers ordered by (`weight`, `index`), and another holds unavailable servers ordered by their finish `time`. When processing a task, we move servers from unavailable to available if their `time` has passed, then pop the best server from the available heap.

```cpp
class Solution {
public:
    vector<int> assignTasks(vector<int>& servers, vector<int>& tasks) {
        int n = servers.size(), m = tasks.size();
        vector<int> res(m);

        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> available;
        priority_queue<vector<int>, vector<vector<int>>, greater<>> unavailable;

        for (int i = 0; i < n; i++) {
            available.emplace(servers[i], i);
        }

        int time = 0;
        for (int i = 0; i < m; i++) {
            time = max(time, i);

            if (available.empty()) {
                time = unavailable.top()[0];
            }

            while (!unavailable.empty() && unavailable.top()[0] <= time) {
                auto server = unavailable.top(); unavailable.pop();
                available.emplace(server[1], server[2]);
            }

            auto [weight, index] = available.top(); available.pop();
            res[i] = index;
            unavailable.push({time + tasks[i], weight, index});
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O((n + m) \log n)$
- Space complexity:
    - $O(n)$ extra space.
    - $O(m)$ space for the output array.

> Where $m$ is the number of tasks and $n$ is the number of servers.

## 3. Two Min-Heaps - II

This is a variation of the two-heap approach with slightly different state tracking. Instead of storing finish `time` separately, we embed the last known free `time` within the available heap entries. When transferring servers between heaps, we update this `time` accordingly. The logic remains the same: efficiently pick the best available server using heaps.

```cpp
class Solution {
public:
    vector<int> assignTasks(vector<int>& servers, vector<int>& tasks) {
        int n = servers.size(), m = tasks.size();
        vector<int> res(m);

        priority_queue<array<int, 3>, vector<array<int, 3>>, greater<>> available;
        priority_queue<array<int, 3>, vector<array<int, 3>>, greater<>> unavailable;

        for (int i = 0; i < n; ++i) {
            available.push({servers[i], i, 0});
        }

        for (int i = 0; i < m; ++i) {
            while (!unavailable.empty() && (unavailable.top()[0] <= i ||
                   available.empty())) {
                auto [timeFree, weight, index] = unavailable.top();
                unavailable.pop();
                available.push({weight, index, timeFree});
            }

            auto [weight, index, timeFree] = available.top();
            available.pop();
            res[i] = index;
            unavailable.push({max(timeFree, i) + tasks[i], weight, index});
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O((n + m) \log n)$
- Space complexity:
    - $O(n)$ extra space.
    - $O(m)$ space for the output array.

> Where $m$ is the number of tasks and $n$ is the number of servers.
