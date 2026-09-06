# 716. Max Stack

- **Difficulty:** Hard  
- **Pattern:** Stack  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/max-stack/>  
- **NeetCode:** <https://neetcode.io/problems/max-stack>  

[← Back to index](../INDEX.md)

## 1. Two Balanced Trees

A regular stack gives us O(1) access to the top element, but finding or removing the maximum requires scanning. To support efficient `peekMax` and `popMax`, we maintain two balanced trees (or sorted sets). One tree orders elements by their insertion index (simulating stack order), while the other orders by value (for quick max access). Each element is stored as a pair of `(index, value)`. When we pop or `popMax`, we remove from both structures to keep them synchronized.

```cpp
class MaxStack {
private:
    set<pair<int, int>> stack;
    set<pair<int, int>> values;
    int cnt;

public:
    MaxStack() { cnt = 0; }

    void push(int x) {
        stack.insert({cnt, x});
        values.insert({x, cnt});
        cnt++;
    }

    int pop() {
        pair<int, int> p = *stack.rbegin();
        stack.erase(p);
        values.erase({p.second, p.first});
        return p.second;
    }

    int top() { return stack.rbegin()->second; }

    int peekMax() { return values.rbegin()->first; }

    int popMax() {
        pair<int, int> p = *values.rbegin();
        values.erase(p);
        stack.erase({p.second, p.first});
        return p.first;
    }
};
```

**Complexity**

- Time Complexity: $O(\log N)$ for each operation except for initialization. All operations other than initialization involve finding/inserting/removing elements in a balanced tree once or twice. In general, the upper bound of time complexity for each of them is $O(\log N)$. However, note that `top` and `peekMax` operations, which require only the last element in a balanced tree, can be done in $O(1)$ with `set::rbegin()` in C++ and special handling on the last element of `SortedList` in Python. However, `last` for `TreeSet` in Java hasn't implemented similar optimization yet, so we have to get the last element in $O(\log N)$.

- Space complexity: $O(N)$ the maximum size of the two balanced trees.

> Where $N$ is the number of elements to add to the stack.

## 2. Heap + Lazy Update

We can use a standard stack for regular push/pop/top operations and a max heap to quickly find the maximum. The challenge is that removing an element from one structure does not automatically remove it from the other. We solve this with lazy deletion: when we remove an element, we record its index in a `removed` set. Before accessing the top of the `stack` or `heap`, we skip over any elements that have been marked as removed. This defers the actual cleanup until it is needed.

```cpp
class MaxStack {
private:
    stack<pair<int, int>> stk;
    priority_queue<pair<int, int>> heap;
    unordered_set<int> removed;
    int cnt;

public:
    MaxStack() { cnt = 0; }

    void push(int x) {
        stk.push({x, cnt});
        heap.push({x, cnt});
        cnt++;
    }

    int pop() {
        while (removed.count(stk.top().second)) {
            stk.pop();
        }

        const pair<int, int> p = stk.top();
        stk.pop();
        removed.insert(p.second);

        return p.first;
    }

    int top() {
        while (removed.count(stk.top().second)) {
            stk.pop();
        }

        return stk.top().first;
    }

    int peekMax() {
        while (removed.count(heap.top().second)) {
            heap.pop();
        }

        return heap.top().first;
    }

    int popMax() {
        while (removed.count(heap.top().second)) {
            heap.pop();
        }

        const pair<int, int> p = heap.top();
        heap.pop();
        removed.insert(p.second);

        return p.first;
    }
};
```

**Complexity**

- Time Complexity:
    - `push`: $O(\log N)$. It costs $O(\log N)$ to add an element to the `heap` and $O(1)$ to add it to the `stack`.
    - The amortized time complexity of operations caused by a single `pop` / `popMax` call is $O(\log N)$. For a `pop` call, we first remove the last element in the `stack` and add its ID to `removed` in $O(1)$, resulting in the deletion of the top element in the `heap` in the future (when `peekMax` or `popMax` is called), which has a time complexity of $O(\log N)$. Similarly, `popMax` needs $O(\log N)$ immediately and $O(1)$ for the operations later. Note that because we lazy-update the two data structures, future operations might never happen in some cases. However, even in the worst cases, the upper bound of the amortized time complexity is still only $O(\log N)$.
    - `top`: $O(1)$, excluding the time cost related to `popMax` calls we discussed above.
    - `peekMax`: $O(1)$, excluding the time cost related to `pop` calls we discussed above.

- Space Complexity: $O(N)$, the maximum size of the `heap`, `stack`, and `removed`.

> Where $N$ is the number of elements to add to the stack.
