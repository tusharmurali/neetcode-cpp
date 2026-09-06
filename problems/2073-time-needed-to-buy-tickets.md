# 2073. Time Needed to Buy Tickets

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/time-needed-to-buy-tickets/>  
- **NeetCode:** <https://neetcode.io/problems/time-needed-to-buy-tickets>  
- **Video:** <https://www.youtube.com/watch?v=cVmS9N6kf2Y>  

[← Back to index](../INDEX.md)

## 1. Queue

We can simulate the ticket buying process exactly as described. People stand in a queue, and each person buys one ticket at a time before going to the back of the line. We continue this process until the person at position `k` has bought all their tickets.

Using a queue data structure naturally models this behavior. We track each person's index and decrement their remaining tickets each time they reach the front. When someone finishes buying all their tickets, they leave the queue. The simulation ends when the person at index `k` completes their purchase.

```cpp
class Solution {
public:
    int timeRequiredToBuy(vector<int>& tickets, int k) {
        int n = tickets.size();
        queue<int> q;

        for (int i = 0; i < n; i++) {
            q.push(i);
        }

        int time = 0;
        while (!q.empty()) {
            time++;
            int cur = q.front();
            q.pop();
            tickets[cur]--;
            if (tickets[cur] == 0) {
                if (cur == k) {
                    return time;
                }
            } else {
                q.push(cur);
            }
        }
        return time;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n)$

> Where $n$ is the size of the input array and $m$ is the maximum value in the input array.

## 2. Iteration

Instead of using a queue, we can simulate the process by iterating through the array in a circular manner. We keep a pointer that cycles through positions `0, 1, 2, ..., n-1, 0, 1, ...` and skip anyone who has already finished buying tickets.

This approach eliminates the need for a separate queue data structure while achieving the same simulation. We track time and decrement ticket counts as we cycle through, stopping when the person at position `k` finishes.

```cpp
class Solution {
public:
    int timeRequiredToBuy(vector<int>& tickets, int k) {
        int n = tickets.size();
        int idx = 0;

        int time = 0;
        while (true) {
            time++;
            tickets[idx]--;
            if (tickets[idx] == 0) {
                if (idx == k) {
                    return time;
                }
            }
            idx = (idx + 1) % n;
            while (tickets[idx] == 0) {
                idx = (idx + 1) % n;
            }
        }

        return time;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(1)$

> Where $n$ is the size of the input array and $m$ is the maximum value in the input array.

## 3. Iteration (One Pass)

Instead of simulating the entire process, we can calculate the answer directly. Consider how many times each person will buy a ticket before person `k` finishes.

For people standing at or before position `k`, they will buy tickets at most `tickets[k]` times, since they get to buy before person `k` in each round. For people standing after position `k`, they will buy at most `tickets[k] - 1` times, since in the final round, person `k` finishes before they get another turn. Each person's contribution is capped by their own ticket needs.

```cpp
class Solution {
public:
    int timeRequiredToBuy(vector<int>& tickets, int k) {
        int res = 0;

        for (int i = 0; i < tickets.size(); i++) {
            if (i <= k) {
                res += min(tickets[i], tickets[k]);
            } else {
                res += min(tickets[i], tickets[k] - 1);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
