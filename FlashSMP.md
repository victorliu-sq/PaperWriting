# Title

FlashSMP:

A stable marriage require cobabitation, atomicMin and Low latency



# Abstract

The Stable Marriage Problem (SMP) is a classical challenge to establish a stable pairing between two groups, traditionally referred to as "men" and "women." Each member of these groups has a ranked preference list for potential partners from the opposite group. The primary objective is to create pairings that are mutually stable, ensuring that no pair of individuals in the resulting arrangement would prefer each other over their assigned partners. The SMP computation has been widely used in various applications, including college admissions, optimizing job scheduling to make efficient use of computing, networking, and storage resources, allocating medical resources, making economic predictions and policy decisions, and many others. The basic SMP computations rely on the Gale-Shapley algorithm, a sequential process that constructs stable pairings iteratively based on the ranked preferences of individuals from both groups. This algorithm is highly time-consuming and data-intensive. While efforts have been made over the years to parallelize the Gale-Shapley algorithm, these attempts have been hindered by three major bottlenecks, namely, suboptimal data access patterns, the overhead of atomic operations caused by inefficiencies with atomicCAS, and the restriction of implementation to either CPU or GPU.   



To address these 3 challenges, in this paper, we introduce FlashSMP, an efficient parallel SMP algorithm and its implementation on hybrid environment of GPU and CPU. 



The high performance of FlashSMP comes from 3 algorithms development efforts. First, we effectively exploit the data accessing locality with a new data structure called PRNodes to eliminate the "residence separation". 



Second, FlashSMP employs a more advanced atomic operation called "atomicMin" provided by CUDA to reduce the inefficiencies caused by atomicCAS under high memory contention. We call this effort to improve SMP as "resolve conflicts in communication".



Thirdly, FlashSMP is implemented in a hybrid environment of both GPU and CPU, leveraging the high bandwidth of the GPU and the low latency of the CPU to achieve optimal performance across a wide range of workloads. We refer to this enhancement as "embracing complementary strengths"



Finally, we demonstrate that FlashSMP exhibits high scalability, consistently delivering exceptional performance even as the problem size grows significantly, through extensive experiments using both synthetic and real-world datasets.

Our evaluation results show that FlashSMP significantly outperforms state-of-the-art parallel algorithms, achieving speedups of up to 28.3x across various workloads.



## AI

The stable marriage problem (SMP) is a well-known combinatorial problem with significant practical applications. The parallel McVitie-Wilson algorithm has been the only parallel algorithm that outperforms sequential implementations for SMP, utilizing atomic compare-and-swap (atomicCAS) operations to prevent data races. However, this approach exhibits inefficiencies on GPUs due to high contention. We introduce FlashSMP, a novel algorithm leveraging atomic minimum (atomicMIN) operations, proven mathematically to reduce wasted work under high contention. Unlike its predecessor, FlashSMP employs both CPU and GPU, capitalizing on the high bandwidth of GPUs and low latency of CPUs for optimal performance. Additionally, FlashSMP includes a preprocessing step to eliminate data dependencies, enabling efficient memory access patterns. Our extensive evaluations demonstrate that FlashSMP consistently outperforms the parallel McVitie-Wilson algorithm across all scenarios, establishing it as the new state-of-the-art for SMP.



# Introduction

## Importance

The motivation of the Stable Marriage Problem (SMP), introduced by David Gale and Lloyd Shapley in 1962, is to find a matching between two equally numbered sets of participants with ranked preferences such that no pair of people would prefer each other over their current partners.  



The SMP plays a fundamental role in a wide range of crucial real-world applications, such as matching doctors to hospitals, students to schools, and organ donors to patients. This broad applicability and the profound influence of SMP on these fields, Dr. Alvin Roth and Dr. Shapley received the Nobel Prize in Economics in 2012. 



It has been demonstrated that every instance of the SMP admits at least one stable matching and presented the Deferred Acceptance (DA) algorithm, also known as Gale-Shapely (GS) Algorithm,  which is guaranteed to find such a matching. \cite{gale1962college}



## AI

The stable marriage problem (SMP) has long been a topic of interest in combinatorial optimization, with applications ranging from matching markets to resource allocation. Efficient solutions to SMP are critical, especially as problem sizes grow and computational resources evolve.



## Why challenge / What problem is left over and required handle

However, despite its importance, there has been relatively limited research focused on the development of parallel SMP algorithms, largely due to the inherent complexities associated with this task.

parallelizing SMP computation presents considerable challenges, both in algorithmic design and implementation. 





## AI

While the parallel McVitie-Wilson algorithm has set a benchmark by running faster than sequential solutions, its performance on GPUs is hindered by high contention during atomic operations and its exclusive implementation on either CPUs or GPUs. There is a pressing need for a more efficient algorithm that fully exploits modern heterogeneous computing environments.



## Target

This research aims to address the limitations of the parallel McVitie-Wilson algorithm by developing an algorithm that not only improves GPU performance but also integrates CPU and GPU resources for optimal execution.



## Definition of Challenges

### Draft

Stable Marriage Problem is very workload-dependent.

