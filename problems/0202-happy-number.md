# 202. Happy Number

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/happy-number/>  
- **NeetCode:** <https://neetcode.io/problems/non-cyclical-number>  
- **Video:** <https://www.youtube.com/watch?v=ljz85bxOYJ0>  

[← Back to index](../INDEX.md)

## 1. Hash Set

A number is called **happy** if repeatedly replacing it with the **sum of the squares of its digits** eventually leads to `1`.

While doing this process, only two things can happen:

- we eventually reach `1` → the number is happy
- we fall into a **cycle** and repeat numbers forever → the number is not happy

So the key problem is **cycle detection**.

A simple and beginner-friendly way to detect a cycle is to:

- keep a **set** of numbers we have already seen
- if a number repeats, we are stuck in a loop and will never reach `1`

```cpp
class Solution {
public:
    bool isHappy(int n) {
        unordered_set<int> visit;

        while (visit.find(n) == visit.end()) {
            visit.insert(n);
            n = sumOfSquares(n);
            if (n == 1) {
                return true;
            }
        }
        return false;
    }

private:
    int sumOfSquares(int n) {
        int output = 0;

        while (n > 0) {
            int digit = n % 10;
            digit = digit * digit;
            output += digit;
            n /= 10;
        }
        return output;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(\log n)$

## 2. Fast And Slow Pointers - I

A number is **happy** if repeatedly replacing it with the **sum of the squares of its digits** eventually reaches `1`.

Just like the hash set approach, the process can:

- reach `1` → happy number
- fall into a **cycle** → not a happy number

Instead of storing all visited numbers, we can detect a cycle using the **fast and slow pointers technique** (also known as Floyd's cycle detection).

The idea:

- treat the transformation `n → sumOfSquares(n)` like moving through a linked list
- use two pointers:
    - `slow` moves **one step at a time**
    - `fast` moves **two steps at a time**
- if there is a cycle, `slow` and `fast` will eventually meet
- if the cycle includes `1`, then the number is happy

This avoids extra memory and still reliably detects cycles.

```cpp
class Solution {
public:
    bool isHappy(int n) {
        int slow = n, fast = sumOfSquares(n);

        while (slow != fast) {
            fast = sumOfSquares(fast);
            fast = sumOfSquares(fast);
            slow = sumOfSquares(slow);
        }

        return fast == 1;
    }

private:
    int sumOfSquares(int n) {
        int output = 0;
        while (n != 0) {
            output += (n % 10) * (n % 10);
            n /= 10;
        }
        return output;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 3. Fast And Slow Pointers - II

A number is **happy** if repeatedly replacing it with the **sum of the squares of its digits** eventually reaches `1`.

Just like before, this process either:

- reaches `1` → happy number
- falls into a **cycle** → not a happy number

This solution uses a different cycle detection method called **Brent's Algorithm**, which is another form of fast–slow pointer technique.

Key idea:

- We still move through the sequence `n → sumOfSquares(n)`
- But instead of moving one pointer twice as fast every step, we:
    - increase the distance between comparisons in **powers of two**
- This reduces the number of comparisons and still guarantees cycle detection

We keep track of:

- `slow` → a checkpoint value
- `fast` → the moving value
- `power` → how far we go before resetting `slow`
- `lam` → current distance since last reset

If `fast` ever equals `slow`, a cycle is detected.

```cpp
class Solution {
public:
    bool isHappy(int n) {
        int slow = n, fast = sumOfSquares(n);
        int power = 1, lam = 1;

        while (slow != fast) {
            if (power == lam) {
                slow = fast;
                power *= 2;
                lam = 0;
            }
            lam++;
            fast = sumOfSquares(fast);
        }

        return fast == 1;
    }

private:
    int sumOfSquares(int n) {
        int output = 0;
        while (n != 0) {
            output += (n % 10) * (n % 10);
            n /= 10;
        }
        return output;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0202-happy-number.cpp` in the NeetCode repo)

```cpp
/*
    Given num, replace by sum of squares of its digits
    Repeat until 1 or endless loop, determine if ends in 1
    Ex. n = 19 -> true, 1^2 + 9^2 = 82, 8^2 + 2^2 = 68 ... 1

    Detect cycle w/ slow/fast pointer technique
    If happy will eventually be 1, else pointers will meet

    Time: O(log n)
    Space: O(1)
*/

class Solution {
public:
    bool isHappy(int n) {
        int slow = n;
        int fast = getNext(n);
        
        while (slow != fast && fast != 1) {
            slow = getNext(slow);
            fast = getNext(getNext(fast));
        }
        
        if (fast == 1) {
            return true;
        }
        return false;
    }
private:
    int getNext(int n) {
        int sum = 0;
        while (n > 0) {
            int digit = n % 10;
            n /= 10;
            sum += pow(digit, 2);
        }
        return sum;
    }
};
```
