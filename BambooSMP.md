# Requirement

rewrite these sentences in more deep and academical way .

develop these sentences Actually, the beginning step, namely prechecking, has one prominent advantage, that is it can skip the initialization of Rank Matrix and PRMatrix to reach the stable matching directly. 

For the  swtich to GPU when there is only one active thread still requires the initialization step.in a more natural way? You Actually, the beginning step, namely prechecking, has one prominent advantage, that is it can skip the initialization of Rank Matrix and PRMatrix to reach the stable matching directly. 

For the  swtich to GPU when there is only one active thread still requires the initialization step.can add sentences or remove duplicate contents to strengthen the connections between sentences



# Overview

Bamboo-SMP is a parallel framework developed to solve SMP in parallel with optimal perfroamnce.

This framework employs a combination of advanced data structures, atomic operations, and a hybrid CPU-GPU execution model to achieve notable improvements in both efficiency and scalability.





Bamboo-SMP is a parallel framework developed to optimize the performance of algorithms on modern heterogeneous computing systems by effectively addressing prevalent challenges such as memory access patterns and contention. This framework employs a combination of advanced data structures, atomic operations, and a hybrid CPU-GPU execution model to achieve notable improvements in both efficiency and scalability.



The core principles of Bamboo-SMP involve several innovative strategies. Firstly, the use of PRNodes optimizes memory access by ensuring that related data elements are stored together, thereby reducing latency and enhancing data locality. Secondly, the framework utilizes the \texttt{atomicMin} operation in CUDA to efficiently resolve contention, minimizing the need for repeated retries and reducing overhead associated with atomic transactions. Lastly, Bamboo-SMP leverages a hybrid CPU-GPU approach, enabling it to capitalize on the complementary strengths of GPUs and CPUs. This hybrid execution model ensures that high parallelism and complex control flows are handled optimally, further contributing to the framework's scalability and efficiency.



Through these strategies, Bamboo-SMP demonstrates a significant advancement in the performance of parallel algorithms on heterogeneous computing systems.



# LA

## PRMatrix

As elaborated in Section \ref{subsec:Challenges with Data Movement}, a significant performance bottleneck in the GS stems from the frequent lookups of rank matrix required to determine ranks. Those accesses to rank matrix are non-sequential and incur substantial overhead.

To optmize the data access pattern of rank matrix, we propose a crucial observation: there exists a bijection between a man’s decision regarding which woman to propose to and his corresponding rank in her preference list. Suppose we have two variables, PrefListsM and RankMatrix, to represent the men’s preference lists and the women’s rank matrix, respectively. In both the GS and MW algorithms, for a given man \texttt{m} proposing to the woman at rank \texttt{r} in his preference list, the woman (\texttt{PrefListM[m, r]}) is identified. The subsequent step involves accessing the rank matrix at \texttt{RankMatrix[PrefListM[m, r], m]} to determine the man’s rank in the woman’s preference list. This process reveals a direct one-to-one correspondence between each entry in the men’s preference list and its implicitly linked entry in the women’s rank matrix. 

By harnessing this inherent relationship, we introduce a locality-aware data structure known as PRMatrix.  In PRMatrix, each pair of interrelated entries of preference lists and rank matrix is co-located within a single entity, referred to as a PRNode. This co-location enables both pieces of information to be accessed simultaneously with a single memory load, thereby eliminating the need for separate lookups in the rank matrix.

As detailed in Section \ref{placeholder}, the Gale-Shapley (GS) algorithm includes an initialization phase to configure the rank matrix. To establish the PRMatrix, an additional preprocessing step is required once the rank matrix setup is complete. This step involves pairing entries from the men’s preference lists with their corresponding ranks in the women’s preference lists, as shown in Figure \cite{fig:PRMatrix}.

