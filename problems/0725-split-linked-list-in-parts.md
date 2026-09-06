# 725. Split Linked List in Parts

- **Difficulty:** Medium  
- **Pattern:** Linked List  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/split-linked-list-in-parts/>  
- **NeetCode:** <https://neetcode.io/problems/split-linked-list-in-parts>  
- **Video:** <https://www.youtube.com/watch?v=-OTlqdrxrVI>  

[← Back to index](../INDEX.md)

## 1. Convert To Array

To split the list into `k` parts as evenly as possible, we first need to know the total length. Converting the linked list to an array gives us random access, making it easy to determine where each part starts and ends. Each part gets `n / k` elements at minimum, and the first `n % k` parts get one extra element to distribute the remainder evenly.

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
    vector<ListNode*> splitListToParts(ListNode* head, int k) {
        vector<ListNode*> arr;
        for (ListNode* cur = head; cur != nullptr; cur = cur->next) {
            arr.push_back(cur);
        }

        int N = arr.size();
        int base_len = N / k, remainder = N % k;

        vector<ListNode*> res(k, nullptr);
        int start = 0;
        for (int i = 0; i < k; i++) {
            if (start < N) {
                res[i] = arr[start];
                int tail = start + base_len - 1;
                if (remainder > 0) {
                    tail++;
                    remainder--;
                }
                arr[tail]->next = nullptr;
                start = tail + 1;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Iteration

We can avoid the extra array by working directly with the linked list. First, count the total nodes. Then traverse again, splitting the list into parts by tracking the current node and severing links at the appropriate positions. The first `remainder` parts each have one more node than the remaining parts.

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
    vector<ListNode*> splitListToParts(ListNode* head, int k) {
        int length = 0;
        ListNode* curr = head;
        while (curr) {
            curr = curr->next;
            length++;
        }

        int baseLen = length / k, remainder = length % k;
        vector<ListNode*> res(k, nullptr);
        curr = head;

        for (int i = 0; i < k; i++) {
            res[i] = curr;
            for (int j = 0; j < baseLen - 1 + (remainder > 0 ? 1 : 0); j++) {
                if (!curr) break;
                curr = curr->next;
            }
            if (curr) {
                ListNode* temp = curr->next;
                curr->next = nullptr;
                curr = temp;
            }
            remainder--;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output array.
