# 341. Flatten Nested List Iterator

- **Difficulty:** Medium  
- **Pattern:** Stack  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/flatten-nested-list-iterator/>  
- **NeetCode:** <https://neetcode.io/problems/flatten-nested-list-iterator>  
- **Video:** <https://www.youtube.com/watch?v=4ILiBgLokM8>  

[← Back to index](../INDEX.md)

## 1. Recursion (Flatten And Store Into Global List)

The nested list can contain integers or other nested lists at any depth. We can flatten the entire structure upfront using depth-first traversal. By storing all integers in a flat array during construction, subsequent `next()` and `hasNext()` calls become simple array operations.

```cpp
class NestedIterator {
private:
    vector<int> arr;
    int ptr;

    void dfs(const vector<NestedInteger> &nestedArr) {
        for (const auto &num : nestedArr) {
            if (num.isInteger()) {
                arr.push_back(num.getInteger());
            } else {
                dfs(num.getList());
            }
        }
    }

public:
    NestedIterator(vector<NestedInteger> &nestedList) {
        ptr = 0;
        dfs(nestedList);
    }

    int next() {
        return arr[ptr++];
    }

    bool hasNext() {
        return ptr < arr.size();
    }
};
```

**Complexity**

- Time complexity: $O(n + d)$
- Space complexity: $O(n + d)$

> Where $n$ is the number of integers and $d$ is the nesting depth.

## 2. Recursion (Flatten And Return)

This is a variation of the first approach where the recursive function returns a flattened list instead of modifying a global variable. Each recursive call builds and returns its own list, which gets merged into the parent's result.

```cpp
class NestedIterator {
private:
    vector<int> arr;
    int ptr;

    vector<int> dfs(const vector<NestedInteger> &nestedArr) {
        vector<int> res;
        for (const auto &num : nestedArr) {
            if (num.isInteger()) {
                res.push_back(num.getInteger());
            } else {
                vector<int> temp = dfs(num.getList());
                res.insert(res.end(), temp.begin(), temp.end());
            }
        }
        return res;
    }

public:
    NestedIterator(vector<NestedInteger> &nestedList) {
        arr = dfs(nestedList);
        ptr = 0;
    }

    int next() {
        return arr[ptr++];
    }

    bool hasNext() {
        return ptr < arr.size();
    }
};
```

**Complexity**

- Time complexity: $O(n + d)$
- Space complexity: $O(n + d)$

> Where $n$ is the number of integers and $d$ is the nesting depth.

## 3. Recursion + Stack

We can use recursion to flatten the list and store the integers in a stack. By reversing the stack after flattening, we can pop elements in the correct order. This combines recursive traversal with stack-based iteration.

```cpp
class NestedIterator {
private:
    vector<int> stack;

    void dfs(const vector<NestedInteger> &nested) {
        for (const auto &num : nested) {
            if (num.isInteger()) {
                stack.push_back(num.getInteger());
            } else {
                dfs(num.getList());
            }
        }
    }

public:
    NestedIterator(vector<NestedInteger> &nestedList) {
        dfs(nestedList);
        reverse(stack.begin(), stack.end());
    }

    int next() {
        int val = stack.back();
        stack.pop_back();
        return val;
    }

    bool hasNext() {
        return !stack.empty();
    }
};
```

**Complexity**

- Time complexity: $O(n + d)$
- Space complexity: $O(n + d)$

> Where $n$ is the number of integers and $d$ is the nesting depth.

## 4. Stack

Instead of flattening everything upfront, we can flatten lazily using a stack. We push the `NestedInteger` objects themselves onto the stack (in reverse order). When checking `hasNext()`, we unpack nested lists on demand until we find an integer at the top. This approach is more memory-efficient when we don't need to iterate through all elements.

```cpp
class NestedIterator {
private:
    vector<NestedInteger> stack;

public:
    NestedIterator(vector<NestedInteger> &nestedList) {
        stack = nestedList;
        reverse(stack.begin(), stack.end());
    }

    int next() {
        int val = stack.back().getInteger();
        stack.pop_back();
        return val;
    }

    bool hasNext() {
        while (!stack.empty()) {
            NestedInteger top = stack.back();
            if (top.isInteger()) {
                return true;
            }
            stack.pop_back();
            vector<NestedInteger> nestedList = top.getList();
            for (auto it = nestedList.rbegin(); it != nestedList.rend(); ++it) {
                stack.push_back(*it);
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n + d)$
- Space complexity: $O(n)$

> Where $n$ is the number of integers and $d$ is the nesting depth.

## Standalone solution file (`cpp/0341-flatten-nested-list-iterator.cpp` in the NeetCode repo)

```cpp
/**
 * // This is the interface that allows for creating nested lists.
 * // You should not implement it, or speculate about its implementation
 * class NestedInteger {
 *   public:
 *     // Return true if this NestedInteger holds a single integer, rather than a nested list.
 *     bool isInteger() const;
 *
 *     // Return the single integer that this NestedInteger holds, if it holds a single integer
 *     // The result is undefined if this NestedInteger holds a nested list
 *     int getInteger() const;
 *
 *     // Return the nested list that this NestedInteger holds, if it holds a nested list
 *     // The result is undefined if this NestedInteger holds a single integer
 *     const vector<NestedInteger> &getList() const;
 * };
 */

class NestedIterator {
private:
    vector<NestedInteger> nestedList;
    vector<int> stack;

    void dfs(vector<NestedInteger> nestedList) {
        for (const auto &item : nestedList) {
            if (item.isInteger()) {
                stack.push_back(item.getInteger());
            } else {
                dfs(item.getList());
            }
        }
    }

public:
    NestedIterator(vector<NestedInteger> &nestedList) : nestedList(nestedList) {
        dfs(nestedList);
        reverse(stack.begin(), stack.end());
    }
    
    int next() {
        if (!hasNext()) {
            return -1;
        }
        int retval = stack.back();
        stack.pop_back();
        return retval;
    }
    
    bool hasNext() {
        return stack.size();
    }
};

/**
 * Your NestedIterator object will be instantiated and called as such:
 * NestedIterator i(nestedList);
 * while (i.hasNext()) cout << i.next();
 */
```
