# 281. Zigzag Iterator

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/zigzag-iterator/>  
- **NeetCode:** <https://neetcode.io/problems/zigzag-iterator>  

[← Back to index](../INDEX.md)

## 1. Two-Pointers

To iterate through multiple vectors in zigzag order, we need to alternate between vectors while tracking our position in each. The key insight is to maintain two pointers: one for the current vector and one for the current element index. We cycle through vectors in round-robin fashion, and when we complete a full round across all vectors, we advance the element `index`. This ensures we visit elements in the correct zigzag order while handling vectors of different lengths.

```cpp
class ZigzagIterator {
private:
    vector<vector<int>> vectors;
    // pointer to vector, and pointer to element
    int pVec = 0, pElem = 0;
    int totalNum = 0, outputCount = 0;

public:
    ZigzagIterator(vector<int>& v1, vector<int>& v2) {
        vectors.push_back(v1);
        vectors.push_back(v2);

        for (const auto& vec : vectors) {
            totalNum += vec.size();
        }
    }

    int next() {
        int iterNum = 0;
        int ret = -1;
        bool found = false;

        while (iterNum < vectors.size()) {
            vector<int>& currVec = vectors[pVec];

            if (pElem < currVec.size()) {
                ret = currVec[pElem];
                outputCount += 1;
                found = true;
            }

            iterNum += 1;
            pVec = (pVec + 1) % vectors.size();

            // increment the element pointer once iterating all vectors
            if (pVec == 0)
                pElem += 1;

            if (found)
                return ret;
        }

        // one should raise an exception here.
        return 0;
    }

    bool hasNext() {
        return outputCount < totalNum;
    }
};
```

**Complexity**

- Time Complexity:
    - For the `next()` function, at most it will take us $K$ iterations to find a valid element to output. Hence, its time complexity is $O(K)$.

    - For the `hasNext()` function, its time complexity is $O(1)$.

- Space Complexity:
    - For the `next()` function, we keep the references to all the input vectors in the variable `self.vectors`.
    - As a result, we would need $O(K)$ space for $K$ vectors.
    - In addition, we used some constant-space variables such as the pointers to the vector and the element.
    - Hence, the overall space complexity for this function is $O(K)$.

    - Note: we did not copy the input vectors, but simply keep references to them.

> Where $K$ is the number of input vectors. Although it is always two in the setting of this problem, this variable becomes relevant once the input becomes $K$ vectors.

## 2. Queue of Pointers

Using a queue to manage pointers provides a cleaner and more efficient approach. Instead of scanning through all vectors on each call, we maintain a queue of (vector `index`, element `index`) pairs representing which elements are ready to be returned. After returning an element, we add the pointer for the next element in that vector (if any) to the back of the queue. This naturally handles vectors of different lengths and ensures `O(1)` time for each `next()` call.

```cpp
class ZigzagIterator {
private:
    vector<vector<int>> vectors;
    queue<pair<int, int>> q;

public:
    ZigzagIterator(vector<int>& v1, vector<int>& v2) {
        vectors.push_back(v1);
        vectors.push_back(v2);

        for (int index = 0; index < vectors.size(); index++) {
            if (vectors[index].size() > 0) {
                // <index_to_vec, index_to_element_within_vec>
                q.push({index, 0});
            }
        }
    }

    int next() {
        // <index_to_vec, index_to_element_within_vec>
        pair<int, int> pointer = q.front();
        q.pop();

        int vecIndex = pointer.first;
        int elemIndex = pointer.second;
        int nextElemIndex = elemIndex + 1;

        // append the pointer for the next round
        // if there are some elements left.
        if (nextElemIndex < vectors[vecIndex].size()) {
            q.push({vecIndex, nextElemIndex});
        }

        return vectors[vecIndex][elemIndex];
    }

    bool hasNext() {
        return q.size() > 0;
    }
};
```

**Complexity**

- Time Complexity: $O(1)$
    - For both the `next()` function and the `hasNext()` function, we have a constant time complexity, as we discussed before.

- Space Complexity: $O(K)$
    - We use a queue to keep track of the _pointers_ to the input vectors in the variable `self.vectors`.
    - As a result, we would need $O(K)$ space for $K$ vectors.

    - Although the size of the queue will reduce over time once we exhaust some shorter vectors, the space complexity for both functions is still $O(K)$.

> Where $K$ is the number of input vectors. Although it is always two in the setting of this problem, this variable becomes relevant once the input becomes $K$ vectors.
