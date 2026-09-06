# 92. Reverse Linked List II

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/reverse-linked-list-ii/>  
- **NeetCode:** <https://neetcode.io/problems/reverse-linked-list-ii>  
- **Video:** <https://www.youtube.com/watch?v=RF_M9tX4Eag>  
- **Video approach:** 4. Iteration - II  

[← Back to index](../INDEX.md)

## 1. Recursion - I

To reverse a portion of a linked list, we first locate the sublist boundaries, disconnect it from the rest, reverse it using standard list reversal, and reconnect the pieces. A dummy node simplifies edge cases where the reversal starts at the head. The recursive reversal handles the sublist by making each node point to its predecessor.

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
    ListNode* reverseBetween(ListNode* head, int left, int right) {
        ListNode dummy(0);
        dummy.next = head;
        ListNode* prev = &dummy;

        for (int i = 0; i < left - 1; ++i) {
            prev = prev->next;
        }

        ListNode* sublistHead = prev->next;
        ListNode* sublistTail = sublistHead;
        for (int i = 0; i < right - left; ++i) {
            sublistTail = sublistTail->next;
        }

        ListNode* nextNode = sublistTail->next;
        sublistTail->next = nullptr;
        prev->next = reverseList(sublistHead);
        sublistHead->next = nextNode;

        return dummy.next;
    }

private:
    ListNode* reverseList(ListNode* head) {
        if (!head || !head->next) {
            return head;
        }

        ListNode* newHead = reverseList(head->next);
        head->next->next = head;
        head->next = nullptr;

        return newHead;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Recursion - II

This approach uses recursion to navigate to the start of the reversal range. Once `left` equals 1, we reverse the first `right` nodes using a helper that tracks the successor node (the node after the reversed portion). The key insight is that as recursion unwinds, we can rewire pointers to achieve the reversal while maintaining the connection to the rest of the list.

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
private:
    pair<ListNode*, ListNode*> reverseList(ListNode* node, int n) {
        if (n == 1) {
            return {node, node->next};
        }
        auto result = reverseList(node->next, n - 1);
        node->next->next = node;
        node->next = result.second;
        return {result.first, node->next};
    }

public:
    ListNode* reverseBetween(ListNode* head, int left, int right) {
        if (left == 1) {
            return reverseList(head, right).first;
        }
        head->next = reverseBetween(head->next, left - 1, right - 1);
        return head;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Iteration - I

The iterative approach follows the same structure as the first recursive solution but reverses the sublist using a loop instead of recursion. We traverse to find the boundaries, detach the sublist, reverse it in place using the standard three-pointer technique, and reconnect everything.

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
    ListNode* reverseBetween(ListNode* head, int left, int right) {
        ListNode dummy(0);
        dummy.next = head;
        ListNode* prev = &dummy;

        for (int i = 0; i < left - 1; ++i) {
            prev = prev->next;
        }

        ListNode* sublistHead = prev->next;
        ListNode* sublistTail = sublistHead;
        for (int i = 0; i < right - left; ++i) {
            sublistTail = sublistTail->next;
        }

        ListNode* nextNode = sublistTail->next;
        sublistTail->next = nullptr;
        prev->next = reverseList(sublistHead);
        sublistHead->next = nextNode;

        return dummy.next;
    }

private:
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
- Space complexity: $O(1)$ extra space.

## 4. Iteration - II ▶ video

This approach reverses in a single pass without explicitly detaching the sublist. After finding the node before the reversal starts, we reverse links one at a time as we traverse. The key is maintaining a reference to the original sublist head (which becomes the tail after reversal) so we can reconnect it to the node following the reversed section.

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
    ListNode* reverseBetween(ListNode* head, int left, int right) {
        ListNode dummy(0);
        dummy.next = head;
        ListNode* leftPrev = &dummy;
        ListNode* cur = head;

        for (int i = 0; i < left - 1; ++i) {
            leftPrev = cur;
            cur = cur->next;
        }

        ListNode* prev = nullptr;
        for (int i = 0; i < right - left + 1; ++i) {
            ListNode* tmpNext = cur->next;
            cur->next = prev;
            prev = cur;
            cur = tmpNext;
        }

        leftPrev->next->next = cur;
        leftPrev->next = prev;

        return dummy.next;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/0092-reverse-linked-list-ii.cpp` in the NeetCode repo)

```cpp
/*
    Given the head of a singly linked list and two integers left and right where left <= right, reverse the nodes of the list from position left to position right, and return the reversed list.
    
    Time complexity: O(n)
    Space complexity: O(1)
*/
class Solution {
public:
    ListNode* reverseBetween(ListNode* head, int left, int right) {
        ListNode* dummy = new ListNode();
        dummy->next = head;

        int i=0;
        ListNode* leftConnector = dummy,*temp = head;
        while(i<left-1){
            leftConnector = temp;
            temp = temp->next;
            i++;
        }
        ListNode* prev = NULL;
        i=0;
        while(i<right-left+1){
            ListNode* store = temp->next;
            temp->next = prev;
            prev = temp;
            temp = store;
            i++;
        }
        leftConnector->next->next = temp;
        leftConnector->next = prev;

        return dummy->next;
    }
};
```
