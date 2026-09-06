# 946. Validate Stack Sequences

- **Difficulty:** Medium  
- **Pattern:** Stack  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/validate-stack-sequences/>  
- **NeetCode:** <https://neetcode.io/problems/validate-stack-sequences>  
- **Video:** <https://www.youtube.com/watch?v=mzua0r94kb8>  

[← Back to index](../INDEX.md)

## 1. Stack

We can simulate the actual push and pop operations on a stack to verify if the sequences are valid. The key insight is that whenever we push an element, we should immediately try to pop as many elements as possible that match the expected pop sequence. If the simulation completes with an empty stack, the sequences are valid.

```cpp
class Solution {
public:
    bool validateStackSequences(vector<int>& pushed, vector<int>& popped) {
        stack<int> stk;
        int i = 0;
        for (int n : pushed) {
            stk.push(n);
            while (i < popped.size() && !stk.empty() && popped[i] == stk.top()) {
                stk.pop();
                i++;
            }
        }
        return stk.empty();
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Two Pointers

Instead of using a separate stack, we can reuse the `pushed` array itself as the stack. The left portion of the array acts as our stack, eliminating the need for extra space. This works because as we process elements, we overwrite positions that are no longer needed.

```cpp
class Solution {
public:
    bool validateStackSequences(vector<int>& pushed, vector<int>& popped) {
        int l = 0, r = 0;
        for (int& num : pushed) {
            pushed[l++] = num;
            while (l > 0 && pushed[l - 1] == popped[r]) {
                r++;
                l--;
            }
        }
        return l == 0;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/0946-validate-stack-sequences.cpp` in the NeetCode repo)

```cpp
/*
  Given two integer arrays pushed and popped each with distinct values,
  return true if this could have been the result of a sequence of push
  and pop operations on an initially empty stack, or false otherwise.

  Time: O(n)
  Space: O(n)
*/

class Solution {
public:
    bool validateStackSequences(vector<int>& pushed, vector<int>& popped) {
        stack<int> stk;
        int i = 0;
        for (int num : pushed) {
            stk.push(num);
            while (!stk.empty() && stk.top() == popped[i]) {
                stk.pop();
                ++i;
            }
        }
        return stk.empty();
    }
};
```
