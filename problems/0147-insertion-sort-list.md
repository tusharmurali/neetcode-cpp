# 147. Insertion Sort List

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/insertion-sort-list/>  
- **NeetCode:** <https://neetcode.io/problems/insertion-sort-list>  
- **Video:** <https://www.youtube.com/watch?v=Kk6mXAzqX3Y>  

[← Back to index](../INDEX.md)

## 1. Convert To Array

Since sorting a linked list in place can be tricky, we can simplify the problem by extracting all the values into an array. Once in array form, we can use any standard sorting algorithm. After sorting, we traverse the linked list again and overwrite each node's value with the sorted values in order.

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
    ListNode* insertionSortList(ListNode* head) {
        vector<int> arr;
        ListNode* cur = head;

        while (cur) {
            arr.push_back(cur->val);
            cur = cur->next;
        }

        sort(arr.begin(), arr.end());
        cur = head;

        for (int val : arr) {
            cur->val = val;
            cur = cur->next;
        }
        return head;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Swapping Values

This approach mimics insertion sort by comparing values rather than rearranging node pointers. For each node, we scan from the head to find any earlier node with a larger value and swap values. This bubbles smaller values toward the front, eventually producing a sorted list. While simpler to implement than pointer manipulation, it still requires O(n^2) comparisons.

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
    ListNode* insertionSortList(ListNode* head) {
        for (ListNode* cur = head->next; cur; cur = cur->next) {
            for (ListNode* tmp = head; tmp != cur; tmp = tmp->next) {
                if (tmp->val > cur->val) {
                    swap(tmp->val, cur->val);
                }
            }
        }
        return head;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 3. Swapping Nodes

This is the classic insertion sort adapted for linked lists. Instead of swapping values, we physically remove a node and reinsert it at the correct position in the already sorted portion. A dummy node simplifies insertions at the head. If the current node is already in order relative to the previous node, we just advance. Otherwise, we unlink it and search from the beginning for the right spot.

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
    ListNode* insertionSortList(ListNode* head) {
        ListNode* dummy = new ListNode(0, head);
        ListNode* prev = head;
        ListNode* cur = head->next;

        while (cur) {
            if (cur->val >= prev->val) {
                prev = cur;
                cur = cur->next;
                continue;
            }

            ListNode* tmp = dummy;
            while (tmp->next->val < cur->val) {
                tmp = tmp->next;
            }

            prev->next = cur->next;
            cur->next = tmp->next;
            tmp->next = cur;
            cur = prev->next;
        }

        return dummy->next;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/0147-insertion-sort-list.cpp` in the NeetCode repo)

```cpp
/*
  Given the head of a singly linked list, sort the list using insertion sort, and return the sorted list's head.
  
  The steps of the insertion sort algorithm:
  
  1. Insertion sort iterates, consuming one input element each repetition and growing a sorted output list.
  2. At each iteration, insertion sort removes one element from the input data, finds the location it belongs within the sorted list and inserts it there.
  3. It repeats until no input elements remain.

  Ex. Input: head = [4,2,1,3]
      Output: [1,2,3,4]
  
  Time : O(N^2)
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
    ListNode* insertionSortList(ListNode* head) {
        if(head == NULL || head -> next == NULL) {
            return head;
        }

        ListNode *ptr1 = head -> next, *sortedPtr = head;
        while(ptr1 != NULL) {
            if(ptr1 -> val < sortedPtr -> val) {
                ListNode *ptr2 = head, *lagPtr = head;
                while(true) {
                    if(ptr2 -> val > ptr1 -> val) {
                        if(ptr2 == head) {
                            sortedPtr -> next = ptr1 -> next;
                            ptr1 -> next = head;
                            head = ptr1;
                            ptr1 = sortedPtr -> next;
                            break;
                        }
                        else {
                            sortedPtr -> next = ptr1 -> next;
                            ptr1 -> next = ptr2;
                            lagPtr -> next = ptr1;
                            ptr1 = sortedPtr -> next;
                            break;
                        }
                    }
                    lagPtr = ptr2;
                    ptr2 = ptr2 -> next;
                }
                
            } else {
                sortedPtr = sortedPtr -> next;
                ptr1 = ptr1 -> next;
            }
        }

        return head;
    }
};
```
