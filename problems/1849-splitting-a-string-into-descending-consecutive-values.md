# 1849. Splitting a String Into Descending Consecutive Values

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/splitting-a-string-into-descending-consecutive-values/>  
- **NeetCode:** <https://neetcode.io/problems/splitting-a-string-into-descending-consecutive-values>  
- **Video:** <https://www.youtube.com/watch?v=eDtMmysldaw>  

[← Back to index](../INDEX.md)

## 1. Backtracking

The problem asks us to split a string into at least two parts where each consecutive part represents a number that is exactly one less than the previous. Since we need to explore all possible ways to split the string, backtracking is a natural choice. We try every possible split point, build numbers digit by digit, and check if they form a valid descending consecutive sequence.

```cpp
class Solution {
public:
    bool splitString(string s) {
        vector<long long> splits;
        return dfs(s, 0, splits);
    }

private:
    bool isValid(vector<long long>& splits) {
        for (int i = 1; i < splits.size(); i++) {
            if (splits[i] != splits[i - 1] - 1) {
                return false;
            }
        }
        return splits.size() > 1;
    }

    bool dfs(string& s, int i, vector<long long>& splits) {
        if (i == s.size()) {
            return isValid(splits);
        }
        unsigned long long num = 0;
        for (int j = i; j < s.size(); j++) {
            num = num * 10 + (s[j] - '0');
            splits.push_back(num);
            if (dfs(s, j + 1, splits)) {
                return true;
            }
            splits.pop_back();
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ n)$
- Space complexity: $O(n)$

## 2. Recursion - I

Instead of collecting all splits and validating at the end, we can optimize by passing the previous number directly. Once we fix the first number, we only need to find subsequent numbers that are exactly one less. This eliminates the need to store all splits and allows early termination when we find a valid sequence.

```cpp
class Solution {
public:
    bool splitString(string s) {
        int n = s.size();
        unsigned long long val = 0;
        for (int i = 0; i < n - 1; i++) {
            val = val * 10 + (s[i] - '0');
            if (dfs(s, i + 1, val)) {
                return true;
            }
        }
        return false;
    }

private:
    bool dfs(string& s, int index, long long prev) {
        if (index == s.size()) {
            return true;
        }
        unsigned long long num = 0;
        for (int j = index; j < s.size(); j++) {
            num = num * 10 + (s[j] - '0');
            if (num + 1 == prev && dfs(s, j + 1, num)) {
                return true;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Recursion - II

Building on the previous approach, we add an important pruning optimization. Since we need descending consecutive values, once the current number we are building becomes greater than or equal to the previous number, there is no point continuing to add more digits. This early termination significantly reduces the search space.

```cpp
class Solution {
public:
    bool splitString(string s) {
        int n = s.size();
        unsigned long long val = 0;
        for (int i = 0; i < n - 1; i++) {
            val = val * 10 + (s[i] - '0');
            if (dfs(s, i + 1, val)) {
                return true;
            }
        }
        return false;
    }

private:
    bool dfs(string& s, int index, long long prev) {
        if (index == s.size()) {
            return true;
        }
        unsigned long long num = 0;
        for (int j = index; j < s.size(); j++) {
            num = num * 10 + (s[j] - '0');
            if (num + 1 == prev && dfs(s, j + 1, num)) {
                return true;
            }
            if (num >= prev) {
                break;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$ for recursion stack.

## 4. Stack

Instead of using recursion with the call stack, we can simulate the same process with an explicit stack. This converts the recursive solution into an iterative one, which can be useful for avoiding stack overflow on very deep recursions and makes the state transitions more explicit.

```cpp
class Solution {
public:
    bool splitString(string s) {
        int n = s.size();
        stack<pair<int, long long>> stack;
        unsigned long long val = 0;

        for (int i = 0; i < n - 1; i++) {
            val = val * 10 + (s[i] - '0');
            stack.push({i + 1, val});

            while (!stack.empty()) {
                auto [index, prev] = stack.top();
                stack.pop();
                unsigned long long num = 0;

                for (int j = index; j < n; j++) {
                    num = num * 10 + (s[j] - '0');
                    if (num + 1 == prev) {
                        if (j + 1 == n) {
                            return true;
                        }
                        stack.push({j + 1, num});
                    } else if (num >= prev) {
                        break;
                    }
                }
            }
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/1849-splitting-a-string-into-descending-consecutive-values.cpp` in the NeetCode repo)

```cpp
typedef unsigned long long ll;
class Solution {
public:
    bool solve(string & s , ll last , int index,int cnt){

        if(index >= s.size()) return cnt > 1;

        ll num = 0;
        bool ret = false;

        for(int i = index ; i < s.size() ; i++){
            num = num * 10;
            num += (s[i] - '0');

            if(last == -1 || last == num + 1){
                ret |= solve(s , num , i + 1 , cnt + 1);
            }else if(last != -1 && num >= last)break;
        }

        return ret;
    }
    bool splitString(string s) {
        return solve(s,-1,0,0);
    }
};
```
