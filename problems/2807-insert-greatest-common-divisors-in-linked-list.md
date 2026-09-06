# 2807. Insert Greatest Common Divisors in Linked List

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/insert-greatest-common-divisors-in-linked-list/>  
- **NeetCode:** <https://neetcode.io/problems/insert-greatest-common-divisors-in-linked-list>  
- **Video:** <https://www.youtube.com/watch?v=SS_IlBrocYQ>  

[← Back to index](../INDEX.md)

## 1. Simulation

The problem asks us to insert a new node between every pair of adjacent nodes, where the new node's value is the GCD of its neighbors. We traverse the list and for each pair of consecutive nodes, compute their `gcd` and create a new node with that value.
The Euclidean algorithm efficiently computes the `gcd`: repeatedly replace the larger number with the remainder of dividing the two numbers until one becomes zero. The other number is the `gcd`.
Since we're inserting nodes as we traverse, we need to be careful to advance the pointer past the newly inserted node to avoid processing it again.

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
    ListNode* insertGreatestCommonDivisors(ListNode* head) {
        if (!head) return nullptr;

        ListNode* cur = head;

        while (cur->next) {
            int n1 = cur->val, n2 = cur->next->val;
            int gcdValue = gcd(n1, n2);
            ListNode* newNode = new ListNode(gcdValue, cur->next);
            cur->next = newNode;
            cur = newNode->next;
        }

        return head;
    }

private:
    int gcd(int a, int b) {
        while (b > 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }
};
```

**Complexity**

- Time complexity: $O(n * \log (min(a, b)))$
- Space complexity:
    - $O(n)$ space for the gcd ListNodes.
    - $O(1)$ extra space.

> Where $n$ is the length of the given list, and $a$ and $b$ are two numbers passed to the $gcd()$ function.
