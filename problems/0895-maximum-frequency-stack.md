# 895. Maximum Frequency Stack

- **Difficulty:** Hard  
- **Pattern:** Stack  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/maximum-frequency-stack/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-frequency-stack>  
- **Video:** <https://www.youtube.com/watch?v=Z6idIicFDOE>  
- **Video approach:** 3. Stack Of Stacks (Hash Map)  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to maintain a regular stack along with a frequency count for each element. When we need to pop, we find the maximum frequency among all elements, then scan backwards through the stack to find the most recent element with that frequency. While simple to understand, this requires scanning the entire stack on every pop operation.

```cpp
class FreqStack {
private:
    unordered_map<int, int> cnt;
    vector<int> stack;

public:
    FreqStack() {}

    void push(int val) {
        stack.push_back(val);
        cnt[val]++;
    }

    int pop() {
        int maxCnt = 0;
        for (auto& [_, frequency] : cnt) {
            maxCnt = max(maxCnt, frequency);
        }
        int i = stack.size() - 1;
        while (cnt[stack[i]] != maxCnt) {
            i--;
        }
        int val = stack[i];
        stack.erase(stack.begin() + i);
        cnt[val]--;
        return val;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for each $push()$ function call.
    - $O(n)$ time for each $pop()$ function call.
- Space complexity: $O(n)$

> Where $n$ is the number of elements in the stack.

## 2. Heap

We can use a max-heap to efficiently retrieve the element that should be popped next. Each heap entry stores three pieces of information: the element's frequency, its insertion order (index), and the value itself. By prioritizing higher frequencies and then more recent insertions, the heap always gives us the correct element to pop in logarithmic time.

```cpp
class FreqStack {
private:
    priority_queue<vector<int>> heap; // {frequency, index, value}
    unordered_map<int, int> cnt;
    int index;

public:
    FreqStack() : index(0) {}

    void push(int val) {
        cnt[val]++;
        heap.push({cnt[val], index++, val});
    }

    int pop() {
        auto top = heap.top();
        heap.pop();
        int val = top[2];
        cnt[val]--;
        return val;
    }
};
```

**Complexity**

- Time complexity:
    - $O(\log n)$ time for each $push()$ function call.
    - $O(\log n)$ time for each $pop()$ function call.
- Space complexity: $O(n)$

> Where $n$ is the number of elements in the stack.

## 3. Stack Of Stacks (Hash Map) ▶ video

The key insight is that we can group elements by their frequency level. When an element is pushed for the first time, it goes into stack `1`. When pushed again, it also goes into stack `2` (while remaining in stack `1`). This way, the stack at the highest frequency level always contains the elements we should consider popping first, and the top of that stack is the most recently pushed among them.

```cpp
class FreqStack {
public:
    unordered_map<int, int> cnt;
    unordered_map<int, stack<int>> stacks;
    int maxCnt;

    FreqStack() {
        maxCnt = 0;
    }

    void push(int val) {
        int valCnt = ++cnt[val];
        if (valCnt > maxCnt) {
            maxCnt = valCnt;
            stacks[valCnt] = stack<int>();
        }
        stacks[valCnt].push(val);
    }

    int pop() {
        int res = stacks[maxCnt].top();
        stacks[maxCnt].pop();
        cnt[res]--;
        if (stacks[maxCnt].empty()) {
            maxCnt--;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for each $push()$ function call.
    - $O(1)$ time for each $pop()$ function call.
- Space complexity: $O(n)$

> Where $n$ is the number of elements in the stack.

## 4. Stack Of Stacks (Dynamic Array)

Instead of using a hash map for frequency-indexed stacks, we can use a dynamic array (list). The index in the array represents the frequency level. When an element reaches a new frequency, we extend the array if needed. The last non-empty stack in the array always corresponds to the maximum frequency, eliminating the need to track `maxCnt` separately.

```cpp
class FreqStack {
public:
    unordered_map<int, int> cnt;
    vector<stack<int>> stacks;

    FreqStack() {
        stacks.push_back(stack<int>());
    }

    void push(int val) {
        int valCnt = ++cnt[val];
        if (valCnt == stacks.size()) {
            stacks.push_back(stack<int>());
        }
        stacks[valCnt].push(val);
    }

    int pop() {
        stack<int>& topStack = stacks.back();
        int res = topStack.top();
        topStack.pop();
        if (topStack.empty()) {
            stacks.pop_back();
        }
        cnt[res]--;
        return res;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for each $push()$ function call.
    - $O(1)$ time for each $pop()$ function call.
- Space complexity: $O(n)$

> Where $n$ is the number of elements in the stack.

## Standalone solution file (`cpp/0895-maximum-frequency-stack.cpp` in the NeetCode repo)

```cpp
class FreqStack {
    unordered_map<int, int> cnt;
    vector<vector<int>> stacks;

public:
    void push(int val) {
        int k = ++cnt[val];
        if (k > stacks.size())
            stacks.push_back({val});
        else
            stacks[k - 1].push_back(val);
    }

    int pop() {
        int val = stacks.back().back();
        stacks.back().pop_back();
        if (stacks.back().empty())
            stacks.pop_back();
        --cnt[val];
        return val;
    }
};
```
