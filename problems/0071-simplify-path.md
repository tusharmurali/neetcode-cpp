# 71. Simplify Path

- **Difficulty:** Medium  
- **Pattern:** Stack  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/simplify-path/>  
- **NeetCode:** <https://neetcode.io/problems/simplify-path>  
- **Video:** <https://www.youtube.com/watch?v=qYlHrAKJfyA>  
- **Video approach:** 2. Stack - II  

[← Back to index](../INDEX.md)

## 1. Stack - I

A Unix-style path can contain special directory references: `.` means the current directory (stay in place), and `..` means the parent directory (go up one level). Multiple slashes should be treated as a single separator. A stack is ideal here because navigating to a parent directory is just like popping from a stack, while entering a subdirectory is like pushing onto it.

```cpp
class Solution {
public:
    string simplifyPath(string path) {
        vector<string> stack;
        string cur;

        for (char c : path + "/") {
            if (c == '/') {
                if (cur == "..") {
                    if (!stack.empty()) stack.pop_back();
                } else if (!cur.empty() && cur != ".") {
                    stack.push_back(cur);
                }
                cur.clear();
            } else {
                cur += c;
            }
        }

        string result = "/";
        for (int i = 0; i < stack.size(); ++i) {
            if (i > 0) result += "/";
            result += stack[i];
        }

        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Stack - II ▶ video

Instead of processing character by character, we can split the path by `/` to get all the directory names at once. This simplifies the logic since we directly work with directory names rather than building them up. The same `stack`-based approach applies: push valid directories and pop on `..`.

```cpp
class Solution {
public:
    string simplifyPath(string path) {
        vector<string> stack;
        string cur;
        stringstream ss(path);
        while (getline(ss, cur, '/')) {
            if (cur.empty()) continue;
            if (cur == "..") {
                if (!stack.empty()) stack.pop_back();
            } else if (!cur.empty() && cur != ".") {
                stack.push_back(cur);
            }
        }

        string result = "/";
        for (int i = 0; i < stack.size(); ++i) {
            if (i > 0) result += "/";
            result += stack[i];
        }

        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0071-simplify-path.cpp` in the NeetCode repo)

```cpp
/*
    Given an absolute path to a file or directory in a Unix-style file system,
    convert it to the simplified canonical path.

    In a Unix-style file system, a period '.' refers to the current directory.
    A double period '..' refers to the directory up a level.
    Any multiple consecutive slashes (i.e. '//') are treated as a single slash '/'.
    For this problem, any other format of periods such as '...' are treated as file/directory names.

    The canonical path should have the following format:
    - The path starts with a single slash '/'.
    - Any two directories are separated by a single slash '/'.
    - The path does not end with a trailing '/'.
    - The path only contains the directories on the path from the root directory to the target file or directory (i.e., no period '.' or double period '..')

    Return the simplified canonical path.

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    string simplifyPath(string path) {
        stringstream ss(path);
        string dir;
        stack<string> stk;

        while (getline(ss, dir, '/')) {
            if (dir.empty() || dir == ".") {
                continue;
            }
            else if (dir == "..") {
                if (!stk.empty())
                    stk.pop();
            }
            else {
                stk.push(dir);
            }
        }

        string res = "";
        while (!stk.empty()) {
            res = "/" + stk.top() + res;
            stk.pop();
        }
        return res.empty()? "/" : res;
    }
};
```
