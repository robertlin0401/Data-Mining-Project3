# Project 3
contributed by < `robertlin0401` >

###### tags: `資料探勘`

> [GitHub](https://github.com/robertlin0401/Data-Mining-Project3)
---

## 作業要求
- [X] 實作 HITS 演算法，輸出 authority 及 hub 值
- [X] 實作 PageRank 演算法，輸出 PageRank 值
- [X] 實作 SimRank 演算法，輸出 SimRank 值
- [X] graph 1~6 和 IBM 檔都須可以執行
- [X] 撰寫 report

## 說明
### 檔案結構
* data：輸入檔案存放之目錄，內含 graph 1~6 和 IBM 檔
* output：輸出檔案存放之目錄
* src：存放主程式以外的原始碼之目錄
    * HITS.<span>py</span>：HITS 演算法之實作
    * PageRank.<span>py</span>：PageRank 演算法之實作
    * SimRank.<span>py</span>：SimRank 演算法之實作
    * dataloader.<span>py</span>：處理讀檔並整理成特定格式
* graph.<span>py</span>：用於繪製 graph 1-3 的圖，並列出 authority、hub 及 PageRank 值
* main.<span>py</span>：主程式
* README.<span>md</span>：即為[本文件](https://hackmd.io/@robertlin0401/Data-Mining-Project3)

### 執行
`python main.py`

### 開發流程與運作原理
#### main
* 執行以下步驟：
    1. 使用 [dataloader 模組](#dataloader) 讀取輸入資料
    2. 使用 [HITS 模組](#HITS) 計算 authority 與 hub 值，並儲存成對應輸出檔案
    3. 使用 [PageRank 模組](#PageRank) 計算 PageRank 值，並儲存成對應輸出檔案
    4. 使用 [SimRank 模組](#SimRank) 計算 SimRank 值，並儲存成對應輸出檔案
* 各模組於下方詳述

#### dataloader
```python=
# Read graph data at {path} and return an adjacent matrix of that graph.
def readGraph(path):
    lines = []
    max_node_id = 0

    # Read lines and find the max node id.
    with open(path, 'r') as fd:
        for line in fd.read().splitlines():
            lines.append(line)
            local_max = max(int(line.split(',')[0]), int(line.split(',')[1]))
            if max_node_id < local_max:
                max_node_id = local_max
        fd.close()
    
    # Build the adjacent matrix.
    adj_matrix = np.zeros((max_node_id, max_node_id))
    for line in lines:
        adj_matrix[int(line.split(',')[0]) - 1][int(line.split(',')[1]) - 1] = 1
    
    return adj_matrix
```
* 對於 graph 資料，傳遞該檔案之路徑給 `readGraph` 函式，即可得到該 graph 資料的 adjacent matrix 作為回傳值
* line 6-13 進行讀檔，將內容暫存於變數 `lines` 中，並在讀檔過程中計算最大 node id，作為 adjacent matrix 大小的依據
* line 15-18 根據最大 node id 生成對應大小的 adjacent matrix，並將暫存資料一一取出，以設置 adjacent matrix 之值

```python=
# Read IBM data at {path}, form a graph which links each transaction id
# to each item id, and return an adjacent matrix of that graph.
def readIBM(path):
    lines = []
    max_node_id = 0

    # Read lines and find the max node id.
    with open(path, 'r') as fd:
        for line in fd.read().splitlines():
            temp = []
            for ele in line.split(" "):
                if ele:
                    temp.append(ele)
            temp.pop(0)
            lines.append(temp)
            if max_node_id < max(int(temp[0]), int(temp[1])):
                max_node_id = max(int(temp[0]), int(temp[1]))
        fd.close()
    
    # Build the adjacent matrix.
    adj_matrix = np.zeros((max_node_id, max_node_id))
    for line in lines:
        adj_matrix[int(line[0]) - 1][int(line[1]) - 1] = 1
    
    return adj_matrix
```
* 對於 IBM 資料亦同理，僅因為資料格式不同而處理過程有些許不同
* edge 的方向規定為從 transaction id 指向 item id

#### HITS
```python=
def run(adj_matrix):
    length = len(adj_matrix)
    a = np.ones(length)
    h = np.ones(length)

    while True:
        new_a = np.dot(adj_matrix.T, h)
        new_h = np.dot(adj_matrix, a)

        new_a = new_a / sum(new_a)
        new_h = new_h / sum(new_h)

        if (sum(abs(a - new_a)) + sum(abs(h - new_h)) < 0.001):
            break
        
        a = new_a
        h = new_h

    return a, h
```
* line 7-8 使用矩陣形式計算
    * `a` 為紀錄所有 node 的 authority 值的矩陣，`h` 為紀錄所有 node 的 hub 值的矩陣
    * 一個 node 的 authority 值為該 node 的 parent 的 hub 值的總和，故只要將 adjacent matrix 做轉置後與 `h` 做矩陣乘法即可得到新的 `a` 矩陣，暫存為 `new_a`
    * 一個 node 的 hub 值為該 node 的 children 的 authority 值的總和，故只要將 adjacent matrix 與 `a` 做矩陣乘法即可得到新的 `h` 矩陣，暫存為 `new_h`
* line 10-11 將 `new_a` 與 `new_h` 進行正規化
* line 13-17 將正規化後的 `new_a` 與 `new_h` 與上一階段的 `a` 與 `h` 做比較，若差距足夠少則視為已收斂並結束計算，否則將 `a` 與 `h` 替換掉並進行下一階段的計算

#### PageRank
```python=
def run(adj_matrix):
    length = len(adj_matrix)
    r = np.ones(length) / length
    d = 0.1

    for index, row in enumerate(adj_matrix):
        if sum(row) != 0:
            adj_matrix[index] = row / sum(row)

    while True:
        new_r = d / length + (1 - d) * np.dot(adj_matrix.T, r)

        new_r = new_r / sum(new_r)

        if (sum(abs(r - new_r)) < 0.001):
            break
        
        r = new_r

    return r
```
* Damping Factor $d = 0.1$
* line 6-8 為了使用矩陣形式做計算，需要對 adjacent matrix 先做處理
    * 若 `adj_matrix[i, j]` 為 1，則須將其除以 node `i` 之 out-degree
* line 11 為 PageRank 的計算公式
    ![](https://i.imgur.com/9n4EVom.png)
* 後續與 HITS 演算法同理，正規化後若與原本差距足夠少則視為已收斂並結束計算，否則進入下一階段計算

#### SimRank
```python=
def run(adj_matrix):
    length = len(adj_matrix)
    C = 0.5

    W = np.array(adj_matrix.T)
    for index, row in enumerate(W):
        W[index] = [(1 / sum(row)) if i == 1 else 0 for i in row]
    W = W.T

    s = np.dot(W.T, W) * C
    np.fill_diagonal(s, 1)

    while True:
        new_s = np.dot(np.dot(W.T, s), W) * C
        np.fill_diagonal(new_s, 1)
        
        if (sum(sum(abs(s - new_s))) < 0.001):
            break

        s = new_s

    return s
```
* Decay Factor $C = 0.5$
* 起初我按照定義以雙層 `for` 迴圈一一計算每個 index 的 SimRank 值，卻發現在資料量較大時，效率會非常差（大約從 graph 5 的資料量就開始看得出有明顯的效率問題）
* 為改善效率問題，我找到了 SimRank 的[矩陣形式計算方法](https://zh.wikipedia.org/wiki/SimRank#%E7%9F%A9%E9%98%B5%E5%BD%A2%E5%BC%8F)，並使用資料量較少的測資驗證後做了一些邏輯上的調整
* line 5-8 與 PageRank 演算法類似，為了使用矩陣形式做計算，需要對 adjacent matrix 先做處理，但處理方法有些微不同
    * 若 `adj_matrix[i, j]` 為 1，則須將其除以 node `j` 之 in-degree
* line 10-11 使用矩陣形式計算將 SimRank 做初始化
    * 根據定義，$\forall\ row\ i\ col\ j, i \not= j$ 的值為 $\displaystyle\frac{C}{in_{-}degree_i \times in_{-}degree_j} \times \#common_{-}parant_{ij}$
    * 以矩陣形式計算即為將 adjacent matrix 的轉置與 adjacent matrix 本身進行矩陣乘法後再乘上係數 `C`，最後再將對角項設為 1
    * adjacent matrix 的轉置與 adjacent matrix 本身進行矩陣乘法，則 $\forall\ row\ i\ col\ j, i \not= j$ 的值會是 $\#common_{-}parant_{ij}$ 個 $\displaystyle\frac{1}{in_{-}degree_i} \times \frac{1}{in_{-}degree_j}$ 相加，故符合定義
* line 14-15 依照矩陣形式計算公式進行計算，並同樣要在最後將對角項設為 1
* line 17-20 直接判斷是否差距足夠小，不須做正規化

## 分析與討論
### 如何提升特定 node 的 hub、authority 與 PageRank
* 題目敘述：Find a way (e.g., add/delete some links) to increase hub, authority, and PageRank of Node 1 in first 3 graphs respectively.

#### 原始圖
![](https://i.imgur.com/ul9PW9t.png)
|           | graph_1   | graph_2 | graph_3  |
| --------- | --------- | ------- | -------- |
| hub       | 0.2       | 0.2     | 0.190909 |
| authority | 0         | 0.2     | 0.190909 |
| PageRank  | 0.0252386 | 0.2     | 0.172544 |

#### hub 提升
* hub 值為 children 的 authority 值的總和，故可以增加 children 數量或是提升現有 children 的 authority 值，使 hub 值得以提升
* 對 graph 1-3 皆新增一條 node 1 到 node 3 的邊（增加 children 數量），hub 值便有明顯提升

![](https://i.imgur.com/V0dXGi9.png)
|           | graph_1 | graph_2 | graph_3  |
| --------- | ------- | ------- | -------- |
| hub       | 0.61776 | 0.61776 | 0.338277 |

#### authority 提升
* authority 值為 parent 的 hub 值的總和，故可以增加 parent 數量或是提升現有 parent 的 hub 值，使 authority 值得以提升
* 對 graph 1 與 graph 3 新增一條指向 node 1 的邊（增加 parent 數量），authority 值便能獲得提升
* 對 graph 2 的 node 5 新增一個 children（提升現有 parent 的 hub 值），authority 值也能獲得提升

![](https://i.imgur.com/UjUtW9C.png)
|           | graph_1  | graph_2  | graph_3  |
| --------- | -------- | -------- | -------- |
| authority | 0.166667 | 0.381797 | 0.499463 |

#### PageRank 提升
* PageRank 值可以透過增加 in-degree、減少 out-degree 以獲得提升
* 對 graph 1 增加 in-degree、對 graph 2 減少 out-degree 皆可以提升 PageRank 值
* 對 graph 3 移除了兩條邊，之所以不是只移除 node 1 的 out-link 邊是因為在這個圖中其他 node 也能作為 link 的終點，只移除 node 1 的 out-link 邊反而會讓 node 1 的 PageRank 下降

![](https://i.imgur.com/U5rNjT8.png)
|          | graph_1  | graph_2  | graph_3  |
| -------- | -------- | -------- | -------- |
| PageRank | 0.166667 | 0.447768 | 0.266553 |

### graph 1-3 之結果分析
![](https://i.imgur.com/ul9PW9t.png)
#### graph 1
* 因為 node 1 沒有 parent，所以 authority 值為 0，而其餘五個 node 各有一個 parent，故其餘五個 node 平分了 authority 值，各為 $\frac{1}{5}$
* 因為 node 6 沒有 children，所以 hub 值為 0，而其餘五個 node 各有一個 children，故其餘五個 node 平分了 hub 值，各為 $\frac{1}{5}$
* PageRank 的部分，因為所有 node 最後都會匯集到 node 6，故 node 6 的 PageRank 值最高，而從 node 6 到 node 1 會陸續遞減
#### graph 2
* 此圖為一個環，故各個 node 的 authority、hub 與 PageRank 值皆相同
#### graph 3
* 與 graph 2 同理，各個 node 的 parent/children 數量為 <text>1:2:2:1</text>，故 authority、hub 與 PageRank 值也是同樣比例
