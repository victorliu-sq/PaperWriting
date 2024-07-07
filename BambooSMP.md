# Requirement

rewrite these sentences in more deep and academical way .

develop these sentences in a more natural way? You can add sentences or remove duplicate contents to strengthen the connections between sentences



# Overview

Bamboo-SMP is a parallel framework developed to solve SMP in parallel with optimal perfroamnce.

This framework employs a combination of advanced data structures, atomic operations, and a hybrid CPU-GPU execution model to achieve notable improvements in both efficiency and scalability.





Bamboo-SMP is a parallel framework developed to optimize the performance of algorithms on modern heterogeneous computing systems by effectively addressing prevalent challenges such as memory access patterns and contention. This framework employs a combination of advanced data structures, atomic operations, and a hybrid CPU-GPU execution model to achieve notable improvements in both efficiency and scalability.



The core principles of Bamboo-SMP involve several innovative strategies. Firstly, the use of PRNodes optimizes memory access by ensuring that related data elements are stored together, thereby reducing latency and enhancing data locality. Secondly, the framework utilizes the \texttt{atomicMin} operation in CUDA to efficiently resolve contention, minimizing the need for repeated retries and reducing overhead associated with atomic transactions. Lastly, Bamboo-SMP leverages a hybrid CPU-GPU approach, enabling it to capitalize on the complementary strengths of GPUs and CPUs. This hybrid execution model ensures that high parallelism and complex control flows are handled optimally, further contributing to the framework's scalability and efficiency.



Through these strategies, Bamboo-SMP demonstrates a significant advancement in the performance of parallel algorithms on heterogeneous computing systems.



# LA

## PRMatrix

As elaborated in Section \ref{subsec:Challenges with Data Movement}, a significant performance bottleneck in the GS stems from the frequent lookups of rank matrix required to determine ranks. Those accesses to rank matrix are non-sequential and incur substantial overhead.

To optmize the data access pattern of rank matrix, we propose a crucial observation: there exists a bijection between a man’s decision regarding which woman to propose to and his corresponding rank in her preference list.

In both the GS and MW algorithms, after a man retrieves the ID of the most preferred woman who has not yet rejected him from his preference list, it is necessary to access the rank matrix to determine his rank in her preference list. 

Specifically, for a given man \texttt{m} at rank \texttt{r} in his preference list (\texttt{PrefListM[m, r]}), we identify woman \texttt{w}. The subsequent step involves accessing the rank matrix at \texttt{RankMatrix[w, m]} to determine the man’s rank in the woman’s preference list.

This reveals a direct one-to-one correspondence between each entry in the men’s preference list and its implicitly linked entry in the women’s rank matrix. 

By harnessing this inherent relationship, we introduce a locality-aware data structure known as PRMatrix. 

In PRMatrix, each pair of interrelated entries of preference lists and rank matrix is co-located within a single entity, referred to as a PRNode. This co-location enables both pieces of information to be accessed simultaneously with a single memory load, thereby eliminating the need for separate lookups in the rank matrix.



As detailed in Section 2, the Gale-Shapley (GS) algorithm includes an initialization phase to configure the rank matrix. To establish the PRMatrix, an additional preprocessing step is required once the rank matrix setup is complete. This step involves a process of pairing entries from the men’s preference lists with their corresponding ranks in the women’s preference lists, as shown in Figure \cite{fig:PRMatrix}.

For example, consider a scenario where man \texttt{M1} is proposing to a woman at \texttt{Rank1}. The algorithm retrieves woman \texttt{W2} from man \texttt{M1}’s preference list. Subsequently, it accesses the rank matrix to find \texttt{Rank2}, which represents the rank of man \texttt{M1} in woman \texttt{W2}‘s preference list. The PRNode at position \texttt{(M1, Rank1)} is then populated with the pair \texttt{(W2, Rank2)}. This systematic approach ensures that each PRNode contains both the target woman and the man’s rank within her preference list, thus consolidating the data into a single, easily accessible structure.

For man \texttt{M1} proposing to woman at \texttt{Rank1},   the woman \texttt{W2} is retrieved from  the man’s preference list. It then retrieves \texttt{Rank2}, which is the rank of man \texttt{M1} from the woman \texttt{W2}'s preference list from \texttt{RankMatrix}. The \texttt{PRMatrix} at position \texttt{(M1, Rank1)} is then assigned the pair \texttt{(W2, Rank2)}.



## LA

We argue that although the initialization of both the RankMatrix and the PRMatrix involves square-level time complexity, leveraging GPUs can significantly expedite this process. The massive parallelism capabilities of GPUs allow for rapid initialization, ensuring that the overall execution time is not adversely impacted.

The configuration of each entry in the RankMatrix and PRMatrix is inherently independent, making it highly amenable to parallel processing. Utilizing the GPU for this initialization process enables significant acceleration due to its ability to handle extensive parallel workloads. This approach efficiently prepares the data structures required for the subsequent algorithmic steps.

