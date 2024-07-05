# Data Access Pattern

The GS algorithm is memory-intensive because it requires frequent and repeated accesses to the men's preference lists and the women's rank matrix. As discussed in Section \ref{subsec:The-GS-Algo}, each proposal involves minimal computation but requires accesses to the proposer's preference list to identify the best woman who has not yet rejected him, and the rank matrix to determine his rank in the woman's preference list. These two data accesses per proposal create a major performance bottleneck.



Locality is a predictable behavior that allows computer systems to anticipate needed data, reducing access times and improving efficiency. Spatial locality refers to the tendency for nearby memory locations to be accessed within a short period. If a specific storage location is referenced, adjacent memory locations are likely to be accessed soon after. This pattern enables prefetching data into the cache, reducing delays. In the case of the MW algorithm, the access pattern for the men’s preference lists is optimized. The proposer immediately moves to the next woman on his preference list, which is likely to be cached from the previous access to a lower-ranked woman, thereby enhancing performance.



However, optimizing memory access patterns of the women's rank matrix remains challenging. The rank matrix is accessed in a completely random order because  the women being proposed to and the men proposing and are dynamically determined. When the number of participants is very large, this random data accessing nature causes high latency, disrupting efficient caching and prefetching mechanisms \cite{zhang2000permutation, zhang2015mega}. These scattered and unpredictable accesses lead to poor memory usage and delayed accessing times.

To illustrate the performance bottleneck caused by data movement, we measured the memory accessing times to the rank matrix in GS and MW algorithm execution across diverse workloads. As shown in Figure \ref{fig:BreakdownGS}, the average time to access the rank matrix accounts for over $50\%$ of the total execution time in all workloads. Reducing the substantial data access time for the rank matrix is the primary focus of our optimization efforts in this paper.



# Synchronization

Parallelizing the GS and MW algorithms in a multi-core or GPU system leverages their inherent parallelism, where each thread can represent a man, allowing simultaneous proposals by multiple men \cite{mcvitie1971stable}. However, efficiently parallelizing these algorithms presents a significant challenge. While multiple threads can read a woman’s partner rank without synchronization, updating this rank requires careful coordination. This coordination is essential to prevent data races from concurrent writes and to ensure that each woman is matched with her best possible choice.



While using locks and barrier synchronization might seem straightforward to ensure each woman accepts the best proposal, these methods hinder the efficiency and scalability of parallelizing the GS algorithm. Locks ensure exclusive access to a woman’s partner rank by requiring threads to lock the data before updating the match state. However, the GS algorithm requires frequent and fine-grained updates to each woman’s partner rank, causing significant overhead from the frequent acquisition and release of locks. Barrier synchronization, on the other hand, forces all threads to wait at fixed points before proceeding. In the GS algorithm, this means all men must wait at a barrier after making proposals, allowing each woman to accept the best proposal and reject the rest before continuing. However, not all threads need synchronization at the same time in the GS algorithm. Some men may be rejected and need to propose again, while others are accepted without competition. This leads to idle time and poor resource utilization, making barrier synchronization inefficient.



The atomicCAS (Compare-And-Swap) operation is an atomic instruction used to compare a memory location's current value with an expected value and, if they match, swap it with a new value. If they do not match, the operation returns the old value, indicating the update was unsuccessful. This operation is performed atomically, ensuring no other thread can interfere during the process. In the parallel GS and MW algorithms, atomicCAS is crucial for updating a woman’s partner rank in a concurrent environment due to its capacity of effective preventing data races.  When a thread representing a man proposes to a woman, it first checks whether the current partner’s rank is higher than the proposing man’s rank.  If so, the thread attempts to update the woman’s partner rank using atomicCAS. This operation compares the current partner rank with the expected rank and, if they match, swaps it with the new rank. Upon a successful atomicCAS operation, one of two scenarios occurs: in the absence of a previous partner, the thread terminates immediately. If a previous partner exists, he becomes available again and may either be re-added to the queue in the parallel GS algorithm or assume the identity of the man that the thread represents. Conversely, when the atomicCAS operation fails, the thread retrieves the updated partner rank and continues to retry the operation until it succeeds. While atomicCAS is a lightweight and fine-grained synchronization approach seemingly suitable for the frequent updates in the GS algorithm, parallel GS and parallel MW algorithms may perform poorly under high contention due to frequent CAS failures. According to Lemma \ref{lem:smp_instance_cas_times}, in the congested case where all men have the same preference lists and processing units are sufficient, the number of atomicCAS operations can reach \( O(n^3) \), offsetting the benefits of parallelization since the time complexity of the GS algorithm is only \( O(n^2) \). 



The limitations of traditional synchronization methods lead to the question: Can we leverage advanced synchronization techniques to further optimize performance in GS parallel processing?



## Unused

Algorithm \ref{Algo:parallelGS} is a parallel implementation of lines 19-27 from Algorithm \ref{Algo:GSAlgo} and is a critical component used in both the parallel GS and parallel MW algorithms to ensure that updates to \texttt{partnerRank} are done atomically, preventing race conditions. 

