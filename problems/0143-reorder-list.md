# 143. Reorder List

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/reorder-list/>  
- **NeetCode:** <https://neetcode.io/problems/reorder-linked-list>  
- **Video:** <https://www.youtube.com/watch?v=S5bfdUTrKLM>  
- **Video approach:** 3. Reverse And Merge  

[← Back to index](../INDEX.md)

## 1. Brute Force

To reorder the linked list in the pattern:

**L0 → Ln → L1 → L(n−1) → L2 → ...**

A straightforward approach is to **store all nodes in an array**.
Once stored, we can easily access nodes from both the start and end using two pointers.
By alternately linking nodes from the front (index `i`) and back (index `j`), we can reshape the list in the required order.

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
    void reorderList(ListNode* head) {
        if (!head) return;

        vector<ListNode*> nodes;
        ListNode* cur = head;
        while (cur) {
            nodes.push_back(cur);
            cur = cur->next;
        }

        int i = 0, j = nodes.size() - 1;
        while (i < j) {
            nodes[i]->next = nodes[j];
            i++;
            if (i >= j) break;
            nodes[j]->next = nodes[i];
            j--;
        }

        nodes[i]->next = nullptr;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Recursion

This recursive approach reorders the list by pairing nodes from the **front** and **back** during the recursion unwind phase.

The idea is:

- Move to the end of the list using recursion.
- On the way back up (unwinding), connect the current node from the end (`cur`) to the corresponding node from the front (`root`).
- Advance the front pointer (`root`) step-by-step as recursion unwinds.
- Stop when the pointers meet or cross.

Recursion naturally processes the list from back to front, making it convenient to match front and back nodes without using extra lists.

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
    void reorderList(ListNode* head) {
        head = rec(head, head->next);
    }

private:
    ListNode* rec(ListNode* root, ListNode* cur) {
        if (cur == nullptr) {
            return root;
        }

        root = rec(root, cur->next);
        if (root == nullptr) {
            return nullptr;
        }

        ListNode* tmp = nullptr;
        if (root == cur || root->next == cur) {
            cur->next = nullptr;
        } else {
            tmp = root->next;
            root->next = cur;
            cur->next = tmp;
        }

        return tmp;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Reverse And Merge ▶ video

To reorder the list into the pattern
**L1 → Ln → L2 → Ln−1 → L3 → Ln−2 → ...**,
we can break the problem into **three simple steps**:

1. **Find the middle** of the linked list using `slow` and `fast` pointers.
   This splits the list into two halves.

2. **Reverse the second half** of the list.
   Doing this makes it easy to merge nodes from the front and back alternately.

3. **Merge the two halves** one-by-one:
   Take one node from the first half (`first`), then one from the reversed second half (`second`), and repeat.

This method is clean, intuitive, and uses only `O(1)` extra space.

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
    void reorderList(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head->next;
        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;
            fast = fast->next->next;
        }

        ListNode* second = slow->next;
        ListNode* prev = slow->next = nullptr;
        while (second != nullptr) {
            ListNode* tmp = second->next;
            second->next = prev;
            prev = second;
            second = tmp;
        }

        ListNode* first = head;
        second = prev;
        while (second != nullptr) {
            ListNode* tmp1 = first->next;
            ListNode* tmp2 = second->next;
            first->next = second;
            second->next = tmp1;
            first = tmp1;
            second = tmp2;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0143-reorder-list.cpp` in the NeetCode repo)

```cpp
/*
    Given head of linked-list, reorder list alternating outside in
    Ex. head = [1,2,3,4] -> [1,4,2,3], head = [1,2,3,4,5] -> [1,5,2,4,3]

    Find middle node, split in half, reverse 2nd half of list, merge

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
class Solution {
public:
    void reorderList(ListNode* head) {
        if (head->next == NULL) {
            return;
        }
        
        ListNode* prev = NULL;
        ListNode* slow = head;
        ListNode* fast = head;
        
        while (fast != NULL && fast->next != NULL) {
            prev = slow;
            slow = slow->next;
            fast = fast->next->next;
        }
        
        prev->next = NULL;
        
        ListNode* l1 = head;
        ListNode* l2 = reverse(slow);
        
        merge(l1, l2);
    }
private:
    ListNode* reverse(ListNode* head) {
        ListNode* prev = NULL;
        ListNode* curr = head;
        ListNode* next = curr->next;
        
        while (curr != NULL) {
            next = curr->next;
            curr->next = prev;
            prev = curr;
            curr = next;
        }
        
        return prev;
    }
    void merge(ListNode* l1, ListNode* l2) {
        while (l1 != NULL) {
            ListNode* p1 = l1->next;
            ListNode* p2 = l2->next;
            
            l1->next = l2;
            if (p1 == NULL) {
                break;
            }
            l2->next = p1;
            
            l1 = p1;
            l2 = p2;
        }
    }
};
```
