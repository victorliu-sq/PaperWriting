# Title

FlashSMP:

A stable marriage needs to cohabitate, resolve conflicts, and embrace complementary strengths



# Abstract

The Stable Marriage Problem (SMP) is a classical challenge to establish a stable pairing between two groups, traditionally referred to as "men" and "women." Each member of these groups has a ranked preference list for potential partners from the opposite group. The primary objective is to create pairings that are mutually stable, ensuring that no pair of individuals in the resulting arrangement would prefer each other over their assigned partners. The SMP computation has been widely used in various applications, including college admissions, optimizing job scheduling to make efficient use of computing, networking, and storage resources, allocating medical resources, making economic predictions and policy decisions, and many others. The basic SMP computations rely on the Gale-Shapley algorithm, a sequential process that constructs stable pairings iteratively based on the ranked preferences of individuals from both groups. This algorithm is highly time-consuming and data-intensive. While efforts have been made over the years to parallelize the Gale-Shapley algorithm, these attempts have been hindered by three major bottlenecks, namely, suboptimal data access patterns, the overhead of atomic operations caused by inefficiencies with atomicCAS, and the restriction of implementation to either CPU or GPU.   



To address these 3 challenges, in this paper, we introduce FlashSMP, an efficient parallel SMP algorithm and its implementation in a hybrid environment of GPU and CPU. 

FlashSMP's high performance stems from three key development efforts. 

First, we effectively exploit the data accessing locality with a new data structure called PRNodes to "cohabitate".

Second, FlashSMP employs a more advanced atomic operation called "atomicMin" provided by CUDA to reduce the inefficiencies caused by atomicCAS under high memory contention, an effort we term "resolving conflicts." 

Thirdly, FlashSMP is implemented in a hybrid environment of both GPU and CPU, leveraging the high bandwidth of the GPU and the low latency of the CPU to achieve optimal performance across a wide range of workloads. We refer to this enhancement as "embrace complementary strengths"



Finally, we demonstrate FlashSMP's high scalability through extensive experiments using both synthetic and real-world datasets, consistently delivering exceptional performance even as the problem size grows significantly. Our evaluation results show that FlashSMP significantly outperforms state-of-the-art parallel algorithms, achieving speedups of up to 28.3x across various workloads.



# Introduction

## Importance

The Stable Marriage Problem (SMP), introduced by David Gale and Lloyd Shapley in 1962, seeks to find a stable matching between two equally numbered sets of participants with ranked preferences, ensuring no pair of individuals would prefer each other over their assigned partners. Gale and Shapley also introduced the Gale-Shapley (GS) Algorithm, also known as the Deferred Acceptance (DA) algorithm, which guarantees a stable matching for any instance of the SMP.\cite{gale1962college} 

The SMP has been a cornerstone in combinatorial optimization with applications spanning matching markets, resource allocation, and more. Its fundamental role in real-world applications such as matching doctors to hospitals, students to schools, and organ donors to patients underscores its significance. The profound impact of SMP on these fields was recognized when Dr. Alvin Roth and Dr. Lloyd Shapley received the Nobel Prize in Economics in 2012.



## Shortcoming of previous work

Efficient algorithms for Stable Marriage Problems (SMP) are critical as problem sizes grow and computational resources evolve. Technological advancements in the twentieth century led to regular increases in processor clock speeds, naturally accelerating the GS algorithm. However, since the early 21st century, we have seen an end to these "free rides" as Moore's Law approaches its limits \cite{10.5555/2385452}. With the rise of advanced parallel architectures like multicore processors and GPUs, exploiting the parallelism of SMP algorithms has become both inevitable and necessary.



Despite its importance, research on parallel SMP algorithms has been limited due to the inherent complexities of this task. To our knowledge, the only parallel algorithm that outperforms the sequential Gale-Shapley (GS) algorithm is the parallel McVitie-Wilson algorithm. While this algorithm has set a benchmark by running faster than sequential solutions, its performance on GPUs is hindered by high contention for shared resources and high-latency memory operations, making it even less efficient than its CPU implementation. 



## Challenges



1

First, optimizing memory access patterns to reduce latency and improve cache performance is crucial since the Gale-Shapley (GS) algorithm is memory-intensive. Poor memory access patterns can lead to frequent cache misses, degrading both sequential and parallel performance.



2.

The workload, namely SMP instances, consists of preference lists for each individual where each man ranks women from highest to lowest preference, and each woman ranks men similarly.

Then, In a parallel algorithm, each unpaired man is represented by a thread to make proposals.

