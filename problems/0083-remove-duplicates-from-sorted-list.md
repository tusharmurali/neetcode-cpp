# 83. Remove Duplicates From Sorted List

- **Difficulty:** Easy  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/remove-duplicates-from-sorted-list/>  
- **NeetCode:** <https://neetcode.io/problems/remove-duplicates-from-sorted-list>  
- **Video:** <https://www.youtube.com/watch?v=p10f-VpO4nE>  

[← Back to index](../INDEX.md)

## 1. Recursion

We solve the problem from the end of the list backward. First, we recursively remove duplicates from the rest of the list, then check if the current node duplicates its (now cleaned) next node. If so, we skip the current node by returning its next. This naturally handles chains of duplicates.

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
    ListNode* deleteDuplicates(ListNode* head) {
        if (!head || !head->next) return head;

        head->next = deleteDuplicates(head->next);
        return head->val != head->next->val ? head : head->next;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Iteration - I

Since the list is sorted, duplicates are consecutive. At each node, we skip over all following nodes with the same value by adjusting the `next` pointer. This removes entire chains of duplicates in one pass through the list.

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
    ListNode* deleteDuplicates(ListNode* head) {
        ListNode* cur = head;
        while (cur) {
            while (cur->next && cur->next->val == cur->val) {
                cur->next = cur->next->next;
            }
            cur = cur->next;
        }
        return head;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 3. Iteration - II

A slightly different structure: instead of a nested loop, we use a single loop with a conditional. If the current and next values match, we skip the next node. If they differ, we advance the pointer. This achieves the same result with cleaner control flow.

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
    ListNode* deleteDuplicates(ListNode* head) {
        ListNode* cur = head;
        while (cur && cur->next) {
            if (cur->next->val == cur->val) {
                cur->next = cur->next->next;
            } else {
                cur = cur->next;
            }
        }
        return head;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/0083-remove-duplicates-from-sorted-list.cpp` in the NeetCode repo)

```cpp
// Time Complexity is O(N).
// Space Complexity is O(1).

class Solution {
public:
    ListNode* deleteDuplicates(ListNode* head) {
      ListNode * fast = head;
      ListNode * slow = head;
      
      while(slow != NULL)
      {
        while(fast != NULL && slow->val == fast->val)
          fast = fast -> next;
        
        slow->next = fast;
        slow = slow -> next;
      }
      
      return head;
        
    }
};
```
