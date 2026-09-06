# 24. Swap Nodes In Pairs

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/swap-nodes-in-pairs/>  
- **NeetCode:** <https://neetcode.io/problems/swap-nodes-in-pairs>  
- **Video:** <https://www.youtube.com/watch?v=o811TZLAWOo>  

[← Back to index](../INDEX.md)

## 1. Convert To Array

The simplest approach is to convert the linked list to an array, where swapping elements is straightforward using index-based access. Once we swap adjacent elements in the array, we rebuild the linked list connections. This trades space efficiency for implementation simplicity.

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
    ListNode* swapPairs(ListNode* head) {
        if (!head) return nullptr;

        vector<ListNode*> arr;
        ListNode* cur = head;

        while (cur) {
            arr.push_back(cur);
            cur = cur->next;
        }

        for (size_t i = 0; i + 1 < arr.size(); i += 2) {
            swap(arr[i], arr[i + 1]);
        }

        for (size_t i = 0; i + 1 < arr.size(); i++) {
            arr[i]->next = arr[i + 1];
        }

        arr.back()->next = nullptr;
        return arr[0];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Recursion

We can think of the problem recursively: swap the first two nodes, then let recursion handle the rest. The first node should point to the result of swapping the remaining list (starting from the third node). The second node becomes the new head of this pair and points to the first node. This recursive structure naturally handles lists of any length.

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
    ListNode* swapPairs(ListNode* head) {
        if (!head || !head->next) {
            return head;
        }

        ListNode* cur = head;
        ListNode* nxt = head->next;
        cur->next = swapPairs(nxt->next);
        nxt->next = cur;

        return nxt;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Iteration

We can swap pairs in place by carefully managing pointers. A dummy node simplifies handling the head change. For each pair, we need to: save the reference to the next pair, reverse the current pair's pointers, and connect the previous node to the new first node of the swapped pair. Moving two nodes at a time ensures we process each pair exactly once.

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
    ListNode* swapPairs(ListNode* head) {
        ListNode dummy(0, head);
        ListNode* prev = &dummy, *curr = head;

        while (curr && curr->next) {
            ListNode* nxtPair = curr->next->next;
            ListNode* second = curr->next;

            // Reverse this pair
            second->next = curr;
            curr->next = nxtPair;
            prev->next = second;

            // Update pointers
            prev = curr;
            curr = nxtPair;
        }

        return dummy.next;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0024-swap-nodes-in-pairs.cpp` in the NeetCode repo)

```cpp
/*
  Given a linked list, swap every two adjacent nodes and return its head. 
  You must solve the problem without modifying the values in the list's nodes (i.e., only nodes themselves may be changed.)

  Ex. Input: head = [1,2,3,4]
      Output: [2,1,4,3]

  Time  : O(N);
  Space : O(1);
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
    ListNode* swapPairs(ListNode* head) {  
        if (!head || !head->next) 
            return head;

        ListNode *new_head = head->next;
        ListNode *prev = NULL;

        while (head && head->next) {
            ListNode *next_pair = head->next->next;
            ListNode *second = head->next;

            if (prev)
                prev->next = second;

            second->next = head;
            head->next = next_pair;

            prev = head;
            head = next_pair;
        }
        return new_head;
    }
};
```
