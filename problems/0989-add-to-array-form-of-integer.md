# 989. Add to Array-Form of Integer

- **Difficulty:** Easy  
- **Pattern:** Bit Manipulation  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/add-to-array-form-of-integer/>  
- **NeetCode:** <https://neetcode.io/problems/add-to-array-form-of-integer>  
- **Video:** <https://www.youtube.com/watch?v=eBTZQt1TWfk>  

[← Back to index](../INDEX.md)

## 1. Reverse and Add

Adding two numbers digit by digit is straightforward when we start from the least significant digit. Since the array represents a number with the most significant digit first, we can either reverse the array or process it from the end.

The trick here is to treat `k` as a running sum that absorbs both the addition and the carry. At each step, we add the current digit to `k`, extract the last digit of `k` as our result digit, and divide `k` by `10` to prepare for the next iteration. This elegantly combines the carry propagation into a single variable.

```cpp
class Solution {
public:
    vector<int> addToArrayForm(vector<int>& num, int k) {
        reverse(num.begin(), num.end());
        int i = 0;
        while (k) {
            int digit = k % 10;
            if (i < num.size()) {
                num[i] += digit;
            } else {
                num.push_back(digit);
            }
            int carry = num[i] / 10;
            num[i] %= 10;
            k /= 10;
            k += carry;
            i++;
        }
        reverse(num.begin(), num.end());
        return num;
    }
};
```

**Complexity**

- Time complexity: $O(max(n, m))$
- Space complexity: $O(n)$.

> Where $n$ is the size of the array $num$ and $m$ is the number of digits in $k$.

## 2. Without Reverse()

We can avoid the explicit reverse operation by inserting digits at the front of our result as we compute them. Using a deque (double-ended queue) or linked list allows O(1) insertion at the front.

The logic remains the same: process from right to left, compute each digit with the carry, and build the result. The difference is just in how we construct the output to avoid a final reversal step.

```cpp
class Solution {
public:
    vector<int> addToArrayForm(vector<int>& num, int k) {
        list<int> result;
        int carry = 0, i = num.size() - 1;

        while (i >= 0 || k > 0 || carry > 0) {
            int digit = k % 10;
            int sum = carry + (i >= 0 ? num[i] : 0) + digit;

            result.push_front(sum % 10);
            carry = sum / 10;

            k /= 10;
            i--;
        }

        return vector<int>(result.begin(), result.end());
    }
};
```

**Complexity**

- Time complexity: $O(max(n, m))$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $num$ and $m$ is the number of digits in $k$.
