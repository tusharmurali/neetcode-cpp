# 678. Valid Parenthesis String

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/valid-parenthesis-string/>  
- **NeetCode:** <https://neetcode.io/problems/valid-parenthesis-string>  
- **Video:** <https://www.youtube.com/watch?v=QhPdNS143Qg>  
- **Video approach:** 2. Dynamic Programming (Top-Down)  

[← Back to index](../INDEX.md)

## 1. Recursion

This problem asks whether a string containing `'('`, `')'`, and `'*'` can be interpreted as a **valid parentheses string**.

The tricky part is `'*'`, because it can represent:

- `'('`
- `')'`
- an empty string `''`

Using recursion, we try **all valid interpretations** of the string while keeping track of how many opening parentheses are currently unmatched.

The recursive function answers:
**"Is it possible to make the substring starting at index `i` valid, given that we currently have `open` unmatched `'('`?"**

Important rules:

- The number of open parentheses (`open`) should **never be negative**
- At the end of the string, all open parentheses must be closed (`open == 0`)

```cpp
class Solution {
public:
    bool checkValidString(string s) {
        return dfs(0, 0, s);
    }

private:
    bool dfs(int i, int open, const string& s) {
        if (open < 0) return false;
        if (i == s.size()) return open == 0;

        if (s[i] == '(') {
            return dfs(i + 1, open + 1, s);
        } else if (s[i] == ')') {
            return dfs(i + 1, open - 1, s);
        } else {
            return dfs(i + 1, open, s) ||
                   dfs(i + 1, open + 1, s) ||
                   dfs(i + 1, open - 1, s);
        }
    }
};
```

**Complexity**

- Time complexity: $O(3 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down) ▶ video

We need to decide if a string containing `'('`, `')'`, and `'*'` can be turned into a **valid parentheses string**.

The character `'*'` is flexible and can act as:

- `'('`
- `')'`
- empty `''`

A brute-force recursion tries all possibilities, but it repeats the same work for the same positions and open counts.
To avoid that, we use **top-down dynamic programming (memoization)**.

We track two things:

- `i`: where we are in the string
- `open`: how many `'('` are currently unmatched

The function `dfs(i, open)` answers:
**"Can the substring `s[i:]` be made valid if we currently have `open` unmatched opening parentheses?"**

Rules:

- `open` must never go below `0`
- when we reach the end, we need `open == 0`

