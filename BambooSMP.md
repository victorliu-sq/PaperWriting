# Overview

Bamboo-SMP is a parallel framework developed to solve SMP in parallel with optimal perfroamnce.

This framework employs a combination of advanced data structures, atomic operations, and a hybrid CPU-GPU execution model to achieve notable improvements in both efficiency and scalability.





Bamboo-SMP is a parallel framework developed to optimize the performance of algorithms on modern heterogeneous computing systems by effectively addressing prevalent challenges such as memory access patterns and contention. This framework employs a combination of advanced data structures, atomic operations, and a hybrid CPU-GPU execution model to achieve notable improvements in both efficiency and scalability.



The core principles of Bamboo-SMP involve several innovative strategies. Firstly, the use of PRNodes optimizes memory access by ensuring that related data elements are stored together, thereby reducing latency and enhancing data locality. Secondly, the framework utilizes the \texttt{atomicMin} operation in CUDA to efficiently resolve contention, minimizing the need for repeated retries and reducing overhead associated with atomic transactions. Lastly, Bamboo-SMP leverages a hybrid CPU-GPU approach, enabling it to capitalize on the complementary strengths of GPUs and CPUs. This hybrid execution model ensures that high parallelism and complex control flows are handled optimally, further contributing to the framework's scalability and efficiency.



Through these strategies, Bamboo-SMP demonstrates a significant advancement in the performance of parallel algorithms on heterogeneous computing systems.



# LA

## relationship

As discussed in Section \ref{subsec:Challenges with Data Movement}, the primary overhead in the GS algorithm arises from random accesses to the rank matrix. We argue that there is a crucial bijective function between each man’s decision on which specific woman to propose and his rank in the woman’s preference list. 

By leveraging this relationship, we can create an innovative locality-aware data structure, optimizing the data access pattern of the rank matrix to minimize global data access and improve algorithm performance. 



In both the GS and MW algorithms, after retrieving the ID of the best woman who has not yet rejected the proposer from his preference list, the rank matrix is accessed to determine the man’s rank in the woman’s preference list. Specifically, when accessing the men’s preference list entry for man \texttt{m} at rank \texttt{r} (denoted as \texttt{PrefListM[m, r]}), we obtain woman \texttt{w}. This process requires a subsequent access to the rank matrix entry for woman \texttt{w} and man \texttt{m} (denoted as \texttt{RankMatrix[w, m]}) to determine the man’s rank in her list. 



This shows, given a man and next rank he is going to make proposal, there is a direct one-to-one correspondence between the entry that includes the woman in the men’s preference list and the entry that contains rank of man to the women in the women’s rank matrix. 



If these interconnected entries are stored together, both pieces of information can be accessed with a single load instructio, eliminating the need to access \texttt{RankMatrix} separately. This optimization can significantly reduce the overhead associated with data access in the GS and MW algorithms.



To achieve this goal, we introducea specialized data structure called PRMatrix, which integrates both the preference lists and the rank matrices. 

The PRMatrix contains \(n \times n\) entries, referred to as PRNodes.

each PRNode includes an entry from the men's preference list, indicating the woman a specific man would propose to at a given rank, along with the corresponding entry from the women's rank matrix, specifying the rank of that man on the woman’s preference list



Each PRNode includes one entry in the men’s preference list is stored together with the unique entry in the women’s rank matrix that it is intrinsically linked to. 

This integration provides opportunities to significantly reduce overhead by eliminating separate data accesses to rank matrix.





## PRMatrix

By understanding and optimizing this dependent relationship between data access patterns, we can achieve significant performance improvements. This illustrates how a well-designed data structure can streamline computations and enhance overall efficiency in these algorithms.



To optimize the data access patterns discussed in Section 2, we introduce a specialized data structure called PRMatrix, which integrates both the preference lists and the rank matrices. This integration provides opportunities to significantly reduce overhead by eliminating separate data accesses to rank matrix.



The PRMatrix contains \(n \times n\) entries, referred to as PRNodes. Each PRNode includes one element from the preference lists and one element from the rank matrices, combining these two pieces of information into a single structure. Because the preference lists and rank matrices are both of size \(n \times n\), where \(n\) represents the number of participants, PRMatrix also has \(n \times n\) entries, ensuring efficient organization and access to all necessary data.



In PRMatrix, each PRNode includes an entry from the men's preference list, indicating the woman a specific man would propose to at a given rank, along with the corresponding entry from the women's rank matrix, specifying the rank of that man on the woman’s preference list. By storing these two elements together, they can be accessed simultaneously with a single load instruction.



As mentioned in Section 2, the GS algorithms has an initialization step to setup rank matrix.

In order to setup PRMatrix, an additional preprocessing step will be introduced once the rank matrix is in place.

In Figrue \cite{fig:PRMatrix}, the process of initialization of PRMatrix is show.

or each man \texttt{m} and each rank \texttt{r\_w}, the algorithm retrieves the woman \texttt{w} corresponding to rank \texttt{r\_w} in the man's preference list. It then retrieves \texttt{r\_m}, which is the rank of man \texttt{m} in the woman's preference list from \texttt{RankMatrixW}. The \texttt{PRMatrixM} at position \texttt{(m, r\_w)} is then assigned the pair \texttt{(w, r\_m)}.



Here we introduce another principle: since the configuration of  each entry of both rank matrix and PRMatrix is independent of each other, the initialization of these data structures should leverage GPU to be executed in massive parallelism to maximize speedup. In Figure \cite{figure:initilaizationOnGPU}, we tested the performance of intialization step with and without PRMatrix (1) sequentially (2) in parallel on CPU (3) in parallel on GPU. To run the kernel on GPU, additional data transfer between host and device is also required. And the figure 6 shows that the time of initialization on GPU is the lowest .



## LA

After the construction of the PRMatrix structure. the foundation for a locality-aware **sequential** implementation of the GS algorithm is laid.

This new locality-aware approach involves iterating through each man who has not yet made a proposal and invoking the \texttt{LocalityAwareMatching} procedure, which is illustrated in Algorithm 3, for each man. 

Compared to GS and MW algorihtm, the main loop in performLocalityAwareMatching procedure works in a similar way but elimiates the random access to the rank matrix.

During each iteration, for the current man at a specific rank, LocalityAwareMatching procedure retreives a PRNode and unbox the information about the woman to propose and his rank at the woman's preference list.

By doing so, the random access to rank matrix is utterly eliminated and the efficiency of the algorithms have been greatly improved.  

Also, no queue is required during this procedure. When a woman who is already paired with a partern,  accepts a new proposal, her previous partner will continue proposing to his next preference instead of being re-added to a queue.





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





# Contention Resolver





# Heterogeneous Computing Model

gpu-cpu hybrid system