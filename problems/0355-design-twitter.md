# 355. Design Twitter

- **Difficulty:** Medium  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/design-twitter/>  
- **NeetCode:** <https://neetcode.io/problems/design-twitter-feed>  
- **Video:** <https://www.youtube.com/watch?v=pNichitDD2E>  
- **Video approach:** 2. Heap  

[← Back to index](../INDEX.md)

## 1. Sorting

Each user has their own tweets, and they also see tweets from all the people they follow.  
To build the news feed:

1. Collect all tweets from the user.
2. Collect all tweets from every followee.
3. Combine these tweets into one list.
4. Sort them by timestamp (most recent first).
5. Return the first `10` tweet IDs.

This works because sorting guarantees we always pick the latest `10` tweets, regardless of who posted them.

```cpp
class Twitter {
    int time;
    unordered_map<int, unordered_set<int>> followMap;
    unordered_map<int, vector<pair<int, int>>> tweetMap;
public:
    Twitter() : time(0) {}

    void postTweet(int userId, int tweetId) {
        tweetMap[userId].push_back({time++, tweetId});
    }

    vector<int> getNewsFeed(int userId) {
        vector<pair<int, int>> feed = tweetMap[userId];
        for (int followeeId : followMap[userId]) {
            feed.insert(feed.end(), tweetMap[followeeId].begin(),
                                    tweetMap[followeeId].end());
        }
        sort(feed.begin(), feed.end(), [](auto &a, auto &b) {
            return a.first > b.first;
        });
        vector<int> res;
        for (int i = 0; i < min(10, (int)feed.size()); ++i) {
            res.push_back(feed[i].second);
        }
        return res;
    }

    void follow(int followerId, int followeeId) {
        if (followerId != followeeId) {
            followMap[followerId].insert(followeeId);
        }
    }

    void unfollow(int followerId, int followeeId) {
        followMap[followerId].erase(followeeId);
    }
};
```

**Complexity**

- Time complexity: $O(n * m + t\log t)$ for each $getNewsFeed()$ call and $O(1)$ for remaining methods.
- Space complexity: $O(N * m + N * M)$

> Where $n$ is the total number of $followeeIds$ associated with the $userId$, $m$ is the maximum number of tweets by any user, $t$ is the total number of tweets associated with the $userId$ and its $followeeIds$, $N$ is the total number of $userIds$ and $M$ is the maximum number of followees for any user.

## 2. Heap ▶ video

Each user can follow many people, and each of those people may have many tweets.  
Instead of combining **all** tweets and sorting them (which is slow), we only need the **`10` most recent tweets**.

We use a **min-heap** (priority queue) because:

- We start by pushing the latest tweet from each followee.
- Smaller `count` means the tweet is more recent.
- When we pop a tweet, we push the next older tweet from that same user.
- We repeat this until we collect `10` tweets.
- One user can still contribute many tweets if they are the most recent.

This ensures:

- We never sort huge lists.
- The heap always contains at most “number of followees” entries.
- We only perform work proportional to the `10` tweets we need.

```cpp
class Twitter {
    int count;
    unordered_map<int, vector<vector<int>>> tweetMap;
    unordered_map<int, set<int>> followMap;

public:
    Twitter() {
        count = 0;
    }

    void postTweet(int userId, int tweetId) {
        tweetMap[userId].push_back({count++, tweetId});
    }

    vector<int> getNewsFeed(int userId) {
        vector<int> res;
        auto compare = [](const vector<int>& a, const vector<int>& b) {
            return a[0] < b[0];
        };
        priority_queue<vector<int>, vector<vector<int>>, decltype(compare)> minHeap(compare);

        followMap[userId].insert(userId);
        for (int followeeId : followMap[userId]) {
            if (tweetMap.count(followeeId)) {
                const vector<vector<int>>& tweets = tweetMap[followeeId];
                int index = tweets.size() - 1;
                minHeap.push({tweets[index][0], tweets[index][1], followeeId, index});
            }
        }

        while (!minHeap.empty() && res.size() < 10) {
            vector<int> curr = minHeap.top();
            minHeap.pop();
            res.push_back(curr[1]);
            int index = curr[3];
            if (index > 0) {
                const vector<int>& tweet = tweetMap[curr[2]][index - 1];
                minHeap.push({tweet[0], tweet[1], curr[2], index - 1});
            }
        }
        return res;
    }

    void follow(int followerId, int followeeId) {
        followMap[followerId].insert(followeeId);
    }

    void unfollow(int followerId, int followeeId) {
        followMap[followerId].erase(followeeId);
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$ for each $getNewsFeed()$ call and $O(1)$ for remaining methods.
- Space complexity: $O(N * m + N * M + n)$

> Where $n$ is the total number of $followeeIds$ associated with the $userId$, $m$ is the maximum number of tweets by any user, $N$ is the total number of $userIds$ and $M$ is the maximum number of followees for any user.

## 3. Heap (Optimal)

The basic heap solution looks at **all tweets of all followees**, which is fast enough but can be improved.

Key observation:

- Each user only cares about the **latest `10` tweets**, because the news feed returns at most `10` items.
- So for each user, instead of storing _all_ tweets, store only their **`10` most recent** tweets.
- This reduces:
    - Memory usage
    - Heap operations
    - Time per query

The trick:

- When a user posts a tweet, append it with a decreasing timestamp (`count`) and keep only the last `10` tweets.
- When getting the news feed:
    - If the user follows many people (>= `10`), keep only the `10` followees with the newest latest tweet by using a max-heap of size `10`.
    - This is safe: if a followee's newest tweet is already too old, none of their older tweets can make the final `10`.
    - Otherwise, push the latest tweet from each followee into a min-heap and keep expanding from the same user after each pop.
- In both cases, we never process more than **`10` tweets per followee**, and never extract more than **`10` results**.

This makes the method very fast even when users post a lot of tweets.

```cpp
class Twitter {
public:
    int count;
    unordered_map<int, vector<pair<int,int>>> tweetMap;
    unordered_map<int, unordered_set<int>> followMap;

