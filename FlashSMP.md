You can insert sentences, deleted sentences and reorder sentences and use other words as long as you think it will make it more readable, logical and native



# Title

FlashSMP:

A stable marriage needs to cohabitate, resolve conflicts, and embrace complementary strengths

A Stable Marriage Needs to have a Shared Residence with Low Contention and to Complement to Each Other



# Abstract

The Stable Marriage Problem (SMP) is a classical challenge to establish a stable pairing between two groups, traditionally referred to as "men" and "women." Each member of these groups has a ranked preference list for potential partners from the opposite group. The primary objective is to create pairings that are mutually stable, ensuring that no pair of individuals in the resulting arrangement would prefer each other over their assigned partners. The SMP computation has been widely used in various applications, including college admissions, optimizing job scheduling to make efficient use of computing, networking, and storage resources, allocating medical resources, making economic predictions and policy decisions, and many others. The basic SMP computations rely on the Gale-Shapley algorithm, a sequential process that constructs stable pairings iteratively based on the ranked preferences of individuals from both groups. This algorithm is highly time-consuming and data-intensive. While efforts have been made over the years to parallelize the Gale-Shapley algorithm, these attempts have been hindered by three major bottlenecks, namely, suboptimal data access patterns, the overhead of atomic operations caused by inefficiencies with atomicCAS, and the restriction of implementation to either CPU or GPU.   



To address these 3 challenges, in this paper, we introduce FlashSMP, an efficient parallel SMP algorithm and its implementation in a hybrid environment of GPU and CPU. 

FlashSMP's high performance stems from three key development efforts. 

First, we effectively exploit the data accessing locality with a new data structure called PRNodes to "cohabitate".

Second, FlashSMP employs a more advanced atomic operation called "atomicMin" provided by CUDA to reduce the inefficiencies caused by atomicCAS under high memory contention, an effort we term "resolving conflicts." 

Thirdly, FlashSMP is implemented in a hybrid environment of both GPU and CPU, leveraging the high bandwidth of the GPU and the low latency of the CPU to achieve optimal performance across a wide range of workloads. We refer to this enhancement as "embrace complementary strengths"



Finally, we demonstrate FlashSMP's high scalability through extensive experiments using both synthetic and real-world datasets, consistently delivering exceptional performance even as the problem size grows significantly. Our evaluation results show that FlashSMP significantly outperforms state-of-the-art parallel algorithms, achieving speedups of up to 28.3x across various workloads.



## Revision

The Stable Marriage Problem (SMP) is a combinatorial optimization problem to establish a stable pairing between two groups, traditionally referred to as "men" and "women", aiming to create pairings that are mutually stable, ensuring that no pair of individuals in the resulting arrangement would prefer each other over their assigned partners. The SMP computation has been widely used in various applications to achieve best resource allocation, matching, and utilization. The basic SMP computations rely on the classical Gale-Shapley algorithm, a sequential process that constructs stable pairings iteratively. This algorithm is highly time-consuming and data intensive, becoming unacceptably slow even for a moderate number of participants in the problem. While efforts have been made over the years to parallelize the Gale-Shapley algorithm, these attempts have been hindered by three major bottlenecks: (1) frequent and expensive data movement, (2) high synchronization overhead, and (3) irregular and workload-dependent parallelisms.

 

To resolve three above mentioned bottlenecks, in this paper, we introduce Balanced-SMP, a highly efficient parallel SMP algorithm and its implementation in a hybrid environment of GPU and CPU. Balanced-SMP’s high performance stems from three key development efforts. First, we effectively exploit the data accessing locality with an effective data structure to maximize the “shared residence” space. Second,  Balanced-SMP employs an advanced hardware atomic operation provided by CUDA to reduce performance degradation caused by memory contention.  Thirdly, Balanced-SMP is implemented in a hybrid environment of both GPU and CPU. It leverages the high bandwidth of the GPU for massive parallel operations and the low latency of CPU for highly sequential execution flows. By complementing the strengths of both CPU and GPU,  our approach achieves optimal performance across a wide range of workloads. We demonstrate Balanced-SMP’s high scalability through extensive experiments using both synthetic and real-world datasets, consistently delivering exceptional performance for increasingly large problem sizes. Our evaluation results show that Balanced-SMP significantly outperforms all existing parallel algorithms, achieving speedups of up to 28.3x across various workloads.



# Introduction

## Importance

The Stable Marriage Problem (SMP), introduced by David Gale and Lloyd Shapley in 1962, seeks to find a stable matching between two equally numbered sets of participants with ranked preferences. In this context, ranked preferences refer to each participant creating a preference list, ordering all members of the opposite set from most to least preferred. A stable matching ensures that no pair of individuals would both prefer each other over their assigned partners. This indicates that, according to their preference lists, no individual has a higher preference for someone other than their assigned partner who would also prefer them in return. Gale and Shapley also introduced the Gale-Shapley (GS) Algorithm, also known as the Deferred Acceptance (DA) algorithm, which guarantees a stable matching for any instance of the SMP. The GS algorithm operates as follows: each man proposes to his most preferred woman, each woman then considers all her proposals and tentatively accepts the one she prefers most, rejecting the others. Rejected men then propose to their next preferred woman, and this process repeats until all men and women are matched.\cite{gale1962college} 



The Stable Marriage Problem (SMP) has been a cornerstone in combinatorial optimization with a wide range of applications. In healthcare, SMP ensures that organ donors are matched to patients \cite{roth2004kidney}, patients to cancer treatment centers, \cite{seidi2024stable} and elderly to healthcare facilities \cite{huang2024application}, optimizing critical resource distribution and enhancing patient care.

The educational sector benefits from SMP by assigning students to schools \cite{abdulkadirouglu2005new, sun2024stable} and allocating rooms \cite{khalili2024roommate} in dormitories, thereby enhancing student satisfaction and meeting institutional requirements.

SMP facilitates mutually beneficial employment relationships by matching  job seekers to employers in the labor market. For instance, the National Resident Matching Program (NRMP) serves more than 50,000 medical students annually seeking their ideal hospital placements \cite{nrmp2023results}.

Additionally, in the field of modern technology, SMP has been widely applied in cloud resource allocation \cite{xu2011egalitarian} and task offloading schemes for computer networks and Internet of Things (IoT) devices \cite{maggs2015algorithmic, wang2016dynamic, muhamad2024energy, pandeeswari2024resource, datta2024esma, alruwaili2024optimizing, yellampalliclient}, as well as in switch scheduling \cite{zhang2017stable}, leading to more efficient network performance and resource utilization. 

The profound impact of SMP across these diverse fields was recognized when Dr. Alvin Roth and Dr. Lloyd Shapley received the Nobel Prize in Economics in 2012.



The SMP has been a cornerstone in combinatorial optimization with applications spanning matching markets, resource allocation, and more. Its fundamental role in real-world applications such as matching doctors to hospitals, students to schools, and organ donors to patients underscores its significance. The profound impact of SMP on these fields was recognized when Dr. Alvin Roth and Dr. Lloyd Shapley received the Nobel Prize in Economics in 2012.



labor market, 

\cite{aziz2024cutoff}



resource assignment in computer networks

task offloading scheme in IoT devices (cellular devices) to fog nodes only

\cite{xu2011egalitarian, maggs2015algorithmic, wang2016dynamic, muhamad2024energy, pandeeswari2024resource, zhang2017stable, datta2024esma, yellampalliclient}



room allocation in dormitories

\cite{khalili2024roommate}



switch scheduling 

\cite{zhang2017stable}



Doctor2hospital

\cite{nrmp2023results}



students2school

\cite{abdulkadirouglu2005new, sun2024stable}



organ donors to patients

\cite{roth2004kidney}



patients2cancerTreatmentCenter

\cite{seidi2024stable}



elderly to healthcare facilities

\cite{huang2024application}



## Shortcoming of previous work

Efficient algorithms for Stable Marriage Problems (SMP) are critical as problem sizes grow and computational resources evolve. 

The recognition of the importance of SMP has exposed the limitations of the classical GS algorithm.  Despite its foundational role, the GS algorithm is both computing- and data-intensive, with time and memory complexities that grow quadratically with the number of participants. This makes it impractical for real-time or large-scale scenarios \cite{lu2003parallel, wynn2024selection}.  As a result, efficient algorithms for SMP are becoming increasingly critical to handle the growing volume of participants \cite{nrmp2023results}, the need for centralized resource allocation \cite{ashlagi2021kidney}, and the frequent recalculations due to the dynamic nature of environments \cite{maggs2015algorithmic}. 



Lots of efforts have been made to solve SMP in a shorter time using parallelism.



Many methods have aimed to solve SMP in a shorter time.



These methods range from   to CPU / GPU paralllization,

Although these methods  