When multiple men propose to the same woman, the threads compete for the same shared memory location, requiring synchronization to ensure the woman accepts the best proposal.

When all men have identical preference lists, their corresponding threads will compete for the same woman. This scenario requires robust synchronization methods since CAS-based data structures may perform poorly under high contention due to work wasted by CAS failures.



Second, when multiple men propose to the same woman, the threads representing these men compete for the same shared memory location. This requires robust synchronization methods like atomicCAS. In extreme cases, where all the men propose to women in the exact same order, memory contention can become very high. As a result, the algorithm may perform poorly due to the wasted work from CAS failures.



3.

The next challenge is that Parallelism can drop significantly when variations are introduced in the preference lists. For example, if all men propose to half of the women in the first round, half of them will be paired. As women pair off and remain paired, the number of free men and active threads decreases. Eventually, only one man will be making proposals, leading to a serial problem. The synchronization overhead then outweighs the benefits of GPU's high bandwidth, making GPU implementations often perform worse than CPU implementations. 



Third, parallelism can drop significantly when there are variations in people's preferences. For instance, if all men propose to half the women in the first round, half will be paired. As women pair off and remain paired, the number of free men and active threads will reduce. Eventually, this leads to a serial problem where only one man is making proposals, negating the benefits of GPU's high bandwidth due to synchronization overhead.



4.

This challenge is because Parallelizing SMP computation presents significant challenges for developing parallel algorithms due to its workload-dependent nature. 



Another challenge is that Different workloads can exhibit distinct properties, significantly affecting the design and implementation of an effective algorithm. Therefore, developing an efficient parallel SMP algorithm requires careful consideration of these varying workload characteristics. That is resolution of conflicts in instance where preference lists are distinct cannot affect the efficiency of algorithm on , the approach to improve the performance of workload that eventually turns into a serial problem should also take into consideration whether efficiency on workload with distinct preference lists will be lowed.   



Lastly, the algorithm must universally handle varying workloads. 

In order to develop a more efficient parallel algorithm to SMP that fully exploits the high bandwidth of modern computing architectures, particularly GPUs, we need to address 4 non-trivial challenges:

Techniques to resolve above issues should  high contention should not negatively impact instances that become serial problems early, and methods to accelerate serial problems should not affect instances with high contention. 

This balance is crucial for maintaining efficient performance across diverse scenarios.





Lastly, Different workloads can exhibit distinct properties, significantly affecting the design and implementation of an effective algorithm. Therefore, developing an efficient parallel SMP algorithm requires careful consideration of these varying workload characteristics such that technique to resolve above issues should not negatively impact instances in other scenarios but maintaining efficient performance across diverse scenarios.



### AI

To develop a more efficient parallel algorithm for SMP that fully leverages the high bandwidth of modern computing architectures, particularly GPUs, we need to address four significant challenges:

First, optimizing memory access patterns to reduce latency and enhance cache performance is crucial due to the memory-intensive nature of the Gale-Shapley (GS) algorithm. Inefficient memory access patterns can result in frequent cache misses, thereby degrading both sequential and parallel performance.



Second, when multiple proposers contend for the same recipient, the threads representing these proposers compete for the same shared memory location, necessitating robust synchronization mechanisms such as atomic compare-and-swap (atomicCAS) to prevent data races. In extreme scenarios where all proposers follow the same sequence, memory contention can become severe, leading to substantial performance degradation due to the inefficiency caused by CAS failures.



Third, parallelism can diminish significantly when there are disparities in individual preferences. 

For instance, if all proposers target half of the recipients at the beginning, then in the first round, half of the proposers will successfully pair with recipients.

As recipients pair off and remain paired, the number of available proposers and active threads will steadily decrease.

This scenario eventually leads to a serial bottleneck, where only a single proposer remains active, thereby negating the advantages of the GPU's high bandwidth due to synchronization overhead.



Lastly, different workloads can exhibit distinct properties, which significantly affect the design and implementation of an effective algorithm. Therefore, developing an efficient parallel SMP algorithm requires careful consideration of these varying workload characteristics. The solutions to the aforementioned issues should be designed to maintain efficient performance across diverse scenarios, without negatively impacting any particular instance.



## Our Work

In order to overcome these challenges, we present FlashSMP, an innovative algorithm that addresses these issues as follows:

By closely analyzing the Gale-Shapley (GS) algorithm, We have uncovered a one-to-one correspondence between the recipient index and the rank of the proposer in the recipient's preference list. We incorporate a preprocessing step to eliminate data dependencies, allowing related data to be accessed together. This enables efficient memory access patterns and reduces latency.

