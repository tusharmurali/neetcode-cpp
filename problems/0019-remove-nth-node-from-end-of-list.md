# 19. Remove Nth Node From End of List

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/remove-nth-node-from-end-of-list/>  
- **NeetCode:** <https://neetcode.io/problems/remove-node-from-end-of-linked-list>  
- **Video:** <https://www.youtube.com/watch?v=XVuQxVej6y8>  
- **Video approach:** 4. Two Pointers  

[← Back to index](../INDEX.md)

## 1. Brute Force

We store all nodes in an array so we can directly access the node that is `n` positions from the end.  
Once we know which node to delete, we simply adjust the `next` pointer of the previous node.

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
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        vector<ListNode*> nodes;
        ListNode* cur = head;
        while (cur != nullptr) {
            nodes.push_back(cur);
            cur = cur->next;
        }

        int removeIndex = nodes.size() - n;
        if (removeIndex == 0) {
            return head->next;
        }

        nodes[removeIndex - 1]->next = nodes[removeIndex]->next;
        return head;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(N)$

## 2. Iteration (Two Pass)

We first count how many nodes are in the list.  
Once we know the total length, the node to delete is at position `N - n` from the start.  
We run a second pass to reach the node just before it and skip it.

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
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        int N = 0;
        ListNode* cur = head;
        while (cur != nullptr) {
            N++;
            cur = cur->next;
        }

        int removeIndex = N - n;
        if (removeIndex == 0) {
            return head->next;
        }

        cur = head;
        for (int i = 0; i < N - 1; i++) {
            if ((i + 1) == removeIndex) {
                cur->next = cur->next->next;
                break;
            }
            cur = cur->next;
        }
        return head;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(1)$

## 3. Recursion

Recursion naturally processes the list from the end toward the start.
When the recursive calls unwind, we count backwards.
When the count reaches the nth node from the end, we skip it by returning `head.next` instead of the current node.

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
    ListNode* rec(ListNode* head, int& n) {
        if (!head) {
            return NULL;
        }

        head -> next = rec(head -> next, n);
        n--;
        if (n == 0) {
            return head -> next;
        }
        return head;
    }

    ListNode* removeNthFromEnd(ListNode* head, int n) {
        return rec(head, n);
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(N)$ for recursion stack.

## 4. Two Pointers ▶ video

Use two pointers so that the gap between them is exactly `n`.
Move the right pointer `n` steps ahead first.
Then move both pointers together.
When the right pointer reaches the end, the left pointer will be just before the node we must remove.
This avoids a separate length-counting pass, while still traversing the list in `O(N)` time.
The key benefit is that the `n`-node gap tells us where to delete without storing nodes or computing the length first.

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
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode* dummy = new ListNode(0, head);
        ListNode* left = dummy;
        ListNode* right = head;

        while (n > 0) {
            right = right->next;
            n--;
        }

        while (right != nullptr) {
            left = left->next;
            right = right->next;
        }

        left->next = left->next->next;
        return dummy->next;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0019-remove-nth-node-from-end-of-list.cpp` in the NeetCode repo)

```cpp
/*
    Given head of a linked list, remove nth node from end of list
    Ex. head = [1,2,3,4,5], n = 2 -> [1,2,3,5]

    Create 2 pointers "n" apart, iterate until end, will be at nth

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
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        if (head->next == NULL) {
            return NULL;
        }
        
        ListNode* slow = head;
        ListNode* fast = head;
        
        while (n > 0) {
            fast = fast->next;
            n--;
        }
        
        if (fast == NULL) {
            return head->next;
        }
        
        while (fast->next != NULL) {
            slow = slow->next;
            fast = fast->next;
        }
        
        slow->next = slow->next->next;
        return head;
    }
};
```
