# 232. Implement Queue using Stacks

- **Difficulty:** Easy  
- **Pattern:** Stack  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/implement-queue-using-stacks/>  
- **NeetCode:** <https://neetcode.io/problems/implement-queue-using-stacks>  
- **Video:** <https://www.youtube.com/watch?v=eanwa3ht3YQ>  
- **Video approach:** 2. Using Two Stacks (Amortized Complexity)  

[← Back to index](../INDEX.md)

## 1. Using Two Stacks (Brute Force)

A stack is LIFO (last in, first out) while a queue is FIFO (first in, first out).
To simulate a queue, we need to reverse the order of elements.
By transferring all elements except the bottom one to a second stack, popping the bottom, and transferring back, we can access the first element.
This approach is simple but inefficient since every pop/peek requires moving all elements twice.

```cpp
class MyQueue {
private:
    stack<int> stack1;
    stack<int> stack2;

public:
    MyQueue() {}

    void push(int x) {
        stack1.push(x);
    }

    int pop() {
        while (stack1.size() > 1) {
            stack2.push(stack1.top());
            stack1.pop();
        }
        int res = stack1.top();
        stack1.pop();
        while (!stack2.empty()) {
            stack1.push(stack2.top());
            stack2.pop();
        }
        return res;
    }

    int peek() {
        while (stack1.size() > 1) {
            stack2.push(stack1.top());
            stack1.pop();
        }
        int res = stack1.top();
        while (!stack2.empty()) {
            stack1.push(stack2.top());
            stack2.pop();
        }
        return res;
    }

    bool empty() {
        return stack1.empty();
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for each $push()$ and $empty()$ function calls.
    - $O(n)$ time for each $pop()$ and $peek()$ function calls.
- Space complexity: $O(n)$

## 2. Using Two Stacks (Amortized Complexity) ▶ video

Instead of moving elements back after each pop, we can keep them in the second stack.
`stack1` handles incoming elements (push), while `stack2` holds elements in reversed order for popping.
When `stack2` is empty and we need to pop, we transfer all elements from `stack1` to `stack2` at once.
Each element is moved at most twice (once to `stack2`, once when popped), giving amortized O(1) per operation.

```cpp
class MyQueue {
private:
    stack<int> s1, s2;

public:
    MyQueue() {}

    void push(int x) {
        s1.push(x);
    }

    int pop() {
        if (s2.empty()) {
            while (!s1.empty()) {
                s2.push(s1.top());
                s1.pop();
            }
        }
        int res = s2.top();
        s2.pop();
        return res;
    }

    int peek() {
        if (s2.empty()) {
            while (!s1.empty()) {
                s2.push(s1.top());
                s1.pop();
            }
        }
        return s2.top();
    }

    bool empty() {
        return s1.empty() && s2.empty();
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for each $push()$ and $empty()$ function calls.
    - $O(1)$ amortized time for each $pop()$ and $peek()$ function calls.
- Space complexity: $O(n)$
