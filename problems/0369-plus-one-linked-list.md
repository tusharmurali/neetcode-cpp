# 369. Plus One Linked List

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/plus-one-linked-list/>  
- **NeetCode:** <https://neetcode.io/problems/plus-one-linked-list>  

[← Back to index](../INDEX.md)

## 1. Sentinel Head + Textbook Addition

When adding one to a number, the only digits that change are trailing nines (which become zeros) and the rightmost non-nine digit (which increments by one). If all digits are nines, we need an extra digit at the front.

By using a sentinel node before the head, we handle the case where a new digit is needed (like `999` becoming `1000`) without special logic. We simply find the rightmost non-nine digit, increment it, and set all following digits to zero.

```cpp
class Solution {
public:
    ListNode* plusOne(ListNode* head) {
        // sentinel head
        ListNode* sentinel = new ListNode(0);
        sentinel->next = head;
        ListNode* notNine = sentinel;

        // find the rightmost not-nine digit
        while (head != nullptr) {
            if (head->val != 9) notNine = head;
            head = head->next;
        }
        // increase this rightmost not-nine digit by 1
        notNine->val++;
        notNine = notNine->next;
        // set all the following nines to zeros
        while (notNine != nullptr) {
            notNine->val = 0;
            notNine = notNine->next;
        }

        delete notNine;
        return sentinel->val != 0 ? sentinel : sentinel->next;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(1)$

> Where $N$ is the length of the input list
