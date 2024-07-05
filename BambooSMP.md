# Overview

Bamboo-SMP is a parallel framework developed to solve SMP in parallel with optimal perfroamnce.

This framework employs a combination of advanced data structures, atomic operations, and a hybrid CPU-GPU execution model to achieve notable improvements in both efficiency and scalability.





Bamboo-SMP is a parallel framework developed to optimize the performance of algorithms on modern heterogeneous computing systems by effectively addressing prevalent challenges such as memory access patterns and contention. This framework employs a combination of advanced data structures, atomic operations, and a hybrid CPU-GPU execution model to achieve notable improvements in both efficiency and scalability.



The core principles of Bamboo-SMP involve several innovative strategies. Firstly, the use of PRNodes optimizes memory access by ensuring that related data elements are stored together, thereby reducing latency and enhancing data locality. Secondly, the framework utilizes the \texttt{atomicMin} operation in CUDA to efficiently resolve contention, minimizing the need for repeated retries and reducing overhead associated with atomic transactions. Lastly, Bamboo-SMP leverages a hybrid CPU-GPU approach, enabling it to capitalize on the complementary strengths of GPUs and CPUs. This hybrid execution model ensures that high parallelism and complex control flows are handled optimally, further contributing to the framework's scalability and efficiency.



Through these strategies, Bamboo-SMP demonstrates a significant advancement in the performance of parallel algorithms on heterogeneous computing systems.



# LA

## relationship

As discussed in Section \ref{subsec:Challenges with Data Movement}, the primary overhead in the GS algorithm arises from random accesses to the rank matrix. 

We argue that there is a crucial bijective function between each man’s decision on which specific woman to propose and his rank in the woman’s preference list. 

By leveraging this relationship, we can create an innovative locality-aware data structure that optimizes the data access pattern of the rank matrix. This optimization minimizes global data access and improves algorithm performance.



In both the GS and MW algorithms, after retrieving the ID of the best woman who has not yet rejected the proposer from his preference list, the rank matrix is accessed to determine the man’s rank in the woman’s preference list. Specifically, when accessing the men’s preference list entry for man \texttt{m} at rank \texttt{r} (denoted as \texttt{PrefListM[m, r]}), we obtain woman \texttt{w}. This process requires a subsequent access to the rank matrix entry for woman \texttt{w} and man \texttt{m} (denoted as \texttt{RankMatrix[w, m]}) to determine the man’s rank in her list.



This shows that for a given man and the next rank he is going to propose, there is a direct one-to-one correspondence between each entry in the men’s preference list and its intrinsically linked entry in the women’s rank matrix.



If these interconnected entries are stored together, both pieces of information can be accessed with a single load instruction, eliminating the need to access \texttt{RankMatrix} separately. 



To achieve this goal, we introduce a specialized data structure called PRMatrix.





## PRMatrix

The PRMatrix contains n \times n entries, referred to as PRNodes. Each PRNode includes an entry from the men’s preference list, indicating the woman a specific man would propose to at a given rank, along with the corresponding entry from the women’s rank matrix, specifying the rank of that man on the woman’s preference list.

As mentioned in Section 2, the GS algorithm has an initialization step to set up the rank matrix. To set up the PRMatrix, an additional preprocessing operation is performed once the rank matrix is in place.

In Figrue \cite{fig:PRMatrix}, the process of initialization of PRMatrix is show.

Figure \cite{fig:PRMatrix} illustrates the initialization process of PRMatrix. For each man \texttt{m} and each rank \texttt{r_w}, the algorithm retrieves the woman \texttt{w} corresponding to rank \texttt{r_w} in the man’s preference list. It then retrieves \texttt{r_m}, which is the rank of man \texttt{m} in the woman’s preference list from \texttt{RankMatrixW}. The \texttt{PRMatrixM} at position \texttt{(m, r_w)} is then assigned the pair \texttt{(w, r_m)}.



Since the configuration of each entry in both the rank matrix and PRMatrix is independent, we can leverage the GPU for massive parallelism to maximize speedup during initialization. In Figure \cite{figure:initilaizationOnGPU}, we tested the initialization performance of RankMatrix and PRMatrix under three conditions: (1) sequentially, (2) in parallel on the CPU, and (3) in parallel on the GPU. The results show that the GPU achieves the fastest initialization time, even considering the additional data transfer between host and device.



## LA

After constructing the PRMatrix, we have established the foundation for a locality-aware sequential implementation of the GS algorithm.



This new approach involves iterating through and invoking the \texttt{LocalityAwareMatching} procedure for  each man who has not yet made a proposal.



As shown in Algorithm 3, In contrast to the GS and MW algorithms, the main loop in the \texttt{LocalityAwareMatching} procedure eliminates random access to the rank matrix.



During each iteration, for for a given man and the rank of woman who he is going to propose, the \texttt{LocalityAwareMatching} procedure retrieves a PRNode and extracts the information about which woman to propose to and his rank in her preference list. By loading this information in a single instruction, random access to the rank matrix is eliminated, greatly improving the algorithm’s efficiency.



Additionally, no queue is required during this procedure. When a woman already paired with a partner accepts a new proposal, her previous partner will immediately proceed to make further proposals without being re-added to a queue, which makes it possible to be implemented on GPU.



### Unused

Thus, each entry in the men’s preference list is intrinsically linked to a unique entry in the women’s rank matrix.



the main loop handles the rejected man from the previous iteration, continuing until a proposal is accepted.

During each iteration, we retrieve the woman \texttt{w} and the rank \texttt{m\_rank} from \texttt{PRNodesM} for the current man \texttt{m}. We then check the current partner's rank \texttt{p\_rank} for woman \texttt{w} from \texttt{partnerRank}. 



and significantly improve the efficiency of the stable mathcing process

Within \texttt{performLocalityAwareMatching}, we initialize \texttt{done} to \texttt{False} and \texttt{w\_rank} to 1, as the man \texttt{m} has not been rejected by any woman yet and can propose to the highest-ranked woman on his list. 



During each iteration, we retrieve the woman \texttt{w} and the rank \texttt{m\_rank} from \texttt{PRNodesM} for the current man \texttt{m}. We then check the current partner's rank \texttt{p\_rank} for woman \texttt{w} from \texttt{partnerRank}. 

If \texttt{p\_rank} is greater than \texttt{m\_rank}, meaning the woman \texttt{w} prefers the current proposer \texttt{m} over her current partner, we update \texttt{partnerRank[w]} to \texttt{m\_rank}. If \texttt{p\_rank} equals \texttt{n + 1}, indicating the woman was previously unpaired and no man is rejected, we set \texttt{done} to \texttt{True} to terminate the main loop. 

If \texttt{p\_rank} is not equal to \texttt{n + 1}, meaning the woman is currently paired with another partner she prefers less, we retrieve the ID of that partner and the rank of his last proposed woman from \texttt{PRNodesW}. 

Then, \texttt{w\_rank} is incremented by 1 to indicate the next rank of the woman the current man will propose to in the next iteration. The loop then checks whether a rejected man exists at the end of the loop to determine if it should terminate or continue.



This optimization can significantly reduce the overhead associated with data access in the GS and MW algorithms.



# Contention Resolver





# Heterogeneous Computing Model

gpu-cpu hybrid system