For example, consider a scenario where man \texttt{M1} is proposing to a woman at \texttt{Rank1}. The algorithm retrieves woman \texttt{W2} from man \texttt{M1}’s preference list. Subsequently, it accesses the rank matrix to find \texttt{Rank2}, which represents the rank of man \texttt{M1} in woman \texttt{W2}‘s preference list. The PRNode at position \texttt{(M1, Rank1)} is then populated with the pair \texttt{(W2, Rank2)}. This systematic approach ensures that each PRNode contains both the target woman and the man’s rank within her preference list, thus consolidating the data into a single, easily accessible structure.



## LA

Although the initialization of both the RankMatrix and the PRMatrix involves square-level time complexity, leveraging GPUs can significantly expedite this process. The massive parallelism capabilities of GPUs allow for rapid initialization, ensuring that the overall execution time is not adversely impacted.

The configuration of each entry in the RankMatrix and PRMatrix is inherently independent, making it highly amenable to parallel processing. Utilizing the GPU for this initialization process enables significant acceleration due to its ability to handle extensive parallel workloads. 

To empirically validate the performance benefits of this approach, we conducted a series of tests comparing the initialization times of the RankMatrix and PRMatrix under three different conditions: (1) sequential execution, (2) parallel execution on the CPU, and (3) parallel execution on the GPU. As illustrated in Figure \cite{figure:initilaizationOnGPU}, our findings unequivocally demonstrate that the GPU achieves the fastest initialization times, even when accounting for the additional data transfer overhead between the host and the device.





The substantial reduction in initialization time afforded by GPU parallelism is pivotal to the overall performance of the GS algorithm, as it ensures that the initialization step does not become a bottleneck.







Following the construction of the PRMatrix, we have established a solid foundation for a Locality-Aware sequential implementation of the GS algorithm (LA). 

After the preprocessing step, LA initializes two additional data structures, `Next` and `PartnerRank`. The \( \text{Next} \) array records, for each man, the rank of the highest-priority woman who hasn't rejected him yet. This array allows each man to propose to women in his preference list in order without rechecking previously rejected proposals. At the start, each man proposes to the woman he prefers the most, so all ranks stored in \( \text{Next} \) are set to 1. The \( \text{PartnerRank} \) array stores the rank of the current partner of each woman. Initially, the partner rank for each woman is set to \( n+1 \), indicating they are all unmatched.

During the execution phase, LA iterates through and invokes the \texttt{LAProposalProcedure} for each man who has not yet made a proposal.

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

As previously discussed in Section \ref{subsec:Challenges with Synchronization}, a significant challenge in parallelized Gale-Shapley (GS) algorithms is the requirement for each woman to select the best proposal, which corresponds to the proposal with the minimum rank value, when multiple proposals are made simultaneously. Traditional synchronization methods, however, tend to be inefficient when updating the \texttt{partnerRank} due to the high cost of coarse-grained synchronization and the wasted work arising from \texttt{atomicCAS} failures under high memory contention.

To overcome these inefficiencies, a find-grained hardware primitive capable of efficiently managing high memory contention is necessary. Modern CPU architectures continue to rely on \texttt{atomicCAS} implementations for certain arithmetic operations, but this approach often falls short in high contention scenarios. In contrast, modern GPU architectures, such as NVIDIA’s CUDA, provide a robust set of atomic functions for arithmetic operations, among which \texttt{atomicMin} stands out as particularly effective for addressing synchronization challenges in parallelized GS algorithms.

The \texttt{atomicMin} function in CUDA takes two parameters: an address in global or shared memory and a given value (\texttt{val}). It performs an atomic transaction consisting of three operations: first, it reads the current value (\texttt{old}) at the specified address; second, it computes the minimum of \texttt{old} and \texttt{val}; and third, it stores the minimum value back at the same address. Finally, this function returns \texttt{old}, enabling the caller to determine whether the memory value has been updated. If \texttt{old} is larger than \texttt{val}, the caller can infer that the value has been updated to \texttt{val}; otherwise, no update has occurred.

The advantage of \texttt{atomicMin} in parallelizing GS is its ability to proceed without requiring an expected value to match current value. This feature ensures that each thread completes its operation in a single attempt, thereby eliminating the need for repeated retries and reducing wasted work.



