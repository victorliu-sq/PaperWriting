# Title

FlashSMP:

A stable marriage require cobabitation, atomicMin and Low latency



# Abstract

The Stable Marriage Problem (SMP) is a classical challenge to establish a stable pairing between two groups, traditionally referred to as "men" and "women." Each member of these groups has a ranked preference list for potential partners from the opposite group. The primary objective is to create pairings that are mutually stable, ensuring that no pair of individuals in the resulting arrangement would prefer each other over their assigned partners. The SMP computation has been widely used in various applications, including college admissions, optimizing job scheduling to make efficient use of computing, networking, and storage resources, allocating medical resources, making economic predictions and policy decisions, and many others. The basic SMP computations rely on the Gale-Shapley algorithm, a sequential process that constructs stable pairings iteratively based on the ranked preferences of individuals from both groups. This algorithm is highly time-consuming and data-intensive. While efforts have been made over the years to parallelize the Gale-Shapley algorithm, these attempts have been hindered by two major bottlenecks, namely, frequent data movement operations and atomic operation overhead.   



To address these two challenges, in this paper, we introduce FlashSMP, an efficient parallel SMP algorithm and its implementation on GPU. The high performance of FlashSMP comes from two algorithms development efforts. First, we effectively exploit the data accessing locality with a new data structure to eliminate the "residence separation". Second, FlashSMP does not need global synchronization that is normally supported by machine-dependent atomic operations with high overhead. We call this effort to improve SMP as ``to eliminate communication locks"。 We give a rigorous analysis for the correctness of this synchronization-free and hardware-independent algorithm. With other GPU programming optimization efforts, we show the effectiveness of FlashSMP by intensive experiments, achieving a speedup of over 70 times compared to the Gale-Shapley algorithm. FlashSMP also significantly outperforms  several other existing parallel algorithms. Furthermore, FlashSMP exhibits high scalability, consistently delivering exceptional performance even as the problem size grows significantly.



# Introduction

## Importance

The motivation of the Stable Marriage Problem (SMP), introduced by David Gale and Lloyd Shapley in 1962, is to find a matching between two equally numbered sets of participants with ranked preferences such that no pair of people would prefer each other over their current partners.  



The SMP plays a fundamental role in a wide range of crucial real-world applications, such as matching doctors to hospitals, students to schools, and organ donors to patients. This broad applicability and the profound influence of SMP on these fields, Dr. Alvin Roth and Dr. Shapley received the Nobel Prize in Economics in 2012. 



It has been demonstrated that every instance of the SMP admits at least one stable matching and presented the Deferred Acceptance (DA) algorithm, also known as Gale-Shapely (GS) Algorithm,  which is guaranteed to find such a matching. \cite{gale1962college}



## Why challenge / What problem

However, despite its importance, there has been relatively limited research focused on the development of parallel SMP algorithms, largely due to the inherent complexities associated with this task.

parallelizing SMP computation presents considerable challenges, both in algorithmic design and implementation. 



## Definition of Challenges

SMP is very workload-dependent.

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

in extreme case, 

If preferences lists rank members on the opposite side distinctively, then in a short time, most of men will be paired and most of time only one man will be proposing to women \cite{NationalLabPaper}

In that case, the parallism can only be exploited at first. And the problem will be highly serial problem and it can only be solved by one thread sequentailly. We do not require the synchronization to guarantee the correctness to prevern data racing, Thus any extra synchronization method will only introduce extra overhead.

In this case, CPU will outperform GPU since CPU has lower latency for each single operation due to its over 10 levels of memory hierarchy.



4.



if preference lists divide the members on the opposite side into groups and rank groups in the same way while randomize the people inside each group, which we call the mixed instance, then the number of proposing men will not dramatically decrease to a single man to make peoposal



## Problem w/ Previous Work





## Our Work

1.High-Contention

2.Serial Tailing

3.Locality



## Evaluation

1.Synthesized Data-Hard Instance

2.Synthesized Data-Easy Instance

3.Real Data+Synthesized Data-Mixed Instance





# Experiment

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



