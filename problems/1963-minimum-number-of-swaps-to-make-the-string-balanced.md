# 1963. Minimum Number of Swaps to Make The String Balanced

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-number-of-swaps-to-make-the-string-balanced/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-number-of-swaps-to-make-the-string-balanced>  
- **Video:** <https://www.youtube.com/watch?v=3YDBT9ZrfaU>  

[← Back to index](../INDEX.md)

## 1. Stack

A balanced string has every `]` matched with a preceding `[`. We use a `stack` to track unmatched opening brackets. When we see `[`, we push it. When we see `]` and the `stack` is not empty, we pop (the bracket is matched). If the `stack` is empty when we see `]`, that closing bracket is unmatched.

After processing, the `stack` contains only unmatched `[` brackets. Since the string has equal counts of `[` and `]`, the number of unmatched `[` equals the number of unmatched `]`. Each swap fixes two unmatched pairs, so we need `(unmatched + 1) / 2` swaps.

```cpp
class Solution {
public:
    int minSwaps(string s) {
        vector<char> stack;
        for (char c : s) {
            if (c == '[') {
                stack.push_back(c);
            } else if (!stack.empty()) {
                stack.pop_back();
            }
        }
        return (stack.size() + 1) / 2;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Greedy - I

Instead of tracking opening brackets, we can track the imbalance directly. We maintain a `close` counter that increases for `]` and decreases for `[`. The `max` value this counter reaches tells us the worst-case imbalance, meaning the maximum number of unmatched closing brackets at any point.

Since each swap can fix at most `2` unmatched brackets, the number of swaps needed is `(max_imbalance + 1) / 2`.

```cpp
class Solution {
public:
    int minSwaps(string s) {
        int close = 0, maxClose = 0;
        for (auto& c : s) {
            if (c == '[') close--;
            else close++;
            maxClose = max(maxClose, close);
        }
        return (maxClose + 1) / 2;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Greedy - II

This approach directly simulates the `stack` without actually using a `stack` data structure. We use a counter `stackSize` that increments for `[` and decrements for `]` only if there is something to match (`stackSize > 0`). The final counter value represents unmatched opening brackets.

This is equivalent to the `stack` approach but uses `O(1)` space since we only track the `count`, not the actual characters.

```cpp
class Solution {
public:
    int minSwaps(string s) {
        int stackSize = 0;
        for (auto& c : s) {
            if (c == '[') stackSize++;
            else if (stackSize > 0) stackSize--;
        }
        return (stackSize + 1) / 2;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/1963-minimum-number-of-swaps-to-make-the-string-balanced.cpp` in the NeetCode repo)

```cpp
/*
    Approach: 
    Just check which '[' brackes are wrongly placed correct that bracket.
    use stack to keep track of bracket
    
    Time complexity : O(n)
    Space complexity: O(n)

    n is length of the string. 
*/

class Solution {
public:
    int minSwaps(string s) {

        int answer=0;

        stack<char> stc;
        stc.push(']'); 

        int n = s.size();

        for(int i=0;i<n;i++){
            char top = stc.top();

            if(s[i]==']'){

                // is the '[' bracket correctly placed
                // if yes then just pop
                if (top=='[') {
                    stc.pop();
                }
                // if '[' is not correctly placed 
                // then correct it (push '[') 
                else{ 
                    stc.push('[');
                    answer++;
                }
            }
            else{
                stc.push('[');
            }
        }
        return answer;
    }
};
```