These methods range from sparse-approximation [51, 74] to low-rank approximation [12, 50, 84],
and their combinations [3, 9, 92]. Although these methods reduce the compute requirements to linear or
near-linear in sequence length, many of them do not display wall-clock speedup against standard attention
and have not gained wide adoption. One main reason is that they focus on FLOP reduction (which may not
correlate with wall-clock speed) and tend to ignore overheads from memory access (IO).





These methods range from theoretical parallel modeling like CRCW PRAM to newly resing advanced parallel architectures like multicore processors and GPUs. 



With the rise of advanced parallel architectures like multicore processors and GPUs, exploiting the parallelism of SMP algorithms has become both inevitable and imperative.



massively parallel processing for TED is not only necessary but imperative. This inevitable shift enables us to effectively address the challenges posed by the ever-increasing volumes of data and the growing need for fast response time in TED computations. Therefore, it is critical to explore a parallel framework that is both efficient and feasible for TED algorithms.



This rise in increasingly high demands in both data processing and computation, along with the fluidity of participants' preferences, underscores the necessity for parallelizing algorithms to ensure stable matches are recalculated efficiently and effectively.



Despite its importance, research on parallel SMP algorithms has been limited due to the inherent complexities of this task.

The classic GS algorithm is slow.

that GS algorithm is computing- and data-intensive since it requires time and memory complexity quadratic in the number of participants.



To our knowledge, the only parallel algorithm that outperforms the sequential Gale-Shapley (GS) algorithm is the parallel McVitie-Wilson algorithm. While this algorithm has set a benchmark by running faster than sequential solutions, its performance on GPUs is hindered by high contention for shared resources and high-latency memory operations, making it even less efficient than its CPU implementation. 



## Challenges of Massive Parallelism

The most challenging aspect of computing SMP arises from the inherent computational and data-intensive nature of the GS algorithm. Its time and space complexities increase quadratically with the number of participants. As a result, when the input size reaches to a certain threshold, centralized computational resources for processing and storing preferences and matchings become quickly overwhelmed. Thus, parallel processing or hardware acceleration is required and necessary in practice. 



However, there are several reasons why parallelizing GS algorithm is challenging. 



First, if multiple men propose to the same woman simultaneously in a parallel environment, conflicts can arise. Ensuring that a woman can efficiently process and respond to multiple proposals in parallel is non-trivial. This issue is compounded by the need for numerous synchronization points to handle updates to the matching state, introducing significant overhead and reducing the potential benefits of parallelism.



Second, the GS algorithm involves a series of proposals and rejections that are inherently sequential. Each man proposes to a woman, who then tentatively accepts, or rejects based on her current best offer. This process depends on the outcome of previous steps, making it difficult to execute multiple proposals simultaneously without conflicts.  





Additionally, the GS algorithm frequently accesses and updates data structures, such as preference lists, rank matrix and current matches. This frequent data movement poses a bottleneck, highlighting the importance of optimizing data access locality to improve overall performance.



### Unused Content

Third, the execution of GS algorithm needs to deal with uneven work distribution. The amount of work done by different parts of the algorithm can vary significantly. For example, some participants can resolve their matches quickly, while others might take many iterations. A load balancing effort in parallel processing is another concern for this algorithm. 



## Shortcoming of Previous Work

Research on parallel algorithms for the Stable Marriage Problem (SMP) has attempted to address these issues, but has not been very effective because it only partially targets the problems. To our knowledge, the only parallel algorithms that outperform the sequential GS algorithm are the parallel Gale-Shapley algorithm and the parallel McVitie-Wilson algorithm. While these algorithms have set benchmarks by resolving load balancing issues and eliminating many synchronization points, they are primarily implemented on CPUs. Their performance on GPUs is hindered by high contention for shared resources and high-latency memory operations, making them less efficient than their CPU implementations. Moreover, none of these works have addressed the issue of inefficient memory access patterns, leaving room for further acceleration.



Currently,  two critical questions remain unanswered:

1. **Is it possible to enhance the real-time performance of the Gale-Shapley algorithm in addressing the Stable Marriage Problem through the optimization of data movement patterns**
2. **Can GPUs be leveraged to revolutionize the speed and scalability of solving the SMP through a parallel framework?**



## Our Work

In this paper, we introduce Balanced-SMP, an innovative parallel framework that addresses these two questions as follows:

Firstly, we discovered a crucial relationship between the recipient index and the rank of the proposer in the recipient's preference list. This insight enabled us to implement a preprocessing step that eliminates data dependencies, allowing related data to be accessed together. This preprocessing step laid the foundation for a new data structure and sequential algorithm designed to fully exploit spatial locality, efficiently handle memory access patterns, and reduce latency.

Building on this new sequential algorithm, we then parallelized it to take advantage of modern hardware capabilities. By utilizing atomicMIN, a hardware primitive introduced by CUDA, we significantly reduced the number of atomic operations under high memory contention, enhancing synchronization efficiency. The parallelization process involved adapting the sequential algorithm to effectively use atomic operations while minimizing contention, ensuring robust performance in a parallel computing environment.

Next, we integrated the parallelized algorithm into a unified framework, creating Balanced-SMP. This involved seamlessly combining CPU and GPU resources to maximize their complementary strengths. The GPU's high bandwidth is leveraged for parallel proposals when there are many active threads, while the CPU's low latency is utilized for fast proposals when there is only a single active thread. This strategic integration ensures the algorithm remains efficient regardless of workload size or distribution, taking full advantage of both CPU and GPU capabilities.

Finally, our evaluation results demonstrate that Balanced-SMP adapts effectively to different workloads, providing consistent and optimal performance across diverse scenarios.



## Contribution

Specifically, we make the following contributions:

1.We developed a new sequential algorithm for SMP that expolits data locality using innovative data structure called PRNode. By incorporating a preprocessing step to initialize these PRNodes, we ensure that all necessary rank information is immediately accessible within the same PRNode during proposals. This significantly enhances the real-time performance of the new sequential algorithm by reducing its reliance on global memory access.



2.We parallelized the new sequential algorithm to leverage modern hardware capabilities, significantly reducing the number of atomic operations under high memory contention by utilizing atomicMIN, a hardware primitive introduced by CUDA. This adaptation enhances synchronization efficiency and ensures robust performance in high-contention scenarios.



3.Building on this, we introduce a novel framework named Balanced-SMP for the parallel computation of SMP. This framework seamlessly integrates CPU and GPU resources to maximize their complementary strengths. The integration of CPU and GPU ensures efficient performance in a heterogeneous environment, regardless of workload distribution.



4.Through exhaustive testing in diverse scenarios, we have proven Balanced-SMP's capacity to deliver consistent and optimal performance regardless of the workload. Our extensive experimental evaluations demonstrate that Balanced-SMP consistently outperforms state-of-the-art parallel algorithms by 2.4x to 28.3x across a wide range of workloads. These results highlight the framework's exceptional efficiency and its robust ability to adapt to different types of computational demands.



## Paper Structure

The remainder of this paper is organized as follows: 

Section 2 provides background information on the Stable Marriage Problem (SMP) and the Gale-Shapley (GS) algorithm.

Section 3 discusses the development of our new sequential algorithm for SMP, focusing on its use of the PRNode data structure to improve data locality and optimize memory access patterns.

Section 4 details the design and implementation of the parallel framework Balanced-SMP. This section also includes a rigorous mathematical proof demonstrating the superiority of atomicMIN in high-contention scenarios and highlights the complementary strengths of CPUs and GPUs, supported by our experimental benchmarks.

Section 5 presents our experimental setup and results, offering a comprehensive evaluation of Balanced-SMP's performance and highlighting its efficiency and adaptability across various workloads.

Section 6 reviews related work, including existing serial and parallel algorithms for SMP.

Finally, Section 7 concludes the paper, summarizing our findings and suggesting potential directions for future research.



## Unused

Most of the existing work is primarily of theoretical interest and typically requires between $O(n^2)$ to $O(n^4)$ processors, rendering real-world implementation impractical.



# Section2-Background

## SMP

```
The Stable Marriage Problem (SMP) involves two groups of participants, often referred to as men and women. Each participant has a ranked preference list of all members from the opposite group. In Figure 1, the two groups are \(\{M_1, M_2, M_3\}\) and \(\{W_1, W_2, W_3\}\). Each member in \(\{M_1, M_2, M_3\}\) ranks all members in \(\{W_1, W_2, W_3\}\) in a strict order, and vice versa. For example, \(M_1\) ranks \(W_2\) first, \(W_1\) second, and \(W_3\) third. This means \(M_1\) prefers \(W_2\) the most, \(W_1\) next, and \(W_3\) the least.

```



```
Given these two groups, a matching is a one-to-one correspondence from participants in one group to those in the other. A blocking pair for a given matching is a pair of participants from opposite groups who would both prefer each other over their current partners. If such a pair exists, the matching is unstable because these two participants would be motivated to leave their assigned partners and pair up with each other instead. The goal of the SMP is to find a stable matching, where no blocking pairs exist. In other words, a matching is stable if no two participants prefer each other over their current partners.
```