To reduce wasted work under high memory contention, FlashSMP utilizes atomicMIN operations instead of atomicCAS. This approach asymptotically decreases the number of atomic operations and enhances synchronization efficiency.

Additionally, our algorithm seamlessly integrates CPU and GPU resources, implementing FlashSMP in heterogeneous computing environments. This integration allows us to leverage the high bandwidth of the GPU to make parallel proposals when the number of active threads is large, and switch to the CPU to utilize its low latency for fast proposals when there is only a single active thread.

Finally, our evaluation results demonstrate that FlashSMP adapts effectively to different workloads, ensuring consistent and optimal performance across diverse scenarios.



## Contribution

Specifically, we make the following contributions:

1.We developed a new data structure, PRNodes, to enhance data locality. By incorporating a preprocessing step to initialize these PRNodes, we ensure that all necessary rank information is immediately accessible within the same PRNode during proposals. This significantly reduces the need for global memory access and enhances real-time performance.



2.We provide a Rigorous mathematical proof demonstrating the superiority of atomicMIN over atomicCAS in high-contention scenarios.



3.Our experimental benchmarks highlight the complementary strengths of CPUs and GPUs. The CPU excels in low-latency operations, while the GPU offers high bandwidth, allowing us to leverage both for optimal performance.



4.Combining these research efforts, we introduce a novel framework named FlashSMP for the parallel computation of SMP. . FlashSMP utilizes atomicMIN to resolve undefined behaviors effectively and is implemented in a heterogeneous environment of CPU and GPU.



5.Our experimental evaluations comprehensively demonstrate FlashSMP's exceptional efficiency that FlashSMP outperforms the state-of-the-art parallel algorithms by from 2.4x to 10x across various workloads, underscoring its capacity of workloads adaptation



## Paper Structure

The remainder of this paper is organized as follows: 

Section 2 provides background information on the Stable Marriage Problem. 



Section 3 details the design and implementation of FlashSMP, including the development of the PRNodes data structure and the preprocessing step to improve data locality and memory access efficiency. This section also discusses the rigorous mathematical proof demonstrating the superiority of atomicMIN over atomicCAS in high-contention scenarios, along with the complementary strengths of CPUs and GPUs, supported by our experimental benchmarks. 



Section 4 presents our experimental setup and results, offering a comprehensive evaluation of FlashSMP's performance and highlighting its efficiency and adaptability across various workloads. 



Section 5 reviews related work, including existing serial and parallel algorithms for SMP. Finally, Section 6 concludes the paper, summarizing our findings and suggesting potential directions for future research.



# Section2-Background

## SMP

The Stable Marriage Problem (SMP) involves finding a stable matching between two sets of participants, typically referred to as men and women. Each participant has a preference list ranking the members of the opposite set. The objective of SMP is to find a stable matching, where no two participants prefer each other over their current partners. In other words, a matching is stable if there are no two individuals who would rather be with each other than with their current partners.

A stable matching is defined as one where there are no blocking pairs. A blocking pair is a pair of participants who would both prefer each other over their current partners. If such a pair exists, the matching is considered unstable because these two participants would have an incentive to deviate from their assigned partners and pair up instead.

Consider three men (M1, M2, M3) and three women (W1, W2, W3) with the following preference lists:

Men:

- M1: W1, W2, W3
- M2: W2, W1, W3
- M3: W2, W3, W1

Women:

- W1: M1, M2, M3
- W2: M2, M1, M3
- W3: M1, M3, M2

To illustrate a stable matching, consider the following example:

M1 is matched with W1, M2 is matched with W2, and M3 is matched with W3. To check if this matching is stable, we need to ensure there are no blocking pairs. M1 prefers W1, and W1 is his top choice. W1 also prefers M1, her top choice. M2 prefers W2, and W2 is his top choice. Although W2 prefers M1 over M2, she is already matched with M1, her second choice. M3 prefers W3, and W3 is his top choice. Although W3 prefers M1 over M3, she is already matched with M3. Since no two participants prefer each other over their current partners, there are no blocking pairs, and this matching is stable.

Now, consider a different matching to illustrate instability:

Suppose M1 is matched with W2, M2 is matched with W1, and M3 is matched with W3. To check if this matching is unstable, we look for blocking pairs. M1 is matched with W2, but he prefers W1 over W2. W1, who is matched with M2, prefers M1 over M2. Thus, M1 and W1 form a blocking pair because they both prefer each other over their current partners. Therefore, this matching is unstable due to the presence of a blocking pair.

