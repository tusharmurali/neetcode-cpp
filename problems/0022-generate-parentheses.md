# 22. Generate Parentheses

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/generate-parentheses/>  
- **NeetCode:** <https://neetcode.io/problems/generate-parentheses>  
- **Video:** <https://www.youtube.com/watch?v=s9fokUqJ76A>  

[← Back to index](../INDEX.md)

## 1. Brute Force

Generate **all** strings of length `2n` using only `'('` and `')'`.
Most will be invalid, so for each completed string we **validate** it:

- Keep a `balance` (opens count).
- `'('` increases `balance`, `')'` decreases it.
- If `balance` ever becomes negative, there are too many `)` early, which is invalid.
- At the end, `balance` must be `0`, meaning all opens are closed.

```cpp
class Solution {
public:
    bool valid(const string& s) {
        int open = 0;
        for (char c : s) {
            open += (c == '(') ? 1 : -1;
            if (open < 0) return false;
        }
        return open == 0;
    }

    void dfs(string s, vector<string>& res, int n) {
        if (s.length() == 2 * n) {
            if (valid(s)) res.push_back(s);
            return;
        }
        dfs(s + '(', res, n);
        dfs(s + ')', res, n);
    }

    vector<string> generateParenthesis(int n) {
        vector<string> res;
        dfs("", res, n);
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ {2n} * n)$
- Space complexity: $O(2 ^ {2n} * n)$

## 2. Backtracking

Instead of generating **all** strings and then checking validity, we **build only valid strings**.

Key rules for valid parentheses:

- You can add `'('` **only if** you still have openings left (`open < n`).
- You can add `')'` **only if** it won't break validity (`close < open`).
- A string is complete and valid **only when** `open == close == n`.

So at every step, we make **safe choices only**, which avoids invalid paths early.

```cpp
class Solution {
public:
    void backtrack(int openN, int closedN, int n, vector<string>& res, string& stack) {
        if (openN == closedN && openN == n) {
            res.push_back(stack);
            return;
        }

        if (openN < n) {
            stack += '(';
            backtrack(openN + 1, closedN, n, res, stack);
            stack.pop_back();
        }
        if (closedN < openN) {
            stack += ')';
            backtrack(openN, closedN + 1, n, res, stack);
            stack.pop_back();
        }
    }

    vector<string> generateParenthesis(int n) {
        vector<string> res;
        string stack;
        backtrack(0, 0, n, res, stack);
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(\frac{4^n}{\sqrt{n}})$
- Space complexity: $O(n)$

## 3. Dynamic Programming

A valid parentheses string can be **built from smaller valid strings**.

Think of this pattern: `( left ) right`

- `left` is a valid parentheses string with `i` pairs.
- `right` is a valid parentheses string with `k - i - 1` pairs.
- Wrapping `left` with `()` guarantees balance.
- Appending `right` keeps the string valid.

So, every valid result for `k` pairs is formed by **combining smaller answers**.

```cpp
class Solution {
public:
    vector<string> generateParenthesis(int n) {
        vector<vector<string>> res(n + 1);
        res[0] = {""};

        for (int k = 0; k <= n; ++k) {
            for (int i = 0; i < k; ++i) {
                for (const string& left : res[i]) {
                    for (const string& right : res[k - i - 1]) {
                        res[k].push_back("(" + left + ")" + right);
                    }
                }
            }
        }

        return res[n];
    }
};
```

**Complexity**

- Time complexity: $O(\frac{4^n}{\sqrt{n}})$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0022-generate-parentheses.cpp` in the NeetCode repo)

```cpp
/*
    Given n pairs of parentheses, generate all combos of well-formed parentheses
    Ex. n = 3 -> ["((()))","(()())","(())()","()(())","()()()"], n = 1 -> ["()"]

    Backtracking, keep valid, favor trying opens, then try closes if still valid

    Time: O(2^n)
    Space: O(n)
*/

class Solution {
public:
    vector<string> generateParenthesis(int n) {
        vector<string> result;
        generate(n, 0, 0, "", result);
        return result;
    }
private:
    void generate(int n, int open, int close, string str, vector<string>& result) {
        if (open == n && close == n) {
            result.push_back(str);
            return;
        }
        if (open < n) {
            generate(n, open + 1, close, str + '(', result);
        }
        if (open > close) {
            generate(n, open, close + 1, str + ')', result);
        }
    }
};

/*
    Using a single stack without recursion

    Time: O(2^n)
    Space: O(n)
*/
class Solution {
public:
    vector<string> generateParenthesis(int n) {
        stack<vector<string>> stk;
        vector<string> result;
        stk.push({"(", "1", "0"}); // {string, left_count, right_count}

        while (!stk.empty()) {
            for (int i = 0; i < stk.size(); i++) {
                vector<string> item = stk.top();
                stk.pop();
                int left = stoi(item[1]), right = stoi(item[2]);
                if (left == n && right == n) {
                    result.push_back(item[0]);
                    continue;
                }
                if (left < n) {
                    stk.push({item[0] + "(", to_string(++left), to_string(right)});
                    left--; // reverse left count
                }
                if (left > right) {
                    stk.push({item[0] + ")", to_string(left), to_string(++right)});
                }
            }
        }
        return result;
    }
};
```
