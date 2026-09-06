# 86. Partition List

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/partition-list/>  
- **NeetCode:** <https://neetcode.io/problems/partition-list>  
- **Video:** <https://www.youtube.com/watch?v=KT1iUciJr4g>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We need to partition the linked list so that all nodes with values less than `x` come before nodes with values greater than or equal to `x`, while preserving the original relative order within each group.

The brute force approach extracts all values into two separate lists based on the partition condition, then writes them back to the original nodes. This simplifies the logic but requires extra space proportional to the list size.

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
    ListNode* partition(ListNode* head, int x) {
        if (!head) return nullptr;

        vector<int> less, greater;
        ListNode* cur = head;

        while (cur) {
            if (cur->val < x) {
                less.push_back(cur->val);
            } else {
                greater.push_back(cur->val);
            }
            cur = cur->next;
        }

        cur = head;
        for (int val : less) {
            cur->val = val;
            cur = cur->next;
        }

        for (int val : greater) {
            cur->val = val;
            cur = cur->next;
        }

        return head;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Two Pointers

Instead of storing values in arrays, we can build two separate linked lists as we traverse: one for nodes less than `x`, one for nodes greater than or equal to `x`. Using dummy head nodes simplifies edge case handling.

At the end, we connect the tail of the "less" list to the head of the "greater" list, and terminate the "greater" list to avoid cycles. This achieves O(1) extra space by reusing the original nodes.

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
    ListNode* partition(ListNode* head, int x) {
        ListNode leftDummy(0), rightDummy(0);
        ListNode *ltail = &leftDummy, *rtail = &rightDummy;

        while (head) {
            if (head->val < x) {
                ltail->next = head;
                ltail = ltail->next;
            } else {
                rtail->next = head;
                rtail = rtail->next;
            }
            head = head->next;
        }

        ltail->next = rightDummy.next;
        rtail->next = nullptr;
        return leftDummy.next;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
