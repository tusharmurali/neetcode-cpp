# 225. Implement Stack Using Queues

- **Difficulty:** Easy  
- **Pattern:** Stack  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/implement-stack-using-queues/>  
- **NeetCode:** <https://neetcode.io/problems/implement-stack-using-queues>  
- **Video:** <https://www.youtube.com/watch?v=rW4vm0-DLYc>  

[← Back to index](../INDEX.md)

## 1. Using Two Queues

A stack follows Last-In-First-Out (LIFO) order, but a queue follows First-In-First-Out (FIFO). To simulate a stack using queues, we need to reverse the order of elements on each push.
The idea is to use two queues: when pushing a new element, we add it to the empty second queue, then move all elements from the first queue behind it. This places the newest element at the front, ready to be popped first.
After rearranging, we swap the two queues so the main queue always has elements in stack order.

```cpp
class MyStack {
private:
    queue<int> q1;
    queue<int> q2;

public:
    MyStack() {}

    void push(int x) {
        q2.push(x);
        while (!q1.empty()) {
            q2.push(q1.front());
            q1.pop();
        }
        swap(q1, q2);
    }

    int pop() {
        int top = q1.front();
        q1.pop();
        return top;
    }

    int top() {
        return q1.front();
    }

    bool empty() {
        return q1.empty();
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(n)$ time for each $push()$ function call.
    - $O(1)$ time for each $pop()$ function call.
- Space complexity: $O(n)$

## 2. Using One Queue

We can achieve the same result with just one queue. The trick is to rotate the queue after each push so the newest element moves to the front.
When we add an element, we push it to the back of the queue, then dequeue and re-enqueue all the elements that were already there. This effectively moves the new element to the front.
This approach uses less space than two queues while maintaining the same time complexity for push operations.

```cpp
class MyStack {
    queue<int> q;

public:
    MyStack() {}

    void push(int x) {
        q.push(x);
        for (int i = q.size() - 1; i > 0; i--) {
            q.push(q.front());
            q.pop();
        }
    }

    int pop() {
        int top = q.front();
        q.pop();
        return top;
    }

    int top() {
        return q.front();
    }

    bool empty() {
        return q.empty();
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(n)$ time for each $push()$ function call.
    - $O(1)$ time for each $pop()$ function call.
- Space complexity: $O(n)$

## 3. Queue Of Queues

This approach takes a different perspective by nesting structures. Instead of rearranging elements, we create a new queue (or node) for each push that contains the value and a reference to the previous structure.
Each push wraps the current state inside a new container, with the new value at the front. This creates a chain where the most recent element is always immediately accessible.
In practice, this behaves like building a linked list where each node holds a value and points to the rest of the stack.

```cpp
class MyStack {
private:
    struct Node {
        int val;
        shared_ptr<Node> next;
        Node(int v, shared_ptr<Node> n) : val(v), next(n) {}
    };
    shared_ptr<Node> q;

public:
    MyStack() : q(nullptr) {}

    void push(int x) {
        q = make_shared<Node>(x, q);
    }

    int pop() {
        if (!q) return -1;
        int top = q->val;
        q = q->next;
        return top;
    }

    int top() {
        if (!q) return -1;
        return q->val;
    }

    bool empty() {
        return q == nullptr;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for each $push()$ function call.
    - $O(1)$ time for each $pop()$ function call.
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0225-implement-stack-using-queues.cpp` in the NeetCode repo)

```cpp
/*
Implement a last-in-first-out (LIFO) stack using only two queues. The implemented stack should support all the functions of a normal stack (push, top, pop, and empty).

Implement the MyStack class:

void push(int x) Pushes element x to the top of the stack.
int pop() Removes the element on the top of the stack and returns it.
int top() Returns the element on the top of the stack.
boolean empty() Returns true if the stack is empty, false otherwise.
Notes:

You must use only standard operations of a queue, which means that only push to back, peek/pop from front, size and is empty operations are valid.
Depending on your language, the queue may not be supported natively. You may simulate a queue using a list or deque (double-ended queue) as long as you use only a queue's standard operations.
 
*/
/**
 * Your MyStack object will be instantiated and called as such:
 * MyStack* obj = new MyStack();
 * obj->push(x);
 * int param_2 = obj->pop();
 * int param_3 = obj->top();
 * bool param_4 = obj->empty();
 */
class MyStack {
    queue<int>q1;
    queue<int>q2;
public:
    MyStack() {
        
    }
    
    void push(int x) {
        q1.push(x);
    }
    
    int pop() {
        while(q1.size()!=1){
            q2.push(q1.front());
                q1.pop();
        }
        int x=q1.front();
        q1.pop();
        swap(q1,q2);
        return x;
        
    }
    
    int top() {
        while(q1.size()!=1){
            q2.push(q1.front());
                q1.pop();
        }
        int x=q1.front();
        q1.pop();
        swap(q1,q2);
        q1.push(x);
        return x;
        
    }
  bool empty() {
        return(q1.empty() && q2.empty());
            
    }
};
```
