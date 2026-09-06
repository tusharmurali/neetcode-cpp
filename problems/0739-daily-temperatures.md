# 739. Daily Temperatures

- **Difficulty:** Medium  
- **Pattern:** Stack  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/daily-temperatures/>  
- **NeetCode:** <https://neetcode.io/problems/daily-temperatures>  
- **Video:** <https://www.youtube.com/watch?v=cTBiBSnjO3c>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each day, we simply look forward to find the next day with a higher temperature.  
We compare the current day with every future day until we either find a warmer one or reach the end.  
If we find a warmer day, we record how many days it took.  
If not, the answer is `0`.  
This method is easy to understand but slow because every day may scan many days ahead.

```cpp
class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        int n = temperatures.size();
        vector<int> res(n);

        for (int i = 0; i < n; i++) {
            int count = 1;
            int j = i + 1;
            while (j < n) {
                if (temperatures[j] > temperatures[i]) {
                    break;
                }
                j++;
                count++;
            }
            count = (j == n) ? 0 : count;
            res[i] = count;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output array.

## 2. Stack

We want to know how long it takes until a warmer day for each temperature.  
A **stack** helps because it keeps track of days that are still waiting for a warmer temperature.  
As we scan forward, whenever we find a temperature higher than the one on top of the stack, it means we just discovered the “next warmer day” for that earlier day.  
We pop it, compute the difference in days, and continue.  
This way, each day is pushed and popped at most once, making the process efficient.

```cpp
class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        vector<int> res(temperatures.size(), 0);
        stack<pair<int, int>> stack; // pair: {temp, index}

        for (int i = 0; i < temperatures.size(); i++) {
            int t = temperatures[i];
            while (!stack.empty() && t > stack.top().first) {
                auto pair = stack.top();
                stack.pop();
                res[pair.second] = i - pair.second;
            }
            stack.push({t, i});
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming

Instead of checking every future day one by one, we can **reuse previously computed answers**.  
If day `j` is not warmer than day `i`, we don’t need to move forward step-by-step — we can simply **jump** ahead by using the result already stored for day `j`.  
This lets us skip many unnecessary comparisons.  
By working backward and using these jumps, we efficiently find the next warmer day for each position.

```cpp
class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        int n = temperatures.size();
        vector<int> res(n, 0);

        for (int i = n - 2; i >= 0; i--) {
            int j = i + 1;
            while (j < n && temperatures[j] <= temperatures[i]) {
                if (res[j] == 0) {
                    j = n;
                    break;
                }
                j += res[j];
            }

            if (j < n) {
                res[i] = j - i;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output array.

## Standalone solution file (`cpp/0739-daily-temperatures.cpp` in the NeetCode repo)

```cpp
/*
    Given array of temps, return an array w/ # of days until warmer
    Ex. temperature = [73,74,75,71,69,72,76,73] -> [1,1,4,2,1,1,0,0]

    Monotonic decr stack, at each day, compare incr from prev days

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        int n = temperatures.size();
        
        // pair: [index, temp]
        stack<pair<int, int>> stk;
        vector<int> result(n);
        
        for (int i = 0; i < n; i++) {
            int currDay = i;
            int currTemp = temperatures[i];
            
            while (!stk.empty() && stk.top().second < currTemp) {
                int prevDay = stk.top().first;
                int prevTemp = stk.top().second;
                stk.pop();
                
                result[prevDay] = currDay - prevDay;
            }
            
            stk.push({currDay, currTemp});
        }
        
        return result;
    }
};
```
