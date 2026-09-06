# 2. Add Two Numbers

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/add-two-numbers/>  
- **NeetCode:** <https://neetcode.io/problems/add-two-numbers>  
- **Video:** <https://www.youtube.com/watch?v=wgFPrzTjm7s>  

[← Back to index](../INDEX.md)

## 1. Recursion

We add the two linked lists exactly like adding two numbers on paper.

Each node contains one digit, and since the lists are stored in **reverse order**, the head contains the ones place — making addition easy.  
At every step:

1. Take a digit from `l1` (or `0` if it's finished)
2. Take a digit from `l2` (or `0` if it's finished)
3. Add them with the incoming `carry`
4. Create a new node for the current digit (`sum % 10`)
5. Pass the new `carry` (`sum // 10`) forward using **recursion**

The recursion naturally processes digits from left to right and stops only when:
- both lists are fully processed **and**
- no carry remains.

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
    ListNode* add(ListNode* l1, ListNode* l2, int carry) {
        if (!l1 && !l2 && carry == 0) {
            return nullptr;
        }

        int v1 = 0;
        int v2 = 0;
        if (l1) {
            v1 = l1->val;
        }
        if (l2) {
            v2 = l2->val;
        }

        int sum = v1 + v2 + carry;
        int newCarry = sum / 10;
        int nodeValue = sum % 10;

        ListNode* nextNode = add(
            (l1 ? l1->next : nullptr),
            (l2 ? l2->next : nullptr),
            newCarry
        );

        return new ListNode(nodeValue, nextNode);
    }

    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        return add(l1, l2, 0);
    }
};
```

**Complexity**

- Time complexity: $O(max(m, n))$
    - This is asymptotically equivalent to $O(m + n)$.
- Space complexity: $O(max(m, n))$
    - $O(max(m, n))$ for the recursion call stack.
    - $O(max(m, n))$ for the output list.

> Where $m$ is the length of $l1$ and $n$ is the length of $l2$.

## 2. Iteration

We simulate normal addition the same way we do on paper — digit by digit.

The linked lists store numbers in **reverse order**, so the first nodes represent the 1’s place.  
This makes addition straightforward:

- Add the two digits.
- Add the `carry` from the previous step.
- Save the resulting digit (`sum % 10`) into a new node.
- Update the `carry` (`sum // 10`).
- Move both pointers forward.

We continue until **both lists are finished AND no carry remains**.  
A dummy node helps us easily build and return the final linked list.

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
        ListNode* dummy = new ListNode();
        ListNode* cur = dummy;

        int carry = 0;
        while (l1 != nullptr || l2 != nullptr || carry != 0) {
            int v1 = (l1 != nullptr) ? l1->val : 0;
            int v2 = (l2 != nullptr) ? l2->val : 0;

            int val = v1 + v2 + carry;
            carry = val / 10;
            val = val % 10;
            cur->next = new ListNode(val);

            cur = cur->next;
            l1 = (l1 != nullptr) ? l1->next : nullptr;
            l2 = (l2 != nullptr) ? l2->next : nullptr;
        }
        ListNode* res = dummy->next;
        delete dummy;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(max(m, n))$
    - This is asymptotically equivalent to $O(m + n)$.
- Space complexity:
    - $O(1)$ extra space.
    - $O(max(m, n))$ for the output list.

> Where $m$ is the length of $l1$ and $n$ is the length of $l2$.

## Standalone solution file (`cpp/0002-add-two-numbers.cpp` in the NeetCode repo)

```cpp
/*
    Given 2 linked lists, digits stored in reverse order, add them
    Ex. l1 = [2,4,3] l2 = [5,6,4] -> [7,0,8] (342 + 465 = 807)

    Sum digit-by-digit + carry, handle if one list becomes null

    Time: O(max(m, n))
    Space: O(max(m, n))
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
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode* dummy = new ListNode();
        
        ListNode* curr = dummy;
        int carry = 0;
        
        while (l1 != NULL || l2 != NULL) {
            int val1 = (l1 != NULL) ? l1->val : 0;
            int val2 = (l2 != NULL) ? l2->val : 0;
            
            int sum = val1 + val2 + carry;
            carry = sum / 10;
            
            curr->next = new ListNode(sum % 10);
            curr = curr->next;
            
            if (l1 != NULL) {
                l1 = l1->next;
            }
            if (l2 != NULL) {
                l2 = l2->next;
            }
        }
        
        if (carry == 1) {
            curr->next = new ListNode(1);
        }
        
        return dummy->next;
    }
};
```
