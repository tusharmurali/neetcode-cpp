# 1669. Merge in Between Linked Lists

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/merge-in-between-linked-lists/>  
- **NeetCode:** <https://neetcode.io/problems/merge-in-between-linked-lists>  
- **Video:** <https://www.youtube.com/watch?v=pI775VutBxg>  
- **Video approach:** 2. Two Pointers (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Convert To Array

The problem asks us to remove nodes from index `a` to `b` in `list1` and insert `list2` in their place. By storing all nodes of `list1` in an array, we gain direct access to any node by index. This makes it straightforward to connect the node just before position `a` to the head of `list2`, and then connect the tail of `list2` to the node just after position `b`.

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
    ListNode* mergeInBetween(ListNode* list1, int a, int b, ListNode* list2) {
        ListNode* cur = list1;
        vector<ListNode*> arr;

        while (cur) {
            arr.push_back(cur);
            cur = cur->next;
        }

        arr[a - 1]->next = list2;
        cur = list2;

        while (cur->next) {
            cur = cur->next;
        }

        cur->next = arr[b + 1];
        return list1;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n)$

> Where $n$ is the length of the first list and $m$ is the length of the second list.

## 2. Two Pointers ▶ video

Instead of using extra space to store all nodes, we can traverse `list1` directly using pointers. We walk through the list, counting nodes until we reach position `a - 1` (the node just before the removal range). We save this position, then continue until we pass position `b` to find the node that should come after `list2`. Finally, we rewire the pointers to splice `list2` in place.

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
    ListNode* mergeInBetween(ListNode* list1, int a, int b, ListNode* list2) {
        ListNode* curr = list1;
        int i = 0;

        while (i < a - 1) {
            curr = curr->next;
            i++;
        }
        ListNode* head = curr;

        while (i <= b) {
            curr = curr->next;
            i++;
        }
        head->next = list2;

        while (list2->next) {
            list2 = list2->next;
        }
        list2->next = curr;

        return list1;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(1)$ extra space.

> Where $n$ is the length of the first list and $m$ is the length of the second list.

## 3. Recursion

We can solve this problem recursively by reducing the indices `a` and `b` as we move deeper into `list1`. When `a` reaches 1, we have found the insertion point and can attach `list2`. We then continue recursing with `list2`'s tail to skip over the nodes that should be removed (while `b` counts down). When `b` reaches 0, we have passed all nodes to remove and can connect the tail of `list2` to the remaining nodes of `list1`.

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
    ListNode* mergeInBetween(ListNode* list1, int a, int b, ListNode* list2) {
        if (a == 1) {
            ListNode* nxt = list1->next;
            list1->next = list2;

            while (list2->next) {
                list2 = list2->next;
            }
            mergeInBetween(nxt, 0, b - 1, list2);
            return list1;
        }

        if (b == 0) {
            list2->next = list1->next;
            return list1;
        }

        mergeInBetween(list1->next, a - 1, b - 1, list2);
        return list1;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n)$ for recursion stack.

> Where $n$ is the length of the first list and $m$ is the length of the second list.