![FlashSMP-PrefList-5](/Users/jiaxinliu/Desktop/FlashSMPEvaluation/Figures/FlashSMP-PrefList-5.jpg)



To illustrate a stable matching, consider the example in Figure 1:

M1 is matched with W3, M2 is matched with W2, and M3 is matched with W1. 

The corresponding matching have been underscore by the blue staright underlines.

To check if this matching is stable, we need to ensure there are no blocking pairs. 

M1 is matched with W3. M1 prefers W2 over W3; however, W2 is matched with M2 and prefers M2 over M1. Therefore, W2 does not prefer M1 over her current partner. Additionally, M1 prefers W1 over W3, but W1 is matched with M3 and prefers M3 over M1. Thus, W1 does not prefer M1 over her current partner.

M2 is matched with W2, his top choice, and W2 is also matched with M2, her top choice. Therefore, there is no issue with this pairing.

M3 is matched with W1. M3 prefers W2 over W1; however, W2 is matched with M2 and prefers M2 over M3. Therefore, W2 does not prefer M3 over her current partner. M3 also prefers W1, and W1 is matched with M3, her top choice. Therefore, there is no issue with this pairing.



To illustrate instability, consider a different matching: M1 is matched with W2, M2 is matched with W1, and M3 is matched with W3.  The corresponding matching have been underscore by the pink staright underlines.

In this case, both M2 and W2,  M3 and W1 form a blocking pair because they both prefer each other over their current partners.

The corresponding matching have been underscore by the pink waving underlines.

Therefore, this matching is unstable due to the presence of a blocking pair.



To check if this matching is unstable, we examine all potential blocking pairs:

M2 prefers W2 over W1. W2, who is matched with M1, prefers M2 over M1. Therefore, M2 and W2 form a blocking pair because they both prefer each other over their current partners.

M3 prefers W2 over W3, but W2 prefers M1 over M3 and is matched with M1. Therefore, M3 and W2 do not form a blocking pair.

M3 also prefers W1 over W3. W1, who is matched with M2, prefers M3 over M2. Therefore, M3 and W1 form a blocking pair because they both prefer each other over their current partners.



M1 is matched with W2, but he prefers W1 over W2. W1, who is matched with M2, prefers M1 over M2. Thus, M1 and W1 form a blocking pair because they both prefer each other over their current partners.



```
To illustrate a stable matching, consider the example in Figure 1: \(M_1\) is matched with \(W_3\), \(M_2\) is matched with \(W_2\), and \(M_3\) is matched with \(W_1\). These matches are indicated by blue straight underlines.

To check if this matching is stable, we need to ensure there are no blocking pairs. \(M_1\) is matched with \(W_3\). Although \(M_1\) prefers \(W_2\) over \(W_3\), \(W_2\) is matched with \(M_2\) and prefers \(M_2\) over \(M_1\). Similarly, \(M_1\) prefers \(W_1\) over \(W_3\), but \(W_1\) is matched with \(M_3\) and prefers \(M_3\) over \(M_1\). Therefore, there are no blocking pairs involving \(M_1\).

\(M_2\) is matched with \(W_2\), his top choice, and \(W_2\) is also matched with \(M_2\), her top choice. There is no issue with this pairing.

\(M_3\) is matched with \(W_1\). Although \(M_3\) prefers \(W_2\) over \(W_1\), \(W_2\) is matched with \(M_2\) and prefers \(M_2\) over \(M_3\). Additionally, \(M_3\) prefers \(W_1\), and \(W_1\) is matched with \(M_3\), her top choice. Therefore, there are no blocking pairs involving \(M_3\).

Consider an example of an unstable matching with blocking pairs in Figure 1: \(M_1\) is matched with \(W_2\), \(M_2\) is matched with \(W_1\), and \(M_3\) is matched with \(W_3\). These matches are indicated by pink straight underlines. In this case, \(M_2\) prefers \(W_2\) over \(W_1\). Similarly, \(W_2\), who is matched with \(M_1\), prefers \(M_2\) over \(M_1\). Additionally, \(M_3\) prefers \(W_1\) over \(W_3\), and \(W_1\), who is matched with \(M_2\), prefers \(M_3\) over \(M_2\). As a result, \(M_2\) and \(W_2\), as well as \(M_3\) and \(W_1\), form blocking pairs because they prefer each other over their current partners. These blocking pairs are marked with pink wavy underlines, indicating that this matching is unstable.
```

 



## GS

### The Generic Procedure

```
//
The Gale-Shapley (GS) algorithm, also known as the Deferred Acceptance algorithm, is a foundational method for solving the Stable Marriage Problem (SMP). Proposed by David Gale and Lloyd Shapley in 1962, the GS algorithm guarantees finding a stable matching between two equally sized sets of participants, typically referred to as men and women, each with their own preference lists.

//
The algorithm operates in iterative rounds consisting of a proposal phase and an acceptance phase. Initially, all participants are free (unmatched). During the proposal phase, each free man proposes to the highest-ranked woman on his preference list who has not yet rejected him. In the acceptance phase, each woman receiving one or more proposals chooses the man she prefers the most among the proposers and tentatively accepts his proposal, rejecting all others. This proposal and acceptance cycle repeats until there are no more free men.

//
Consider the preference lists in Figure 1 to understand the execution of the Gale-Shapley algorithm:

At the start, all participants are free. In the first iteration, \(M_1\) proposes to \(W_2\), the highest-ranked womanon on his list. \(W_2\) tentatively accepts, resulting in the tentative match \((M_1, W_2)\). Next, \(M_2\) proposes to \(W_2\). Since \(W_2\) prefers \(M_2\) over \(M_1\), she accepts \(M_2\)'s proposal and rejects \(M_1\). The tentative match is now \((M_2, W_2)\). Then, \(M_3\) proposes to \(W_2\), but \(W_2\) prefers \(M_2\) over \(M_3\), so she rejects \(M_3\). The tentative match remains \((M_2, W_2)\).

Now free again, \(M_1\) proposes to \(W_1\), the next highest-ranked woman who has yet to reject him. \(W_1\) tentatively accepts, resulting in the match \((M_1, W_1)\) alongside \((M_2, W_2)\). Subsequently, \(M_3\) proposes to \(W_1\). Since \(W_1\) prefers \(M_3\) over \(M_1\), she accepts \(M_3\)'s proposal and rejects \(M_1\). The tentative matches are now \((M_3, W_1)\) and \((M_2, W_2)\).

Once more free, \(M_1\) proposes to \(W_3\), the next available woman on his list. \(W_3\) tentatively accepts \(M_1\)'s proposal, resulting in the tentative match \((M_1, W_3)\) alongside \((M_3, W_1)\) and \((M_2, W_2)\).

Now every participant has been matched, so the algorithm terminates with the following stable matching: \(M_1\) is paired with \(W_3\), \(M_2\) with \(W_2\), and \(M_3\) with \(W_1\). In this matching, there are no blocking pairs because no two individuals prefer each other over their current partners, ensuring that the matching is stable.
```



```
It's also important to note that the solution provided by the GS algorithm is man-optimal. This means that, in this stable matching, no man has a better possible partner than his current one among all potential stable matchings in the instance of the SMP.
```



### The detailed Implementation

Algorithm Gale-Shapley Algorithm

Input: n x n 2D arrays ManPref and WomanPref // preference lists for 

Output: A stable matching S

for man m = 1 ... n do

​	for rank r = 1 ... n do

​		ManRank[m ,ManPref[m, r]] = r // initialize men's rank matrix



for woman w = 1 ... n do

​	for rank r = 1 ... n do

​		WomanRank[w ,WomanPref[w, r]] = r / initialize women's rank matrix



FreeManQueue = [1 ... n] // At first, all men are free

for i = 1 ... n do

​	Next[i] = 1 // The rank of the best unproposed woman for every man is initialized to 1

​	PartnerRank[i] = n + 1 // All woman have not paired, initialize their partner rank to n + 1



while Not FreeManQueue.Empty() do

​	m = FreeManQueue.Pop()

​	w_rank = Next[m]

​	w = ManPref[m, w_rank]

​	m_rank  = WomanRank[w, m]

​	c_rank = PartnerRank[w_idx]

​	if  c_rank == n+1 do

​		PartnerRank[m] = m_rank

​	else 

​		if c_rank < m_rank do

​			FreeManQueue.push(m)		

​		else

​			Current[m] = m_rank

​			FreeManQueue.push(WomenPref[w, c_rank])

​	Next[m]+=1



for w = 1 ... n do

​	S[w] = WomenPref[w, PartnerRank[w]]

return S



