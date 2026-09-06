# 708. Insert into a Sorted Circular Linked List

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/insert-into-a-sorted-circular-linked-list/>  
- **NeetCode:** <https://neetcode.io/problems/insert-into-a-sorted-circular-linked-list>  

[← Back to index](../INDEX.md)

## 1. Two-Pointers Iteration

In a sorted circular linked list, we need to find the right spot to insert while maintaining sorted order. There are three cases to consider: the value fits between two existing nodes, the value is a new maximum or minimum (insert at the tail/head boundary), or all nodes have the same value.
We use two pointers to traverse the list, looking for the gap where our value belongs. The tail-to-head boundary is special because it's where the values wrap around from largest to smallest.
If we traverse the entire list without finding a spot, it means all values are equal, so we can insert anywhere.

```cpp
class Solution {
public:
    Node* insert(Node* head, int insertVal) {
        if (head == nullptr) {
            Node* newNode = new Node(insertVal, nullptr);
            newNode->next = newNode;
            return newNode;
        }

        Node* prev = head;
        Node* curr = head->next;
        bool toInsert = false;

        do {
            if (prev->val <= insertVal && insertVal <= curr->val) {
                // Case 1
                toInsert = true;
            } else if (prev->val > curr->val) {
                // Case 2
                if (insertVal >= prev->val || insertVal <= curr->val)
                    toInsert = true;
            }

            if (toInsert) {
                prev->next = new Node(insertVal, curr);
                return head;
            }

            prev = curr;
            curr = curr->next;
        } while (prev != head);

        // Case 3
        prev->next = new Node(insertVal, curr);
        return head;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(1)$

> Where $N$ is the size of the list.
