# 206. Reverse Linked List

- **Difficulty:** Easy  
- **Pattern:** Linked List  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/reverse-linked-list/>  
- **NeetCode:** <https://neetcode.io/problems/reverse-a-linked-list>  
- **Video:** <https://www.youtube.com/watch?v=G0_I-ZF0S38>  
- **Video approach:** 2. Iteration  

[← Back to index](../INDEX.md)

## 1. Recursion

Reversing a linked list using recursion works by thinking in terms of **"reverse the rest, then fix the pointer for the current node."**
When we recursively go to the end of the list, that last node becomes the new head.
While the recursion unwinds, each node points **backward** to the one that called it.
Finally, we set the original head's `next` to `null` to finish the reversal.

This approach uses the call stack to naturally reverse the direction of the pointers.

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */

class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        if (!head) {
            return nullptr;
        }

        ListNode* newHead = head;
        if (head->next) {
            newHead = reverseList(head->next);
            head->next->next = head;
        }
        head->next = nullptr;

        return newHead;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Iteration ▶ video

Reversing a linked list iteratively is all about **flipping pointers one step at a time**.
We walk through the list from left to right, and for each node, we redirect its `next` pointer to point to the node behind it.

To avoid losing track of the rest of the list, we keep three pointers:

- `curr` → the current node we are processing
- `prev` → the node that should come after `curr` once reversed
- `temp` → the original next node (so we don't break the chain)

By moving these pointers forward in each step, we gradually reverse the entire list.
When `curr` becomes `null`, the list is fully reversed, and `prev` points to the new head.

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */

class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* curr = head;

        while (curr) {
            ListNode* temp = curr->next;
            curr->next = prev;
            prev = curr;
            curr = temp;
        }
        return prev;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0206-reverse-linked-list.cpp` in the NeetCode repo)

```cpp
/*
    Given the head of a singly linked list, reverse list & return
    Ex. head = [1,2,3,4,5] -> [5,4,3,2,1], head = [1,2] -> [2,1]

    Maintain prev, curr pointers, iterate thru & reverse

    Time: O(n)
    Space: O(1)
*/

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution
{
public:
    ListNode *reverseList(ListNode *head)
    {
        if (head == NULL || head->next == NULL)
            return head;

        ListNode *prev = NULL;
        ListNode *curr = head;

        while (curr != NULL)
        {
            ListNode *temp = curr->next;
            curr->next = prev;
            prev = curr;
            curr = temp;
        }
        return prev;
    }
};
```
