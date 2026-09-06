# 61. Rotate List

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/rotate-list/>  
- **NeetCode:** <https://neetcode.io/problems/rotate-list>  
- **Video:** <https://www.youtube.com/watch?v=UcGtPs2LE_c>  

[← Back to index](../INDEX.md)

## 1. Convert To Array

The challenge with linked lists is that we cannot directly access elements by index. One straightforward approach is to convert the list to an array, perform the rotation using array indexing, and then write the values back to the list nodes. This trades memory for simplicity, allowing us to use familiar array rotation logic.

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
    ListNode* rotateRight(ListNode* head, int k) {
        if (!head) return nullptr;

        vector<int> arr;
        ListNode* cur = head;
        while (cur) {
            arr.push_back(cur->val);
            cur = cur->next;
        }

        int n = arr.size();
        k %= n;
        cur = head;
        for (int i = n - k; i < n; i++) {
            cur->val = arr[i];
            cur = cur->next;
        }
        for (int i = 0; i < n - k; i++) {
            cur->val = arr[i];
            cur = cur->next;
        }
        return head;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Iteration

Rotating a linked list by `k` means moving the last `k` nodes to the front. We can do this by finding the new tail (the node at position `n - k - 1`), breaking the list there, and reconnecting the old `tail` to the old `head`. The key insight is that we only need to find two positions: where to break the list and where to reconnect.

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
    ListNode* rotateRight(ListNode* head, int k) {
        if (!head) {
            return head;
        }

        int length = 1;
        ListNode* tail = head;
        while (tail->next) {
            tail = tail->next;
            length++;
        }

        k = k % length;
        if (k == 0) {
            return head;
        }

        ListNode* cur = head;
        for (int i = 0; i < length - k - 1; i++) {
            cur = cur->next;
        }
        ListNode* newHead = cur->next;
        cur->next = nullptr;
        tail->next = head;

        return newHead;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 3. Iteration (Using One Pointer)

We can simplify the two-pointer approach by first creating a circular list. Connect the `tail` to the `head`, then traverse `n - k` steps from the `tail` to find the new `tail`. Break the circle at that point. This approach uses a single pointer and avoids the need to track both the `tail` and find the break point separately.

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
    ListNode* rotateRight(ListNode* head, int k) {
        if (!head) {
            return head;
        }

        ListNode* cur = head;
        int n = 1;
        while (cur->next) {
            n++;
            cur = cur->next;
        }

        cur->next = head;
        k %= n;
        for (int i = 0; i < n - k; i++) {
            cur = cur->next;
        }

        head = cur->next;
        cur->next = nullptr;
        return head;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/0061-rotate-list.cpp` in the NeetCode repo)

```cpp
/*
    Given the head of a linked list, rotate the list to the right by k places.
    Example: list = [1,2,3,4,5] and k = 2
    Output: [4,5,1,2,3]
    
    Time complexity: O(n)
    Space complexity: O(1)
*/

class Solution {
private:
    int findLen(ListNode* head){
        int len = 0;
        while(head!=NULL){
            len++;
            head = head->next;
        }
        return len;
    }
    ListNode* findNewHead(ListNode* head,int k){
        int i=0;
        while(i+1<k){
            i++;
            head = head->next;
        }
        ListNode* ret = head->next;
        head->next = NULL;
        return ret;
    }
    ListNode* findLast(ListNode* head){
        while(head->next!=NULL) head = head->next;
        return head;
    }
public:
    ListNode* rotateRight(ListNode* head, int k) {
        int len = findLen(head); // Finds the length of the Linked List
        if(len==0) return head;
        k = k%len;
        if(k==0) return head;
        ListNode* newHead = findNewHead(head,len-k); // Finds the node that is the new head
        ListNode* last = findLast(newHead); // Finds the last node from the new head and connects it to the previous head
        last->next = head;
        return newHead;
    }
};
```