    Twitter() {
        count = 0;
    }

    void postTweet(int userId, int tweetId) {
        tweetMap[userId].push_back({count, tweetId});
        if (tweetMap[userId].size() > 10) {
            tweetMap[userId].erase(tweetMap[userId].begin());
        }
        count--;
    }

    vector<int> getNewsFeed(int userId) {
        vector<int> res;
        followMap[userId].insert(userId);
        priority_queue<vector<int>, vector<vector<int>>, greater<vector<int>>> minHeap;
        if (followMap[userId].size() >= 10) {
            priority_queue<vector<int>> maxHeap;
            for (auto f : followMap[userId]) {
                if (!tweetMap.count(f)) continue;
                int idx = tweetMap[f].size() - 1;
                auto &p = tweetMap[f][idx];
                maxHeap.push({-p.first, p.second, f, idx - 1});
                if (maxHeap.size() > 10) maxHeap.pop();
            }
            while (!maxHeap.empty()) {
                auto t = maxHeap.top();
                maxHeap.pop();
                minHeap.push({-t[0], t[1], t[2], t[3]});
            }
        } else {
            for (auto f : followMap[userId]) {
                if (!tweetMap.count(f)) continue;
                int idx = tweetMap[f].size() - 1;
                auto &p = tweetMap[f][idx];
                minHeap.push({p.first, p.second, f, idx - 1});
            }
        }
        while (!minHeap.empty() && res.size() < 10) {
            auto t = minHeap.top();
            minHeap.pop();
            res.push_back(t[1]);
            int idx = t[3];
            if (idx >= 0) {
                auto &p = tweetMap[t[2]][idx];
                minHeap.push({p.first, p.second, t[2], idx - 1});
            }
        }
        return res;
    }

    void follow(int followerId, int followeeId) {
        followMap[followerId].insert(followeeId);
    }

    void unfollow(int followerId, int followeeId) {
        if (followMap[followerId].count(followeeId)) {
            followMap[followerId].erase(followeeId);
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$ for each $getNewsFeed()$ call and $O(1)$ for remaining methods.
- Space complexity: $O(N * m + N * M + n)$

> Where $n$ is the total number of $followeeIds$ associated with the $userId$, $m$ is the maximum number of tweets by any user ($m$ can be at most $10$), $N$ is the total number of $userIds$ and $M$ is the maximum number of followees for any user.

## Standalone solution file (`cpp/0355-design-twitter.cpp` in the NeetCode repo)

```cpp
/*
    Design Twitter: post tweets, follow/unfollow, see recent tweets

    Maintain user -> tweet pairs & hash map {user -> ppl they follow}

    Time: O(n)
    Space: O(n)
*/

class Twitter {
public:
    Twitter() {
        
    }
    
    void postTweet(int userId, int tweetId) {
        posts.push_back({userId, tweetId});
    }
    
    vector<int> getNewsFeed(int userId) {
        // 10 tweets
        int count = 10;
        vector<int> result;
        
        // since postTweet pushes to the back, looping from back gets most recent
        for (int i = posts.size() - 1; i >= 0; i--) {
            if (count == 0) {
                break;
            }
            
            int followingId = posts[i].first;
            int tweetId = posts[i].second;
            unordered_set<int> following = followMap[userId];
            // add to result if they're following them or it's a tweet from themself
            if (following.find(followingId) != following.end() || followingId == userId) {
                result.push_back(tweetId);
                count--;
            }
        }
        
        return result;
    }
    
    void follow(int followerId, int followeeId) {
        followMap[followerId].insert(followeeId);
    }
    
    void unfollow(int followerId, int followeeId) {
        followMap[followerId].erase(followeeId);
    }
private:
    // pairs: [user, tweet]
    vector<pair<int, int>> posts;
    // hash map: {user -> people they follow}
    unordered_map<int, unordered_set<int>> followMap;
};

/**
 * Your Twitter object will be instantiated and called as such:
 * Twitter* obj = new Twitter();
 * obj->postTweet(userId,tweetId);
 * vector<int> param_2 = obj->getNewsFeed(userId);
 * obj->follow(followerId,followeeId);
 * obj->unfollow(followerId,followeeId);
 */
```
