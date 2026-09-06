# 622. Design Circular Queue

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/design-circular-queue/>  
- **NeetCode:** <https://neetcode.io/problems/design-circular-queue>  
- **Video:** <https://www.youtube.com/watch?v=aBbsfn863oA>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach is to use a dynamic array and treat it like a regular queue. We add elements to the back and remove from the front. While this works, removing from the front requires shifting all remaining elements, making it inefficient. We check the array size against the capacity to determine if the queue is full.

```cpp
class MyCircularQueue {
private:
    vector<int> queue;
    int capacity;

public:
    MyCircularQueue(int k) {
        capacity = k;
    }

    bool enQueue(int value) {
        if (queue.size() == capacity) {
            return false;
        }
        queue.push_back(value);
        return true;
    }

    bool deQueue() {
        if (queue.empty()) {
            return false;
        }
        queue.erase(queue.begin());
        return true;
    }

    int Front() {
        return queue.empty() ? -1 : queue.front();
    }

    int Rear() {
        return queue.empty() ? -1 : queue.back();
    }

    bool isEmpty() {
        return queue.empty();
    }

    bool isFull() {
        return queue.size() == capacity;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(1)$ time for each $enQueue()$, $Front()$, $Rear()$, $isEmpty()$ and $isFull()$ function calls.
    - $O(n)$ time for each $deQueue()$ function call.
- Space complexity: $O(n)$

> Where $n$ is the size of the queue.

## 2. Array

To achieve O(1) operations, we use a fixed-size array with two pointers: `front` pointing to the first element and `rear` pointing to the last. The "circular" aspect comes from using modulo arithmetic so that when we reach the end of the array, we wrap around to the beginning. We track the current size separately to distinguish between empty and full states.

```cpp
class MyCircularQueue {
private:
    vector<int> queue;
    int size;
    int front;
    int rear;
    int capacity;

public:
    MyCircularQueue(int k) {
        queue = vector<int>(k);
        size = 0;
        front = 0;
        rear = -1;
        capacity = k;
    }

    bool enQueue(int value) {
        if (isFull()) {
            return false;
        }
        rear = (rear + 1) % capacity;
        queue[rear] = value;
        size++;
        return true;
    }

    bool deQueue() {
        if (isEmpty()) {
            return false;
        }
        front = (front + 1) % capacity;
        size--;
        return true;
    }

    int Front() {
        return isEmpty() ? -1 : queue[front];
    }

    int Rear() {
        return isEmpty() ? -1 : queue[rear];
    }

    bool isEmpty() {
        return size == 0;
    }

    bool isFull() {
        return size == capacity;
    }
};
```

**Complexity**

- Time complexity:
    - $O(n)$ time for initialization.
    - $O(1)$ time for each $enQueue()$, $deQueue()$, $Front()$, $Rear()$, $isEmpty()$ and $isFull()$ function calls.
- Space complexity: $O(n)$

> Where $n$ is the size of the queue.

## 3. Doubly Linked List

A doubly linked list allows O(1) insertions and deletions at both ends. We use dummy head and tail nodes to simplify edge cases. New elements are inserted before the tail (at the rear), and elements are removed after the head (from the front). We track remaining space to know when the queue is full.

```cpp
class MyCircularQueue {
private:
    struct ListNode {
        int val;
        ListNode* next;
        ListNode* prev;
        ListNode(int v, ListNode* n = nullptr, ListNode* p = nullptr)
            : val(v), next(n), prev(p) {}
    };

    int space;
    ListNode* left;
    ListNode* right;

public:
    MyCircularQueue(int k) {
        space = k;
        left = new ListNode(0);
        right = new ListNode(0, nullptr, left);
        left->next = right;
    }

    bool enQueue(int value) {
        if (isFull()) return false;
        ListNode* cur = new ListNode(value, right, right->prev);
        right->prev->next = cur;
        right->prev = cur;
        space--;
        return true;
    }

    bool deQueue() {
        if (isEmpty()) return false;
        ListNode* tmp = left->next;
        left->next = left->next->next;
        left->next->prev = left;
        delete tmp;
        space++;
        return true;
    }

    int Front() {
        return isEmpty() ? -1 : left->next->val;
    }

    int Rear() {
        return isEmpty() ? -1 : right->prev->val;
    }

    bool isEmpty() {
        return left->next == right;
    }

    bool isFull() {
        return space == 0;
    }
};
```

**Complexity**

- Time complexity:
    - $O(n)$ time for initialization.
    - $O(1)$ time for each $enQueue()$, $deQueue()$, $Front()$, $Rear()$, $isEmpty()$ and $isFull()$ function calls.
- Space complexity: $O(n)$

> Where $n$ is the size of the queue.

## 4. Singly Linked List

A singly linked list can also work, using less memory per node than a doubly linked list. We maintain a dummy head node and a pointer to the actual tail. New elements are added at the tail, and elements are removed from the front (after the dummy head). The only complication is updating the tail pointer when the queue becomes empty.

```cpp
class MyCircularQueue {
private:
    struct ListNode {
        int val;
        ListNode* next;
        ListNode(int v) : val(v), next(nullptr) {}
    };

    int space;
    ListNode* left;
    ListNode* right;

public:
    MyCircularQueue(int k) {
        space = k;
        left = new ListNode(0);
        right = left;
    }

    bool enQueue(int value) {
        if (isFull()) return false;

        ListNode* cur = new ListNode(value);
        if (isEmpty()) {
            left->next = cur;
            right = cur;
        } else {
            right->next = cur;
            right = cur;
        }

        space--;
        return true;
    }

    bool deQueue() {
        if (isEmpty()) return false;

        ListNode* tmp = left->next;
        left->next = left->next->next;
        delete tmp;
        if (!left->next) {
            right = left;
        }

        space++;
        return true;
    }

    int Front() {
        return isEmpty() ? -1 : left->next->val;
    }

    int Rear() {
        return isEmpty() ? -1 : right->val;
    }

    bool isEmpty() {
        return left->next == nullptr;
    }

    bool isFull() {
        return space == 0;
    }
};
```

**Complexity**

- Time complexity:
    - $O(n)$ time for initialization.
    - $O(1)$ time for each $enQueue()$, $deQueue()$, $Front()$, $Rear()$, $isEmpty()$ and $isFull()$ function calls.
- Space complexity: $O(n)$

> Where $n$ is the size of the queue.
