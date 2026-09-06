# 160. Intersection of Two Linked Lists

- **Difficulty:** Easy  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/intersection-of-two-linked-lists/>  
- **NeetCode:** <https://neetcode.io/problems/intersection-of-two-linked-lists>  
- **Video:** <https://www.youtube.com/watch?v=D0X0BONOQhI>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to check every node in the first list against every node in the second list. If two nodes are the same object (not just equal values), we found the intersection point. This works because intersection means the lists share actual node references, not just duplicate values.

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode* getIntersectionNode(ListNode* headA, ListNode* headB) {
        while (headA) {
            ListNode* cur = headB;
            while (cur) {
                if (headA == cur) {
                    return headA;
                }
                cur = cur->next;
            }
            headA = headA->next;
        }
        return nullptr;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(1)$ extra space.

> Where $m$ is the length of the first list and $n$ is the length of the second list.

## 2. Hash Set

We can use a hash set to store all nodes from the first list. Then, as we traverse the second list, we check if each node exists in the set. The first node found in the set is the intersection point since it is the earliest shared node.

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode* getIntersectionNode(ListNode* headA, ListNode* headB) {
        unordered_set<ListNode*> nodeSet;

        ListNode* cur = headA;
        while (cur) {
            nodeSet.insert(cur);
            cur = cur->next;
        }

        cur = headB;
        while (cur) {
            if (nodeSet.find(cur) != nodeSet.end()) {
                return cur;
            }
            cur = cur->next;
        }

        return nullptr;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(m)$

> Where $m$ is the length of the first list and $n$ is the length of the second list.

## 3. Two Pointers - I

If the two lists have different lengths, the intersection point is at the same distance from the end of both lists. By computing the lengths and advancing the pointer on the longer list by the difference, we align the two pointers. Then we move both forward together until they meet at the intersection or reach the end.

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
    int getLength(ListNode* head) {
        int length = 0;
        while (head) {
            length++;
            head = head->next;
        }
        return length;
    }

public:
    ListNode* getIntersectionNode(ListNode* headA, ListNode* headB) {
        int m = getLength(headA), n = getLength(headB);
        ListNode* l1 = headA, *l2 = headB;

        if (m < n) {
            swap(m, n);
            swap(l1, l2);
        }

        while (m-- > n) {
            l1 = l1->next;
        }

        while (l1 && l1 != l2) {
            l1 = l1->next;
            l2 = l2->next;
        }

        return l1;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(1)$ extra space.

> Where $m$ is the length of the first list and $n$ is the length of the second list.

## 4. Two Pointers - II

A clever approach avoids computing lengths explicitly. Two pointers start at the heads of each list. When a pointer reaches the end, it jumps to the head of the other list. After at most `m + n` steps, both pointers will have traversed the same total distance. If an intersection exists, they will meet there; otherwise, they both reach `null` simultaneously.

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode* getIntersectionNode(ListNode* headA, ListNode* headB) {
        ListNode* l1 = headA;
        ListNode* l2 = headB;
        while (l1 != l2) {
            l1 = l1 ? l1->next : headB;
            l2 = l2 ? l2->next : headA;
        }
        return l1;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(1)$ extra space.

> Where $m$ is the length of the first list and $n$ is the length of the second list.

## Standalone solution file (`cpp/0160-intersection-of-two-linked-lists.cpp` in the NeetCode repo)

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */

class Solution {
public:
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
        ListNode *trevA = headA, *trevB = headB;

        while (trevA != trevB) {
            trevA = (trevA != NULL) ? trevA->next : headB;
            trevB = (trevB != NULL) ? trevB->next : headA;
        }
        return trevA;
    }
};
```
