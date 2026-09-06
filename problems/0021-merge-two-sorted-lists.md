# 21. Merge Two Sorted Lists

- **Difficulty:** Easy  
- **Pattern:** Linked List  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/merge-two-sorted-lists/>  
- **NeetCode:** <https://neetcode.io/problems/merge-two-sorted-linked-lists>  
- **Video:** <https://www.youtube.com/watch?v=XIdigk956u0>  
- **Video approach:** 2. Iteration  

[← Back to index](../INDEX.md)

## 1. Recursion

Merging two sorted linked lists recursively works by always choosing the **smaller head node** of the two lists.
Whichever list has the smaller value should appear first in the merged list.
So we:

- Pick the smaller node.
- Recursively merge the rest of the lists.
- Attach the result to the chosen node.

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
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        if (!list1) {
            return list2;
        }
        if (!list2) {
            return list1;
        }
        if (list1->val <= list2->val) {
            list1->next = mergeTwoLists(list1->next, list2);
            return list1;
        } else {
            list2->next = mergeTwoLists(list1, list2->next);
            return list2;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$

> Where $n$ is the length of $list1$ and $m$ is the length of $list2$.

## 2. Iteration ▶ video

To merge two sorted linked lists iteratively, we build the result step-by-step.
We keep a pointer (`node`) to the current end of the merged list, and at each step we choose the **smaller head node** from `list1` or `list2`.

Because the lists are already sorted, whichever head is smaller must come next in the merged list.
We attach that node, move the pointer forward, and continue until one list is empty.
Finally, we attach the remaining nodes from the non-empty list.

Using a dummy node makes handling the head of the merged list simple and clean.

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
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        ListNode dummy(0);
        ListNode* node = &dummy;

        while (list1 && list2) {
            if (list1->val < list2->val) {
                node->next = list1;
                list1 = list1->next;
            } else {
                node->next = list2;
                list2 = list2->next;
            }
            node = node->next;
        }

        if (list1) {
            node->next = list1;
        } else {
            node->next = list2;
        }

        return dummy.next;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(1)$

> Where $n$ is the length of $list1$ and $m$ is the length of $list2$.

## Standalone solution file (`cpp/0021-merge-two-sorted-lists.cpp` in the NeetCode repo)

```cpp
/*
    Given heads of 2 sorted linked lists, merge into 1 sorted list
    Ex. list1 = [1,2,4], list2 = [1,3,4] -> [1,1,2,3,4,4]

    Create curr pointer, iterate thru, choose next to be lower one

    Time: O(m + n)
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
class Solution {
public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        if (list1 == NULL && list2 == NULL) {
            return NULL;
        }
        if (list1 == NULL) {
            return list2;
        }
        if (list2 == NULL) {
            return list1;
        }
        
        ListNode* dummy = new ListNode();
        ListNode *curr = dummy;
        while (list1 != NULL && list2 != NULL) {
            if (list1->val <= list2->val) {
                curr->next = list1;
                list1 = list1->next;
            } else {
                curr->next = list2;
                list2 = list2->next;
            }
            curr = curr->next;
        }
        
        if (list1 == NULL) {
            curr->next = list2;
        } else {
            curr->next = list1;
        }
        
        return dummy->next;
    }
};
```