```
The implementation details of the GS algorithm are described in Algorithm 1.

The algorithm begins by initializing one matrix, \( \text{WomanRank} \), which represents the rank of each man in the preference lists of women. For each man, the algorithm assigns ranks to all women according to his preference list. This matrix, referred to as \( \text{RankMatrix} \), is crucial because it provides a quick way to determine the preference order of any individual in constant time.

Initially, all men are free, and a queue called \( \text{FreeManQueue} \) is created to keep track of them. Each man starts with the first woman on his preference list as the next woman to propose to. The \( \text{Next} \) array stores the index of the next woman each man will propose to. By incrementing the index in the \( \text{Next} \) array after each proposal, the algorithm ensures that each man sequentially proposes to women in his preference list without rechecking previously rejected proposals.

\( \text{PartnerRank} \) is an array that stores the rank of the current partner of each woman. At the start, the partner rank for each woman is set to \( n+1 \), indicating that they are all currently unmatched. 

The main loop of the algorithm runs until there are no free men left in the queue. Within this loop, a man \( m \) is taken from the queue to propose to the next woman on his preference list. The algorithm checks the rank of this man in the woman’s preference list and compares it with the rank of her current partner (if she has one).

If the woman is free (i.e., her partner rank is \( n+1 \)), she accepts the proposal, and her partner rank is updated to reflect this new match. If she is already matched, the algorithm compares the ranks: if the current partner has a higher preference (lower rank) than the proposing man, the proposing man remains free and is added back to the queue. If the proposing man has a higher preference, the woman accepts his proposal, and her previous partner becomes free and is added back to the queue.

Once the main loop finishes, the algorithm constructs the final stable matching list \( S \) by pairing each woman with her final partner according to the \( \text{PartnerRank} \) list. The initialization of the \( \text{RankMatrix} \) and the proposal process, both having \( O(n^2) \) complexity, ensure that the overall time complexity of the algorithm is \( O(n^2) \).
```



```
\begin{algorithm}
\caption{Gale-Shapley Algorithm}
\label{GSAlgo}
\begin{algorithmic}[1]

\newcommand{\StateNoLine}[1]{\Statex \hspace*{-\algorithmicindent} #1}
\newcommand{\CommentNoLine}[1]{\hfill \(\triangleright\) #1}

\StateNoLine{\textbf{Input:}  $ManPref$ and $WomanPref$} \CommentNoLine{preference lists}
\StateNoLine{\textbf{Output:} A stable matching $S$}

\For{$w = 1$ to $n$} \CommentNoLine{initialize rank matrix}
    \For{$r = 1$ to $n$}
        \State $m \gets WomanPref[w, r]$
        \State $WomanRank[w, m] \gets r$ 
    \EndFor
\EndFor

\State $FreeManQueue \gets [1, 2, \ldots, n]$ %\CommentNoLine{all men are free}
\For{$i = 1$ to $n$}
    \State $Next[i] \gets 1$
    % \State \CommentNoLine{the rank of next woman to propose is 1}
    \State $PartnerRank[i] \gets n + 1$ 
    % \CommentNoLine{all women are unpaired}
\EndFor

\vspace{1\baselineskip}  % Add vertical space here

\While{not $FreeManQueue$.Empty()} \CommentNoLine{Main Loop}
    \State $m \gets FreeManQueue$.Pop() 
    
    \State $w\_rank \gets Next[m]$
    \StateNoLine \CommentNoLine{Get the rank of the next woman to propose to}
    
    \State $w \gets ManPref[m, w\_rank]$
    % \StateNoLine \CommentNoLine{Get the actual woman to propose to}
    
    \State $m\_rank \gets WomanRank[w, m]$
    \StateNoLine \CommentNoLine{Get the rank of the man for the woman}
    
    \State $p\_rank \gets PartnerRank[w\_idx]$
    % \StateNoLine \CommentNoLine{Get the rank of the current partner of the woman}
    
    \If{$p\_rank == n + 1$}
        \State $PartnerRank[m] \gets m\_rank$
    \Else
        \If{$p\_rank < m\_rank$}
            \State $FreeManQueue$.Push($m$) \CommentNoLine{$m$ remains free}
        \Else
            \State $Current[m] \gets m\_rank$
            \State $p \gets WomenPref[w, p\_rank]$
            \State $FreeManQueue$.Push($p$) 
            \StateNoLine \CommentNoLine{Previous partner $p$ becomes free}
        \EndIf
    \EndIf
    \State $Next[m] \gets Next[m] + 1$ % \CommentNoLine{Move to the next woman}
\EndWhile

\vspace{1\baselineskip}  % Add vertical space here

\For{$w = 1$ to $n$}
    \State $S[w] \gets WomenPref[w, PartnerRank[w]]$ 
    \StateNoLine \CommentNoLine{Create the final matching list}
\EndFor

\State \Return $S$

\end{algorithmic}
\end{algorithm}
```



## Unused

In conclusion, a matching in the context of SMP is stable if and only if there are no blocking pairs. The Gale-Shapley algorithm ensures that a stable matching is always found, thus addressing the issue of instability in matchings by systematically eliminating blocking pairs through its proposal and acceptance phases. This guarantees that the final matching is stable, demonstrating the robustness and efficiency of the algorithm in solving the Stable Marriage Problem.



The Gale-Shapley algorithm ensures that such a stable matching is always found, demonstrating its robustness and efficiency in solving the Stable Marriage Problem. The properties of the Gale-Shapley algorithm include guaranteed stability, male-optimality, and polynomial time complexity (O(n^2)), making it efficient for practical use. The algorithm has widespread applications beyond the traditional SMP, including college admissions, job placements, and organ donation matching, highlighting its importance in various domains requiring stable matchings.




The GS Algorithm

```
\begin{algorithm}
\caption{The Gale-Shapley Algorithm}
\label{GS}
\begin{algorithmic}[1]
% \State \textbf{Input:}
% \State Set of men $M = \{m_1, m_2, \ldots, m_n\}$
% \State Set of women $W = \{w_1, w_2, \ldots, w_n\}$V
% \State \textbf{Initialize:}

\State $Q \gets M$

\While{$Q \neq \emptyset$}
    \State $m \gets Q.dequeue()$
    \State $w \gets getMostPreferredUnproposedWoman(m)$
    \State $m' \gets getPartner(w)$
    \If{$m' \neq NULL$}
        \If{$m \succ_{w} m'$}
            \State $Q.enqueue(m')$
            \State $setPartner(w, m)$
        \Else
            \State $Q.enqueue(m)$
        \EndIf
    \Else
        \State $setPartner(w, m)$
    \EndIf
\EndWhile
\end{algorithmic}
\end{algorithm}
```



**Mcvitie-Wilson**

The algorithm proposed by McVitie and Wilson[10] is based on the Gale-Shapley algorithm, together with the observation that the order in which the suitors propose does not change the set of matched vertice.

The key difference between the Gale-Shapley and McVitie-Wilson algorithms is in how they handle proposals.The Gale-Shapley algorithm selects a free man from the queue and makes proposals on his behalf until he is matched.In contrast, the McVitie-Wilson algorithm also selects a free man from the queue. If he proposes to a woman who is already paired, the rejected man then makes proposals. This process continues until a man proposes to an unpaired woman, ensuring no man is left unmatched.

Consider the preference lists in Figure 1. The execution of the Mcvitie-Wilson algorithm proceeds as follows:

Initially, M1 proposes to W2. W2 tentatively accepts M1's proposal, forming the initial pair (M1, W2). Since no man has been rejected yet, the algorithm proceeds to the next free man, M2.

M2 then proposes to W2. W2 prefers M2 over M1, so she accepts M2's proposal and rejects M1. The new pairing is (M2, W2). Now free again, M1 proposes to W1. W1 tentatively accepts M1, resulting in the pairs (M1, W1) and (M2, W2). The algorithm then moves on to the next free man, M3.

M3 proposes to W2, but W2 prefers M2, so she rejects M3. M3 then proposes to W1. W1 prefers M3 over M1, so she accepts M3's proposal and rejects M1. The pairs are now (M3, W1) and (M2, W2). M1, now free, proposes to W3, who tentatively accepts. The final pairs are (M1, W3), (M3, W1), and (M2, W2).

This results in a stable matching identical to the man-optimal stable marriage produced by the Gale-Shapley algorithm.





# Section-The bottlenecks in GS Computation

In this section, we first provide an in-depth look at the implementation of the GS algorithm, analyze its inefficient memory access patterns, and identify the bottlenecks caused by frequent and costly data movements.



## Data Movements

The GS algorithm is memory-intensive because it requires frequent and repeated accesses to the men's preference lists ($MenPref$), the women's rank matrix ($WomanRank$), and the next array ($Next$). As shown in Algorithm 1, each proposal involves minimal computation but requires a man to access the $Next$ array on line 14 to find the rank of the best woman who has not yet rejected him, and the $WomanRank$ matrix on line 16 to determine his rank in the woman's preference list. This makes memory access the primary bottleneck.

Figure 2 shows the access patterns of the men's preference lists and the women's rank matrix. The access pattern for the men's preference lists can be optimized by using an additional while-loop to allow the proposer to immediately propose to the next woman instead of being pushed back into the queue on line 18.

