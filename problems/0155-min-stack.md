# 155. Min Stack

- **Difficulty:** Medium  
- **Pattern:** Stack  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/min-stack/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-stack>  
- **Video:** <https://www.youtube.com/watch?v=qkLl7nAwDPo>  
- **Video approach:** 2. Two Stacks  

[← Back to index](../INDEX.md)

## 1. Brute Force

To get the minimum value, this approach simply looks through **all elements** in the stack.
Since a normal stack does not store any extra information about the minimum, the only way to find it is to temporarily remove every element, track the smallest one, and then put everything back.
It's easy to understand but slow because each `getMin` call scans the entire stack.

```cpp
class MinStack {
public:
    stack<int> stk;
    MinStack() {

    }

    void push(int val) {
        stk.push(val);
    }

    void pop() {
        stk.pop();
    }

    int top() {
        return stk.top();
    }

    int getMin() {
        stack<int> tmp;
        int mini = stk.top();
        while (stk.size()) {
            mini = min(mini, stk.top());
            tmp.push(stk.top());
            stk.pop();
        }

        while (tmp.size()) {
            stk.push(tmp.top());
            tmp.pop();
        }

        return mini;
    }
};
```

**Complexity**

- Time complexity: $O(n)$ for $getMin()$ and $O(1)$ for other operations.
- Space complexity: $O(n)$ for $getMin()$ and $O(1)$ for other operations.

## 2. Two Stacks ▶ video

Instead of searching the whole stack to find the minimum every time, we can keep a **second stack** that always stores the minimum value _up to that point_.
So whenever we push a new value, we compare it with the current minimum and store the smaller one on the `minStack`.
This guarantees that the top of `minStack` is always the minimum of the entire stack — allowing `getMin()` to work in constant time.

```cpp
class MinStack {
private:
    std::stack<int> stack;
    std::stack<int> minStack;

public:
    MinStack() {}

    void push(int val) {
        stack.push(val);
        val = std::min(val, minStack.empty() ? val : minStack.top());
        minStack.push(val);
    }

    void pop() {
        stack.pop();
        minStack.pop();
    }

    int top() {
        return stack.top();
    }

    int getMin() {
        return minStack.top();
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for all operations.
- Space complexity: $O(n)$

## 3. One Stack

This approach keeps only **one stack** and stores **encoded values** instead of the actual numbers.
The trick is to record the _difference_ between the pushed value and the current minimum.
Whenever a new minimum is pushed, we store a **negative encoded value**, which signals that the minimum has changed.
Later, when popping such a value, we can decode it to restore the previous minimum.

This way, the stack internally keeps track of all minimum updates without needing a second stack — giving constant-time operations with minimal space.

```cpp
class MinStack {
private:
    long min;
    std::stack<long> stack;

public:
    MinStack() {}

    void push(int val) {
        if (stack.empty()) {
            stack.push(0);
            min = val;
        } else {
            stack.push(val - min);
            if (val < min) min = val;
        }
    }

    void pop() {
        if (stack.empty()) return;

        long pop = stack.top();
        stack.pop();

        if (pop < 0) min = min - pop;
    }

    int top() {
        long top = stack.top();
        return (top > 0) ? (top + min) : (int)min;
    }

    int getMin() {
        return (int)min;
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for all operations.
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0155-min-stack.cpp` in the NeetCode repo)

```cpp
/*
    Design stack that supports push, pop, top, & retriving min element
    
    2 stacks, 1 normal & 1 monotonic decr, only push if lower than top
    
    Time: O(1)
    Space: O(n)
*/

class MinStack {
public:
    MinStack() {
        
    }
    
    void push(int val) {
        stk.push(val);
        
        if (minStk.empty() || val < minStk.top().first) {
            minStk.push({val, 1});
        } else if (val == minStk.top().first) {
            minStk.top().second++;
        }
    }
    
    void pop() {
        if (stk.top() == minStk.top().first) {
            minStk.top().second--;
            if (minStk.top().second == 0) {
                minStk.pop();
            }
        }
        stk.pop();
    }
    
    int top() {
        return stk.top();
    }
    
    int getMin() {
        return minStk.top().first;
    }
private:
    stack<int> stk;
    stack<pair<int, int>> minStk;
};

/**
 * Your MinStack object will be instantiated and called as such:
 * MinStack* obj = new MinStack();
 * obj->push(val);
 * obj->pop();
 * int param_3 = obj->top();
 * int param_4 = obj->getMin();
 */
```
