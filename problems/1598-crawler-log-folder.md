# 1598. Crawler Log Folder

- **Difficulty:** Easy  
- **Pattern:** Stack  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/crawler-log-folder/>  
- **NeetCode:** <https://neetcode.io/problems/crawler-log-folder>  
- **Video:** <https://www.youtube.com/watch?v=Ur3saIXP7ro>  

[← Back to index](../INDEX.md)

## 1. Stack

A file system path can be naturally modeled using a stack. Moving into a folder pushes onto the stack, while moving to the parent folder pops from the stack. The operation `"./"` does nothing (stay in current folder). At the end, the stack's size represents how deep we are from the main folder, which equals the minimum operations needed to return.

```cpp
class Solution {
public:
    int minOperations(vector<string>& logs) {
        stack<string> st;
        for (auto& log : logs) {
            if (log == "../") {
                if (!st.empty()) {
                    st.pop();
                }
            } else if (log != "./") {
                st.push(log);
            }
        }
        return st.size();
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Iteration

We do not actually need to store the folder names since we only care about the depth. A simple counter can track how many levels deep we are. Moving into a folder increments the counter, moving to parent decrements it (but never below `0` since we cannot go above the main folder), and `"./"` leaves it unchanged.

```cpp
class Solution {
public:
    int minOperations(vector<string>& logs) {
        int res = 0;
        for (auto& log : logs) {
            if (log == "./") {
                continue;
            }
            if (log == "../") {
                res = max(0, res - 1);
            } else {
                res++;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