However, optimizing memory access patterns of women's rank matrix remains challenging. The $WomanRank$ matrix is accessed in a non-linear order because the IDs of the men proposing and the women being proposed to are dynamically determined. Even with optimized access patterns for the men's preference lists, the randomization of the proposed women's IDs results in non-sequential accesses to the $WomanRank$ matrix. When the number of participants (n) is very large, this non-sequential nature of access causes significant memory jumps, disrupting efficient caching and prefetching mechanisms. These scattered and unpredictable accesses lead to poor memory usage and slower access times.

To illustrate the importance of optimizing memory access, we tested the GS algorithm across diverse workloads to measure the impact of memory accesses to the $WomanRank$ matrix and the $Next$ array. As shown in Figure 3, the combined time to access the $WomanRank$ matrix to get a man's rank in a woman's preference list and the $Next$ array to get the rank of the next woman to propose to accounts for over 50% of the total execution time in all workloads. (The specific details of these workloads will be explained in Section 6; for now, just note this fact.)





### Uesless Content

Clearly, a sequential algorithm that initializes rank matrix runs in O(n^2) time, where n is the number of participants. The Rank Matrix is designed such that each entry 𝑅[𝑖][𝑗]*R*[*i*][*j*] represents the rank of man 𝑀𝑖*M**i* in woman 𝑊𝑗*W**j*'s preference list.

Thanks to Rank matrix, reduces the complexity of rank retrieval to O(1) time. As GS algorithm is described before, for each iteration, preference list and rank matrix will be access in a constant times, O(1), thus resulting in time O(1) for each iteration. 

Furthermore, it has been proven the number of proposals for an SMP instance is O(n^2). And each proposal takes O(1) time, thus the total execution time of GS algorithm takes O(n^2) to precompute rank matrix and O(n^2) to make proposals.

In contrast, the preference lists of men are accessed sequentially because each man makes proposals from his highest preference to his lowest. However, the irregular access patterns of the Rank Matrix can significantly impact overall performance due to frequent cache misses.



According to section 2, the acceptance phase of GS algorithm requires determining the rank of each man in the preference list of the proposed woman. An efficient approach is to utilize a precomputed data structure, called Rank Matrix, that allows for O(1) time complexity in retrieving these ranks. 

To illustrate how the Rank Matrix works, consider rank matrices in Figure1, which are built upon prefereneces lists in Figure2:

Constructing the Rank Matrix involves preprocessing each woman's preference list.

The rank matrix for men should indicate the rank each man assigns to each woman and We scan the preference list of each woman from rank 1(highest) to rank 3(lowest)   For example, M1's row in the matrix has (M1, W1) as rank 2 because W1 is his second preference, (M1, W2) as rank 1 because W2 is his first preference, and (M1, W3) as rank 3 because W3 is his third preference. You can determine other entries in the rank matrix from the corresponding preference lists using the same method.

Similarly, for women, W1's row in the matrix has (W1, M1) as rank 3 because M1 is her third preference, (W1, M2) as rank 2 because M2 is her second preference, and (W1, M3) as rank 1 because M3 is her first preference. The same method can be used to determine the other entries in the women's rank matrix from their preference lists.



For instance, if M1 starts by proposing to W2, he will refer to RankMatrixWoman(W2, M1) to determine his rank, which is 1. Following his rejection by W2, M1 will then approach W1 and look up RankMatrixWoman(W1, M1) to find his rank, which is 3. Upon being turned down by W1, M1 will move on to W3 and consult RankMatrixWoman(W3, M1), where his rank is recorded as 2.





For instance, if M1 starts by proposing to W2, he will refer to RankMatrixWoman(W2, M1) to determine his rank, which is 1. Following his rejection by W2, M1 will then approach W1 and look up RankMatrixWoman(W1, M1) to find his rank, which is 3. Upon being turned down by W1, M1 will move on to W3 and consult RankMatrixWoman(W3, M1), where his rank is recorded as 2.

The access patterns of M1, M2, and M3 are shown in Figure 2.



For example, in a scenario with tens of thousands of participants, M1 may first propose to W200, then to W31020, and finally to W1780, resulting in accesses to RankMatrixWoman(W200, M1), RankMatrixWoman(W31020, M1), and RankMatrixWoman(W1780, M1).



## Synchronization Issues

The GS algorithm naturally lends itself to parallelization because multiple men can propose simultaneously.

In a multi-core system or GPU, we can assign each thread to represent one man, allowing each man to make his proposal independently. When several men propose to the same woman at the same time, they can read her current partner's rank without synchronization. However, updating the suitor's value must be done in a way that prevents other threads from changing the value simultaneously, to avoid data races if one of the men is indeed a better partner.

Specifically, in Algorithm 1, the operation on line 17 can be executed without synchronization, but the operation on line 21 requires synchronization to ensure that the woman accepts the best proposal.

In parallelizing the GS algorithm, certain common synchronization methods are not suitable due to their inherent shortcomings. Here, we discuss three such methods: Locks, Barrier Synchronization, and Atomic Compare-And-Swap (AtomicCAS).

### Lock

One way to mitigate data racing is to lock the threads before updating, one per woman to ensure that each thread gets exclusive access to this critical section. However, locks can significantly slow down the algorithm because of the overhead associated with acquiring and releasing them. In a highly concurrent environment, this overhead can become a bottleneck. The GS algorithm requires frequent and fine-grained updates to the partner status of participants. Since locks are coarse-grained, they are inefficient for such frequent updates and can cause excessive waiting times for threads. Therefore, locks are too heavy-weight and inefficient for the frequent and fine-grained synchronization required in the GS algorithm.The performance overhead make locks unsuitable for this parallelization.



### Barrier Synchronization

Barrier synchronization is a method where all threads must reach a specific point before any can proceed.

When parallelizing the GS algorithm, one straightforward approach is to make all threads wait at a barrier, allowing each woman to accept the best proposal and reject the rest before letting all threads proceed.

However, due to the dynamic nature of the GS algorithm, this method has limitations. Some men may get rejected and not participate in the updating process, while others may be accepted without any competition, making synchronization unnecessary for them.

As a result, some threads may complete their tasks sooner and have to wait at the barrier, which does not align well with the static checkpoints of barrier synchronization. This leads to idle time and poor resource utilization.

Thus, barrier synchronization is too rigid and introduces significant delays, especially in the dynamic and continuous operation environment of the GS algorithm. The synchronization points force threads to wait unnecessarily, negating the benefits of parallelization.



### AtomicCAS


The atomicCAS (Compare-And-Swap) operation is an atomic instruction used to compare a memory location's current value with a given expected value and, if they match, swap it with a new value. Otherwise, the operation fails and returns the old value, indicating the update was unsuccessful. This logic is performed atomically, ensuring no other thread can interfere during the comparison and swap.

Using atomicCAS, multiple threads can update the partnerRank correctly to parallelize the GS algorithm. Algorithm 2 is a parallel version of lines 21-26 from Algorithm 1.

```
while (p_rank > m_rank) {
	p_rank2 = atomicCAS(&partnerRank, p_rank, m_rank)
	if (p_rank2 == p_rank) {
		if (p_rank != n + 1) {
			p <- WomenPref[w, p_rank]
			FreeManQueue.Push(p)
		}
		p_rank = m_rank
	} else {
		p_rank = p_rank2
	}
}
```



```
\begin{algorithm}
\caption{Parallel Procedure to Update PartnerRank Using atomicCAS}
\begin{algorithmic}[1]
\While{(p\_rank > m\_rank)}
    \State p\_rank2 = atomicCAS(\&partnerRank, p\_rank, m\_rank)
    \If{(p\_rank2 == p\_rank)}
        \If{(p\_rank != n + 1)}
            \State p $\gets$ WomenPref[w, p\_rank]
            \State FreeManQueue.Push(p)
        \EndIf
        \State p\_rank = m\_rank
    \Else
        \State p\_rank = p\_rank2
    \EndIf
\EndWhile
\end{algorithmic}
\end{algorithm}
```



In algorithm 3, each thread has its own FreeManQueue, so FreeManQueue.Push(p) does not have data racing issues. However, partnerRank is shared among threads.

When a thread notices that m_rank is lower than the partner's rank, it will try to update the partnerRank atomically with m_rank using atomicCAS. If the returned partner_rank matches p_rank, the operation succeeds, and the rejected man is pushed to the queue if there is someone rejected, similar to the sequential version. If the returned partner_rank does not match p_rank, the atomicCAS operation fails, requiring a retry.

While atomicCAS is a lightweight and fine-grained synchronization method effective for single-variable updates, however, it can become a contention point and bottleneck when too many threads try to update the rank of the same partner. The retries and wasted work from atomicCAS operations can significantly slow down the overall algorithm, offsetting the benefits of parallelization.



