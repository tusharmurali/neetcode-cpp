# 983. Minimum Cost For Tickets

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-cost-for-tickets/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-cost-for-tickets>  
- **Video:** <https://www.youtube.com/watch?v=4Kww-zIkWWY>  

[← Back to index](../INDEX.md)

## 1. Recursion

We need to cover all travel days with the minimum cost using 1-day, 7-day, or 30-day passes. At each travel day, we have three choices: buy a 1-day pass (covers today), buy a 7-day pass (covers 7 days starting today), or buy a 30-day pass (covers 30 days starting today). We try all possibilities recursively and pick the minimum cost.

```cpp
class Solution {
public:
    int mincostTickets(vector<int>& days, vector<int>& costs) {
        int n = days.size();

        function<int(int)> dfs = [&](int i) -> int {
            if (i == n) return 0;

            int res = costs[0] + dfs(i + 1);

            int j = i;
            while (j < n && days[j] < days[i] + 7) {
                j++;
            }
            res = min(res, costs[1] + dfs(j));

            j = i;
            while (j < n && days[j] < days[i] + 30) {
                j++;
            }
            res = min(res, costs[2] + dfs(j));

            return res;
        };

        return dfs(0);
    }
};
```

**Complexity**

- Time complexity: $O(3 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The recursive solution recomputes the same subproblems many times. Since the minimum cost from day `i` onward depends only on `i`, we can cache these results. This transforms our exponential solution into a linear one by ensuring each state is computed only once.

```cpp
class Solution {
private:
    vector<int> dp;

    int dfs(int i, const vector<int>& days, const vector<int>& costs) {
        if (i == days.size()) return 0;
        if (dp[i] != -1) return dp[i];

        dp[i] = INT_MAX;
        int idx = 0, j = i;
        for (int d : {1, 7, 30}) {
            while (j < days.size() && days[j] < days[i] + d) {
                j++;
            }
            dp[i] = min(dp[i], costs[idx] + dfs(j, days, costs));
            idx++;
        }
        return dp[i];
    }

public:
    int mincostTickets(vector<int>& days, vector<int>& costs) {
        dp = vector<int>(days.size(), -1);
        return dfs(0, days, costs);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Instead of recursing from day 0 forward, we can build the solution backwards. Starting from the last travel day, we compute the minimum cost for each position. When we reach day 0, we have the answer. This eliminates recursion overhead and makes the solution iterative.

```cpp
class Solution {
public:
    int mincostTickets(vector<int>& days, vector<int>& costs) {
        int n = days.size();
        vector<int> dp(n + 1, 0);

        for (int i = n - 1; i >= 0; i--) {
            dp[i] = INT_MAX;
            int j = i;
            for (int k = 0; k < 3; ++k) {
                while (j < n && days[j] < days[i] + (k == 0 ? 1 : k == 1 ? 7 : 30)) {
                    j++;
                }
                dp[i] = min(dp[i], costs[k] + dp[j]);
            }
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Bottom-Up) + Two Pointers

In the previous approach, we search for coverage boundaries repeatedly. Since we iterate backwards and the days array is sorted, we can maintain two pointers that track where 7-day and 30-day passes would end. As we move backwards, these pointers only need to move backwards as well, avoiding redundant searches.

```cpp
class Solution {
public:
    int mincostTickets(vector<int>& days, vector<int>& costs) {
        days.push_back(days.back() + 30);
        int n = days.size();
        vector<int> dp(n, 0);
        int last7 = n, last30 = n;

        for (int i = n - 2; i >= 0; --i) {
            dp[i] = dp[i + 1] + costs[0];

            while (last7 > i + 1 && days[last7 - 1] >= days[i] + 7) {
                --last7;
            }
            dp[i] = min(dp[i], costs[1] + dp[last7]);

            while (last30 > i + 1 && days[last30 - 1] >= days[i] + 30) {
                --last30;
            }
            dp[i] = min(dp[i], costs[2] + dp[last30]);
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 5. Dynamic Programming (Space Optimized) - I

We can process days forward instead of backward. At each day, we only need to know the minimum cost to reach that day using passes bought on earlier days. We use two queues to track when 7-day and 30-day passes expire. Passes that have expired (started more than 7 or 30 days ago) are removed from consideration.

```cpp
class Solution {
public:
    int mincostTickets(vector<int>& days, vector<int>& costs) {
        queue<pair<int, int>> dp7, dp30;
        int dp = 0;

        for (int& d : days) {
            while (!dp7.empty() && dp7.front().first + 7 <= d) {
                dp7.pop();
            }

            while (!dp30.empty() && dp30.front().first + 30 <= d) {
                dp30.pop();
            }

            dp7.emplace(d, dp + costs[1]);
            dp30.emplace(d, dp + costs[2]);
            dp = min({dp + costs[0], dp7.front().second, dp30.front().second});
        }

        return dp;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we keep at most $30$ values in the queue.

## 6. Dynamic Programming (Space Optimized) - II

Similar to the previous approach but processing backwards. We use deques to track costs for 7-day and 30-day passes. As we move backwards, we pop entries that would now be within coverage range of the current day, keeping track of the last popped cost which represents the best option for that pass type.

```cpp
class Solution {
public:
    int mincostTickets(vector<int>& days, vector<int>& costs) {
        deque<pair<int, int>> dp7, dp30;
        int dp = 0, last7 = 0, last30 = 0;

        for (int i = days.size() - 1; i >= 0; --i) {
            dp += costs[0];

            while (!dp7.empty() && dp7.back().first >= days[i] + 7) {
                last7 = dp7.back().second;
                dp7.pop_back();
            }
            dp = min(dp, costs[1] + last7);

            while (!dp30.empty() && dp30.back().first >= days[i] + 30) {
                last30 = dp30.back().second;
                dp30.pop_back();
            }
            dp = min(dp, costs[2] + last30);

            dp7.push_front({days[i], dp});
            dp30.push_front({days[i], dp});
        }
        return dp;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we keep at most $30$ values in the deque.

## 7. Dynamic Programming (Space Optimized) - III

Instead of indexing by travel day positions, we can index by actual calendar days (1 to 365). For non-travel days, the cost stays the same as the previous day. For travel days, we consider all three pass options. This approach is efficient when travel days are sparse across the year.

```cpp
class Solution {
public:
    int mincostTickets(vector<int>& days, vector<int>& costs) {
        vector<int> dp(366, 0);
        int i = 0;

        for (int d = 1; d < 366; d++) {
            dp[d] = dp[d - 1];

            if (i == days.size()) {
                return dp[d];
            }

            if (d == days[i]) {
                dp[d] += costs[0];
                dp[d] = min(dp[d], costs[1] + dp[max(0, d - 7)]);
                dp[d] = min(dp[d], costs[2] + dp[max(0, d - 30)]);
                i++;
            }
        }
        return dp[365];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since the size of the $dp$ array is $366$.

## 8. Dynamic Programming (Space Optimized) - IV

The previous approach uses 366 slots, but we only ever look back at most 30 days. By using modular arithmetic with a size-31 array, we can reduce space to constant while still accessing the necessary previous states. The index `d % 31` ensures we have access to all values within the 30-day window.

```cpp
class Solution {
public:
    int mincostTickets(vector<int>& days, vector<int>& costs) {
        vector<int> dp(31, 0);
        int i = 0;

        for (int d = 1; d <= 365; d++) {
            if (i >= days.size()) break;

            dp[d % 31] = dp[(d - 1) % 31];

            if (d == days[i]) {
                dp[d % 31] += costs[0];
                dp[d % 31] = min(dp[d % 31], costs[1] + dp[max(0, d - 7) % 31]);
                dp[d % 31] = min(dp[d % 31], costs[2] + dp[max(0, d - 30) % 31]);
                i++;
            }
        }

        return dp[days.back() % 31];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since the size of the $dp$ array is $31$.

## Standalone solution file (`cpp/0983-minimum-cost-for-tickets.cpp` in the NeetCode repo)

```cpp
/*
The days of the year in which you will travel are given as an integer array days. Each day is an integer from 1 to 365.

Train tickets are sold in three different ways:

a 1-day pass is sold for costs[0] dollars,
a 7-day pass is sold for costs[1] dollars, and
a 30-day pass is sold for costs[2] dollars.
The passes allow that many days of consecutive travel.

Return the minimum number of dollars you need to travel every day in the given list of days.


Example. For days = [1,4,6,7,8,20] and costs = [2,7,15] we can buy a 1-day pass
	 for costs[0] = $2, which covers day 1. On day 3 we can buy a 7-day pass
	 for costs[1] = $7, which covers days 3,4....9. On day 20 we can again buy a
	 1-day pass for costs[0] = $2 that will cover the 20th day. So in total we spent
	 2 + 7 + 2 = $11 which is the minimum dollars needed for travelling in this case.


Time: O(n)
Space: O(n)

*/


class Solution {
public:
    int mincostTickets(vector<int>& days, vector<int>& costs) {

    vector<int> dp(days.size() + 1, 1e9);
    dp[days.size()] = 0;
    for(int i=days.size()-1; i>=0; i--) {
        for(int j=0; j<3; j++) {
            if(j == 0) {
                auto it = lower_bound(days.begin()+i, days.end(), days[i]+1);
                dp[i] = min(dp[i], costs[j] + dp[it-days.begin()]);
            }
            else if(j == 1) {
                auto it = lower_bound(days.begin()+i, days.end(), days[i]+7);
                dp[i] = min(dp[i], costs[j] + dp[it-days.begin()]);
            } else {
                auto it = lower_bound(days.begin()+i, days.end(), days[i]+30);
                dp[i] = min(dp[i], costs[j] + dp[it-days.begin()]);
            }
        }
    }
    return dp[0];

    }
};
```