To empirically validate the performance benefits of this approach, we conducted a series of tests comparing the initialization times of the RankMatrix and PRMatrix under three different conditions: (1) sequential execution, (2) parallel execution on the CPU, and (3) parallel execution on the GPU. As illustrated in Figure \cite{figure:initilaizationOnGPU}, our findings unequivocally demonstrate that the GPU achieves the fastest initialization times, even when accounting for the additional data transfer overhead between the host and the device.

The substantial reduction in initialization time afforded by GPU parallelism is pivotal to the overall performance of the GS algorithm, as it ensures that the initialization step does not become a bottleneck.

Following the construction of the PRMatrix, we have established a solid foundation for a Locality-Aware sequential implementation of the GS algorithm (LA). 

LA iterates through and invokes the \texttt{LAProposalProcedure} for each man who has not yet made a proposal.

As demonstrated in Algorithm 3, the \texttt{LAProposalProcedure} distinguishes itself from the traditional GS and MW algorithms by access PRMatrix instead of Rank. During each iteration, a PRNode is retrieved  for the given man and the rank of the woman he is proposing to. This PRNode includes the combined information of both the woman’s identity and the man’s rank in her preference list, thereby eliminating random access to the rank matrix in its main loop and increasing the algorithmic performance.

Furthermore, this procedure also eliminates the need for a queue, smilar to MW. When a woman already paired with a partner accepts a new proposal, her previous partner immediately proceeds to make further proposals without being re-added to a queue. This streamlined process makes LA well-suited for parallel execution on a GPU.



### Unused

Thus, each entry in the men’s preference list is intrinsically linked to a unique entry in the women’s rank matrix.



the main loop handles the rejected man from the previous iteration, continuing until a proposal is accepted.

During each iteration, we retrieve the woman \texttt{w} and the rank \texttt{m\_rank} from \texttt{PRNodesM} for the current man \texttt{m}. We then check the current partner's rank \texttt{p\_rank} for woman \texttt{w} from \texttt{partnerRank}. 



and significantly improve the efficiency of the stable mathcing process

Within \texttt{LAProposalProcedure}, we initialize \texttt{done} to \texttt{False} and \texttt{w\_rank} to 1, as the man \texttt{m} has not been rejected by any woman yet and can propose to the highest-ranked woman on his list. 



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



# BambooSMP

## Adaptive Execution Policy

While the Locality-Aware (LA) implementation excels at minimizing data movements and BambooKernel effectively manages contention, both approaches have limitations for certain workloads. The LA implementation struggles with workloads that benefit from concurrent processing, whereas BambooKernel becomes costly in solo cases due to the unnecessary synchronization overhead and high latency inherent to GPU operations, as discussed in section {Challenges}.

To overcome these workload-dependent limitations, we propose a parallel framework called BambooSMP. This framework optimizes performance across diverse workloads through an adaptive execution policy that dynamically adjusts processing units based on the varying levels of parallelism inherent in the SMP workload.

At the beginning of any workload, when all men are unmatched and ready to make their initial proposals, BambooSMP initiates by running BambooKernel on the GPU. This approach leverages the GPU’s capacity for massive parallelism, efficiently handling the initial phase where numerous proposals are made concurrently.

As the kernel execution progresses and the number of unmatched men decreases, the workload gradually transitions from a highly parallel to a more serial nature. Recognizing this shift, BambooSMP adapts by transitioning from the massively parallel GPU execution to a more suitable sequential execution on the CPU. This transition is crucial to avoid the inefficiencies associated with reduced parallelism on the GPU.

By dynamically balancing the load between the GPU and CPU, BambooSMP ensures optimal performance and resource utilization. This seamless transition highlights the framework’s ability to adapt to varying workload demands, thereby optimizing computational efficiency.



## FindUnmatchedManKernel

To effectively implement the adaptive execution policy, we propose another GPU kernel named `FindUnmatchedManKernel` to perform two critical operations:
\begin{enumerate}
    \item ascertain if only one man remains unmatched.
    \item Identify the sole unmatched man to proceed with the sequential algorithm.
\end{enumerate}

These two operations fundamentally rely on the partnerRank data structure, which is integral to the execution of BambooKernel on the primary GPU.

To determine if only one man remains unmatched, the variable`num_unmatched` is initialized to zero. And the ID of the unmatched man `id_unmatched` is set to the total sum of IDs of all men, calculated as \frac{n(n+1)}{2}. Both variables are reinitialized prior to each launch of FindUnmatchedManKernel.

Within FindUnmatchedManKernel, each CUDA thread assesses the rank of a woman’s current partner by referencing partnerRank. If a woman’s partner rank is n+1, it signifies an unmatched man. Consequently, the thread atomically increments num_unmatched to keep track of the number of unmatched men. Conversely, if the woman is paired, her partner’s ID—retrieved from her preference list at the corresponding rank—is subtracted atomically from `id_unmatched` to pinpoint the ID of the unmatched man.

These calculations are iteratively executed on the secondary GPU until the number of unmatched men is definitively confirmed to be less than or equal to one.

If the count of unmatched men reduces to one, the sole unmatched man is then precisely identified. At this point, the LAProcedure can be invoked, passing the unmatched man’s ID as  an argument to finalize the remaining sequential proposing process.