```
In the worst-case scenario, if the preference list size is \( n \), and all threads contend to update the same memory location, each thread may need to repeatedly attempt the atomicCAS operation until it succeeds. This can result in \( O(n) \) atomicCAS operations per thread, leading to a total of \( O(n^2) \) operations for all threads combined.

To analyze the behavior of atomicCAS more closely, consider the scenario where multiple threads attempt to update a shared memory location to the smallest value. Let the values proposed by these threads be \( v_1, v_2, \ldots, v_n \), sorted such that \( v_1 < v_2 < \ldots < v_n \).

The smallest value \( v_1 \) will execute atomicCAS successfully on its first attempt, as there is no smaller value in the memory yet. The second smallest value \( v_2 \) will execute atomicCAS successfully only after \( v_1 \) has updated the memory location, meaning it might attempt the operation twice—first failing when \( v_1 \) updates the location and then succeeding. Similarly, the \( k \)-th smallest value \( v_k \) may need up to \( k \) attempts, as it will fail for each smaller value that has already updated the location.

The total number of atomicCAS executions \( T(n) \) for \( n \) values is the sum of these attempts:

\[
T(n) = \sum_{k=1}^{n} k = 1 + 2 + 3 + \ldots + n = \frac{n(n+1)}{2} = O(n^2)
\]

Consequently, the total number of CAS operations to decide a minimum value among \( n \) values will be \( O(n^2) \).

Additionally, for an SMP instance with \( n \) men and \( n \) women, due to the nature of SMP where a woman never gets unpaired once being proposed to, a woman can be proposed to by at most \( n \) men.

In this case, the total number of atomicCAS executions in the worst case is \( O(n^3) \).

While atomicCAS is useful for simple atomic operations, it is not well-suited for the more complex and frequent updates required in the GS algorithm. The high contention and retry overheads negate the benefits of parallel execution.

```





### Unused Content

The GS algorithm naturally lends itself to parallelization, as multiple proposers (men) can make proposals simultaneously. For example, by assigning each thread to simulate a man making proposals when implemented on an actual multithreading hardware, all men will initially propose to their preferred women. However, for the GS algorithm to make progress, it is crucial for threads to communicate with each other. Considering the preference lists given in Figure\ref{perferences}, men m1, m3, m5, and m6 will be paired with their proposed women directly whereas m2 and m7, as well as m4 and m8, will communicate to resolve conflicts if they are proposing to the same woman simultaneously.

In parallel computing, atomic operations are essential for managing shared memory access without data races. 

In CUDA, atomicCAS guarantees correctness by allowing only one thread to successfully update the memory location at a time.



## GPU Challenges

Implementing the parallel Gale-Shapley (GS) algorithm on a GPU presents significant challenges, largely due to the unique architecture and operational characteristics of GPUs. 

These challenges about memory access and synchronization exacerbate the issues inherent in parallelizing the GS algorithm, making efficient implementation difficult.

GPUs excel at handling highly parallel, data-parallel tasks with regular memory access patterns, providing high bandwidth for large-scale computations. This high bandwidth allows many threads to access memory simultaneously, which is advantageous for many parallel algorithms.

However, GPUs typically have higher latency than CPUs when it comes to certain operations, particularly those involving memory access and synchronization.



### Memory

First,the GS algorithm involves irregular and dynamic access patterns during its iterative proposal and acceptance processes. The memory access problem becomes more pronounced on a GPU. Unlike CPUs, which have multiple levels of memory hierarchy (e.g., L1, L2, and L3 caches), GPUs typically have fewer levels of memory hierarchy. This limitation results in higher latency when accessing global memory. Since the GS algorithm involves frequent reads and writes to preference lists and rank matrices during proposals, the reduced memory hierarchy of GPUs can lead to significant delays. Each memory access incurs higher latency, slowing down the overall performance and negating some of the parallel execution benefits.



### Synchronization

Second, the synchronization challenge is magnified on GPUs. GPUs are designed with a high number of parallel processing units, which require synchronization to ensure correct execution of parallel tasks. This high bandwidth and large number of parallel units lead to increased contention when multiple threads attempt to access shared resources simultaneously. In the context of the GS algorithm, where many threads may need to update the partner status of participants concurrently, this contention can result in considerable wasted work. 

Besides, the overhead associated with global synchronization  to ensure consistent state across all threads in such a highly parallel environment can significantly diminish the efficiency gains expected from parallelization.



### Existing Methods

To our knowledge, the parallel versions of both the Gale-Shapley (GS) and McVitie-Wilson (MW) algorithms are the only parallel algorithms that run faster than the sequential GS when implemented on CPUs. The speedup achieved is about 10 times with 72 threads. 

However, both of parallel GS and parallel MW algorithm fail to acheive speedup when implemented on GPU compared to their CPU counterparts.

First of all, the two problems mentioned above will be exacerated when implmented on GPU.  CPUs are better at handling irregular memory access patterns due to their more flexible memory hierarchy and caching mechanisms. GPUs, on the other hand,  are optimized for regular, contiguous memory access patterns to maximize memory throughput. Irregular memory accesses lead to poor memory performance on GPUs because they cannot fully leverage their high-bandwidth memory architecture in such scenarios.

Both parallel GS and McVitie-Wilson (MW) algorithms utilize atomic compare-and-swap (CAS) operations to safely update the suitor status of women during the proposal process. GPUs, with their large number of parallel units, experience high contention when multiple threads attempt to perform atomic operations simultaneously. This contention significantly slows down the execution, as threads often need to retry operations multiple times due to conflicts, undermining the potential speedup from parallel execution.

In addition, the need for frequent and coordinated synchronization makes GPUs less efficient for implementing the parallel GS algorithm. The parallel Gale-Shapley (GS) algorithm requires global synchronization across multiple threads to ensure the correct redistribution of unmarried men among threads for load balancing. GPUs are not well-suited for global synchronization because it involves significant overhead and latency, disrupting the parallel execution flow and leading to performance degradation. 



### Unused Content

GPU can exacerate the issues that we mention above: 

(1)Memory Access problem will become pronounced, GPU only has less levels of memory hierarcheis

(2)Synchronization:High Bandwidth => More parallel Units => High Contention => more wasted work

Additionally, GPUs typically have higher latency than CPUs when it comes to certain operations, particularly those involving memory access and synchronization



Issues with existing parallel methods (Why bad behavior) 



Implementing the parallel Gale-Shapley (GS) algorithm on a GPU presents significant challenges due to the unique architecture and execution model of GPUs. GPUs excel at handling highly parallel, data-parallel tasks with regular memory access patterns, providing high bandwidth for large-scale computations. This high bandwidth allows many threads to access memory simultaneously, which is advantageous for many parallel algorithms. However, the GS algorithm involves irregular and dynamic access patterns due to its iterative proposal and acceptance processes, leading to high contention when many threads attempt to update and access shared data structures concurrently.



Each thread on a GPU would need to frequently perform atomic operations, such as `atomicCAS`, to prevent data races. These atomic operations can become bottlenecks under high contention, causing significant wasted work and reducing overall efficiency. The frequent need for atomic operations leads to threads repeatedly attempting and failing to perform updates, creating delays and reducing the effective parallelism of the algorithm.



Furthermore, the GS algorithm's need for frequent global synchronization to ensure consistent state across all threads adds complexity, as GPUs are designed for fine-grained parallelism rather than frequent synchronization barriers. Managing these synchronization challenges while maintaining the algorithm's correctness and efficiency requires sophisticated techniques that can be difficult to implement and optimize on GPU architectures.



Third, parallelism can diminish significantly when there are disparities in individual preferences. For instance, if all proposers target half of the recipients at the beginning, then in the first round, half of the proposers will successfully pair with recipients. As recipients pair off and remain paired, the number of available proposers and active threads will steadily decrease. This scenario eventually leads to a serial bottleneck, where only a single proposer remains active, thereby negating the advantages of the GPU's high bandwidth due to synchronization overhead. This bottleneck is exacerbated by the GPU's architecture, which is optimized for massive parallelism and suffers in performance when only a few threads are active. 



Additionally, GPUs typically have higher latency than CPUs when it comes to certain operations, particularly those involving memory access and synchronization. GPUs are designed to hide latency through massive parallelism and high throughput, scheduling thousands of threads to keep the processing units busy while some threads wait for memory operations to complete. However, this approach relies on having enough parallel work to keep the GPU fully occupied. In the context of the parallel GS algorithm, as the number of active threads decreases due to successful pairings, the latency hiding mechanism becomes less effective. Higher latency in memory access and synchronization operations can significantly impact performance, as remaining threads spend more time waiting for these operations to complete. This leads to increased idle time and reduced overall efficiency, further highlighting the challenges of implementing the parallel GS algorithm on GPUs.



Therefore, the inherent nature of the GS algorithm, with its need for dynamic and often unequal work distribution, makes it particularly challenging to implement efficiently on a GPU.



The parallel versions of both the Gale-Shapley and McVitie-Wilson algorithms partition the set of men among multiple threads, each running a local version of the algorithm. 