Differnt workload can have completely distinct properties and that will greatly affect how to defign an effective algorithm and implement it in an efficient way.

1

If preference lists rank members in the exactly the same way as others, then all men will competing for the same woman. 

In this case, we need the synchronization method to make sure a woman will accept the best proposal and all other men will be rejected.

After this proposal, only one man will be paired, and all the failing men will move to the next women. In that case, the number of men making proposal will only decrement one at a time so the parrellism is mostly reserved. And GPU will provide a great paradigm to accelerate the algorithm thanks to the high bandwidth provided by GPU.



2.

However, it is clearly  impossible that in real-world every one will rank the member in the same order. Once we introduce randomness to ranking, the degree of parallism will be affected.

For instance, If all man will propose up to half of distinct woman in the first round of proposal, then half of them will be paired, and the number independent threads will decrease by half.  

Since the parallism drops so quickly, the reason why we use GPU is to utilize its high bandwidth will ecplise and the overhead of synchronization will dominate



3.



in extreme case, If preferences lists rank members on the opposite side distinctively, then in a short time, most of men will be paired and most of time only one man will be proposing to women \cite{NationalLabPaper}

In that case, the parallism can only be exploited at first. And the problem will be highly serial problem and it can only be solved by one thread sequentailly. We do not require the synchronization to guarantee the correctness to prevern data racing, Thus any extra synchronization method will only introduce extra overhead.

In this case, CPU will outperform GPU since CPU has lower latency for each single operation due to its over 10 levels of memory hierarchy.



### AI

The Stable Marriage Problem presents significant challenges when developing algorithms to solve it in parallel due to its workload-dependent nature. Different workloads can exhibit completely distinct properties, significantly affecting the design of an effective algorithm and its efficient implementation.



If preference lists rank members identically, all men will compete for the same woman. In this scenario, synchronization methods are required to ensure a woman accepts the best proposal while rejecting others. After this proposal, only one man will be paired, and the remaining men will move to the next woman. Consequently, the number of men making proposals will only decrement one at a time, thus preserving parallelism. GPUs can accelerate the algorithm due to their high bandwidth.



However, in real-world scenarios, it is unlikely that everyone will rank members identically. Introducing randomness to the rankings affects the degree of parallelism. For instance, if all men propose to up to half of the distinct women in the first round, then half of them will be paired, and the number of independent threads will decrease by half. As parallelism drops rapidly, the benefit of using a GPU for its high bandwidth is overshadowed by the synchronization overhead.



In extreme cases, if preference lists rank members distinctly and oppositely, most men will be paired quickly, and eventually, only one man will be proposing at a time. This situation results in a highly serial problem that can only be solved sequentially by one thread. No synchronization is required to prevent data races, and any additional synchronization methods would introduce unnecessary overhead.



### AI

The key challenges in developing an improved algorithm include:

- **Efficient synchronization**: Reducing contention and wasted work during atomic operations.
- **Heterogeneous execution**: Seamlessly integrating CPU and GPU resources.
- **Data dependency elimination**: Preprocessing data to remove dependencies and improve memory access patterns.
- **Workload adaptation**: Ensuring the algorithm performs well across different scenarios.



## Problem w/ Previous Work

Previous work has showcased the potential of implementing parallel GS algorithm on GPU due to its independent nature at the first round of proposing to improve the efficienty.

In hard instances, they use atomicCAS to guarantee the correctness of algorithm, which can introduce lots of wasted workload and affect the efficiency a lot even scaling to large size of SMP instances.

in easy instances. Their synchronization overhead could dominate and even run slower than CPU implementation.

Therefore, there is still no an universally effective implementation of GS algorithm to solve all kinds of SMP instance due to its nature of distinction. 



## Our Work

In this paper, we present FlashSMP.

The key feature of FlashSMP is its ability to efficiently solve handle all kinds of SMP workloads out of all possilble algorithms.



1.High-Contention

2.Serial Tailing

3.Locality



### AI

To overcome these challenges, we present FlashSMP, an innovative algorithm that:

- Utilizes atomicMIN operations instead of atomicCAS, reducing wasted work under high contention.
- Combines CPU and GPU execution to exploit their respective strengths.
- Incorporates a preprocessing step to eliminate data dependencies, enabling efficient memory access patterns.
- Adapts to different workloads, consistently outperforming the parallel McVitie-Wilson algorithm.



## Contribution

### AI

The main contributions of this paper are:

1. **Algorithm Design**: Introduction of FlashSMP, which utilizes atomicMIN operations and integrates CPU-GPU execution.
2. **Mathematical Proof**: Rigorous proof demonstrating the superiority of atomicMIN over atomicCAS in high-contention scenarios.
3. **Performance Evaluation**: Comprehensive benchmarks showing FlashSMP's superior performance across various scenarios.
4. **Preprocessing Technique**: Development of a preprocessing step to enhance memory access efficiency.



## Evaluation

1.Synthesized Data-Hard Instance

2.Synthesized Data-Easy Instance

3.Real Data+Synthesized Data-Mixed Instance



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