In conclusion, a matching in the context of SMP is stable if and only if there are no blocking pairs. The Gale-Shapley algorithm ensures that a stable matching is always found, thus addressing the issue of instability in matchings by systematically eliminating blocking pairs through its proposal and acceptance phases. This guarantees that the final matching is stable, demonstrating the robustness and efficiency of the algorithm in solving the Stable Marriage Problem.



## GS

The Gale-Shapley algorithm, also known as the Deferred Acceptance algorithm, is a foundational method for solving the Stable Marriage Problem (SMP). Proposed by David Gale and Lloyd Shapley in 1962, the algorithm guarantees finding a stable matching between two equally sized sets of participants, typically referred to as men and women, each with their own preference lists.

The algorithm operates in iterative rounds where each unengaged man proposes to the highest-ranked woman on his preference list who has not yet rejected him. Women then consider these proposals and tentatively accept the one they prefer most while rejecting the rest. If a woman receives multiple proposals, she keeps the proposal from the man she prefers the most (even if she was already holding a different proposal) and rejects all others. This process continues until there are no more unengaged men left.

Initially, all participants are free (unmatched). During the proposal phase, each free man proposes to the highest-ranked woman on his list who has not yet rejected him. In the acceptance phase, each woman receiving one or more proposals chooses the man she prefers the most among the proposers and tentatively accepts his proposal, rejecting all other proposals. This proposal and acceptance cycle repeats until there are no more free men.

Consider the following example with three men (M1, M2, M3) and three women (W1, W2, W3) with the respective preference lists:

Men:

- M1: W1, W2, W3
- M2: W2, W1, W3
- M3: W2, W3, W1

Women:

- W1: M1, M2, M3
- W2: M2, M1, M3
- W3: M1, M3, M2

The execution of the Gale-Shapley algorithm proceeds as follows:

Initially, M1 proposes to W1. W1 accepts M1's proposal tentatively, resulting in the tentative match (M1, W1). Next, M2 proposes to W2, and W2 accepts M2's proposal tentatively, resulting in the tentative match (M2, W2). Then, M3 proposes to W2. W2 prefers M3 over M2, so she accepts M3's proposal and rejects M2. The tentative matches are now (M1, W1) and (M3, W2).

M2, now free, proposes to W1. However, W1 prefers M1 over M2 and rejects M2. The tentative matches remain unchanged. M2, still free, proposes to W1 again, and W1 once again rejects him in favor of M1. The tentative matches still remain (M1, W1) and (M3, W2). Subsequently, M2 proposes to W3. W3 accepts M2's proposal tentatively, resulting in the tentative match (M2, W3).

M1, now free, proposes to W2. W2 prefers M1 over M3, so she accepts M1's proposal and rejects M3. The tentative matches are now (M1, W2) and (M2, W3). M3, now free, proposes to W3. However, W3 prefers M2 over M3 and rejects M3. The tentative matches remain (M1, W2) and (M2, W3). Finally, M3 proposes to W1, but W1 prefers M1 over M3 and rejects him, leaving the tentative matches unchanged.

The algorithm terminates with the following stable matching: M1 is matched with W2, M2 is matched with W3, and M3 is unmatched. This matching is stable as there are no two individuals who prefer each other over their current partners.

The Gale-Shapley algorithm ensures that such a stable matching is always found, demonstrating its robustness and efficiency in solving the Stable Marriage Problem. The properties of the Gale-Shapley algorithm include guaranteed stability, male-optimality, and polynomial time complexity (O(n^2)), making it efficient for practical use. The algorithm has widespread applications beyond the traditional SMP, including college admissions, job placements, and organ donation matching, highlighting its importance in various domains requiring stable matchings.



# Section3-Challenges

## Optimizing Memory Access Patterns

According to section 2, the acceptance phase of GS algorithm requires determining the rank of each man in the preference list of the proposed woman. An efficient approach is to utilize a precomputed data structure, called Rank Matrix, that allows for O(1) time complexity in retrieving these ranks. 

To illustrate how the Rank Matrix works, consider the following preference lists:

Men:

- M1: W1, W2, W3
- M2: W2, W1, W3
- M3: W2, W3, W1

Women:

- W1: M1, M2, M3
- W2: M2, M1, M3
- W3: M1, M3, M2

From these preference lists, we construct the Rank Matrices for each woman. Each entry R_WM in the matrix represents the rank of man M in woman W's preference list. Here's how the Rank Matrices look for this example:

