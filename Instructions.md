# Bazaar-Style Peer-to-Peer (P2P) Marketplace

### Lab 1 (COMPSCI 677 - Fall 2024)

## Source: [Click Here - Instructions in the PDF](./Instructions.pdf)

---

## Requirements and Progress (Checklist)

### 1. **Participant Representation**

- [x] The buyers and sellers must be represented as separate processes that are forked from a parent program, using threads. Communication between participants should occur via RPCs, RMIs, or sockets.
  - **Progress:** We used **sockets** for communication between threads, representing the buyers and sellers as separate threads in a multi-threaded environment.

### 2. **P2P Topology**

- [x] The network should be structured as a P2P network with participant processes acting as peers. Specify whether the network is structured or unstructured.
  - **Progress:** The system is based on an **unstructured P2P topology**, where peers are randomly connected without a fixed structure.

### 3. **Predefined Number of Participants**

- [ ] The number of participants in the bazaar, denoted as `N`, should be specified beforehand as a command-line argument.
  - **Progress:** We have not yet implemented the functionality to specify `N` as a command-line argument.

### 4. **Peer Connectivity Limits**

- [ ] Each peer should have no more than three direct neighbors, and peers should only communicate with their direct neighbors during the simulation.
  - **Progress:** We have not yet restricted peers to having only three direct neighbors.

### 5. **Fully Connected Network**

- [ ] The network must be fully connected, meaning there should be a path between any two peers. No need for neighbor discovery; the list of all participants should be provided beforehand.
  - **Progress:** We have not ensured a fully connected network or provided a list of neighbors.

### 6. **Random Role Assignment**

- [ ] Once the network is formed, each peer should be assigned a random role as either a fish seller, salt seller, boar seller, or buyer.
  - **Progress:** Roles are currently assigned manually; random assignment of roles is not yet implemented.

### 7. **At Least One Buyer and One Seller**

- [x] There must be at least one buyer and one seller in the system.
  - **Progress:** The system includes at least one buyer and one seller.

### 8. **Buyer and Seller Behavior**

- [ ] Each buyer should randomly pick items to purchase and then wait a random amount of time before purchasing another item. Each seller should start with a set number of items, and once all items are sold, switch to selling a different item.
  - **Progress:** Buyers do not yet randomly select items, and sellers do not switch items after selling out.

### 9. **Concurrent Request Handling**

- [x] Each peer should be able to accept multiple requests concurrently using threads. Synchronization should be applied to prevent deadlocks or inconsistency, especially for decrementing items in stock.
  - **Progress:** We have implemented thread synchronization to handle concurrent requests and stock decrementing, using threads and sockets to handle multiple buyer requests simultaneously.

### 10. **Deployment of Peers**

- [ ] Deploy at least 6 peers on a single machine (different directories) or on different machines.
  - **Progress:** We are testing the peers as separate threads in the same process. Full deployment across directories or machines is pending.

### 11. **Multi-Machine Deployment**

- [ ] Deploy the peers on at least two separate machines to simulate a distributed network.
  - **Progress:** We have not yet deployed the system across multiple machines.

### 12. **Documentation**

- [ ] Answer the questions and other details in the [Instructions PDF](./Instructions.pdf)
  - **Progress:** Yet to describe...

---
