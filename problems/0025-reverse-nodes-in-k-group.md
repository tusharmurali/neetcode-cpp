# 25. Reverse Nodes In K Group

- **Difficulty:** Hard  
- **Pattern:** Linked List  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/reverse-nodes-in-k-group/>  
- **NeetCode:** <https://neetcode.io/problems/reverse-nodes-in-k-group>  
- **Video:** <https://www.youtube.com/watch?v=1UOPsfP85V4>  

[← Back to index](../INDEX.md)

## 1. Recursion

To reverse nodes in groups of **k**, we first check whether the current segment contains at least **k** nodes.

- If **fewer than k**, we leave the nodes as they are.
- If we **do** have k nodes, then:
    1. **Recursively** reverse the rest of the list starting from the node after these k nodes.
    2. Then reverse the current group of k nodes.
    3. Attach the reversed group to the already-processed remainder.

This gives a clean top-down approach:
**solve the rest of the list first, then fix the current group.**

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
    ListNode* reverseKGroup(ListNode* head, int k) {
        ListNode* cur = head;
        int group = 0;
        while (cur != nullptr && group < k) {
            cur = cur->next;
            group++;
        }

        if (group == k) {
            cur = reverseKGroup(cur, k);
            while (group-- > 0) {
                ListNode* tmp = head->next;
                head->next = cur;
                cur = head;
                head = tmp;
            }
            head = cur;
        }
        return head;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(\frac{n}{k})$

## 2. Iteration

We reverse the list **one k-sized group at a time** using pointers, without recursion.

Key ideas:

- Use a **dummy node** before the head to simplify edge cases.
- For each step, we:
    1. Find the **k-th node** from the current group's previous node.
        - If there aren't `k` nodes left, we stop (leave the rest as-is).
    2. Reverse the nodes in this k-sized segment.
    3. Re-connect the reversed segment back into the list.
    4. Move forward to the next group.

By repeating this process, we reverse every full group of `k` nodes while keeping the rest of the list intact.

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
    ListNode* reverseKGroup(ListNode* head, int k) {
        ListNode* dummy = new ListNode(0, head);
        ListNode* groupPrev = dummy;

        while (true) {
            ListNode* kth = getKth(groupPrev, k);
            if (!kth) {
                break;
            }
            ListNode* groupNext = kth->next;

            ListNode* prev = kth->next;
            ListNode* curr = groupPrev->next;
            while (curr != groupNext) {
                ListNode* tmp = curr->next;
                curr->next = prev;
                prev = curr;
                curr = tmp;
            }

            ListNode* tmp = groupPrev->next;
            groupPrev->next = kth;
            groupPrev = tmp;
        }
        return dummy->next;
    }

private:
    ListNode* getKth(ListNode* curr, int k) {
        while (curr && k > 0) {
            curr = curr->next;
            k--;
        }
        return curr;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0025-reverse-nodes-in-k-group.cpp` in the NeetCode repo)

```cpp
/*
    Given head of linked list, reverse nodes of list k at a time
    Ex. head = [1,2,3,4,5], k = 2 -> [2,1,4,3,5]

    Maintain prev, curr, & temp pointers to reverse, count k times

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
    ListNode* reverseKGroup(ListNode* head, int k) {
        ListNode* dummy = new ListNode();
        dummy->next = head;
        
        ListNode* prev = dummy;
        ListNode* curr = dummy->next;
        ListNode* temp = NULL;
        
        int count = k;
        
        while (curr != NULL) {
            if (count > 1) {
                temp = prev->next;
                prev->next = curr->next;
                curr->next = curr->next->next;
                prev->next->next = temp;

                count--;
            } else {
                prev = curr;
                curr = curr->next;
                count = k;
                
                ListNode* end = curr;
                for (int i = 0; i < k; i++) {
                    if (end == NULL) {
                        return dummy->next;
                    }
                    end = end->next;
                }
            }
        }
        
        return dummy->next;
    }
};
```
