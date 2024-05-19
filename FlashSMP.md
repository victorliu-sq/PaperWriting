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



## First

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

The remainder of this paper is organized as follows: Section 2 reviews related work and background. Section 3 details the design and implementation of FlashSMP. Section 4 presents our experimental setup and results. Section 5 discusses the implications and potential future work. Finally, Section 6 concludes the paper.



# Experiment

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



