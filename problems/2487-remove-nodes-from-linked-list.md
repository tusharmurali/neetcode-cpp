# 2487. Remove Nodes From Linked List

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/remove-nodes-from-linked-list/>  
- **NeetCode:** <https://neetcode.io/problems/remove-nodes-from-linked-list>  
- **Video:** <https://www.youtube.com/watch?v=y783sRTezDg>  

[← Back to index](../INDEX.md)

## 1. Convert To Array

A node should be removed if there exists a larger value somewhere to its right. To check this efficiently, we first convert the linked list into an array. Then we traverse the array from right to left, keeping track of the maximum value seen so far. Any node with a value smaller than this running maximum gets removed by adjusting the previous node's pointer.

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
    ListNode* removeNodes(ListNode* head) {
        vector<ListNode*> arr;
        arr.push_back(new ListNode(0, head));
        ListNode* cur = head;

        while (cur) {
            arr.push_back(cur);
            cur = cur->next;
        }

        ListNode* rightMaxi = new ListNode(0, nullptr);
        for (int i = arr.size() - 1; i > 0; i--) {
            if (rightMaxi->val > arr[i]->val) {
                arr[i - 1]->next = rightMaxi;
            } else {
                rightMaxi = arr[i];
            }
        }

        return arr[0]->next;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Monotonic Decreasing Stack

We need to keep only nodes that have no larger value to their right. A monotonic decreasing stack naturally maintains this property. As we traverse the list, we pop any stack elements that are smaller than the current node's value. This ensures the stack always contains values in decreasing order from bottom to top, which are exactly the nodes that should remain.

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
    ListNode* removeNodes(ListNode* head) {
        vector<int> stack;
        ListNode* cur = head;

        while (cur) {
            while (!stack.empty() && cur->val > stack.back()) {
                stack.pop_back();
            }
            stack.push_back(cur->val);
            cur = cur->next;
        }

        ListNode* dummy = new ListNode();
        cur = dummy;

        for (int num : stack) {
            cur->next = new ListNode(num);
            cur = cur->next;
        }

        return dummy->next;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Recursion

Recursion lets us process the list from right to left naturally. We first recurse to the end, then on the way back, each node compares itself to whatever remains in the processed suffix. If the next node has a larger value, the current node should be removed, so we return `head.next` instead. Otherwise, we keep the current node.

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
    ListNode* removeNodes(ListNode* head) {
        if (!head) return nullptr;

        head->next = removeNodes(head->next);
        if (head->next && head->val < head->next->val) {
            return head->next;
        }
        return head;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 4. Reverse Twice

Finding the maximum to the right is hard when traversing left to right, but finding the maximum to the left is easy. By reversing the list first, the problem transforms: now we just need to keep nodes that are greater than or equal to all previous nodes. We traverse once while tracking the running maximum and remove smaller nodes. Finally, we reverse again to restore the original order.

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
    ListNode* reverse(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* cur = head;
        while (cur) {
            ListNode* tmp = cur->next;
            cur->next = prev;
            prev = cur;
            cur = tmp;
        }
        return prev;
    }

    ListNode* removeNodes(ListNode* head) {
        head = reverse(head);
        ListNode* cur = head;
        int cur_max = head->val;

        while (cur && cur->next) {
            if (cur->next->val < cur_max) {
                cur->next = cur->next->next;
            } else {
                cur_max = cur->next->val;
                cur = cur->next;
            }
        }
        return reverse(head);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
