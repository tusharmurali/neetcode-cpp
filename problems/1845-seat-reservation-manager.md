# 1845. Seat Reservation Manager

- **Difficulty:** Medium  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/seat-reservation-manager/>  
- **NeetCode:** <https://neetcode.io/problems/seat-reservation-manager>  
- **Video:** <https://www.youtube.com/watch?v=ahobllKXEEY>  
- **Video approach:** 2. Min-Heap (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest way to manage seat reservations is to track each seat's status with a boolean array. When someone reserves, we scan from the beginning to find the first unreserved seat. When someone unreserves, we simply mark that seat as available again. This guarantees we always return the smallest available seat number, but the linear scan makes reservations slow for large numbers of seats.

```cpp
class SeatManager {
private:
    vector<bool> seats;

public:
    SeatManager(int n) : seats(n, false) {}

    int reserve() {
        for (int i = 0; i < seats.size(); i++) {
            if (!seats[i]) {
                seats[i] = true;
                return i + 1;
            }
        }
        return -1;
    }

    void unreserve(int seatNumber) {
        seats[seatNumber - 1] = false;
    }
};
```

**Complexity**

- Time complexity:
    - $O(n)$ time for initialization.
    - $O(n)$ time for each $reserve()$ function call.
    - $O(1)$ time for each $unreserve()$ function call.
- Space complexity: $O(n)$

## 2. Min-Heap ▶ video

To efficiently retrieve the smallest available seat, we can use a min-heap. By initializing the heap with all seat numbers from 1 to `n`, the smallest seat is always at the top. Reserving pops from the heap, and unreserving pushes back onto it. The heap maintains the ordering automatically.

```cpp
class SeatManager {
private:
    priority_queue<int, vector<int>, greater<int>> unres;

public:
    SeatManager(int n) {
        for (int i = 1; i <= n; i++) {
            unres.push(i);
        }
    }

    int reserve() {
        int seat = unres.top();
        unres.pop();
        return seat;
    }

    void unreserve(int seatNumber) {
        unres.push(seatNumber);
    }
};
```

**Complexity**

- Time complexity:
    - $O(n \log n)$ time for initialization.
    - $O(\log n)$ time for each $reserve()$ function call.
    - $O(\log n)$ time for each $unreserve()$ function call.
- Space complexity: $O(n)$

## 3. Min-Heap (Optimal)

Rather than pre-populating the heap with all `n` seats, we can lazily assign seats. We track a counter `nextSeat` that represents the next fresh seat to assign. When reserving, if no previously unreserved seats are in the heap, we simply hand out `nextSeat` and increment it. This avoids O(n log n) initialization and handles the common case where seats are reserved in order very efficiently.

```cpp
class SeatManager {
private:
    priority_queue<int, vector<int>, greater<int>> minHeap;
    int nextSeat;

public:
    SeatManager(int n) {
        nextSeat = 1;
    }

    int reserve() {
        if (!minHeap.empty()) {
            int seat = minHeap.top();
            minHeap.pop();
            return seat;
        }
        return nextSeat++;
    }

    void unreserve(int seatNumber) {
        minHeap.push(seatNumber);
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(\log n)$ time for each $reserve()$ function call.
    - $O(\log n)$ time for each $unreserve()$ function call.
- Space complexity: $O(n)$

## 4. Ordered Set

An ordered set (like TreeSet or SortedSet) keeps elements sorted and allows efficient retrieval of the minimum. Similar to the optimal min-heap approach, we lazily track unreserved seats. The ordered set provides O(log n) insertion, deletion, and minimum retrieval, making it a clean alternative to the heap.

```cpp
class SeatManager {
private:
    set<int> available;
    int nextSeat;

public:
    SeatManager(int n) {
        nextSeat = 1;
    }

    int reserve() {
        if (!available.empty()) {
            int seat = *available.begin();
            available.erase(available.begin());
            return seat;
        }
        return nextSeat++;
    }

    void unreserve(int seatNumber) {
        available.insert(seatNumber);
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ time for initialization.
    - $O(\log n)$ time for each $reserve()$ function call.
    - $O(\log n)$ time for each $unreserve()$ function call.
- Space complexity: $O(n)$

## Standalone solution file (`cpp/1845-seat-reservation-manager.cpp` in the NeetCode repo)

```cpp
class SeatManager {
private:
    priority_queue<int, vector<int>, greater<int>> minHeap;
public:
    SeatManager(int n) {
        for (int i=1; i<=n; ++i)
            minHeap.push(i);
    }
    
    int reserve() {
        int smallestSeat = minHeap.top();
        minHeap.pop();
        return smallestSeat;
    }
    
    void unreserve(int seatNumber) {
        minHeap.push(seatNumber);
    }
};

/**
 * Your SeatManager object will be instantiated and called as such:
 * SeatManager* obj = new SeatManager(n);
 * int param_1 = obj->reserve();
 * obj->unreserve(seatNumber);
 */
```
