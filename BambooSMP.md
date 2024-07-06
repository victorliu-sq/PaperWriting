# Overview

Bamboo-SMP is a parallel framework developed to solve SMP in parallel with optimal perfroamnce.

This framework employs a combination of advanced data structures, atomic operations, and a hybrid CPU-GPU execution model to achieve notable improvements in both efficiency and scalability.





Bamboo-SMP is a parallel framework developed to optimize the performance of algorithms on modern heterogeneous computing systems by effectively addressing prevalent challenges such as memory access patterns and contention. This framework employs a combination of advanced data structures, atomic operations, and a hybrid CPU-GPU execution model to achieve notable improvements in both efficiency and scalability.



The core principles of Bamboo-SMP involve several innovative strategies. Firstly, the use of PRNodes optimizes memory access by ensuring that related data elements are stored together, thereby reducing latency and enhancing data locality. Secondly, the framework utilizes the \texttt{atomicMin} operation in CUDA to efficiently resolve contention, minimizing the need for repeated retries and reducing overhead associated with atomic transactions. Lastly, Bamboo-SMP leverages a hybrid CPU-GPU approach, enabling it to capitalize on the complementary strengths of GPUs and CPUs. This hybrid execution model ensures that high parallelism and complex control flows are handled optimally, further contributing to the framework's scalability and efficiency.



Through these strategies, Bamboo-SMP demonstrates a significant advancement in the performance of parallel algorithms on heterogeneous computing systems.



# LA

## relationship

As discussed in Section \ref{subsec:Challenges with Data Movement}, the primary overhead in the GS algorithm arises from random accesses to the rank matrix. 

We argue that there is a crucial bijection between each man’s decision on which specific woman to propose and his rank in the woman’s preference list. 

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

After constructing the PRMatrix, we have established the groundwork for a locality-aware sequential implementation of the GS algorithm.



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

As previously mentioned in Section \ref{subsec:Challenges with Synchronization}, in parallelized GS algorithms, each woman needs to select the best proposal with the minimum numerical value when multiple proposals are made simultaneously. However, traditional synchronization methods can be inefficient when updating \texttt{partnerRank} due to the high cost of coarse-grained synchronization and wasted work from \texttt{atomicCAS} failures under high memory contention.

To overcome this problem, we need a fine-grained hardware primitive that handles high memory contention efficiently. Modern CPUs still rely on \texttt{atomicCAS} implementations to perform specific arithmetic functions. In contrast, modern GPU architectures, such as NVIDIA's CUDA, offer a comprehensive set of atomic functions for arithmetic operations. Among these, \texttt{atomicMin} effectively addresses the challenges of synchronization and high contention in parallelized GS algorithms.

The \texttt{atomicMin} function in CUDA reads the 32-bit or 64-bit word \texttt{old} at the address in global or shared memory, computes the minimum of \texttt{old} and \texttt{val}, stores the result back to memory at the same address—all in one atomic transaction. The function then returns \texttt{old} so the caller can determine whether the value has been updated. If \texttt{old} is larger, the caller knows the value has been updated to \texttt{val}; otherwise, no update has occurred.



The advantage of \texttt{atomicMin} in parallelizing GS is that it does not require an expected value to proceed only if the expected value matches the \texttt{old}. This ensures that each thread performs the operation only once, eliminating the need for repeated retries. 

To provide a rigorous proof that \texttt{atomicMin} significantly reduces the number of atomic operations compared to using \texttt{atomicCAS}, we provide Lemma \ref{lem:smp_instance_min_times}, which indicates that, in the congested case, for a Stable Marriage Problem (SMP) instance with \(n\) men and \(n\) women, the total number of \texttt{atomicMin} operations is \(O(n^2)\), which is significantly smaller than the \(O(n^3)\) operations required by \texttt{atomicCAS}.



By leveraging the atomic functions provided by modern GPU architectures, we develop a GPU kernel, BambooKernel, which is essentialy a parallel version of the Locality-Aware \texttt{GS} algorithm in Algorithm \ref{Algo:LA-GSAlgo}, to efficiently solve \texttt{SMP} instances associated with high contention. 



BambooKernel kernel inherits most of the logic of the GPU kernel of parallel MW algortihm. 

The key differences lie in how it  it exploits locality using \texttt{PRMatrix} and how it ensures m

utual exclusion and prevents race conditions by using \texttt{atomicMin} to update the shared data structure \texttt{partnerRank}.

Specifically, even if the returned value mismatches the previously read one but is still larger than \texttt{val}, \texttt{atomicMin} can proceed to update the minimum value with \texttt{val}, whereas \texttt{atomicCAS} would need to repeat the operation.

If the update is unsuccessful, as indicated by the returned value being not larger than \(m\_rank\), \(m\) will be rejected and will have to propose to the next woman on his preference list in the next iteration. 



### Unused

Specifically, even if the returned value mismatches the previously read one but is still larger than \texttt{val}, \texttt{atomicMin} can proceed to update the minimum value with \texttt{val}, whereas \texttt{atomicCAS} would need to repeat the operation.



Each thread, representing a man \(m\), starts by proposing to the highest-ranked woman on his preference list that he has not yet proposed to. 



After retrieving the current partner's rank \(p\_rank\) for woman \(w\) from \texttt{partnerRank[w]}, the algorithm checks if \(p\_rank\) is greater than \(m\_rank\). If \(p\_rank > m\_rank\), meaning the woman \(w\) prefers the current proposer \(m\) over her current partner, we attempt to update \texttt{partnerRank[w]} to \(m\_rank\) using \texttt{atomicMin}. 



