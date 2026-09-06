# 1057. Campus Bikes

- **Difficulty:** Medium  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/campus-bikes/>  
- **NeetCode:** <https://neetcode.io/problems/campus-bikes>  

[← Back to index](../INDEX.md)

## 1. Sorting

We need to assign bikes to workers based on priority: smallest Manhattan distance first, then smallest worker index, then smallest bike index. By generating all possible worker-bike pairs with their distances and sorting them by these criteria, we can greedily assign each pair in order, skipping pairs where either the worker or bike is already taken.

```cpp
class Solution {
public:
    // Function to return the Manhattan distance
    int findDistance(vector<int>& worker, vector<int>& bike) {
        return abs(worker[0] - bike[0]) + abs(worker[1] - bike[1]);
    }

    vector<int> assignBikes(vector<vector<int>>& workers, vector<vector<int>>& bikes) {
        // List of WorkerBikeTuples's to store all the possible triplets
        vector<tuple<int, int, int>> allTriplets;

        // Generate all the possible pairs
        for (int worker = 0; worker < workers.size(); worker++) {
            for (int bike = 0; bike < bikes.size(); bike++) {
                int distance = findDistance(workers[worker], bikes[bike]);
                allTriplets.push_back({distance, worker, bike});
            }
        }

        // Sort the triplets. By default, each sorting will prioritize the
        // Tuple's first value, then second value, and finally the third value
        sort(allTriplets.begin(), allTriplets.end());

        // Initialize all values to false, to signify no bikes have been taken
        vector<int> bikeStatus(bikes.size(), false);
        // Initialize all index to -1, to signify no worker has a bike
        vector<int> workerStatus(workers.size(), -1);
        // Keep track of how many worker-bike pairs have been made
        int pairCount = 0;

        for (auto[dist, worker, bike] : allTriplets) {
            // If both worker and bike are free, assign them to each other
            if (workerStatus[worker] == -1 && !bikeStatus[bike]) {
                bikeStatus[bike] = true;
                workerStatus[worker] = bike;
                pairCount++;

                // If all the workers have the bike assigned, we can stop
                if (pairCount == workers.size()) {
                    return workerStatus;
                }
            }
        }

        return workerStatus;
    }
};
```

**Complexity**

- Time complexity: $O(N M \log (N M))$
- Space complexity: $O(N M)$

> Where $N$ is the number of workers, and $M$ is the number of bikes.

## 2. Bucket Sort

Since Manhattan distances on a 1000x1000 grid are bounded (maximum `1998`), we can use bucket sort instead of comparison-based sorting. By grouping worker-bike pairs by their distance, we can process pairs in distance order without explicit sorting. Within each distance bucket, pairs are naturally ordered by their insertion order (worker index first, then bike index).

```cpp
class Solution {
public:
    // Function to return the Manhattan distance
    int findDistance(vector<int>& worker, vector<int>& bike) {
        return abs(worker[0] - bike[0]) + abs(worker[1] - bike[1]);
    }

    vector<int> assignBikes(vector<vector<int>>& workers, vector<vector<int>>& bikes) {
        int minDis = INT_MAX;
        // Stores the list of (worker, bike) pairs corresponding to its distance
        vector<pair<int, int>> disToPairs[1999];

        // Add the (worker, bike) pairs corresponding to their distance list
        for (int worker = 0; worker < workers.size(); worker++) {
            for (int bike = 0; bike < bikes.size(); bike++) {
                int distance = findDistance(workers[worker], bikes[bike]);
                disToPairs[distance].push_back({worker, bike});
                minDis = min(minDis, distance);
            }
        }

        int currDis = minDis;
        // Initialize all values to false, to signify no bikes have been taken
        vector<int> bikeStatus(bikes.size(), false);
        // Initialize all index to -1, to signify no worker has a bike
        vector<int> workerStatus(workers.size(), -1);
        // Keep track of how many worker-bike pairs have been made
        int pairCount = 0;

        // Until all workers have not been assigned a bike
        while (pairCount != workers.size()) {
            for (auto[worker, bike] : disToPairs[currDis]) {
                if (workerStatus[worker] == -1 && !bikeStatus[bike]) {
                    // If both worker and bike are free, assign them to each other
                    bikeStatus[bike] = true;
                    workerStatus[worker] = bike;
                    pairCount++;
                }
            }
            currDis++;
        }

        return workerStatus;
    }
};
```

**Complexity**

- Time complexity: $O(N M + K)$
- Space complexity: $O(N M + K)$

> Where $N$ is the number of workers, $M$ is the number of bikes, and $K$ is the maximum possible Manhattan distance of a worker/bike pair. In this problem, $K$ equals $1998$.

## 3. Priority Queue

Instead of storing all worker-bike pairs upfront, we can use a priority queue that only tracks the current best option for each worker. When a bike is taken, we add the next best option for that worker to the queue. This reduces memory usage since we only need the closest available bike for each unassigned worker at any time.

```cpp
class Solution {
public:
    // Function to return the Manhattan distance
    int distance(vector<int>& worker_loc, vector<int>& bike_loc) {
        return abs(worker_loc[0] - bike_loc[0]) + abs(worker_loc[1] - bike_loc[1]);
    }

    vector<int> assignBikes(vector<vector<int>>& workers, vector<vector<int>>& bikes) {
        // List of triplets (distance, worker, bike) for each bike corresponding to worker
        vector<vector<tuple<int, int, int>>> workerToBikeList;

        priority_queue<tuple<int, int, int>, vector<tuple<int, int, int>>,
                       greater<tuple<int, int, int>>> pq;

        for (int worker = 0; worker < workers.size(); worker++) {
            // Add all the bikes with their distances from the current worker
            vector<tuple<int, int, int>> currWorkerPairs;
            for (int bike = 0; bike < bikes.size(); bike++) {
                int dist = distance(workers[worker], bikes[bike]);
                currWorkerPairs.push_back({dist, worker, bike});
            }

            // Sort the workerToBikeList for the current worker in reverse order.
            sort(currWorkerPairs.begin(), currWorkerPairs.end(), greater<tuple<int, int, int>>());

            // For each worker, add their closest bike to the priority queue
            pq.push(currWorkerPairs.back());
            // Second last bike is now the closest bike for this worker
            currWorkerPairs.pop_back();

            // Store the remaining options for the current worker in workerToBikeList
            workerToBikeList.push_back(currWorkerPairs);
        }

        // Initialize all values to false, to signify no bikes have been taken
        vector<int> bikeStatus(bikes.size(), false);
        // Initialize all index to -1, to signify no worker has a bike
        vector<int> workerStatus(workers.size(), -1);

        while (!pq.empty()) {
            // Pop the pair with smallest distance
            auto[dist, worker, bike] = pq.top();
            pq.pop();
            bike = bike;
            worker = worker;

            if (!bikeStatus[bike]) {
                // If the bike is free, assign the bike to the worker
                bikeStatus[bike] = true;
                workerStatus[worker] = bike;
            } else {
                // Otherwise, add the next closest bike for the current worker
                pq.push(workerToBikeList[worker].back());
                workerToBikeList[worker].pop_back();
            }
        }

        return workerStatus;
    }
};
```

**Complexity**

- Time complexity: $O(N M \log M)$
- Space complexity: $O(N M)$

> Where $N$ is the number of workers, and $M$ is the number of bikes.
