# 2130. Maximum Twin Sum Of A Linked List

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-twin-sum-of-a-linked-list/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-twin-sum-of-a-linked-list>  
- **Video:** <https://www.youtube.com/watch?v=doj95MelfSA>  

[← Back to index](../INDEX.md)

## 1. Convert To Array

A twin sum pairs the `i`-th node from the start with the `i`-th node from the end. Since linked lists do not support random access, we first convert the list into an array. With an array, we can use two pointers starting at opposite ends to easily compute each twin sum and track the maximum.

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
    int pairSum(ListNode* head) {
        vector<int> arr;
        ListNode* cur = head;

        while (cur) {
            arr.push_back(cur->val);
            cur = cur->next;
        }

        int i = 0, j = arr.size() - 1, res = 0;
        while (i < j) {
            res = max(res, arr[i] + arr[j]);
            i++;
            j--;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Reverse the Second Half

To avoid extra space from converting to an array, we can modify the list itself. Using the `slow` and `fast` pointer technique, we find the middle of the list. Then we reverse the second half in place. Now the first half and the reversed second half can be traversed simultaneously, allowing us to compute twin sums directly without extra storage.

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
    int pairSum(ListNode* head) {
        ListNode* slow = head, *fast = head;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }

        ListNode* prev = nullptr, *cur = slow;
        while (cur) {
            ListNode* nxt = cur->next;
            cur->next = prev;
            prev = cur;
            cur = nxt;
        }

        int res = 0;
        ListNode* first = head, *second = prev;
        while (second) {
            res = max(res, first->val + second->val);
            first = first->next;
            second = second->next;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 3. Reverse the First Half

Instead of reversing the second half after finding the middle, we can reverse the first half as we go. While traversing with `slow` and `fast` pointers, we reverse the links behind `slow`. By the time `slow` reaches the middle, the first half is already reversed. Now `slow` points to the start of the second half, and `prev` points to the end of the reversed first half. We can traverse both halves in parallel to find the maximum twin sum.

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
    int pairSum(ListNode* head) {
        ListNode* slow = head, *fast = head, *prev = nullptr;

        while (fast && fast->next) {
            fast = fast->next->next;
            ListNode* tmp = slow->next;
            slow->next = prev;
            prev = slow;
            slow = tmp;
        }

        int res = 0;
        while (slow) {
            res = max(res, prev->val + slow->val);
            prev = prev->next;
            slow = slow->next;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/2130-maximum-twin-sum-of-a-linked-list.cpp` in the NeetCode repo)

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

// Time: O(n)
// Space: O(1)
class Solution {
public:
    int pairSum(ListNode* head) {
        ListNode *fast = head, *slow = head;

        while(fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        slow = reverseList(slow);
        
        int mx = 0;
        while(head && slow) {
            mx = max(mx, head->val + slow->val);
            head = head->next;
            slow = slow->next;
        }
        
        return mx;
    }
private:
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = NULL;
        ListNode* curr = head;
        ListNode* NEXT = NULL;
        
        while(curr) {
            NEXT = curr->next;
            curr->next = prev;
            prev = curr;
            curr = NEXT;
        }
        
        return prev;
    }
};
```