To rigorously demonstrate the efficiency of \texttt{atomicMin}, we present Lemma \ref{lem:smp_instance_min_times}, which proves that in highly congested scenarios of the Stable Marriage Problem (SMP) with n men and n women, the total number of \texttt{atomicMin} operations is O(n^2). This is a marked improvement over the O(n^3) operations required when using \texttt{atomicCAS}, underscoring the superior performance of \texttt{atomicMin} in high contention environments.



By leveraging the advanced atomic functions provided by modern GPU architectures, we have developed a specialized GPU kernel named BambooKernel. This kernel represents a parallelized adaptation of the Locality-Aware GS algorithm detailed in Algorithm \ref{Algo:LA-GSAlgo}, specifically designed to efficiently handle SMP instances characterized by high contention. BambooKernel inherits much of the logic from the parallel MW algorithm’s GPU kernel. However, its key innovations lie in exploiting data locality through the use of \texttt{PRMatrix} and implementing \texttt{atomicMin} to ensure mutual exclusion and prevent race conditions during updates to the shared data structure \texttt{PartnerRank}. The use of \texttt{atomicMin} allows for a direct update of the rank of \texttt{PartnerRank[w]} with \texttt{m_rank} without requiring an expected value. 

If the update is unsuccessful, indicated by the returned value being not larger than m\_rank, the man m will be rejected and will have to propose to the next woman on his preference list in the next iteration.

Otherwise, there are two scenarios to consider:

	1.	If p\_rank equals n + 1, indicating that the woman was previously unpaired and no man is rejected, the variable \texttt{done} is set to \texttt{true} to terminate the main loop.
	2.	If p\_rank is not equal to n + 1, meaning the woman is currently paired with another partner whom she prefers less, the ID of that partner and the rank of his last proposed woman are retrieved from \texttt{PRNodesW[w, m_rank]}.

These innovations collectively enhance the efficiency and robustness of the BambooKernel, making it well-suited for handling high contention scenarios.



### Unused

Specifically, even if the returned value mismatches the previously read one but is still larger than \texttt{val}, \texttt{atomicMin} can proceed to update the minimum value with \texttt{val}, whereas \texttt{atomicCAS} would need to repeat the operation.



Each thread, representing a man \(m\), starts by proposing to the highest-ranked woman on his preference list that he has not yet proposed to. 



After retrieving the current partner's rank \(p\_rank\) for woman \(w\) from \texttt{partnerRank[w]}, the algorithm checks if \(p\_rank\) is greater than \(m\_rank\). If \(p\_rank > m\_rank\), meaning the woman \(w\) prefers the current proposer \(m\) over her current partner, we attempt to update \texttt{partnerRank[w]} to \(m\_rank\) using \texttt{atomicMin}. 



If the update is unsuccessful, as indicated by the returned value being not larger than \(m\_rank\), \(m\) will be rejected and will have to propose to the next woman on his preference list in the next iteration. 

Otherwise, there are two scenarios to consider:



# The Hybrid Structure in Bamboo-SMP

## Adaptive Execution Policy

While PRMatrix excels at minimizing data movements and BambooKernel effectively manages contention, both approaches exhibit limitations for certain workloads. The locality-aware sequential implementation struggles with workloads that benefit from parallel processing, whereas BambooKernel becomes costly in solo cases due to the unnecessary synchronization overhead and high latency inherent to GPU operations.

To overcome these workload-dependent limitations, we propose a parallel processing software framework called BambooSMP. This framework optimizes performance across diverse workloads through an adaptive execution policy that dynamically adjusts processing units in response to the varying levels of parallelism during the execution of SMP workloads.

At the beginning of any workload, when all men are unmatched and prepared to make their initial proposals, BambooSMP initiates execution by launching the BambooKernel on the GPU. This approach leverages the GPU’s capacity for massive parallelism, efficiently handling the initial phase where numerous proposals are made concurrently.