For 𝑊1*W*1's preference list:

- M1 is ranked 1 (first choice)
- M2 is ranked 2 (second choice)
- M3 is ranked 3 (third choice)

For 𝑊2*W*2's preference list:

- M2 is ranked 1 (first choice)
- M1 is ranked 2 (second choice)
- M3 is ranked 3 (third choice)

For 𝑊3*W*3's preference list:

- M1 is ranked 1 (first choice)
- M3 is ranked 2 (second choice)
- M2 is ranked 3 (third choice)

Constructing the Rank Matrix involves preprocessing each woman's preference list. We scan the preference list of each woman from rank 0 (highest) to rank 𝑛−1*n*−1 (lowest). For example, in 𝑊2*W*2's preference list, if the entries are M2, M1, and M3 for ranks 1, 2, and 3, respectively, the Rank Matrix would be initialized as 𝑅𝑊2𝑀2=1*R**W*2*M*2=1, 𝑅𝑊2𝑀1=2*R**W*2*M*1=2, and 𝑅𝑊2𝑀3=3*R**W*2*M*3=3.

The Rank Matrices for the women will be as follows:

𝑅𝑊1*R**W*1

𝑀1𝑀2𝑀3𝑊1123*W*1*M*11*M*22*M*33

𝑅𝑊2*R**W*2

𝑀1𝑀2𝑀3𝑊2213*W*2*M*12*M*21*M*33

𝑅𝑊3*R**W*3

𝑀1𝑀2𝑀3𝑊3132*W*3*M*11*M*23*M*32

The GS algorithm is memory-intensive because it involves frequent and repeated accesses to the preference lists and the Rank Matrix. Specifically, each proposal involves minimal computation but requires a man to access the Rank Matrix to determine his rank in the preference list of the woman he is proposing to, thereby making memory access the primary bottleneck. 

Despite the Rank Matrix’s efficiency, optimizing memory access remains challenging due to non-sequential access patterns. 

Because fast memory is expensive, a modern memory hierarchy is structured into levels—each smaller, faster, and more expensive per byte than the next lower level, which is farther from the processor. Modern architectures also employs a strategy known as locality, where consecutive data stored in memory locations are loaded in batches into the cache. This occurs in two forms: temporal locality and spatial locality. When a processor references some data, it first looks it up in the cache. If not found, the data must be fetched from a lower level of the hierarchy and placed in the cache before proceeding.To improve efficiency, data is moved in blocks, exploiting the spatial locality \cite{architecture6th}.

The Rank Matrix is accessed in a non-linear order because the index of the woman to propose to and the man's rank in her preference list are determined dynamically at runtime.

For instance, if M1 proposes to W1 first, he will access 𝑅𝑊1𝑀1*R**W*1*M*1 to check his rank, which is 1. If W1 rejects M1 and he then proposes to W2, he will access 𝑅𝑊2𝑀1*R**W*2*M*1, where his rank is 2. This dynamic decision-making process causes unpredictable memory accesses.

These accesses are not sequential and result in memory jumps, disrupting efficient caching and prefetching mechanisms. Consequently, these scattered and irregular memory accesses challenge the optimization of the GS algorithm's performance.



### Uesless Content

Clearly, a sequential algorithm that initializes rank matrix runs in O(n^2) time, where n is the number of participants. The Rank Matrix is designed such that each entry 𝑅[𝑖][𝑗]*R*[*i*][*j*] represents the rank of man 𝑀𝑖*M**i* in woman 𝑊𝑗*W**j*'s preference list.

Thanks to Rank matrix, reduces the complexity of rank retrieval to O(1) time. As GS algorithm is described before, for each iteration, preference list and rank matrix will be access in a constant times, O(1), thus resulting in time O(1) for each iteration. 

Furthermore, it has been proven the number of proposals for an SMP instance is O(n^2). And each proposal takes O(1) time, thus the total execution time of GS algorithm takes O(n^2) to precompute rank matrix and O(n^2) to make proposals.

In contrast, the preference lists of men are accessed sequentially because each man makes proposals from his highest preference to his lowest. However, the irregular access patterns of the Rank Matrix can significantly impact overall performance due to frequent cache misses.



## Synchronization in Shared Memory Contention

When parallelizing the GS algorithm, the challenges of synchronization and wasted work become even more pronounced due to the algorithm's inherent properties.

In the parallel GS algorithm, multiple threads simultaneously propose matches and check conditions for acceptance or rejection. This requires frequent updates to shared data structures, such as lists of proposals and acceptance statuses. Synchronizing these updates without causing significant wasted work is particularly challenging:

