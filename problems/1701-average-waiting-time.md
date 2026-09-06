# 1701. Average Waiting Time

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/average-waiting-time/>  
- **NeetCode:** <https://neetcode.io/problems/average-waiting-time>  
- **Video:** <https://www.youtube.com/watch?v=2fN7uIgCIBA>  

[← Back to index](../INDEX.md)

## 1. Simulation - I

We simulate the chef serving customers one by one. The chef can only start a new order when they finish the previous one. If a customer arrives while the chef is busy, they wait. The waiting time for each customer is the time from arrival until their order is complete. We track the current time and accumulate total waiting time.

```cpp
class Solution {
public:
    double averageWaitingTime(vector<vector<int>>& customers) {
        long long t = 0, total = 0;

        for (auto& c : customers) {
            int arrival = c[0], order = c[1];
            if (t > arrival) {
                total += t - arrival;
            } else {
                t = arrival;
            }
            total += order;
            t += order;
        }

        return (double) total / customers.size();
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Simulation - II

This is a more concise version of the simulation. The key observation is that the chef starts cooking at whichever is later: their current finish time or the customer's arrival. The finish time becomes `max(t, arrival) + order`. The customer's waiting time is simply `finish_time - arrival`. This formula captures both cases (chef idle or busy) in one expression.

```cpp
class Solution {
public:
    double averageWaitingTime(vector<vector<int>>& customers) {
        long long t = 0, total = 0;

        for (auto& c : customers) {
            int arrival = c[0], order = c[1];
            t = max(t, (long long)arrival) + order;
            total += t - arrival;
        }

        return (double) total / customers.size();
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