If the update is unsuccessful, as indicated by the returned value being not larger than \(m\_rank\), \(m\) will be rejected and will have to propose to the next woman on his preference list in the next iteration. 

Otherwise, there are two scenarios to consider:



# Heterogeneous Computing Model

While BambooKernel is effective at managing contention by minimizing retries and ensuring efficient updates, it remains an expensive operation due to the high overhead associated with atomic transactions. As discussed in Section \ref{subsec:Challenges with Implementations on GPU}, this overhead becomes particularly pronounced in solo case . In such scenarios, only one thread remains active and the advantages of parallel execution diminish.As a result,the costs associated with unnecessary atomic operations can outweigh their benefits, leading to inefficiencies.

However, BambooKernel is also required to solve SMP workloads where parallelism is high, like congested cases and random cases.

To address the workload-dependent limitation of SMP, we propose a parallel framework, called BambooSMP, that leverages a hybrid CPU-GPU execution model. 



BambooSMP employs an effective exeuction policy such that it will run first BambooKernel for high parallelism and then transfer execution from the GPU to the CPU to run locality-aware implmenetation of GS sequentially when the active thread decreases dramatically and the overhead of synchronization among multiple threads outweighs the benefits of concurrent exeuction .

In order to take advantage of the complementary strengths of both GPUs and CPUs, the framework needs to ensure a seamless transition between these processing units under varying conditions of parallelism, which requires addressing two fundamental questions: (1) when to switch and (2) how to switch.



## \subsubsection{When to switch}

The guiding principle of BambooSMP for switching from GPU to CPU execution is when the number of unmatched men reduces to one. In this scenario, only a single CUDA thread remains active on the GPU, the synchronization overhead and high latency inherent to GPU operations become significant bottlenecks.

Transitioning to CPU execution at this point allows for efficient handling of high parallelism when many threads are active, while avoiding the inefficiencies associated with reduced parallelism on the GPU. 

The critical aspect of this switch is detecting when there is only one proposer left, signifying that only one thread remains active. 

This situation marks the transition fr om massively parallel GPU execution to more suitable sequential execution on the CPU.



## \subsubsection{How to switch}

To effectively switch to the CPU, two key sub-questions must be addressed to determine the appropriate timing and method:
\begin{enumerate}
    \item How to ascertain if only one man remains unmatched.
    \item How to identify the unmathced man to proceed with the sequential algorithm.
\end{enumerate}

Determining if only one thread remains active relies on the \texttt{partnerRank} data structure, which is used during the execution of the parallel locality-aware GS algorithm. Since each woman's partner rank is initialized to \(n+1\), any rank value smaller than \(n+1\) indicates that the woman is paired, implying the presence of a paired man. If exactly one woman's partner rank is \(n+1\), it signifies that only one proposer remains free.

Identifying the ID of the free man involves additional computations. After reading the partner ranks of all women to confirm that only one woman is unpaired, the algorithm calculates the total sum of IDs of all men, which is \(\frac{n(n+1)}{2}\). By subtracting the IDs of the paired men from this total sum, the algorithm determines the ID of the free man.

The above calculations are repeated until it is confirmed that only one proposer remains active and the free man is identified. At this point, the computation transitions from the GPU to the CPU to efficiently handle the remaining sequential steps. This is accomplished by copying the \texttt{partnerRank} from device memory to host memory and invoking the procedure in Algorithm \ref{Algo:LA-GSAlgo} for the free man to make further proposals based on the existing \texttt{partnerRank}.

This transition leverages the CPU's strengths in managing tasks with limited parallelism and more complex control flow, thereby maintaining the overall efficiency of the GS algorithm execution.



## BambooSMP



gpu-cpu hybrid system

```
BambooSMP:

BambooInit();
std::thread t1(doWorkOnGPU)
std::thread t1(doWorkOnCPU)
std::atomic<int> termianteFlag(0);

while (terminateFlag.load() == 0) {
	sleep()
}

if (terminateFlag.load() == 1) {
	t1.join()
	t2.detach()
	postprocess(Bamboo::device_postproc)
} else {
	t2.join()
	t1.detach()
	postprocess(Bamboo::host_postproc)
}
====================================================
doWorkOnGPU:
BambooKernel<<<...>>>(...)
setTerminateFlag(&terminateFlag, 1)

====================================================
doWorkOnCPU:
while (host_num_unmatched_men > 1) {
	FindUnmatchedMen<<<...>>>(partnerRank,device_num_unmatched_men, device_unmatched_man)
	cudaMemcpy(&host_num_unmatched_men, device_num_unmatched_men)
}

if (# of unmatched men = 1) {
	cudaMemcpy(&host_unmatched_man,device_unmatched_man)
	LAProcedure(unmatched_man)
	setTerminateFlag(&terminateFlag, 2)
}

====================================================
setTerminateFlag(terminateFlag, mode):
int expect = 0;
terminateFlag.compare_exchange_strong(terminateFlag, mode);

====================================================
FindUnmatchedMen(n, device_partnerRank, device_pref_lists_w, device_num_unmatched_men, device_unmatched_man,):
  int w = blockIdx.x * blockDim.x + threadIdx.x;

  if (w < n) {
    int partner_rank = husband_rank[w];
    split_husband_rank[w] = partner_rank;
    if (partner_rank == n + 1) {
      atomicAdd(device_num_unmatched_men, 1);
    } else {
      atomicSub(device_unmatched_man, pref_lists_w[wi * n + hr]);
    }
  }
```



## Unused

By integrating the complementary strengths of both GPUs and CPUs, the framework aims to optimize performance under varying conditions of parallelism. 