Threads make proposals on behalf of men using atomic compare-and-swap (CAS) operations to update the suitor status of women safely. In the parallel Gale-Shapley algorithm, rejected men are added to local queues and processed in subsequent rounds, with optional synchronization to redistribute unmarried men among threads for load balancing.

In contrast, the parallel McVitie-Wilson algorithm adds rejected men to local stacks, allowing threads to continue making proposals immediately until all men are matched, thus avoiding the need for periodic synchronization.



The parallel versions of both the Gale-Shapley and McVitie-Wilson algorithms partition the set of men among multiple threads, each running a local version of the algorithm. Threads make proposals on behalf of men using atomic compare-and-swap (CAS) operations to update the suitor status of women safely. In the parallel Gale-Shapley algorithm, rejected men are added to local queues and processed in subsequent rounds, with optional synchronization to redistribute unmarried men among threads for load balancing.

In contrast, the parallel McVitie-Wilson algorithm adds rejected men to local stacks, allowing threads to continue making proposals immediately until all men are matched, thus avoiding the need for periodic synchronization.



# Section-FlashSMP

## Overview

FlashSMP is a parallel framework designed to enhance the performance of algorithms on modern heterogeneous computing systems by addressing common challenges such as memory access patterns and contention. 

we introduce a data structure called PRNodes and present a new sequential algorithm that enhances performance by optimizing memory access patterns.

The framework leverages a combination of innovative data structures, atomic operations, and a hybrid CPU-GPU execution model to achieve significant improvements in efficiency and scalability. The core ideas behind FlashSMP include the use of PRNodes to optimize memory access, atomicMin in CUDA for contention resolution, and a hybrid approach to harness the strengths of both GPU and CPU.

![FlashSMP-Overview-2](/Users/jiaxinliu/Desktop/FlashSMPEvaluation/Figures/FlashSMP-Overview-2.jpg)

As show in Figure-5, FlashSMP operates in three main stages:



Initialization of PRNodes on GPU1: FlashSMP begins by initializing PRNodes on the first GPU (GPU1). These nodes contain the  information to perform the SMP computations in a regular access pattern.



Main Procedure of thread1: 

After initialization, thread1 starts execution of MIN Locality Unified CUDA Kernel on GPU1: FlashSMP then launches the MIN Locality Unified CUDA Kernel on GPU1. This kernel processes the PRNodes in parallel, leveraging the GPU's computational power to handle the locality constraints and perform initial matching operations efficiently.



Main Procedure of thread2: 

The main procedure of thread2 involves the use of both the second GPU (GPU2) and the CPU to finalize the matching process. At the beginning, GPU2 is used to continuously check whether only one free man is left by launching the `CheckLessThanNUnified` kernel, which processes each woman in parallel and updates the ranks. When it is determined that only one free man remains, the algorithm transitions to the CPU. The CPU then handles the final stage of the matching process, utilizing its low latency to speed up the completion of the remaining tasks without the need for synchronization, ensuring a rapid convergence to a stable matching.



## Cohabitation-PRNode

As discussed in Section 2, solving the Stable Marriage Problem (SMP) traditionally relies on two key data structures: preference lists and rank matrices.

For each proposal from a man to a woman, two types of data are required from the men's preference lists and the women's rank matrices. When a man, m, decides to propose, he needs to determine which woman, w, to propose to. To get this information, m provides his highest unproposed rank, r, and retrieves w from his preference list at index r.

To evaluate the proposal and decide whether or not to accept it, woman w then looks up her rank matrix to determine m's relative ranking from her perspective. This process often leads to inefficiencies due to irregular access patterns.

To address this issue, FlashSMP introduces PRNodes, a specialized data structure designed to enhance memory access patterns by closely coupling related data elements from the preference lists and rank matrices.

A PRNode is a struct that encapsulates both the data element from a man's preference list and the corresponding rank entry from the woman's rank matrix, facilitating efficient access during both the proposal and acceptance phases of the algorithm.

This organization ensures that when a proposer accesses their PRNode, they can retrieve both the woman to propose to and the relevant rank information in a single memory operation, thereby reducing the frequency of data access and enhancing memory access efficiency.



### Descrition of Algorithm

The preprocessing algorithm begins with the input of preference lists for men and women, both represented as n by n matrices. The goal is to transform this input into an output of an n by n PRNode matrix.



Each PRNode combines information from both the men's and women's preference lists. Specifically, a PRNode includes the woman that a particular man would propose to at a given rank and the rank of that man on the woman’s preference list.



The preprocessing consists of two phases: initializing the rank matrices and then initializing the PRNodes.



```latex
\section*{Phase 1: Initializing the Rank Matrices}

In this phase, the algorithm initializes the rank matrices using parallel processing to ensure efficiency. Each processing unit handles a specific element in the preference lists for men and women.

For the men's rank matrix, the algorithm iterates over each man \(m\) and each rank \(r\) in parallel. It retrieves the woman \(w\) from the men's preference list at position \((m, r)\) and assigns the rank \(r\) to the men's rank matrix at position \((m, w)\). This indicates that woman \(w\) is the \(r\)-th preference of man \(m\). The women's rank matrix is generated in a similar way. By leveraging parallel processing, the algorithm ensures that both men's and women's preferences are accurately represented in the rank matrices.

\section*{Phase 2: Initializing the PRNodes}

Once the rank matrices are initialized, the algorithm proceeds to the second phase: initializing the PRNodes. This phase further leverages the information established in the first phase to create a more efficient data structure.

For each man \(m\) and each rank \(r_w\), the algorithm retrieves the woman \(w\) corresponding to rank \(r_w\) in man \(m\)'s preference list. It then retrieves \(r_m\), which is the rank of man \(m\) in woman \(w\)'s preference list from the women's rank matrix. The PRNode matrix at position \((m, r_w)\) is then assigned the pair \((w, r_m)\). This encapsulation of data ensures that when the Gale-Shapley algorithm runs, each access to a PRNode provides both the woman to whom a proposal should be made and her ranking of the proposer in a single operation.

By organizing the data in this manner, the PRNodes effectively encapsulate the necessary entries from the preference lists and rank matrices, ensuring that related data is closely coupled and can be accessed efficiently. The use of parallel processing in both phases allows the algorithm to handle large datasets quickly and efficiently, optimizing memory access patterns and reducing the frequency and impact of memory jumps.

```



**Conclusion**

This two-phase preprocessing algorithm processes 𝑂(𝑛2)*O*(*n*2) entries in each phase. The independence of each entry during processing allows for significant parallelization. Theoretically, with a sufficient number of processors, the entire preprocessing can be accomplished in constant time. By utilizing the large number of SIMD threads provided by a GPU, the algorithm can efficiently handle large datasets, quickly initializing the PRNodes and optimizing the overall execution of the Gale-Shapley algorithm.



### Unused

Even if  the irregular access patterns of the Rank Matrix can significantly impact overall performance due to frequent cache misses, the preference lists of men are accessed sequentially because each man makes proposals from his highest preference to his lowest.



When a proposer accesses their next preference, the corresponding rank entry is fetched simultaneously or with minimal additional memory accesses. 

By storing these entries next to each other, PRNodes optimize memory access patterns, thereby improving efficiency.

This spatial locality ensures that related data is loaded together, reducing cache misses and improving memory access efficiency. 

PRNodes address this problem by organizing data in a way that aligns better with memory access patterns, reducing the frequency and impact of memory jumps. 



This index is stored in the device node vector at the position corresponding to the man's index and the woman's rank.

Next, row m and column r corresponds to the PRNode on entry (w, r).

Then, we can know the w's preference list on rank r is m.

Based on that information, the unit calculates the index of the woman (`w_idx`) and the rank of the man (`m_rank`) based on its ID.

Using the woman's preference list (`pref_list_w`), it determines the corresponding man index (`m_idx`). 

In that way, we can set the member m_rank on PRNode entry m, r to w

This index is stored in the device node vector at the position corresponding to the woman's index and the man's rank.



This approach optimizes memory access patterns, improving the efficiency of both the sequential Gale-Shapley algorithm or its parallel verion during execution. 



The parallel nature of the algorithm allows for rapid initialization of the PRNodes, leveraging the computational power of parallel processors to handle large datasets efficiently.



## Conflict Resolution-atomicMin

Handling the optimal proposer in the Gale-Shapley (GS) algorithm involves finding the minimum value among possible proposals for a woman, corresponding to the highest priority proposal from the proposing man. This minimization process is critical for determining optimal matches and ensuring the algorithm converges efficiently to a stable state.

To solve this synchronization problem, the `atomicMin` operation can be used effectively. `atomicMin` is an atomic operation implemented on GPUs, similar to `atomicCAS`. According to the CUDA documentation, `atomicMin` reads a 32-bit or 64-bit word located at a given address in global or shared memory, computes the minimum of this value and a given value, and stores the result back to the memory address in a single atomic transaction. The function returns the original value before the update, allowing us to check if the atomic operation succeeded.

