# 1249. Minimum Remove to Make Valid Parentheses

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-remove-to-make-valid-parentheses>  
- **Video:** <https://www.youtube.com/watch?v=mgQ4O9iUEbg>  

[← Back to index](../INDEX.md)

## 1. Stack

A string of parentheses is valid when every opening parenthesis has a matching closing one, and they nest properly. The key insight is that we can process the string in two passes. In the first pass (left to right), we skip any closing parenthesis that doesn't have a matching open one. After this pass, we know exactly how many unmatched opening parentheses remain. In the second pass (right to left), we remove those excess opening parentheses from the end.

```cpp
class Solution {
public:
    string minRemoveToMakeValid(string s) {
        string res;
        int cnt = 0;

        for (char c : s) {
            if (c == '(') {
                res.push_back(c);
                cnt++;
            } else if (c == ')' && cnt > 0) {
                res.push_back(c);
                cnt--;
            } else if (c != ')') {
                res.push_back(c);
            }
        }

        string filtered;
        for (int i = res.size() - 1; i >= 0; i--) {
            char c = res[i];
            if (c == '(' && cnt > 0) {
                cnt--;
            } else {
                filtered.push_back(c);
            }
        }
        reverse(filtered.begin(), filtered.end());
        return filtered;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Without Stack

This approach follows the same logic as the stack solution but modifies the string in place. Instead of building a new result list during the first pass, we mark invalid closing parentheses directly in the original array. The second pass still removes excess opening parentheses from the right side.

```cpp
class Solution {
public:
    string minRemoveToMakeValid(string s) {
        vector<char> arr(s.begin(), s.end());
        int cnt = 0;

        for (int i = 0; i < s.size(); i++) {
            if (s[i] == '(') {
                cnt++;
            } else if (s[i] == ')' && cnt > 0) {
                cnt--;
            } else if (s[i] == ')') {
                arr[i] = '\0';
            }
        }

        string res;
        for (int i = arr.size() - 1; i >= 0; i--) {
            if (arr[i] == '(' && cnt > 0) {
                cnt--;
            } else if (arr[i] != '\0') {
                res.push_back(arr[i]);
            }
        }

        reverse(res.begin(), res.end());
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Stack (Optimal)

Instead of using a counter, we can use a stack to store the indices of unmatched opening parentheses. When we see a closing parenthesis, we either pop from the stack (if there's a matching open) or mark it as invalid. After the first pass, any indices remaining in the stack are unmatched opening parentheses that need removal.

```cpp
class Solution {
public:
    string minRemoveToMakeValid(string s) {
        stack<int> stack;
        for (int i = 0; i < s.size(); i++) {
            if (s[i] == '(') {
                stack.push(i);
            } else if (s[i] == ')') {
                if (!stack.empty()) {
                    stack.pop();
                } else {
                    s[i] = '\0';
                }
            }
        }

        while (!stack.empty()) {
            s[stack.top()] = '\0';
            stack.pop();
        }

        string result;
        for (char& c : s) {
            if (c != '\0') {
                result += c;
            }
        }
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Without Stack (Optimal)

We can solve this in a single pass by counting closing parentheses upfront. Knowing the total number of `)` characters tells us the maximum number of `(` we can keep. As we iterate, we track how many opening parentheses we've included and use this to decide whether each parenthesis should be kept or skipped.

```cpp
class Solution {
public:
    string minRemoveToMakeValid(string s) {
        int openCnt = 0, closeCnt = 0;
        for (char& c : s) {
            if (c == ')') closeCnt++;
        }

        string res;
        for (char& c : s) {
            if (c == '(') {
                if (openCnt == closeCnt) continue;
                openCnt++;
            } else if (c == ')') {
                closeCnt--;
                if (openCnt == 0) continue;
                openCnt--;
            }
            res.push_back(c);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output string.

## Standalone solution file (`cpp/1249-minimum-remove-to-make-valid-parentheses.cpp` in the NeetCode repo)

```cpp
/*
* [1249] Minimum Remove to Make Valid Parentheses *

Given a string s of '(' , ')' and lowercase English characters.

Your task is to remove the minimum number of parentheses ( '(' or ')', in any positions ) so that the resulting parentheses string is valid and return any valid string.

Formally, a parentheses string is valid if and only if:

    It is the empty string, contains only lowercase characters, or
    It can be written as AB (A concatenated with B), where A and B are valid strings, or
    It can be written as (A), where A is a valid string.

Example 1:

Input: s = "lee(t(c)o)de)"
Output: "lee(t(c)o)de"
Explanation: "lee(t(co)de)" , "lee(t(c)ode)" would also be accepted.

Time: O(n)
Space: O(n)

Runtime: 14 ms, faster than 98.14% of C++ online submissions for Minimum Remove to Make Valid Parentheses.
Memory Usage: 14.2 MB, less than 10.57% of C++ online submissions for Minimum Remove to Make Valid Parentheses.
*/



class Solution {
public:
    string minRemoveToMakeValid(string s) {
        stack<pair<char,int>> st;
        
        for (int i = 0; i < s.size(); i++) {
            if (s[i] == '(') {
                st.push(make_pair(s[i], i));
            } else if (s[i] == ')') {
                if (!st.empty() and st.top().first == '(') {
                    st.pop();                
                } else {
                    st.push(make_pair(')', i));
                }
            }
        }

        while (!st.empty()) {
            s.erase(s.begin() + st.top().second);
            st.pop();
        }

        return s;
    }
};
```
