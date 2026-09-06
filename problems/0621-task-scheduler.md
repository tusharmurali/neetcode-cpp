# 621. Task Scheduler

- **Difficulty:** Medium  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/task-scheduler/>  
- **NeetCode:** <https://neetcode.io/problems/task-scheduling>  
- **Video:** <https://www.youtube.com/watch?v=s8p8ukTyA2I>  
- **Video approach:** 2. Max-Heap  

[← Back to index](../INDEX.md)

## 1. Brute Force

We simulate the CPU one time unit at a time.
At every step, we look at all remaining tasks and pick:

- A task that **is not in the cooldown** (not executed in the last `n` time units),
- Among those, the one with the **highest remaining count**.

If no such task is available, the CPU **idles** for that time unit.
We repeat this until all tasks are finished.
This is a direct, brute-force simulation: very easy to understand, but not efficient.

```cpp
class Solution {
public:
    int leastInterval(vector<char>& tasks, int n) {
        vector<int> count(26, 0);
        for (char task : tasks) {
            count[task - 'A']++;
        }

        vector<pair<int, int>> arr;
        for (int i = 0; i < 26; i++) {
            if (count[i] > 0) {
                arr.emplace_back(count[i], i);
            }
        }

        int time = 0;
        vector<int> processed;
        while (!arr.empty()) {
            int maxi = -1;
            for (int i = 0; i < arr.size(); i++) {
                bool ok = true;
                for (int j = max(0, time - n); j < time; j++) {
                    if (j < processed.size() && processed[j] == arr[i].second) {
                        ok = false;
                        break;
                    }
                }
                if (!ok) continue;
                if (maxi == -1 || arr[maxi].first < arr[i].first) {
                    maxi = i;
                }
            }

            time++;
            int cur = -1;
            if (maxi != -1) {
                cur = arr[maxi].second;
                arr[maxi].first--;
                if (arr[maxi].first == 0) {
                    arr.erase(arr.begin() + maxi);
                }
            }
            processed.push_back(cur);
        }
        return time;
    }
};
```

**Complexity**

- Time complexity: $O(t * n)$
- Space complexity: $O(t)$

> Where $t$ is the time to process given tasks and $n$ is the cooldown time.

## 2. Max-Heap ▶ video

We always want to run the task that still has the **most remaining occurrences**, because those are the hardest to fit into the schedule (they need more slots with cooldown gaps).

So we:

- Keep a **max-heap** of tasks by their remaining count (most frequent on top).
- At each time unit, we take the **most frequent available task** and run it.
- After running a task, it goes into a **cooldown queue** with the time when it will be available again (current time + `n`).
- When a task’s cooldown finishes, we push it back into the heap so it can be scheduled again.
- If the heap is empty but some tasks are still in cooldown, we can **jump the current time forward** to the next time when a task becomes available.

This way we always use the CPU as efficiently as possible while respecting the cooldown.

```cpp
class Solution {
public:
    int leastInterval(vector<char>& tasks, int n) {
        vector<int> count(26, 0);
        for (char task : tasks) {
            count[task - 'A']++;
        }

        priority_queue<int> maxHeap;
        for (int cnt : count) {
            if (cnt > 0) {
                maxHeap.push(cnt);
            }
        }

        int time = 0;
        queue<pair<int, int>> q;
        while (!maxHeap.empty() || !q.empty()) {
            time++;

            if (maxHeap.empty()) {
                time = q.front().second;
            } else {
                int cnt = maxHeap.top() - 1;
                maxHeap.pop();
                if (cnt > 0) {
                    q.push({cnt, time + n});
                }
            }

            if (!q.empty() && q.front().second == time) {
                maxHeap.push(q.front().first);
                q.pop();
            }
        }

        return time;
    }
};
```

**Complexity**

- Time complexity: $O(m)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

> Where $m$ is the number of tasks.

## 3. Greedy

Instead of simulating the whole schedule, we can think in terms of **slots**:

- Let `maxf` be the **maximum frequency** of any task (e.g., if `A` appears 5 times, `B` 3 times, then `maxf = 5`).
- Imagine placing all copies of the most frequent task in a row:

    `A _ _ A _ _ A _ _ A _ _ A`

- There are `maxf - 1` **gaps** between these most frequent tasks.
- Each gap must be at least size `n` to satisfy the cooldown.
- So initial **idle slots needed** = `(maxf - 1) * n`.

Now, we try to **fill these idle slots** using other tasks:

- For each other task with count `c`, it can fill up to `min(c, maxf - 1)` of these gaps (because there are only `maxf - 1` gaps).
- Subtract this filled amount from the idle slots.
- After considering all tasks, if `idle` is still positive, we must add those idle slots to the total time.
- If `idle` becomes zero or negative, it means all gaps are already filled (or over-filled) by tasks, so no extra idle time is needed.

Finally:

- Total time = `len(tasks)` (each task takes 1 unit) + `max(0, idle)` (extra gaps we couldn’t fill).

```cpp
class Solution {
public:
    int leastInterval(vector<char>& tasks, int n) {
        vector<int> count(26, 0);
        for (char task : tasks) {
            count[task - 'A']++;
        }

        sort(count.begin(), count.end());
        int maxf = count[25];
        int idle = (maxf - 1) * n;

        for (int i = 24; i >= 0; i--) {
            idle -= min(maxf - 1, count[i]);
        }
        return max(0, idle) + tasks.size();
    }
};
```

**Complexity**

- Time complexity: $O(m)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

> Where $m$ is the number of tasks.

## 4. Math

The task with the highest frequency determines the minimum needed structure of the schedule.
If a task appears `maxf` times, these copies must be at least `n` units apart.
This creates `(maxf - 1)` "gaps", and each gap must have a length of `(n + 1)` slots (the task itself + n cooldowns).

If multiple tasks share this maximum frequency (`maxCount` tasks), they all occupy the final row of the structure.

So the minimal time required to schedule all tasks without violating cooldown rules is: `time = (maxf - 1) * (n + 1) + maxCount`

However, if the number of tasks is larger than this calculated time, then simply performing all tasks takes longer.
Thus, the actual answer must be: `max(len(tasks), time)`

```cpp
class Solution {
public:
    int leastInterval(vector<char>& tasks, int n) {
        vector<int> count(26, 0);
        for (char task : tasks) {
            count[task - 'A']++;
        }

        int maxf = *max_element(count.begin(), count.end());
        int maxCount = 0;
        for (int i : count) {
            if (i == maxf) {
                maxCount++;
            }
        }

        int time = (maxf - 1) * (n + 1) + maxCount;
        return max((int)tasks.size(), time);
    }
};
```

**Complexity**

- Time complexity: $O(m)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

> Where $m$ is the number of tasks.

## Standalone solution file (`cpp/0621-task-scheduler.cpp` in the NeetCode repo)

```cpp
/*
    Given array of tasks & cooldown b/w same tasks, return least # of units of time
    Ex. tasks = ["A","A","A","B","B","B"] n = 2 -> 8 (A->B->idle->A->B->idle->A->B)

    Key is to determine # of idles, greedy: always arrange task w/ most freq first
    3A, 2B, 1C -> A??A??A -> AB?AB?A -> ABCAB#A, since A most freq, needs most idles

    Time: O(n)
    Space: O(1)
*/
/*
class Solution {
public:
    int leastInterval(vector<char>& tasks, int n) {
        vector<int> counter(26);
        
        int maxCount = 0;
        int maxCountFrequency = 0;
        
        for (int i = 0; i < tasks.size(); i++) {
            counter[tasks[i] - 'A']++;
            int currCount = counter[tasks[i] - 'A'];
            
            if (maxCount == currCount) {
                maxCountFrequency++;
            } else if (maxCount < currCount) {
                maxCount = currCount;
                maxCountFrequency = 1;
            }
        }
        
        int partCount = maxCount - 1;
        int partLength = n - (maxCountFrequency - 1);
        int emptySlots = partCount * partLength;
        int availableTasks = tasks.size() - maxCount * maxCountFrequency;
        int idles = max(0, emptySlots - availableTasks);
        
        return tasks.size() + idles;
    }
};
*/

// Time O(n * cooldown)
class Solution {
public:
    int leastInterval(vector<char>& tasks, int n) {
        priority_queue<int> pq;
        queue<vector<int>> q;
        vector<int> counter(26);

        for (int i = 0; i < tasks.size(); ++i)
            ++counter[tasks[i] - 'A'];
        for (int i = 0; i < 26; ++i){
            if (counter[i])
                pq.push(counter[i]);
        }

        int time = 0;
        while (!q.empty() || !pq.empty()){
            ++time;
            if (!pq.empty()){
                if (pq.top() - 1)
                    q.push({pq.top() - 1, time + n});
                pq.pop();
            }
            if (!q.empty() && q.front()[1] == time){
                pq.push(q.front()[0]);
                q.pop();
            }
        }
        return time;
    }
};
```