`atomicMin` significantly reduces the number of atomic operations compared to `atomicCAS`. With `atomicMin`, each value attempts to update the shared memory location to the minimum of the current value and the new value. If the new value is smaller, it replaces the original value; otherwise, the original value remains unchanged. This ensures that each thread performs the operation only once, eliminating the need for repeated retries.

In a scenario with 𝑛*n* values, `atomicMin` ensures that each value attempts the update operation exactly once, resulting in a total of 𝑂(𝑛)*O*(*n*) atomic operations. For a Stable Marriage Problem (SMP) instance with 𝑛*n* men and 𝑛*n* women, a woman can be proposed to by at most 𝑛*n* men. Thus, the total number of `atomicMin` operations will be 𝑂(𝑛2)*O*(*n*2), similar to the total number of `atomicCAS` operations, which is asymptotically smaller than the 𝑂(𝑛3)*O*(*n*3) operations required by `atomicCAS`.



### Descrition of Algorithm

```
int atomicMin(int* addr, int val) {
	int old = *addr;
	*addr = min(old, val);
	return old;
}
```

Using `atomicMin`, we can implement a parallel version of the McVitie-Wilson algorithm for the Stable Marriage Problem (SMP) that handles contention efficiently, as described in Algorithm 2.

The algorithm operates in parallel, with each processor (thread) corresponding to a unique man. The main data structures used are PRNodes, preference lists for women, and the rank matrix for men. Another crucial data structure is Women's Match Ranks, an array initialized with 𝑛*n* entries set to 𝑛*n*, indicating that all women are unpaired and ready to pair with any proposer. This array stores the rank of the current partner for each woman and will be returned as the result of the SMP instance.

The algorithm proceeds as follows: each processor starts by initializing variables for the man's ID (`manID`), the rank of the current proposal (`r_w`), and a flag (`matched`) to track whether the man has successfully paired. Each man then repeatedly proposes to the next woman on his preference list. The processor retrieves the next woman and the rank of the man from the PRNodes array. When a man proposes to a woman, `atomicMin` attempts to update the woman's current match to the proposing man if his rank is better (lower) than her current match. This atomic operation ensures that only one man's proposal is accepted if multiple proposals are made simultaneously.

There are three cases for a proposal. If a proposal is accepted by an unpaired woman, the processor sets the `matched` flag to true, indicating that the processor should complete its execution. If the proposal is rejected because the woman's current match has a lower rank, the man moves to the next woman on his list, and the loop continues. If the proposal is accepted but the woman prefers the new proposer over her current match, the processor updates the `manID` to the rejected man (the woman's previous match), using the preference list of that woman, and sets `r_w` to the next rank this rejected man should propose to, based on the woman's rank matrix. The rejected man then continues proposing to the next woman on his preference list.

The loop continues until a proposal is accepted by an unpaired woman. By using `atomicMin`, the algorithm ensures efficient handling of contention, allowing multiple proposals and updates to occur simultaneously. This leads to improved performance and faster convergence.



### Unused

A straightforward solution is to use barrier synchronization. In parallel computing, a barrier is a method that forces threads or processes to wait until all participating threads reach a certain point in the code to ensure synchronized behavior. However, this approach can lead to high communication traffic due to all threads repeatedly accessing a global variable to check their status, diminishing scalability. An alternative method, as utilized in \cite{lerring2017parallel}, involves the use of an atomic instruction known as compare-and-swap (CAS) for synchronization in multithreading. CAS works by taking two values: a new value to be written to a memory location and a comparison value to ensure the operation's validity. It reads the old value from the memory, compares it with the provided comparison value, and, if they match, writes the new value to the memory location—all in a single atomic operation. The old value is returned, indicating whether the substitution was successful based on whether the return value matches the comparison value. Nevertheless, CAS can lead to inefficiencies in high-contention scenarios, such as when multiple threads (simulating men proposing to the same woman) compete to update a shared resource. In such cases, only one thread succeeds, while the others must retry, leading to wasted efforts due to CAS failures and significant overhead from frequent synchronization among many processors.



## Embrace Complementary Strengths - GPU and CPU

GPUs can accelerate performance over CPUs due to their massively parallel architecture and high-bandwidth memory. However, while `atomicMin` on a GPU is effective at handling contention by ensuring minimal retries and efficient updates, it remains an expensive operation due to the high overhead associated with atomic transactions. This overhead becomes particularly pronounced when the workload reduces to only one active thread, which is a common scenario for the Stable Marriage Problem (SMP) when preference lists are randomized. In such cases, the benefits of parallel execution diminish, and the costs associated with atomic operations can outweigh their advantages, leading to inefficiencies.

To overcome this shortcoming, FlashSMP employs an efficient strategy to switch between GPU and CPU modes to optimize performance. The key idea behind this switch is to detect when there is only one proposer left, indicating that only one thread remains active. This scenario signals the transition from the massively parallel GPU execution to the more suitable sequential execution on the CPU.

FlashSMP determines when to switch from GPU to CPU mode by checking the pairing status of the recipients (women). Each woman's partner rank is initialized to 𝑛+1*n*+1, where 𝑛*n* is the size of the preference list. A rank value smaller than 𝑛+1*n*+1 indicates that the woman is paired. Throughout the execution, each woman's partner rank is updated with the rank of her partner if she is paired. The algorithm reads the partner rank of each woman to determine if only one woman remains unpaired. If exactly one woman's partner rank is 𝑛+1*n*+1, it indicates that only one proposer remains free.

To find the free man, the algorithm performs additional computations. First, it reads the partner ranks of all women to ensure only one woman is unpaired. Next, it uses the preference lists of the men to identify the paired men for each woman. This step involves reading the indices of the paired men from the preference lists. The algorithm calculates the total sum of indices of all men, which is 1+2+…+𝑛=𝑛(𝑛+1)21+2+…+*n*=2*n*(*n*+1). By subtracting the indices of the paired men from this total sum, the algorithm identifies the index of the free man.

To illustrate, consider the following match ranks for the women:

- W1: 3 (paired with M3)
- W2: 𝑛+1*n*+1 (unpaired)
- W3: 1 (paired with M1)

In this example, the partner rank of W2 is 𝑛+1*n*+1, indicating that W2 is unpaired. We need to determine which man is free. First, read the partner ranks of all women: W1 is 3, W2 is 𝑛+1*n*+1 (unpaired), and W3 is 1. Confirm that only one woman is unpaired by checking that only one rank equals 𝑛+1*n*+1. Identify the indices of the paired men from the partner ranks of the women: W1 is paired with M3, so M3 is paired; W2 is unpaired; W3 is paired with M1, so M1 is paired. Calculate the total sum of indices of all men, which is 1+2+3=3(3+1)2=61+2+3=23(3+1)=6. Subtract the indices of the paired men from the total sum: Paired men indices are 1 (M1) + 3 (M3) = 4. The free man index is 6−4=26−4=2. Therefore, the free man is M2, whose index is 2.

Once the free man is identified and it is confirmed that only one proposer remains active, FlashSMP transitions the computation from the GPU to the CPU. The CPU handles the remaining sequential steps efficiently, ensuring optimal performance for the final part of the algorithm. This transition leverages the CPU's strengths in handling tasks with limited parallelism and more complex control flow, thus maintaining the overall efficiency of the GS algorithm execution.





### Description of Algorithm

The main procedure of this algorithm involves using both GPU and CPU to efficiently solve the Stable Marriage Problem (SMP) with a hybrid approach.

In Phase 1, the algorithm begins by initializing the number of unpaired women to 𝑛*n* and the free man ID to the sum of all men's IDs. It then launches a kernel named `CheckMatchStatus` on GPU2. This kernel processes each woman in parallel. For each woman, it fetches the current match rank from GPU1 and stores it in another array on GPU2. If the woman's match rank is equal to `n+1`, indicating that she is unpaired, an atomic operation decrements a counter for unpaired women, which was initialized to 𝑛*n*. Otherwise, the ID of the matched man is subtracted from the free man ID using an atomic subtraction based on the woman’s preference list.

After launching the `CheckMatchStatus` kernel, the algorithm copies the number of paired men, which is the same as the number of paired women, from the device to the host. If there is exactly one free man, the algorithm proceeds to copy the ID of the free man from the device to the host and then enters Phase 2. If not, the algorithm reinitializes the number of unpaired women and the free man ID, and launches the `CheckMatchStatus` kernel again to check if only one free man remains.

In Phase 2, the algorithm transitions to the CPU to handle the remaining tasks using a normal sequential Gale-Shapley algorithm. It identifies the free man and initializes the proposal rank.

This hybrid approach ensures that the initial parallel processing on the GPU efficiently handles the bulk of proposals, while any remaining complex decisions are managed on the CPU. This balance of workload leads to efficient computation and optimal performance.



# Section-Experiment

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



# Related Work

Newest Lu

\cite{wynn2024selection}







# Drafts

