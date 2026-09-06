# 1472. Design Browser History

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/design-browser-history/>  
- **NeetCode:** <https://neetcode.io/problems/design-browser-history>  
- **Video:** <https://www.youtube.com/watch?v=i1G-kKnBu8k>  

[← Back to index](../INDEX.md)

## 1. Two Stacks

A browser's back and forward functionality naturally maps to two stacks. Think of browsing as a timeline where the back stack holds pages you've visited (including the current one), and the forward stack holds pages you can go forward to. When you visit a new URL, you push it onto the back stack and clear the forward stack since you've branched off onto a new path. Going back means moving pages from the back stack to the forward stack, and going forward is the reverse.

```cpp
class BrowserHistory {
private:
    stack<string> backHistory, frontHistory;

public:
    BrowserHistory(string homepage) {
        backHistory.push(homepage);
    }

    void visit(string url) {
        backHistory.push(url);
        frontHistory = stack<string>();
    }

    string back(int steps) {
        while (steps-- && backHistory.size() > 1) {
            frontHistory.push(backHistory.top());
            backHistory.pop();
        }
        return backHistory.top();
    }

    string forward(int steps) {
        while (steps-- && !frontHistory.empty()) {
            backHistory.push(frontHistory.top());
            frontHistory.pop();
        }
        return backHistory.top();
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for each $visit()$ function call.
    - $O(min(n, steps))$ time for each $back()$ and $forward()$ function calls.
- Space complexity: $O(m * n)$

> Where $n$ is the number of visited urls, $m$ is the average length of each url, and $steps$ is the number of steps we go forward or back.

## 2. Dynamic Array

Instead of two stacks, we can use a single list and a cursor pointer. The list stores all visited URLs in order, and the cursor indicates which page we're currently viewing. Going back decreases the cursor, going forward increases it. The key insight is that when we visit a new URL, we truncate the list at the current position before appending the new URL, since forward history becomes invalid.

```cpp
class BrowserHistory {
private:
    vector<string> history;
    int cur;

public:
    BrowserHistory(string homepage) {
        history.push_back(homepage);
        cur = 0;
    }

    void visit(string url) {
        cur++;
        history.resize(cur);
        history.push_back(url);
    }

    string back(int steps) {
        cur = max(0, cur - steps);
        return history[cur];
    }

    string forward(int steps) {
        cur = min((int)history.size() - 1, cur + steps);
        return history[cur];
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(n)$ time for each $visit()$ function call.
    - $O(1)$ time for each $back()$ and $forward()$ function calls.
- Space complexity: $O(m * n)$

> Where $n$ is the number of visited urls and $m$ is the average length of each url.

## 3. Dynamic Array (Optimal)

The previous approach truncates the array on each visit, which requires copying elements. We can avoid this by keeping track of the "logical" end of the array separately from its physical size. Instead of removing elements when visiting a new URL, we simply overwrite the element at the current position and update a variable that tracks how many elements are valid. This allows O(1) visit operations.

```cpp
class BrowserHistory {
private:
    vector<string> history;
    int cur, n;

public:
    BrowserHistory(string homepage) {
        history.push_back(homepage);
        cur = 0;
        n = 1;
    }

    void visit(string url) {
        cur++;
        if (cur == history.size()) {
            history.push_back(url);
            n++;
        } else {
            history[cur] = url;
            n = cur + 1;
        }
    }

    string back(int steps) {
        cur = max(0, cur - steps);
        return history[cur];
    }

    string forward(int steps) {
        cur = min(n - 1, cur + steps);
        return history[cur];
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for each $visit()$ function call.
    - $O(1)$ time for each $back()$ and $forward()$ function calls.
- Space complexity: $O(m * n)$

> Where $n$ is the number of visited urls and $m$ is the average length of each url.

## 4. Doubly Linked List

A doubly linked list provides a natural representation of browser history where each node contains a URL and pointers to the previous and next pages. We maintain a pointer to the current node. Navigating back follows the `prev` pointer, navigating forward follows the `next` pointer, and visiting a new URL creates a new node linked to the current one while discarding any forward history.

```cpp
class BrowserHistory {
    struct ListNode {
    public:
        string val;
        ListNode* prev;
        ListNode* next;

        ListNode(string val, ListNode* prev = nullptr, ListNode* next = nullptr)
            : val(val), prev(prev), next(next) {}
    };

    ListNode* cur;

public:
    BrowserHistory(string homepage) {
        cur = new ListNode(homepage);
    }

    void visit(string url) {
        cur->next = new ListNode(url, cur, nullptr);
        cur = cur->next;
    }

    string back(int steps) {
        while (cur->prev != nullptr && steps > 0) {
            cur = cur->prev;
            steps--;
        }
        return cur->val;
    }

    string forward(int steps) {
        while (cur->next != nullptr && steps > 0) {
            cur = cur->next;
            steps--;
        }
        return cur->val;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for each $visit()$ function call.
    - $O(min(n, steps))$ time for each $back()$ and $forward()$ function calls.
- Space complexity: $O(m * n)$

> Where $n$ is the number of visited urls, $m$ is the average length of each url, and $steps$ is the number of steps we go forward or back.
