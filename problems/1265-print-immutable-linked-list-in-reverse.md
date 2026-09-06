# 1265. Print Immutable Linked List in Reverse

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/print-immutable-linked-list-in-reverse/>  
- **NeetCode:** <https://neetcode.io/problems/print-immutable-linked-list-in-reverse>  

[← Back to index](../INDEX.md)

## 1. Recursion

Recursion naturally reverses the order of operations. When we recurse to the end of the list first and then print on the way back, we effectively print in reverse. The call stack holds all the nodes, and as each call returns, it prints its node's value.

```cpp
class Solution {
public:
    void printLinkedListInReverse(ImmutableListNode* head) {
        if (head != NULL) {
            printLinkedListInReverse(head->getNext());
            head->printValue();
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the size of the linked list.

## 2. Using Stack

A stack provides Last-In-First-Out (LIFO) ordering, which is exactly what we need to reverse the print order. We traverse the list once to push all nodes onto the `stack`, then pop them one by one to print in reverse order.

```cpp
class Solution {
public:
    void printLinkedListInReverse(ImmutableListNode* head) {
        stack<ImmutableListNode*> s;
        while (head) {
            s.push(head);
            head = head->getNext();
        }

        while (!s.empty()) {
            ImmutableListNode* node = s.top();
            s.pop();
            node->printValue();
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the size of the linked list.

## 3. Square Root Decomposition

To reduce space complexity, we can divide the list into blocks of size approximately `sqrt(n)`. We only store pointers to the start of each block, requiring `O(sqrt(n))` space. For each block, we use recursion to print in reverse. Since each block is small, the recursion depth stays at `O(sqrt(n))`.

```cpp
class Solution {
public:
    void printLinkedListInReverseRecursively(ImmutableListNode* head, int size) {
        if (size && head) {
            printLinkedListInReverseRecursively(head->getNext(), size - 1);
            head->printValue();
        }
    }

    int getLinkedListSize(ImmutableListNode* head) {
        int size = 0;
        while (head) {
            size += 1;
            head = head->getNext();
        }
        return size;
    }

    void printLinkedListInReverse(ImmutableListNode* head) {
        int linkedListSize = getLinkedListSize(head);
        int blockSize = ceil(sqrt(linkedListSize));

        stack<ImmutableListNode*> blocks;
        ImmutableListNode* curr = head;
        for (int i = 0; i < linkedListSize; i++) {
            if (i % blockSize == 0) {
                blocks.push(curr);
            }
            curr = curr->getNext();
        }

        while (!blocks.empty()) {
            printLinkedListInReverseRecursively(blocks.top(), blockSize);
            blocks.pop();
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(\sqrt n)$

> Where $n$ is the size of the linked list.

## 4. Divide and Conquer

We can use the slow and fast pointer technique to find the middle of any segment. By recursively printing the second half first, then the first half, we achieve reverse order. The recursion depth is `O(log n)` because we halve the problem at each level.

```cpp
class Solution {
public:
    void helper(ImmutableListNode* start, ImmutableListNode* end) {
        if (start == NULL || start == end) {
            return;
        }
        if (start->getNext() == end) {
            start->printValue();
            return;
        }

        ImmutableListNode* slow = start;
        ImmutableListNode* fast = start;

        while (fast != end && fast->getNext() != end) {
            slow = slow->getNext();
            fast = fast->getNext()->getNext();
        }

        helper(slow, end);
        helper(start, slow);
    }

    void printLinkedListInReverse(ImmutableListNode* head) {
        helper(head, NULL);
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot \log n)$
- Space complexity: $O(\log n)$

> Where $n$ is the size of the linked list.

## 5. Constant Space

Without any extra data structures, we can print in reverse by repeatedly finding the last unprinted node. We maintain an `end` pointer that marks the boundary. Each iteration traverses from `head` to find the node just before `end`, prints it, and moves `end` backward. This uses constant space but requires `O(n)` traversals.

```cpp
class Solution {
public:
    void printLinkedListInReverse(ImmutableListNode* head) {
        ImmutableListNode* curr;
        ImmutableListNode* end = NULL;

        while (head != end) {
            curr = head;
            while (curr->getNext() != end) {
                curr = curr->getNext();
            }
            curr->printValue();
            end = curr;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n^2)$
- Space complexity: $O(1)$

> Where $n$ is the size of the linked list.
