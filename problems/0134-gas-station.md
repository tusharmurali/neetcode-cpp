# 134. Gas Station

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/gas-station/>  
- **NeetCode:** <https://neetcode.io/problems/gas-station>  
- **Video:** <https://www.youtube.com/watch?v=lJwbPZGo05A>  
- **Video approach:** 2. Two Pointers  

[← Back to index](../INDEX.md)

## 1. Brute Force

We need to find a starting gas station index such that we can travel around the entire circle exactly once without the gas tank ever going negative.

The most direct (brute force) idea is:

- try starting from every station `i`
- simulate the trip around the circle
- if at any point the tank becomes negative, that start index fails
- if we return back to `i` successfully, then `i` is a valid answer

At each station:

- we gain `gas[j]`
- we spend `cost[j]` to travel to the next station
  So the tank changes by `gas[j] - cost[j]`.

This models refueling at station `j` first, then spending `cost[j]` to drive from station `j` to station `(j + 1) % n`.

```cpp
class Solution {
public:
    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
        int n = gas.size();

        for (int i = 0; i < n; i++) {
            int tank = gas[i] - cost[i];
            if (tank < 0) continue;

            int j = (i + 1) % n;
            while (j != i) {
                tank += gas[j] - cost[j];
                if (tank < 0) break;
                j = (j + 1) % n;
            }

            if (j == i) return i;
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Two Pointers ▶ video

We need to find a gas station index from which we can complete the full circular route without the gas tank ever becoming negative.

Instead of simulating the trip from every station (brute force), this approach uses **two pointers** to narrow down the possible starting station efficiently.

Think of the route as a circle that we are trying to “cover” from both ends:

- `start` moves backward from the end of the array
- `end` moves forward from the beginning of the array
- `tank` keeps track of the current gas balance for the segment we are considering

At every step, we decide **which side to expand** based on whether the current `tank` is sufficient:

- If the `tank` is negative, the current segment cannot work, so we must include more gas by moving `start` backward
- If the `tank` is non-negative, we can safely extend the route forward by moving `end`

By doing this, we gradually merge the segment until `start` meets `end`.  
If the final `tank` is non-negative, `start` is a valid starting station.

```cpp
class Solution {
public:
    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
        int n = gas.size();
        int start = n - 1, end = 0;
        int tank = gas[start] - cost[start];
        while (start > end) {
            if (tank < 0) {
                start--;
                tank += gas[start] - cost[start];
            } else {
                tank += gas[end] - cost[end];
                end++;
            }
        }
        return tank >= 0 ? start : -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Greedy

We want to find a gas station index from which we can complete the entire circular route without the gas tank ever going negative.

First, notice an important fact:

- If the **total gas available** is less than the **total cost required**, then it is **impossible** to complete the circuit from any station.

If the total gas is sufficient, then at least one valid starting station exists. Under this problem's guarantee, there will be at most one valid answer.

The greedy idea is to scan the stations from left to right while keeping track of the **current tank balance**.

- If at some index the tank becomes negative, it means **we cannot start from any station between the previous start and this index**, because they would all run out of gas at the same point.
- So we reset the tank and try the **next station as a new starting point**.

```cpp
class Solution {
public:
    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
        if (accumulate(gas.begin(), gas.end(), 0) <
            accumulate(cost.begin(), cost.end(), 0)) {
            return -1;
        }

        int total = 0;
        int res = 0;
        for (int i = 0; i < gas.size(); i++) {
            total += (gas[i] - cost[i]);

            if (total < 0) {
                total = 0;
                res = i + 1;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0134-gas-station.cpp` in the NeetCode repo)

```cpp
/*
    Gas stations along circular route, return where to start to complete 1 trip
    Ex. gas = [1,2,3,4,5] cost = [3,4,5,1,2] -> index 3 (station 4), tank = 4,8,7,6,5

    At a start station, if total ever becomes negative won't work, try next station

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
        int n = gas.size();
        
        int totalGas = 0;
        int totalCost = 0;
        for (int i = 0; i < n; i++) {
            totalGas += gas[i];
            totalCost += cost[i];
        }
        if (totalGas < totalCost) {
            return -1;
        }
        
        int total = 0;
        int result = 0;
        
        for (int i = 0; i < n; i++) {
            total += gas[i] - cost[i];
            if (total < 0) {
                total = 0;
                result = i + 1;
            }
        }
        
        return result;
    }
};
```
