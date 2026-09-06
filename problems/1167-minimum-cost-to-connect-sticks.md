# 1167. Minimum Cost to Connect Sticks

- **Difficulty:** Medium  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-cost-to-connect-sticks/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-cost-to-connect-sticks>  

[← Back to index](../INDEX.md)

## 1. Greedy

When combining two sticks, the cost equals the sum of their lengths, and that combined stick may be used in future combinations. Sticks combined early contribute their length to multiple subsequent operations. To minimize total cost, we should combine the smallest sticks first so that larger values are added fewer times. A `min-heap` lets us efficiently retrieve and combine the two smallest sticks at each step.

```cpp
class Solution {
public:
    int connectSticks(vector<int>& sticks) {
        int totalCost = 0;

        priority_queue<int, vector<int>, greater<int>> pq;

        for (int i = 0; i < sticks.size(); i++) {
            pq.push(sticks[i]);
        }

        // combine two of the smallest sticks until we are left with just one.
        while (pq.size() > 1) {
            int stick1 = pq.top();
            pq.pop();
            int stick2 = pq.top();
            pq.pop();

            int cost = stick1 + stick2;
            totalCost += cost;

            pq.push(stick1+stick2);
        }

        return totalCost;
    }
};
```

**Complexity**

- Time complexity: $O(N \log N)$
- Space complexity: $O(N)$

> Where $N$ is the length of the input array.
