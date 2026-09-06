# 141. Linked List Cycle

- **Difficulty:** Easy  
- **Pattern:** Linked List  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/linked-list-cycle/>  
- **NeetCode:** <https://neetcode.io/problems/linked-list-cycle-detection>  
- **Video:** <https://www.youtube.com/watch?v=gBTe7lFR3vc>  

[← Back to index](../INDEX.md)

## 1. Hash Set

To detect whether a linked list has a cycle, one simple idea is to **remember every node we visit**.  
As we move forward through the list, if we ever reach a node we’ve already seen before, it means the list loops back on itself — so a cycle exists.

If we reach the end (`null`) without repeating a node, then there is no cycle.

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
    bool hasCycle(ListNode* head) {
        unordered_set<ListNode*> seen;
        ListNode* cur = head;
        while (cur) {
            if (seen.find(cur) != seen.end()) {
                return true;
            }
            seen.insert(cur);
            cur = cur->next;
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Fast And Slow Pointers

We use two pointers moving through the list at different speeds:

- `slow` moves one step at a time
- `fast` moves two steps at a time

If the list has a cycle, the `fast` pointer will eventually "lap" the `slow` pointer, meaning they will meet at some node inside the cycle.

If the list has no cycle, the `fast` pointer will reach the end (`null`) and the loop stops.

This method is efficient and uses constant extra space.

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
    bool hasCycle(ListNode* head) {
        ListNode* fast = head;
        ListNode* slow = head;

        while (fast != nullptr && fast->next != nullptr) {
            fast = fast->next->next;
            slow = slow->next;

            if (fast == slow) {
                return true;
            }
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0141-linked-list-cycle.cpp` in the NeetCode repo)

```cpp
/*
    Given head of a linked list, determine if it has a cycle in it

    Slow/fast pointers, if they ever intersect then there's a cycle

    Time: O(n)
    Space: O(1)
*/

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    bool hasCycle(ListNode *head) {
        if (head == NULL) {
            return false;
        }
        
        ListNode* slow = head;
        ListNode* fast = head;
        
        while (fast->next != NULL && fast->next->next != NULL) {
            slow = slow->next;
            fast = fast->next->next;
            if (slow == fast) {
                return true;
            }
        }
        
        return false;
    }
};
```