```cpp
class Solution {
public:
    bool checkValidString(string s) {
        int n = s.size();
        memo = vector<vector<int>>(n + 1, vector<int>(n + 1, -1));
        return dfs(0, 0, s);
    }

private:
    vector<vector<int>> memo;

    bool dfs(int i, int open, const string& s) {
        if (open < 0) return false;
        if (i == s.size()) return open == 0;

        if (memo[i][open] != -1) return memo[i][open] == 1;

        bool result;
        if (s[i] == '(') {
            result = dfs(i + 1, open + 1, s);
        } else if (s[i] == ')') {
            result = dfs(i + 1, open - 1, s);
        } else {
            result = (dfs(i + 1, open, s) ||
                      dfs(i + 1, open + 1, s) ||
                      dfs(i + 1, open - 1, s));
        }

        memo[i][open] = result ? 1 : 0;
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Dynamic Programming (Bottom-Up)

We need to check if a string containing `'('`, `')'`, and `'*'` can be interpreted as a **valid parentheses string**.

A helpful way to solve this is to track how many opening parentheses are currently unmatched:

- `open` = number of `'('` we still need to close

The tricky character is `'*'`, because it can act as:

- `'('` (increase `open`)
- `')'` (decrease `open`)
- empty (keep `open` the same)

In bottom-up DP, we build answers for smaller suffixes first.

We define:

- `dp[i][open]` = whether it is possible to make `s[i:]` valid if we currently have `open` unmatched `'('`

We fill this table from the end of the string back to the start.

```cpp
class Solution {
public:
    bool checkValidString(string s) {
        int n = s.size();
        vector<vector<bool>> dp(n + 1, vector<bool>(n + 1, false));
        dp[n][0] = true;

        for (int i = n - 1; i >= 0; --i) {
            for (int open = 0; open < n; ++open) {
                bool res = false;
                if (s[i] == '*') {
                    res |= dp[i + 1][open + 1];
                    if (open > 0) res |= dp[i + 1][open - 1];
                    res |= dp[i + 1][open];
                } else {
                    if (s[i] == '(') {
                        res |= dp[i + 1][open + 1];
                    } else if (open > 0) {
                        res |= dp[i + 1][open - 1];
                    }
                }
                dp[i][open] = res;
            }
        }
        return dp[0][0];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 4. Dynamic Programming (Space Optimized)

We need to check if a string containing `'('`, `')'`, and `'*'` can be interpreted as a **valid parentheses string**.

A common DP idea is to track how many opening parentheses are currently unmatched:

- `open` = number of `'('` that still need to be closed

In the 2D bottom-up DP version:

- `dp[i][open]` told us whether `s[i:]` can be valid with `open` unmatched `'('`

But notice something important:

- to compute values for position `i`, we only need values from position `i + 1`

So we don’t need the full 2D table. We can keep just one 1D array for the “next row” and build a new one for the “current row”.

Here:

- `dp[open]` represents the answer for the suffix starting at `i + 1`
- `new_dp[open]` represents the answer for the suffix starting at `i`

```cpp
class Solution {
public:
    bool checkValidString(string s) {
        int n = s.size();
        vector<bool> dp(n + 1, false);
        dp[0] = true;

        for (int i = n - 1; i >= 0; --i) {
            vector<bool> newDp(n + 1, false);
            for (int open = 0; open < n; ++open) {
                if (s[i] == '*') {
                    newDp[open] = dp[open + 1] ||
                                  (open > 0 && dp[open - 1]) || dp[open];
                } else if (s[i] == '(') {
                    newDp[open] = dp[open + 1];
                } else if (open > 0) {
                    newDp[open] = dp[open - 1];
                }
            }
            dp = newDp;
        }
        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 5. Stack

We want to check whether a string containing `'('`, `')'`, and `'*'` can be interpreted as a **valid parentheses string**.

The character `'*'` is flexible and can act as:

- `'('`
- `')'`
- or an empty string

A stack-based approach works well because:

- parentheses validity depends on **order**
- `'*'` can be used later to fix mismatches if needed

The key idea is to:

- keep track of indices of unmatched `'('`
- keep track of indices of `'*'`
- use `'*'` as a backup when we encounter an unmatched `')'`

At the end, we must also ensure that any remaining `'('` can be matched with a `'*'` **that appears after it**.

```cpp
class Solution {
public:
    bool checkValidString(string s) {
        stack<int> left, star;
        for (int i = 0; i < s.size(); ++i) {
            if (s[i] == '(') {
                left.push(i);
            } else if (s[i] == '*') {
                star.push(i);
            } else {
                if (left.empty() && star.empty()) return false;
                if (!left.empty()) {
                    left.pop();
                } else {
                    star.pop();
                }
            }
        }

        while (!left.empty() && !star.empty()) {
            if (left.top() > star.top()) return false;
            left.pop();
            star.pop();
        }
        return left.empty();
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 6. Greedy

We want to check whether a string containing `'('`, `')'`, and `'*'` can be interpreted as a **valid parentheses string**.

Instead of trying all possibilities or using stacks, we can solve this greedily by tracking a **range** of possible unmatched `'('` counts.

Think of it this way:

- At any point, we don’t need the exact number of open parentheses
- We only need to know the **minimum** and **maximum** number of `'('` that _could_ be open

Why this works:

- `'('` always increases the number of open parentheses
- `')'` always decreases it
- `'*'` is flexible and can:
    - decrease open count (act as `')'`)
    - increase open count (act as `'('`)
    - keep it unchanged (act as empty)

So we maintain:

- `leftMin` → the **minimum possible** number of unmatched `'('`
- `leftMax` → the **maximum possible** number of unmatched `'('`

If at any point the maximum possible opens becomes negative, the string is invalid.
At the end, if the minimum possible opens is zero, the string can be valid.

```cpp
class Solution {
public:
    bool checkValidString(string s) {
        int leftMin = 0, leftMax = 0;

        for (char c : s) {
            if (c == '(') {
                leftMin++;
                leftMax++;
            } else if (c == ')') {
                leftMin--;
                leftMax--;
            } else {
                leftMin--;
                leftMax++;
            }
            if (leftMax < 0) {
                return false;
            }
            if (leftMin < 0) {
                leftMin = 0;
            }
        }
        return leftMin == 0;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0678-valid-parenthesis-string.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    bool checkValidString(string s) {
        int n = s.size();
    
        int balanced = 0;
        for(int i=0; i<n; i++) {
            if(s[i] == '(' || s[i] == '*') 
                balanced++;
            else 
                balanced--;

            if(balanced < 0) 
                return false;
        }

        if(balanced == 0) 
            return true;

        balanced = 0;
        for(int i=n-1; i>=0; i--) {
            if(s[i] == ')' || s[i] == '*') 
                balanced++;
            else 
                balanced--;

            if(balanced < 0) 
                return false;
        }

        return true;
    }
};
```
