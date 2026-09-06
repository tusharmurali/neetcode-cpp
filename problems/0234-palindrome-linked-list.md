# 234. Palindrome Linked List

- **Difficulty:** Easy  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/palindrome-linked-list/>  
- **NeetCode:** <https://neetcode.io/problems/palindrome-linked-list>  
- **Video:** <https://www.youtube.com/watch?v=yOzXms1J6Nk>  

[← Back to index](../INDEX.md)

## 1. Convert To Array

A palindrome reads the same forwards and backwards. Linked lists only allow forward traversal, making direct comparison difficult. The simplest approach is to convert the linked list to an array where we can use random access.

Once we have an array, we can use two pointers from both ends moving toward the center, comparing values as we go.

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
    bool isPalindrome(ListNode* head) {
        std::vector<int> arr;
        ListNode* cur = head;
        while (cur) {
            arr.push_back(cur->val);
            cur = cur->next;
        }

        int l = 0, r = arr.size() - 1;
        while (l < r) {
            if (arr[l] != arr[r]) {
                return false;
            }
            l++;
            r--;
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Recursion

We can use recursion to simulate traversing from the end of the list. By recursing to the end first and comparing on the way back, we effectively compare nodes from both ends simultaneously.

We maintain a pointer starting at the head. As recursion unwinds from the tail, we compare each node with the head pointer and advance the head pointer after each match.

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
    ListNode* cur;

    bool rec(ListNode* node) {
        if (node != nullptr) {
            if (!rec(node->next)) {
                return false;
            }
            if (cur->val != node->val) {
                return false;
            }
            cur = cur->next;
        }
        return true;
    }

public:
    bool isPalindrome(ListNode* head) {
        cur = head;
        return rec(head);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Stack

A stack provides LIFO (last-in-first-out) access. If we push all elements onto a stack and then traverse the list while popping, we compare elements from the front and back simultaneously.

This is similar to the array approach but uses a stack to reverse the order of comparison.

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
    bool isPalindrome(ListNode* head) {
        stack<int> stack;
        ListNode* cur = head;

        while (cur != nullptr) {
            stack.push(cur->val);
            cur = cur->next;
        }

        cur = head;
        while (cur != nullptr && cur->val == stack.top()) {
            stack.pop();
            cur = cur->next;
        }

        return cur == nullptr;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Fast & Slow Pointers

To achieve O(1) extra space, we can reverse the second half of the list in place. Then we compare the first half with the reversed second half node by node.

We use the fast and slow pointer technique to find the middle of the list. The fast pointer moves twice as fast, so when it reaches the end, the slow pointer is at the middle.

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
    bool isPalindrome(ListNode* head) {
        ListNode *fast = head, *slow = head;

        // find middle (slow)
        while (fast && fast->next) {
            fast = fast->next->next;
            slow = slow->next;
        }

        // reverse second half
        ListNode *prev = nullptr;
        while (slow) {
            ListNode *tmp = slow->next;
            slow->next = prev;
            prev = slow;
            slow = tmp;
        }

        // check palindrome
        ListNode *left = head, *right = prev;
        while (right) {
            if (left->val != right->val) {
                return false;
            }
            left = left->next;
            right = right->next;
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/0234-palindrome-linked-list.cpp` in the NeetCode repo)

```cpp
class Solution{    
    public:    
        bool isPalindrome(ListNode* head){            
            vector<int> v;            
            while(head != nullptr){                
                v.push_back(head -> val);                
                head = head -> next;              
            }         
            for(int i = 0; i < v.size() / 2; i++){                
                if(v[i] != v[v.size() - i - 1]){                    
                    return false;                    
                }                
            }            
            return true;
        }    
};
```
