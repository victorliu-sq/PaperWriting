# Abstract

The Stable Marriage Problem (SMP) is a classical challenge to establish a stable pairing between two groups, traditionally referred to as "men" and "women." Each member of these groups has a ranked preference list for potential partners from the opposite group. The primary objective is to create pairings that are mutually stable, ensuring that no pair of individuals in the resulting arrangement would prefer each other over their assigned partners. The SMP computation has been widely used in various applications, including college admissions, optimizing job scheduling to make efficient use of computing, networking, and storage resources, allocating medical resources, making economic predictions and policy decisions, and many others. The basic SMP computations rely on the Gale-Shapley algorithm, a sequential process that constructs stable pairings iteratively based on the ranked preferences of individuals from both groups. This algorithm is highly time-consuming and data-intensive. While efforts have been made over the years to parallelize the Gale-Shapley algorithm, these attempts have been hindered by two major bottlenecks, namely, frequent data movement operations and atomic operation overhead.   

To address these two challenges, in this paper, we introduce FlashSMP, an efficient parallel SMP algorithm and its implementation on GPU. The high performance of FlashSMP comes from two algorithms development efforts. First, we effectively exploit the data accessing locality with a new data structure to eliminate the "residence separation". Second, FlashSMP does not need global synchronization that is normally supported by machine-dependent atomic operations with high overhead. We call this effort to improve SMP as ``to eliminate communication locks"。 We give a rigorous analysis for the correctness of this synchronization-free and hardware-independent algorithm. With other GPU programming optimization efforts, we show the effectiveness of FlashSMP by intensive experiments, achieving a speedup of over 70 times compared to the Gale-Shapley algorithm. FlashSMP also significantly outperforms  several other existing parallel algorithms. Furthermore, FlashSMP exhibits high scalability, consistently delivering exceptional performance even as the problem size grows significantly.



# Introduction

## Importance



## Why challenge / What problem



## Definition of Challenges



## Problem w/ Previous Work



## Our Work



## Evaluation







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



