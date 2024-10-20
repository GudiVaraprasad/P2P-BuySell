# Bazaar-Style Peer-to-Peer (P2P) Marketplace

### Lab 1 (COMPSCI 677 - Fall 2024)

## Source: [Click Here - Instructions in the PDF](./Instructions.pdf)

---

## Requirements and Progress (Checklist)

### 1. **Used sockets with threads for communication**

- [x] The buyers and sellers must communicate via sockets and handle requests using threads.
  - **Progress:** Implemented **sockets** for communication between participants, with buyers and sellers represented as threads.

### 2. **Unstructured P2P Topology**

- [x] The network should be unstructured with random peer connections.
  - **Progress:** The network is based on an **unstructured P2P topology**, where peers are randomly connected.

### 3. **At least one buyer and one seller**

- [x] There must be at least one buyer and one seller in the system.
  - **Progress:** At least one buyer and one seller are guaranteed at initialization.

### 4. **Thread synchronization with stock decrement functionality**

- [x] Thread synchronization should be used to prevent conflicts, especially when stock is decremented after a sale.
  - **Progress:** Implemented thread synchronization to safely handle stock decrement across concurrent requests.

### 5. **Multiple requests handled using threads**

- [x] Each peer must handle multiple requests at the same time using threads.
  - **Progress:** Each peer can handle multiple concurrent requests, with threads processing these requests independently.

### 6. **Limit peers to three direct neighbors**

- [x] Each peer should have a maximum of three direct neighbors.
  - **Progress:** Peers are limited to three randomly assigned neighbors, ensuring the correct network structure.

### 7. **Fully connected network with predefined neighbors**

- [x] The network should be fully connected, ensuring there is a path between any two peers, even if indirectly.
  - **Progress:** Predefined neighbors ensure that the network is fully connected, allowing messages to propagate between any two peers.

### 8. **Random assignment of roles (fish seller, salt seller, boar seller, buyer)**

- [x] Each peer should be randomly assigned a role as either a seller or buyer.
  - **Progress:** Roles are randomly assigned, ensuring a mix of sellers and buyers with random product assignments.

### 9. **Buyers randomly picking items**

- [x] Buyers should randomly pick items to purchase and repeat the process after a random wait time.
  - **Progress:** Buyers randomly choose a product to search for and then wait a random amount of time before making another purchase.

### 10. **Sellers switching roles after selling out**

- [x] Sellers should switch products after selling out of their initial stock.
  - **Progress:** Sellers switch products randomly after their stock runs out, continuing to operate with new items.

### 11. **Avoid handling duplicate requests with timestamps or request counts**

- [x] Prevent duplicate lookup requests from being processed using unique identifiers or timestamps.
  - **Progress:** Implemented request tracking to avoid processing duplicate requests, using a set to store processed request identifiers.

### 12. **Command-line argument for N (number of peers)**

- [x] The number of peers should be provided as a command-line argument.
  - **Progress:** Implemented **argparse** to handle the `N` argument, specifying the number of peers during the simulation startup.

### 13. **Handle concurrent buy requests with limited stock**

- [x] Concurrent buy requests should be managed by synchronizing stock decrement operations.
  - **Progress:** Synchronized stock management ensures that concurrent buy requests are handled without race conditions or conflicts.

### 14. **Use hop count to prevent infinite message propagation (calculate the actual graph diameter and use it to initialize the hop count dynamically)**

- [x] Use hop count to limit message propagation, avoiding infinite loops in the network.
  - **Progress:** dynamically calculate the graph diameter (i.e., the maximum shortest path between any two peers)

### 15. **Max Requests and Evaluation**

- [ ] The system should stop after processing a maximum number of requests (e.g., 1000 sequential requests) and report the average response time.
  - **Progress:** Implemented request counting, limiting the system to process a predefined maximum number of requests before stopping and calculating average response time. Need to test this during deployment.

---

### **Multi-Machine Deployment**

- [ ] Deploy the peers on at least two separate machines to simulate a distributed network.
  - **Progress:** Multi-machine deployment is still pending. Currently, all peers are tested as threads within a single process.

### **Documentation**

- [ ] Answer the questions and provide details in the [Instructions PDF](./Instructions.pdf).
  - **Progress:** Documentation and analysis are still pending.