The retries and wasted work from `atomicCAS` operations can significantly slow down the overall algorithm, offsetting the benefits of parallelization.

As the number of threads increases, the likelihood of contention and wasted work also increases. Optimizing `atomicCAS` for a small number of threads may not scale well to larger numbers, exacerbating the problem in highly parallel systems.

To mitigate the wasted work caused by `atomicCAS` under high memory contention, The parallel GS algorithm presents unique challenges that make these methods less effective:

Backoff strategies involve making threads wait for a random or increasing amount of time before retrying the `atomicCAS` operation. This reduces the likelihood of repeated contention at the same memory location. The parallel GS algorithm requires rapid and frequent updates to shared data structures. Introducing delays with backoff strategies can significantly slow down the overall progress of the algorithm, leading to inefficiencies and longer convergence times.

Partitioning involves dividing the data and workload into smaller, independent segments that can be processed in parallel with minimal interaction between threads. The GS algorithm involves global comparisons and updates (e.g., matching proposals and rejections across the entire dataset). Partitioning the problem space can lead to incorrect matches and instability, as the algorithm's correctness depends on considering all possible matches globally.

one potential strategy to manage contention and synchronization issues is to limit the number of working threads. While this approach can reduce contention. One of the key goals of parallelizing the GS algorithm is to achieve scalability—being able to handle larger datasets and more complex matching problems efficiently as computational resources increase. As the size of the dataset increases, the workload for the GS algorithm grows. With a limited number of threads, the algorithm's ability to scale and handle larger datasets efficiently is compromised, leading to longer processing times and reduced performance.





## GPU

Implementing the parallel Gale-Shapley (GS) algorithm on a GPU presents significant challenges due to the unique architecture and execution model of GPUs. GPUs excel at handling highly parallel, data-parallel tasks with regular memory access patterns, providing high bandwidth for large-scale computations. This high bandwidth allows many threads to access memory simultaneously, which is advantageous for many parallel algorithms. However, the GS algorithm involves irregular and dynamic access patterns due to its iterative proposal and acceptance processes, leading to high contention when many threads attempt to update and access shared data structures concurrently.



Each thread on a GPU would need to frequently perform atomic operations, such as `atomicCAS`, to prevent data races. These atomic operations can become bottlenecks under high contention, causing significant wasted work and reducing overall efficiency. The frequent need for atomic operations leads to threads repeatedly attempting and failing to perform updates, creating delays and reducing the effective parallelism of the algorithm.



Furthermore, the GS algorithm's need for frequent global synchronization to ensure consistent state across all threads adds complexity, as GPUs are designed for fine-grained parallelism rather than frequent synchronization barriers. Managing these synchronization challenges while maintaining the algorithm's correctness and efficiency requires sophisticated techniques that can be difficult to implement and optimize on GPU architectures.



Third, parallelism can diminish significantly when there are disparities in individual preferences. For instance, if all proposers target half of the recipients at the beginning, then in the first round, half of the proposers will successfully pair with recipients. As recipients pair off and remain paired, the number of available proposers and active threads will steadily decrease. This scenario eventually leads to a serial bottleneck, where only a single proposer remains active, thereby negating the advantages of the GPU's high bandwidth due to synchronization overhead. This bottleneck is exacerbated by the GPU's architecture, which is optimized for massive parallelism and suffers in performance when only a few threads are active. 



Additionally, GPUs typically have higher latency than CPUs when it comes to certain operations, particularly those involving memory access and synchronization. GPUs are designed to hide latency through massive parallelism and high throughput, scheduling thousands of threads to keep the processing units busy while some threads wait for memory operations to complete. However, this approach relies on having enough parallel work to keep the GPU fully occupied. In the context of the parallel GS algorithm, as the number of active threads decreases due to successful pairings, the latency hiding mechanism becomes less effective. Higher latency in memory access and synchronization operations can significantly impact performance, as remaining threads spend more time waiting for these operations to complete. This leads to increased idle time and reduced overall efficiency, further highlighting the challenges of implementing the parallel GS algorithm on GPUs.



Therefore, the inherent nature of the GS algorithm, with its need for dynamic and often unequal work distribution, makes it particularly challenging to implement efficiently on a GPU.



# Section4-FlashSMP