However, when the count of unmatched men drops to zero without ever reaching one, it indicates that the proposal process is already complete, thus eliminating the need for further sequential execution. 



## BambooSMP

Building upon the adaptive execution policy and GPU Kernel to identify the unmatched man, the BambooSMP framework leverages a coordinated interplay between the Primary GPU, the Secondary GPU, and the Host CPU to manage data structures efficiently and ensure optimal performance. Each of these components plays a critical role in the framework’s execution, handling specific data structures necessary for the framework’s operations.

On the Primary GPU, BambooKernel is executed to handle the parallel processing of proposals. For this, both men’s and women’s preference lists are copied into the Primary GPU. Additionally, the rankMatrix and PRMatrix are initialized on the Primary GPU to facilitate efficient computation.

FindUnmatchedManKernel is executed on the Secondary GPU, which requires access to women’s preference lists. Peer-to-Peer (P2P) memory access is employed to allow the Secondary GPU to access these lists directly from the Primary GPU, ensuring seamless data sharing and minimizing overhead.

The Host CPU manages several key data structures and coordinates the transition of computation from the GPU to the CPU. The partnerRank and Next on the secondary GPU are copied from device memory to host memory to handle the remaining sequential steps efficiently. The procedure in Algorithm \ref{Algo:LA-GSAlgo} is invoked to enable the unmatched man to make further proposals based on the existing partnerRank.

Both the secondary GPU and Host CPU maintain the Next array and PartnerRank. The Host CPU also allocates an atomic integer, terminateFlag, to monitor and determine the completion of the proposing process on either the GPU or CPU.



## Algorithm

By initializing and maintaining these critical data structures, BambooSMP can dynamically adjust its execution strategy based on the current state of the computation, optimizing performance and resource utilization.

As illustrated in Algorithm 4, the workflow of BambooSMP begins with copying the men’s and women’s preference lists from the Host CPU to the Primary GPU. The main thread of BambooSMP initializes the rankMatrix, PRMatrix, partnerRank, and the Next array on the Primary GPU.



The terminateFlag is set to 0 on the Host CPU, indicating that neither the GPU nor the CPU has completed the proposal work. Two threads, t1 and t2, are then launched to execute doWorkOnGPU and doWorkOnCPU, respectively.



The doWorkOnGPU thread launches BambooKernel on the Primary GPU to handle proposals in parallel. Concurrently, the doWorkOnCPU thread repeatedly executes FindUnmatchedManKernel on the Secondary GPU. If it determines that only one man remains unmatched, it copies the PRMatrix from the Primary GPU to Host CPU memory and runs LAProcedure to manage proposals sequentially.



To determine which process completes first, both threads use an atomicCAS operation to set terminateFlag to either 1 or 2. If terminateFlag is set to 1, indicating that BambooKernel finished first, the main thread joins t1 and detaches t2, postprocessing the partnerRank on the Primary GPU into a stable matching. If terminateFlag is set to 2, indicating that the CPU procedure finished first, the main thread joins t2 and detaches t1. The partnerRank in Host CPU memory is then copied back to the GPU and postprocessed, ensuring efficient and accurate completion of the proposal process.





gpu-cpu hybrid system

```
BambooSMP:

BambooInit();
std::thread t1(doWorkOnGPU)
std::thread t1(doWorkOnCPU)

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
BambooInit();

std::atomic<int> termianteFlag(0);

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
    int partner_rank = partner_ranks[w];
    split_husband_rank[w] = partner_rank;
    if (partner_rank == n + 1) {
      atomicAdd(device_num_unmatched_men, 1);
    } else {
      atomicSub(device_unmatched_man, pref_lists_w[wi * n + hr]);
    }
  }
  
====================================================
postprocess(int* partnerRank, int* S) {
	int w = blockIdx.x * blockDim.x + threadIdx.x;
	if (w < n) {
		S[w] = pref_lists_w[w * n + partnerRank[w]]
	}
}7
```



## Why Correct?

(1) BambooKernel is correct



(2) BambooSMP is correct

if only BambooKernel is used, then done

if both BambooKernel and LAProcedure are invoked,

then the copied PartnerRank, each woman will have a partner who has a rank at most as good as her final result from BambooKernel.

Because only after the woman has accepted a proposal and the entry of Next in device 1 for that man will be updated to the next woman, 



## Unused

By integrating the complementary strengths of both GPUs and CPUs, the framework aims to optimize performance under varying conditions of parallelism. 





At this point, the computation transitions from the GPU to the CPU to efficiently handle the remaining sequential steps. This is accomplished by copying the \texttt{partnerRank} from device memory to host memory and invoking the procedure in Algorithm \ref{Algo:LA-GSAlgo} for the free man to make further proposals based on the existing \texttt{partnerRank}.

This transition leverages the CPU's strengths in managing tasks with limited parallelism and more complex control flow, thereby maintaining the overall efficiency of the GS algorithm execution.



Now we clarify that the critical aspect of this switch is detecting when there is only one proposer left, signifying that only one thread remains active. 





If exactly one woman's partner rank is \(n+1\), it signifies that only one proposer remains free. 