The way atomicCAS makes sense is that if a thread finds that \texttt{m\_rank} is lower than the partner's rank, it attempts to update \texttt{partnerRank} with \texttt{m\_rank} using atomicCAS. If the returned \texttt{partner\_rank} does not match \texttt{p\_rank} and \texttt{m\_rank} is still lower, the operation fails and will be retried with the returned partner rank. The only difference between these two parallel versions of GS algorithms lies in handling the rejected man on line 7. In the parallel GS algorithm, if the returned rank of the current partner \texttt{p\_rank2} matches the expected \texttt{p\_rank}, the operation succeeds, and the rejected man is pushed to the \texttt{FreeManQueue} for further proposals. To prevent data races, each thread has its own \texttt{FreeManQueue}. In contrast, the parallel MW algorithm allows the thread representing the rejected man to propose again.



Therefore, GPUs, with their large number of parallel units, can even exacerbate the contention problem, diminishing the potential advantages of parallel execution. 



Can we leverage advanced hardware functions to further optimize synchronization performance in GS parallel processing?





# Irregular Parallelism

Both GPUs (Graphics Processing Units) and CPUs (Central Processing Units) are critical computing engines, each excelling in specific tasks. 

CPUs are designed for general-purpose computing with complex control logic, multi-level caches (L1, L2, L3), and higher clock speeds, enabling efficient handling of diverse tasks that require quick memory access and low latency. 

In contrast, GPUs are optimized for parallel tasks like graphics rendering and large-scale computations. They execute tasks using a function called a kernel, with the smallest execution unit being a CUDA thread. Modern GPUs have tens of thousands of SIMD (Single Instruction Multiple Data) processing units, allowing massive parallelism by running tens of thousands of threads concurrently. Each CUDA thread executes a part of the kernel function on the GPU cores, handling specific portions of the overall computation.

Implementing the parallel McVitie-Wilson (MW) algorithm on a GPU is straightforward and quite similar to its CPU version. When the GPU kernel is executed, each CUDA thread is initially assigned a man and makes proposals in parallel using atomicCAS operations. The CUDA thread continues to make proposals for the man and any rejected individuals until he is accepted by an unmatched woman.

On the other hand, implementing the parallel Gale-Shapley algorithm on a GPU is impractical due to excessive overhead. Unlike the MW algorithm, Gale-Shapley requires threads to work in groups and utilize a shared queue to manage unmatched men. This process necessitates additional synchronization, which significantly slows down the operation on a GPU.

While GPUs excel in bandwidth and handling large data volumes in parallel, they have simpler two-level caches and lower clock speeds compared to CPUs. This memory hierarchy still works well for tasks with high parallelism because the high bandwidth of GPUs boosts the overall throughput and compensates for increased memory access latency. However, when tasks are unevenly distributed, some of the GPU’s parallel units remain idle, leading to reduced performance and inefficincies. 



Irregular parallelism is a common issue in SMP workloads. In the solo case shown in Figure \ref{Workload}, only one individual may be unmatched and able to make a proposal after the initial step. Each subsequent proposal then depends on the outcomes of previous steps. This dependency leaves no room for parallelism, making the workload inherently sequential. As a result, the potential advantages of parallel execution for the MW algorithm diminish, and performance can sometimes be even slower than the sequential algorithm.



To illustrate the inefficiency of using GPUs for workload with Irregular parallelism,  we conducted a comparison between five different implementations of the GS and MW algorithms using an SMP solo case of size 10,000. The experiment results are presented in Figure \ref{fig:SerialWorkloadPerformance}. The five implementations are:

1. GS-sequential-CPU: the sequential GS executed on a CPU

2. MW-sequential-CPU: sequential MW executed on a GPU 
3. GS-parallel-CPU: the parallel GS algorithm executed on a CPU, 
4. MW-parallel-CPU: parallel MW algorithm executed on CPU 
5. MW-parallel-GPU: parallel MW algorithm executed on GPU

The results clearly show that the GPU’s performance is inferior to the CPU’s for the GS algorithm. Specifically, the parallel MW implemented on the GPU is 64.42 times slower than the sequential GS algorithm on the CPU. This slowdown is mainly due to the serial execution of most proposals and the longer data access latencies on the GPU. Additionally, it is notable that both the parallel GS on the CPU and the parallel MW on the CPU also execute slower than their sequential versions. This slowdown is due to the additional synchronization overhead caused by the atomicCAS operation.



## Unused

​	•	**GPUs**: Typically have a more simpler memory hierarchy with smaller caches and high-bandwidth memory. They can handle large datasets well if the memory access patterns are predictable.

​	•	**CPUs**: Have a more sophisticated memory hierarchy with larger caches optimized for low-latency access to frequently used data, which benefits tasks requiring frequent memory accesses with less predictability.



Therefore, GPUs, despite of their large number of parallel units, can even exacerbate the contention problem, diminishing the potential advantages of parallel execution. 



In contrast,  CPUs are designed for general-purpose computing with complex control logic, multi-level caches (L1, L2, L3), and higher clock speeds, enabling efficient handling of diverse tasks that require quick memory access and low latency. 



Executing the massively parallel MW algorithm on a GPU is challenging because certain workloads are inherently sequential. 



Efficiently implementing the massively parallel MW algorithm on a GPU presents significant challenges due to its inherently sequential nature for certain workloads. In specific SMP instances, such as the solo case  illustrated in Figure \ref{Workload}, after the initial round of proposals, only one individual may remain free and ready to make another proposal. This scenario leaves no opportunity for parallelism, as each subsequent proposal depends on the outcomes of previous steps. This sequential dependency complicates the effective use of the massively multithreaded architecture of GPUs for the GS algorithm. 



This problem can negate the benefits of using the massively multithreaded architecture of GPUs.



Irregular parallelism means that the computation has a required sequential computation that will best fit on CPU. 