FlashSMP is a parallel framework designed to enhance the performance of algorithms on modern heterogeneous computing systems by addressing common challenges such as memory access patterns and contention. The framework leverages a combination of innovative data structures, atomic operations, and a hybrid CPU-GPU execution model to achieve significant improvements in efficiency and scalability. The core ideas behind FlashSMP include the use of PRNodes to optimize memory access, atomicMin in CUDA for contention resolution, and a hybrid approach to harness the strengths of both GPU and CPU.



## Cohabitation-PRNode

As discussed in Section 2, solving the SMP traditionally relies on two key data structures: preference lists and rank matrices. Preference lists arrange each man's proposals from the most to the least preferred woman. To evaluate a proposal, a woman then looks up the rank matrix to determine the proposer's relative ranking from her perspective. The limitations and inefficiencies of this approach do not become apparent until the algorithm and data structures are implemented on real hardware. 

Even if  the irregular access patterns of the Rank Matrix can significantly impact overall performance due to frequent cache misses, the preference lists of men are accessed sequentially because each man makes proposals from his highest preference to his lowest.

FlashSMP introduces PRNodes, a specialized data structure designed to enhance memory access patterns by closely coupling related data elements from the preference lists and rank matrices used in the Gale-Shapley (GS) algorithm. PRNodes encapsulate entries from a proposer’s preference list along with the corresponding rank entry from the recipient’s rank matrix, facilitating efficient access during both the proposal and acceptance phases of the algorithm.

By storing these entries next to each other, PRNodes optimize memory access patterns, thereby improving efficiency. When a proposer accesses their next preference, the corresponding rank entry is fetched simultaneously or with minimal additional memory accesses. This spatial locality ensures that related data is loaded together, reducing cache misses and improving memory access efficiency. PRNodes address this problem by organizing data in a way that aligns better with memory access patterns, reducing the frequency and impact of memory jumps. This organization ensures that when a proposer accesses their PRNode, they can retrieve both the woman to propose to and the relevant rank information in a single, efficient memory operation.



## Conflict Resolution-atomicMin

The Deferred Acceptance (DA) algorithm naturally lends itself to parallelization, as multiple proposers (men) can make proposals simultaneously. For example, by assigning each thread to simulate a man making proposals when implemented on an actual multithreading hardware, all men will initially propose to their preferred women. However, for the DA algorithm to make progress, it is crucial for threads to communicate with each other. Considering the preference lists given in Figure\ref{perferences}, men m1, m3, m5, and m6 will be paired with their proposed women directly whereas m2 and m7, as well as m4 and m8, will communicate to resolve conflicts if they are proposing to the same woman simultaneously.



Handling the optimal proposer in the Gale-Shapley (GS) algorithm involves finding the minimal value among possible proposals, which corresponds to the highest priority match according to the rank matrix. This minimization process is critical for determining the optimal matches and ensuring the algorithm converges to a stable state efficiently.



A straightforward solution is to use barrier synchronization. In parallel computing, a barrier is a method that forces threads or processes to wait until all participating threads reach a certain point in the code to ensure synchronized behavior. However, this approach can lead to high communication traffic due to all threads repeatedly accessing a global variable to check their status, diminishing scalability. An alternative method, as utilized in \cite{lerring2017parallel}, involves the use of an atomic instruction known as compare-and-swap (CAS) for synchronization in multithreading. CAS works by taking two values: a new value to be written to a memory location and a comparison value to ensure the operation's validity. It reads the old value from the memory, compares it with the provided comparison value, and, if they match, writes the new value to the memory location—all in a single atomic operation. The old value is returned, indicating whether the substitution was successful based on whether the return value matches the comparison value. Nevertheless, CAS can lead to inefficiencies in high-contention scenarios, such as when multiple threads (simulating men proposing to the same woman) compete to update a shared resource. In such cases, only one thread succeeds, while the others must retry, leading to wasted efforts due to CAS failures and significant overhead from frequent synchronization among many processors.

In parallel computing, atomic operations are essential for managing shared memory access without data races. The atomicCAS (Compare-And-Swap) operation is an atomic instruction used to compare a memory location's current value with a given expected value and, if they match, replace it with a new value. This operation is performed atomically, ensuring that no other thread can interfere during the comparison and swap process. In CUDA, atomicCAS guarantees correctness by allowing only one thread to successfully update the memory location at a time.

In the worst-case scenario, if the preference list size is 𝑛*n*, and all threads contend to update the same memory location, each thread may need to repeatedly attempt the atomicCAS operation until it succeeds. This can result in 𝑂(𝑛)*O*(*n*) atomicCAS operations per thread, leading to a total of 𝑂(𝑛2)*O*(*n*2) operations for all threads combined.

