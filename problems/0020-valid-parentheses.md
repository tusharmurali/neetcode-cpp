# 20. Valid Parentheses

- **Difficulty:** Easy  
- **Pattern:** Stack  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/valid-parentheses/>  
- **NeetCode:** <https://neetcode.io/problems/validate-parentheses>  
- **Video:** <https://www.youtube.com/watch?v=WTzjTskDFMg>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The idea is simple:
valid parentheses must always appear in matching pairs like `"()"`, `"{}"`, or `"[]"`.
So if the string is valid, we can repeatedly remove these matching pairs until nothing is left.
If, after removing all possible pairs, the string becomes empty, then the parentheses were properly matched.
Otherwise, some unmatched characters remain, meaning the string is invalid.

```cpp
class Solution {
public:
    bool isValid(string s) {
        while (true) {
            size_t pos = string::npos;
            if ((pos = s.find("()")) != string::npos) {
                s.erase(pos, 2);
                continue;
            }
            if ((pos = s.find("{}")) != string::npos) {
                s.erase(pos, 2);
                continue;
            }
            if ((pos = s.find("[]")) != string::npos) {
                s.erase(pos, 2);
                continue;
            }
            break;
        }
        return s.empty();
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Stack

Valid parentheses must follow a last-opened, first-closed order — just like stacking plates.
So we use a **stack** to track opening brackets.
Whenever we see a closing bracket, we simply check whether it matches the most recent opening bracket on top of the stack.
If it matches, we remove that opening bracket.
If it doesn't match (or the stack is empty), the string is invalid.
A valid string ends with an empty stack.

```cpp
class Solution {
public:
    bool isValid(string s) {
        std::stack<char> stack;
        std::unordered_map<char, char> closeToOpen = {
            {')', '('},
            {']', '['},
            {'}', '{'}
        };

        for (char c : s) {
            if (closeToOpen.count(c)) {
                if (!stack.empty() && stack.top() == closeToOpen[c]) {
                    stack.pop();
                } else {
                    return false;
                }
            } else {
                stack.push(c);
            }
        }
        return stack.empty();
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0020-valid-parentheses.cpp` in the NeetCode repo)

```cpp
/*
    Given s w/ '(, ), {, }, [, ]', determine if valid
    Ex. s = "()[]{}" -> true, s = "(]" -> false

    Stack of opens, check for matching closes & validity

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    bool isValid(string s) {
        stack<char> open;
        unordered_map<char, char> parens = {
            {')', '('},
            {']', '['},
            {'}', '{'},
        };
        
        for (const auto& c : s) {
            if (parens.find(c) != parens.end()) {
                // if input starts with a closing bracket.
                if (open.empty()) {
                    return false;
                }

                if (open.top() != parens[c]) {
                    return false;
                }

                open.pop();
            } else {
                open.push(c);
            }
        }
        
        return open.empty();
    }
};
```