As the kernel execution progresses and the number of unmatched men decreases, the workload gradually transitions from a highly parallel to a more serial one. Recognizing this shift, BambooSMP adapts by transitioning from the massively parallel GPU execution to a lower-latency sequential execution on the CPU. This transition is crucial to circumvent the inefficiencies associated with reduced parallelism on the GPU.

By dynamically balancing the load between the GPU and CPU, BambooSMP ensures optimal performance and resource utilization. This seamless transition highlights the framework’s ability to adapt to varying workload demands, thereby optimizing computational efficiency.



## FindUnmatchedManKernel

To effectively implement the adaptive execution policy, we introduce a GPU kernel named `IdentifyUnmatchedManKernel`. When BambooKernel processes an SMP workload on the primary GPU, this kernel concurrently operates on the secondary GPU to monitor the workload’s level of parallelism by carrying out two core tasks:
\begin{enumerate}
    \item Determine if only one man remains unmatched.
    \item Identify the sole unmatched man to proceed with the sequential algorithm.
\end{enumerate}

As shown in Algorithm \ref{Algo:IdentifyUnmatchedManKernel}, the IdentifyUnmatchedKernel requires access to data structures on both the primary and secondary GPUs. To facilitate data sharing, Peer-to-Peer (P2P) memory access is employed, enabling the secondary GPU to directly access data structures on the primary GPU.

To ascertain whether only one man remains unmatched, a variable named unmatchedNum is initialized to zero. The ID of the unmatched man, unmatchedID, is set to the sum of the IDs of all men, \frac{n(n+1)}{2}. Both variables, unmatchedNum and unmatchedID, are allocated on the secondary GPU.

In preparation for the sequential proposing process, duplicate sets of Next and PartnerRank are allocated on the secondary GPU, designated as NextSecondary and PartnerRankSecondary, respectively. These structures mirror the corresponding contents on the primary GPU. Each CUDA thread within the IdentifyUnmatchedKernel is responsible for reading entries from these data structures on the primary GPU and duplicating them into the corresponding structures on the secondary GPU.

When a CUDA thread accesses an entry from PartnerRank and observes that a woman’s partner rank is n+1, the thread atomically increments unmatchedNum to account for the presence of an unmatched man. Conversely, if the woman’s partner rank is different, her partner’s ID—retrieved from her preference list at the corresponding rank on the Primary GPU—is atomically subtracted from unmatchedID to precisely identify the unmatched man’s ID. If the count of unmatched men has reduced to one, it implies that all IDs of the other n - 1 matched men have been subtracted from unmatchedID, thereby accurately identifying the sole unmatched man. 





## Heterogeneous Computing Model

Building upon the adaptive execution policy, Bamboo-SMP leverages a coordinated interplay between the primary GPU, the secondary GPU, and the host CPU to manage data structures and dynamically adjust its execution flow to ensure optimal performance.

Bamboo-SMP also incorporates a prechecking step to handle the prefect case.At the beginning, each participant selects their top choices from their preference lists, and a corresponding match is established. If all participants have distinct top choices, the matching is stable, making further steps unnecessary. Otherwise, the algorithm proceeds to the initialization step to prepare data structures for further proposals.

During the initialization phase, BambooSMP transfers the men’s and women’s preference lists from the host CPU to the primary GPU, establishing the basis for initializing the RankMatrix and PRMatrix. These data structures are then initialized on the primary GPU, while the PartnerRank and Next arrays are set up on the host CPU and subsequently copied to the primary GPU, preparing for the execution of the BambooKernel.

Following the initlialization, two threads, represented by t1 and t2, are then launched to execute procedures `doWorkOnGPU` and `doWorkOnCPU`, respectively. As the names indicate, doWorkOnGPU launches the BambooKernel on the primary GPU to handle proposals in parallel. Concurrently, t2 iteratively launches the IdentifyUnmatchedKernel on the secondary GPU until the count of unmatched men is confirmed to be less than or equal to one, performing potential operations on the host. The variables unmatchedNum and unmatchedID are reinitialized prior to each invocation of the IdentifyUnmatchedKernel.



