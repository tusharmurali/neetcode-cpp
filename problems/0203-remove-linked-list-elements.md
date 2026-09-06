# 203. Remove Linked List Elements

- **Difficulty:** Easy  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/remove-linked-list-elements/>  
- **NeetCode:** <https://neetcode.io/problems/remove-linked-list-elements>  
- **Video:** <https://www.youtube.com/watch?v=JI71sxtHTng>  
- **Video approach:** 3. Iteration (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Brute Force

A straightforward approach is to extract all values we want to keep into an array, then build a new linked list from scratch.
We traverse the original list, skipping nodes with the target value, and collect the remaining values.
Finally, we create new nodes from this array and link them together.
This works but requires extra space and creates entirely new nodes.

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
    ListNode* removeElements(ListNode* head, int val) {
        vector<int> arr;
        ListNode* cur = head;

        while (cur) {
            if (cur->val != val) {
                arr.push_back(cur->val);
            }
            cur = cur->next;
        }

        if (arr.empty()) {
            return nullptr;
        }

        ListNode* res = new ListNode(arr[0]);
        cur = res;
        for (int i = 1; i < arr.size(); i++) {
            ListNode* node = new ListNode(arr[i]);
            cur->next = node;
            cur = cur->next;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Recursion

Recursion naturally fits linked list problems because each node is structurally similar to the rest of the list.
We recursively process the remainder of the list first, then decide whether to include the current node.
If the current node matches the target value, we skip it by returning the already-processed next portion.
Otherwise, we attach the current node to the processed tail and return it.

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
    ListNode* removeElements(ListNode* head, int val) {
        if (head == nullptr) return nullptr;
        head->next = removeElements(head->next, val);
        return head->val != val ? head : head->next;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Iteration ▶ video

To remove nodes in place without recursion, we use a dummy node to handle edge cases like removing the head.
We maintain two pointers: `prev` (the last valid node) and `curr` (the node being examined).
When we find a matching value, we bypass the current node by updating `prev.next`.
When the value does not match, we simply advance `prev`.

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
    ListNode* removeElements(ListNode* head, int val) {
        ListNode dummy(0, head);
        ListNode *prev = &dummy, *curr = head;

        while (curr) {
            ListNode* nxt = curr->next;
            if (curr->val == val) {
                prev->next = nxt;
            } else {
                prev = curr;
            }
            curr = nxt;
        }

        return dummy.next;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 4. Iteration Without Prev Pointer

We can simplify the iteration by always looking ahead at the next node instead of the current one.
By checking `curr.next` rather than `curr`, we can remove nodes without needing a separate `prev` pointer.
If the next node should be removed, we skip it by updating `curr.next` directly.
Otherwise, we advance `curr` to continue scanning.

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
    ListNode* removeElements(ListNode* head, int val) {
        ListNode dummy(-1, head);
        ListNode *curr = &dummy;

        while (curr->next) {
            if (curr->next->val == val) {
                curr->next = curr->next->next;
            } else {
                curr = curr->next;
            }
        }

        return dummy.next;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/0203-remove-linked-list-elements.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    ListNode* removeElements(ListNode* head, int val) {
        ListNode *dummy = new ListNode(0, head);
        ListNode *prev = dummy, *curr = head;
        
        while(curr) {
            ListNode *nxt = curr->next;
            
            if(curr->val == val)
                prev->next = nxt;
            else
                prev = curr;
            
            curr = nxt;
        }
        return dummy->next;
    }
};
```