To analyze the behavior of atomicCAS more closely, consider the scenario where multiple threads attempt to update a shared memory location to the smallest value. Let the values proposed by these threads be 𝑣1,𝑣2,…,𝑣𝑛*v*1,*v*2,…,*v**n*, sorted such that 𝑣1<𝑣2<…<𝑣𝑛*v*1<*v*2<…<*v**n*.

The smallest value 𝑣1*v*1 will execute atomicCAS successfully on its first attempt, as there is no smaller value in the memory yet. The second smallest value 𝑣2*v*2 will execute atomicCAS successfully only after 𝑣1*v*1 has updated the memory location, meaning it might attempt the operation twice—first failing when 𝑣1*v*1 updates the location and then succeeding. Similarly, the 𝑘*k*-th smallest value 𝑣𝑘*v**k* may need up to 𝑘*k* attempts, as it will fail for each smaller value that has already updated the location.

The total number of atomicCAS executions 𝑇(𝑛)*T*(*n*) for 𝑛*n* values is the sum of these attempts:

𝑇(𝑛)=∑𝑘=1𝑛𝑘=1+2+3+…+𝑛=𝑛(𝑛+1)2*T*(*n*)=∑*k*=1*n**k*=1+2+3+…+*n*=2*n*(*n*+1)

Thus, the total number of atomicCAS executions in the worst case is 𝑂(𝑛2)*O*(*n*2).

The atomicMin operation, described in the CUDA documentation, reads the 32-bit or 64-bit word located at a given address in global or shared memory, computes the minimum of this value and a given value, and stores the result back to the memory address in one atomic transaction. The function returns the original value before the update. This means that atomicMin ensures the minimum value is stored efficiently with minimal contention and retries.

AtomicMin can asymptotically reduce the number of atomic operations compared to atomicCAS. With atomicMin, each value directly attempts to update the shared memory location to the minimum of the current value and the new value. Since atomicMin ensures that only the smallest value updates the memory location, each thread attempts the operation only once, eliminating the need for repeated retries and reducing contention significantly.

Given the same scenario with 𝑛*n* values, atomicMin ensures that each value attempts the update operation exactly once. Therefore, the total number of atomic operations using atomicMin is simply 𝑂(𝑛)*O*(*n*).

By using atomicMin instead of atomicCAS, we achieve a significant reduction in the number of atomic operations, leading to improved efficiency and faster convergence in parallel algorithms such as the Gale-Shapley algorithm. This optimization is particularly beneficial in a parallel computing environment, where efficient memory access and reduced contention are critical for achieving high performance.



## Embrace Complementary Strengths - GPU and CPU

GPU can accelerate performance over CPU due to its massively parallel architecture and high bandwidth memory. \cite{nestedGPU}





# Section5-Experiment

if preference lists divide the members on the opposite side into groups and rank groups in the same way while randomize the people inside each group, which we call the mixed instance, then the number of proposing men will not dramatically decrease to a single man to make peoposal



## Bike

We use bike sharing data2 to calculate distances from a start point to an end point as agent preferences on the 𝑋 side.
Agent preferences on the 𝑌 side are the values of orders for a bike on its start point; order values of follow a uniform distribution.



values of orders must range from the highest to lowest.

Due to the uniform distribution, there can be duplicate value of orders. Especially for those values that are quite similar.



We can randomize ranks that correspond to order with those similar values.



calculate distances from a start point to an end point as agent preferences on the 𝑋 side.

(1) Divide into Groups: criteria for vehicle types

(2) Distance: each group is further divided into groups for distances.

Those groups will randomize ranks and all nodes inside Each group for distances will randomize the rank



## TAXI

TAXI/TAXI+. As with the BIKE dataset, we construct a two-sided market from taxi and user data in the NYC Taxi dataset3.



https://kaggle.com/datasets/marcusrb/uber-peru-dataset



## ADM

University admission forms a classic scenario for the stable
marriage problem [2, 43]. We obtain university ranking data5
and GRE and TOEFL score from anonymous admission data6.
We construct preference lists by a two-order sort, first by type
of institute, then by rank within each type.



(1) University Side:

Rank by TOEFL and GRE



(2) Student Side:

Institution Type and Rank



https://www.kaggle.com/datasets/mohansacharya/graduate-admissions



## JOB

Person-fit is the core task in online recruitment platforms [11,
56]. We construct a two-sided market using work experience7
and salary8 as the preferences of recruiters and job hunters.



(1) Recruiter Side:

Work Experience



(2) Worker Side:

Salary



# Drafts