As described in Algorithm \ref{Algo:IdentifyUnmatchedManKernel}, upon confirming that the count of unmatched men has reduced to one, the sole unmatched man is identified. Following this identification, the replicated data structures on the secondary GPU, along with the PRMatrix on the primary GPU, are transferred to the host system. This transfer enables the invocation of the LAProposalProcedure, passing the unmatched man’s ID as an argument, to finalize the remaining sequential proposing process. On the other hand, If the count of unmatched men drops to zero without ever reaching one, it indicates that BambooKernel already completes, thus eliminating the need for further sequential execution. 



To ensure optimal performance, the main thread dynamically joins the thread that completes its task first while detaching the other. This mechanism is controlled by an atomic variable, `terminateFlag`, which is initialized to 0 on the Host CPU, indicating that neither the GPU nor the CPU has completed the proposal work. As each thread progresses, the main thread monitors terminateFlag to determine the state of the computation. Both doWorkOnGPU and doWorkOnCPU employ an atomic compare-and-swap (atomicCAS) operation to set terminateFlag to either 1 or 2. 



As t1 and t2 progress, the main thread monitors terminateFlag to determine the state of the computation. If terminateFlag is set to 1, indicating that the BambooKernel completes processing first, the main thread joins t1 and detaches t2. Subsequently, the PartnerRank on the primary GPU will be copied back to the host CPU memory, awaiting further postprocessing into a stable matching. Conversely, if terminateFlag is set to 2, indicating that doWorkOnCPU finished first, the main thread joins t2 and detaches t1.



gpu-cpu hybrid system

```
BambooSMP:

PreChecking();
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
	IdentifyUnmatchedMen<<<...>>>(partnerRank,device_num_unmatched_men, device_unmatched_man)
	cudaMemcpy(&host_num_unmatched_men, device_num_unmatched_men)
}

if (# of unmatched men = 1) {
	cudaMemcpy(&host_unmatched_man,device_unmatched_man)
	LAProcedure(unmatched_man)
	setTerminateFlag(&terminateFlag, 2)
}

====================================================
setTerminateFlag(terminateFlag, expected, value):
terminateFlag.compare_exchange_strong(expected, value);


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



# Experiment

One algorithmic challenge is to identify the unmatched man for subsequent sequential proposal when only one single thread remains active. 



To empirically validate the performance benefits of this approach, we conducted a series of tests comparing the initialization times of the RankMatrix and PRMatrix under three different conditions: (1) sequential execution, (2) parallel execution on the CPU, and (3) parallel execution on the GPU. As illustrated in Figure \ref{fig:PPResult}, we show that the GPU achieves the lowest initialization times consistently, even when accounting for the additional data transfer overhead between the host and the device. 

For an SMP workload of size 30,000, the time required to initialize the RankMatrix was $6792.78$ milliseconds when executed sequentially on a single CPU core. When utilizing multicore parallel execution on the CPU, this time was reduced to $732.99$ milliseconds. However, the most dramatic improvement was observed with GPU execution, where the total initialization time was reduced to $302.77$ milliseconds, including $281.12$ milliseconds for data transfer between the host and the device. A similar trend was observed when initializing both the RankMatrix and PRMatrix. Sequential execution on a single CPU core required $46,444.17$ milliseconds, while multicore parallel execution on the CPU reduced this time to $15,946.05$ milliseconds. In contrast, GPU execution achieved the lowest initialization time of $619.63$ milliseconds, which includes $559.12$ milliseconds for data transfer. These results underscore the substantial performance advantages of GPU execution for large-scale data initialization tasks.

The preprocessing times by GPU are 1 to 2 orders of magnitude lower than those using CPU and multicore. This effective GPU acceleration allows us to leverage the initialization step as a critical component to significantly improve the overall performance of the GS algorithm. 