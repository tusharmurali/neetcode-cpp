# 682. Baseball Game

- **Difficulty:** Easy  
- **Pattern:** Stack  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/baseball-game/>  
- **NeetCode:** <https://neetcode.io/problems/baseball-game>  
- **Video:** <https://www.youtube.com/watch?v=Id_tqGdsZQI>  
- **Video approach:** 1. Stack - I  

[← Back to index](../INDEX.md)

## 1. Stack - I ▶ video

A stack is perfect for this problem because each operation depends on the most recent scores. When we see `+`, we need the last two scores. When we see `D`, we need the last score. When we see `C`, we need to remove the last score. A stack gives us efficient access to these recent elements.

```cpp
class Solution {
public:
    int calPoints(vector<string>& operations) {
        vector<int> stack;
        for (const string& op : operations) {
            if (op == "+") {
                int top = stack.back(); stack.pop_back();
                int newTop = top + stack.back();
                stack.push_back(top);
                stack.push_back(newTop);
            } else if (op == "D") {
                stack.push_back(2 * stack.back());
            } else if (op == "C") {
                stack.pop_back();
            } else {
                stack.push_back(stoi(op));
            }
        }
        return accumulate(stack.begin(), stack.end(), 0);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Stack - II

This approach is similar to the first one, but we maintain a running total as we process operations instead of computing the sum at the end. Whenever we add a score, we add it to our result. When we remove a score with `C`, we subtract it. This gives us the same answer but avoids a final pass through the stack.

```cpp
class Solution {
public:
    int calPoints(vector<string>& ops) {
        stack<int> stack;
        int res = 0;
        for (const string& op : ops) {
            if (op == "+") {
                int top = stack.top(); stack.pop();
                int newTop = top + stack.top();
                stack.push(top);
                stack.push(newTop);
                res += newTop;
            } else if (op == "D") {
                stack.push(2 * stack.top());
                res += stack.top();
            } else if (op == "C") {
                res -= stack.top();
                stack.pop();
            } else {
                stack.push(stoi(op));
                res += stack.top();
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0682-baseball-game.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int calPoints(vector<string>& ops) {
        stack<int> stack;
        int sum =  0;
        
        for (int i = 0; i < ops.size(); i++){
            if (ops[i] == "+"){
                int first = stack.top();
                stack.pop();
                
                int second = stack.top();
                
                stack.push(first);
                
                stack.push(first + second);
                
                sum += first + second;
            }
            
            else if (ops[i] == "D"){
                sum += 2 * stack.top();
                stack.push(2 * stack.top());
            }
            
            else if (ops[i] == "C"){
                sum -= stack.top();
                stack.pop();
            }
            
            else{
                sum += stoi(ops[i]);
                stack.push(stoi(ops[i]));
            }
        }
        
        return sum;
        
        
    }
};
```
