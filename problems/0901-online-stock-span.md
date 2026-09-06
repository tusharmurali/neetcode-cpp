# 901. Online Stock Span

- **Difficulty:** Medium  
- **Pattern:** Stack  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/online-stock-span/>  
- **NeetCode:** <https://neetcode.io/problems/online-stock-span>  
- **Video:** <https://www.youtube.com/watch?v=slYh0ZNEqSw>  
- **Video approach:** 2. Monotonic Decreasing Stack  

[← Back to index](../INDEX.md)

## 1. Brute Force

The stock span is the number of consecutive days (including today) where the price was less than or equal to today's price. The simplest approach is to store all prices and, for each new price, look backward through the history counting days until we find a higher price.

```cpp
class StockSpanner {
    vector<int> arr;

public:
    StockSpanner() {}

    int next(int price) {
        arr.push_back(price);
        int i = arr.size() - 2;
        while (i >= 0 && arr[i] <= price) {
            i--;
        }
        return arr.size() - i - 1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

> Where $n$ is the number of function calls.

## 2. Monotonic Decreasing Stack ▶ video

The brute force approach repeatedly scans the same elements. We can avoid this by using a monotonic decreasing stack that stores pairs of `(price, span)`.

When a new price arrives, we pop all entries from the stack that have prices less than or equal to the current price. The span of the current day is `1` (for today) plus the sum of spans of all popped entries. This works because those popped entries represent consecutive days that are now "covered" by the current higher price.

The stack remains in decreasing order of prices, so each element is pushed and popped at most once across all operations.

```cpp
class StockSpanner {
    stack<pair<int, int>> stack; // pair: (price, span)

public:
    StockSpanner() {}

    int next(int price) {
        int span = 1;
        while (!stack.empty() && stack.top().first <= price) {
            span += stack.top().second;
            stack.pop();
        }
        stack.push({price, span});
        return span;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the number of function calls.

## Standalone solution file (`cpp/0901-online-stock-span.cpp` in the NeetCode repo)

```cpp
class StockSpanner {
public:
    
    stack<pair<int, int>> st;
    pair<int, int> pr;
    StockSpanner() {
        pr = {0, 0};
    }
    
    int next(int price) {

        int ret = 1;
        while (!st.empty() && price >= pr.first)
        {
            ret += pr.second;
            st.pop();
            if (!st.empty())
                pr = st.top();
        }
        st.push(make_pair(price, ret));
        pr = st.top();
        return (ret);
    }
};

/**
 * Your StockSpanner object will be instantiated and called as such:
 * StockSpanner* obj = new StockSpanner();
 * int param_1 = obj->next(price);
 */
```
