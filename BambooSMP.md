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



## LA Algorithm

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



## Host and Device Data structure

Based on the execution policy, we are able to develop a complete parallel framework called Bamboo to handle.

BambooSMP will use 3 parts: device1 (GPU1), device2(GPU2) and host.

Each part has its own data structures to complete the BambooSMP.

BambooKernel is going to be executed on device 1, it requires  both men's and women's preference lists copied into the device, and rankMatrix, and PRMatrix are initialized on the device 1.

 `FindUnmatchedManKernel` needs to be executed on the seond device to  use women's preference lists, CUDA have ...(some techniques) to allow the device 2 to access women's preference lists from device1. 

That the computation transitions from the GPU to the CPU to efficiently handle the remaining sequential steps is accomplished by copying the \texttt{partnerRank} from device memory to host memory and invoking the procedure in Algorithm \ref{Algo:LA-GSAlgo} for the unmatched man to make further proposals based on the existing \texttt{partnerRank}.

It needs to have a Next array and PartnerRank on the device and host side separately.

In order to know whether the proposing kernel on the GPU finishes or the proposing procedure on the CPU finishes first, an atomic int called termianteFlag will be utiliazed.

In summary, 

on the host side, men' preference lists and women's preference lists are inputs so allocated. And we need a Next array and PartnerRank for the LAProcedure that efficiently handle the remaining sequential steps after there is only one active thread. And an atomic int called terminate will be allocated on the host side.

On the device1, PRMatrix, Next, PartnerRank is initialized, women's preference lists are copied for BambooKernel executed on device 1 and FindUnmatchedManKernel on device 2

On the device2, Next, PartnerRank on device 1 will be copied into device 2.  



## Algorithm

As shown in Algorithm 4, after copying the men's preference lists and women's preference lists from host into device 1,  the main thread of BambooSMP  BambooSMP will first initialize rankMatrix and PRMatrix , along with other data structures like partnerRank and Next array on device 1 first.

Then, the main thread will initialize termianteFlag to 0 on the host, indicating the proposal work on both GPU and CPU has not finished yet.

After that, the main thread will launch 2 threads, t1 and t2 to run doWorkOnGPU and doWorkOnCPU individually.

Specifically, doWorkOnGPU will launch BambooKernel on a GPU to make proposals in parallel whereas doWorkOnCPU will repeatedly launch `FindUnmatchedManKernel` on the second GPU, if there is only one unmathced man, it will copy PRMatrix from the first GPU into host memory, and run LAProcedure to make proposal in serial.

doWorkOnGPU and doWorkOnCPU will compete to use an atomicCAS operation to set the termianteFlag to 1 and 2 respectively to indicate BambooKernel completes first or the copying and the sequential LA completes first.

In the main thread, if termianteFlag is set to 1, meaning the BambooKernel finishes first, and main thread will join t1 and detach t2. In addition, the partnerRank that is stored in the first GPU will  be postprocessed into a stable matching.

On the other hand, if termianteFlag is set to 2, meaning the procedure executing on CPU completes first, and the main thread will join t2 and detach t1.

In this case, the he partnerRank that in the host memory will  be copied into GPU, then postprocessed into a stable matching.



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