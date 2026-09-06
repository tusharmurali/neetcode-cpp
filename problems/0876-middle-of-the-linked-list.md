# 876. Middle of the Linked List

- **Difficulty:** Easy  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/middle-of-the-linked-list/>  
- **NeetCode:** <https://neetcode.io/problems/middle-of-the-linked-list>  
- **Video:** <https://www.youtube.com/watch?v=A2_ldqM4QcY>  
- **Video approach:** 3. Fast & Slow Pointers (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Convert To Array

Linked lists do not support random access, so finding the middle node directly is not straightforward. By storing all nodes in an array, we gain index-based access. Once we have the array, the middle node is simply at index `length / 2`.

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
    ListNode* middleNode(ListNode* head) {
        vector<ListNode*> arr;
        ListNode* cur = head;
        while (cur) {
            arr.push_back(cur);
            cur = cur->next;
        }
        return arr[arr.size() / 2];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Find Length of the List

We can avoid storing all nodes by first counting the total number of nodes, then making a second pass to reach the middle. This uses constant extra space since we only store the count and a pointer.

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
    ListNode* middleNode(ListNode* head) {
        int n = 0;
        ListNode* cur = head;
        while (cur) {
            cur = cur->next;
            n++;
        }

        n /= 2;
        cur = head;
        while (n) {
            n--;
            cur = cur->next;
        }
        return cur;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 3. Fast & Slow Pointers ▶ video

The fast and slow pointer technique finds the middle in a single pass. The `slow` pointer moves one step at a time, while the `fast` pointer moves two steps. When the `fast` pointer reaches the end, the `slow` pointer will be at the middle. This works because the `fast` pointer covers twice the distance in the same number of iterations.

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
    ListNode* middleNode(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head;

        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        return slow;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/0876-middle-of-the-linked-list.cpp` in the NeetCode repo)

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
    ListNode* middleNode(ListNode* head) {
        /*
        The slow and fast pointer algorithm is used to find the middle 
        of a linked list by iterating through the list with a slow 
        pointer that moves one step at a time and a fast pointer that
        moves two steps at a time. When the fast pointer reaches the 
        end of the list, the slow pointer will be at the midpoint of the list.
        */
        ListNode *slow_pointer = head, *fast_pointer = head;
        while (fast_pointer != NULL && fast_pointer->next != NULL) {
            slow_pointer = slow_pointer->next;
            fast_pointer = fast_pointer->next->next;
        }
        return slow_pointer;
    }
};
```
