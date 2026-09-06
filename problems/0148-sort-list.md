# 148. Sort List

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/sort-list/>  
- **NeetCode:** <https://neetcode.io/problems/sort-list>  
- **Video:** <https://www.youtube.com/watch?v=TGveA1oFhrc>  

[← Back to index](../INDEX.md)

## 1. Convert To Array

Linked lists are notoriously difficult to sort in place due to lack of random access. A straightforward workaround is to extract all node values into an array, sort the array using a built-in sorting algorithm, and then write the sorted values back into the linked list nodes. This leverages efficient array sorting while preserving the original list structure.

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
    ListNode* sortList(ListNode* head) {
        if (!head) return nullptr;

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

## 2. Recursive Merge Sort

Merge sort is well suited for linked lists because merging two sorted lists can be done efficiently without extra space by rearranging pointers. We recursively split the list in half using the slow and fast pointer technique to find the middle, sort each half, and then merge the two sorted halves together. This divide-and-conquer approach achieves O(n log n) time complexity.

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
    ListNode* sortList(ListNode* head) {
        if (!head || !head->next) {
            return head;
        }

        ListNode* left = head;
        ListNode* right = getMid(head);
        ListNode* temp = right->next;
        right->next = nullptr;
        right = temp;

        left = sortList(left);
        right = sortList(right);
        return merge(left, right);
    }

private:
    ListNode* getMid(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head->next;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        return slow;
    }

    ListNode* merge(ListNode* list1, ListNode* list2) {
        ListNode dummy(0);
        ListNode* tail = &dummy;

        while (list1 && list2) {
            if (list1->val < list2->val) {
                tail->next = list1;
                list1 = list1->next;
            } else {
                tail->next = list2;
                list2 = list2->next;
            }
            tail = tail->next;
        }

        if (list1) {
            tail->next = list1;
        }
        if (list2) {
            tail->next = list2;
        }

        return dummy.next;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(\log n)$ for recursion stack.

## 3. Iterative Merge Sort

The recursive merge sort uses O(log n) space for the call stack. To achieve true O(1) extra space, we can implement merge sort iteratively using a bottom-up approach. Instead of recursively splitting the list, we start by treating each node as a sorted sublist of size 1, then merge adjacent pairs into sorted sublists of size 2, then 4, and so on until the entire list is sorted.

```cpp
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
public:
    ListNode* sortList(ListNode* head) {
        if (!head || !head->next) {
            return head;
        }

        int length = 0;
        ListNode* cur = head;
        while (cur) {
            length++;
            cur = cur->next;
        }

        ListNode dummy(0);
        dummy.next = head;
        int step = 1;

        while (step < length) {
            ListNode* prev = &dummy, *curr = dummy.next;
            while (curr) {
                ListNode* left = curr;
                ListNode* right = split(left, step);
                curr = split(right, step);
                ListNode* merged = merge(left, right);
                prev->next = merged;
                while (prev->next) {
                    prev = prev->next;
                }
            }
            step *= 2;
        }

        return dummy.next;
    }

private:
    ListNode* split(ListNode* head, int step) {
        if (!head) return nullptr;
        for (int i = 0; i < step - 1 && head->next; i++) {
            head = head->next;
        }
        ListNode* nextPart = head->next;
        head->next = nullptr;
        return nextPart;
    }

    ListNode* merge(ListNode* list1, ListNode* list2) {
        ListNode dummy(0);
        ListNode* tail = &dummy;

        while (list1 && list2) {
            if (list1->val < list2->val) {
                tail->next = list1;
                list1 = list1->next;
            } else {
                tail->next = list2;
                list2 = list2->next;
            }
            tail = tail->next;
        }

        tail->next = list1 ? list1 : list2;
        return dummy.next;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0148-sort-list.cpp` in the NeetCode repo)

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
    // find middle of LL using slow and fast pointers
    ListNode* findLLMid(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head->next;
        while (fast != NULL && fast->next != NULL) {
            slow = slow->next;
            fast = fast->next->next;
        }
        return slow;
    }

    // merges two sorted LLs
    ListNode* merge(ListNode* head1, ListNode* head2) {
        ListNode* dummy = new ListNode();
        ListNode* p = dummy;
        ListNode* p1 = head1;
        ListNode* p2 = head2;

        while (p1 != NULL && p2 != NULL) {
            if (p1->val < p2->val) {
                ListNode* temp = p1->next;
                p->next = p1;
                p1->next = NULL;
                p1 = temp;
            } else {
                ListNode* temp = p2->next;
                p->next = p2;
                p2->next = NULL;
                p2 = temp;
            }
            p = p->next;
        }

        if (p1 == NULL) {
            p->next = p2;
        } else if (p2 == NULL) {
            p->next = p1;
        }

        return dummy->next;
    }
public:
    // merge sort implementation
    ListNode* sortList(ListNode* head) {
        // base cases
        if (head == NULL)
            return NULL;
        if (head->next == NULL) 
            return head;
        
        // split LL into two halves
        ListNode* middleOfLL = findLLMid(head);
        ListNode* leftHalf = head;
        ListNode* rightHalf = middleOfLL->next;
        middleOfLL->next = NULL; // this cuts off the right half from the left half

        // sort the two halves seperately and then merge them into one 
        leftHalf = sortList(leftHalf); 
        rightHalf = sortList(rightHalf);
        head = merge(leftHalf, rightHalf);

        return head;
    }
};
```
