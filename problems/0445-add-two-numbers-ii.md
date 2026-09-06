# 445. Add Two Numbers II

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/add-two-numbers-ii/>  
- **NeetCode:** <https://neetcode.io/problems/add-two-numbers-ii>  

[← Back to index](../INDEX.md)

## 1. Reverse List

When adding two numbers, we naturally start from the least significant digit. The problem gives us numbers stored with the most significant digit first, so reversing both lists makes the addition straightforward.

After reversing, we can walk through both lists simultaneously, adding corresponding digits along with any carry. We build the result by prepending each new digit to our answer, which naturally produces the correct order without needing another reversal at the end.

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

public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        l1 = reverseList(l1);
        l2 = reverseList(l2);
        ListNode* head = nullptr;
        int carry = 0;

        while (l1 || l2 || carry) {
            int v1 = l1 ? l1->val : 0;
            int v2 = l2 ? l2->val : 0;
            int total = v1 + v2 + carry;
            carry = total / 10;
            ListNode* node = new ListNode(total % 10);
            node->next = head;
            head = node;
            l1 = l1 ? l1->next : nullptr;
            l2 = l2 ? l2->next : nullptr;
        }

        return head;
    }
};
```

**Complexity**

* Time complexity: $O(m + n)$
* Space complexity: $O(max(m, n))$ for the output list.

> Where $m$ is the length of $l1$ and $n$ is the length of $l2$.

## 2. Stack

If we want to avoid modifying the input lists, we can use stacks to reverse the digit order implicitly. Pushing all digits onto stacks gives us access to them in reverse order when we pop.

This approach preserves the original lists while still allowing us to process digits from least significant to most significant. The rest of the logic is identical: add digits with carry and build the result by prepending nodes.

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
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        stack<int> s1, s2;

        while (l1) {
            s1.push(l1->val);
            l1 = l1->next;
        }

        while (l2) {
            s2.push(l2->val);
            l2 = l2->next;
        }

        int carry = 0;
        ListNode* head = nullptr;

        while (!s1.empty() || !s2.empty() || carry) {
            int v1 = s1.empty() ? 0 : s1.top(); if (!s1.empty()) s1.pop();
            int v2 = s2.empty() ? 0 : s2.top(); if (!s2.empty()) s2.pop();
            int total = v1 + v2 + carry;
            carry = total / 10;
            ListNode* node = new ListNode(total % 10);
            node->next = head;
            head = node;
        }

        return head;
    }
};
```

**Complexity**

* Time complexity: $O(m + n)$
* Space complexity: $O(m + n)$

> Where $m$ is the length of $l1$ and $n$ is the length of $l2$.
