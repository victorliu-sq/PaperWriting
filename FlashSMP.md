Can you rewrite these sentences to make it more academical? 

You can insert sentences, deleted sentences and reorder sentences, (also for words) to strengthen the connections between sentences.



 These paragraphs also have too many duplicated information / words. Please make it concise and easy to read



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



Currently,  3 critical questions remain unanswered:

\textbf{Currently, three critical questions remain unresolved:}
\begin{enumerate}
    \item \textbf{Can we significantly accelerate GS parallel processing tasks by minimizing data movement?}
    \item \textbf{Can we leverage advanced hardware functions to further optimize the synchronization performance in GS parallel processing?}
    \item \textbf{Can we adaptively use the GPU for massive parallel processing and the CPU for quickly completing non-parallel sections to achieve highly efficient GS computation?}
\end{enumerate}



## Our Work

In this paper, we introduce Balanced-SMP, an effective parallel processing framework by addressing the above three questions in the following ways. 

First, we recognize a critical relationship between the recipient index and the rank of the proposer in the recipient’s preference list. Our finding enables us to implement a preprocessing step that eliminates data dependencies, allowing related data to be accessed together. This preprocessing step lays the foundation for a new data structure for the sequential algorithm implementation so that spatial locality can be fully exploited to significantly reduce the data accessing latency. 



Second, we parallelize this new locality-aware sequential algorithm on GPU and utilize an advanced hardware synchronization utility, called “atomicMIN”. With this hardware primitive by CUDA, we can significantly reduce the number of atomic operations under high memory contention during parallel GS processing, enhancing the synchronization efficiency. 



Finally, we integrate our parallel algorithm into a unified framework for Balanced-SMP. This involves seamlessly combining CPU and GPU resources to maximize their complementary strengths. The GPU’s high bandwidth is leveraged for parallel proposals when there are many active threads, while the CPU’s low latency is utilized for fast proposals when there is only a single active thread. This adaptive approach ensures the algorithm remains efficient regardless of workload size and distribution, taking full advantage of both CPU and GPU capabilities. 



Our experimental evaluation results demonstrate that Balanced-SMP adapts effectively to different workloads, providing consistent and optimal performance across diverse scenarios.



## Contribution

Specifically, we make the following contributions:

1.We have developed a new data structure for implementing the GS algorithm that effectively exploits data locality This locality-aware approach ensures that all necessary rank references are accessible locally during the proposing procedure, eliminating the need for data movement. As a result, this implementation significantly reduces the execution latency of the GS algorithm by minimizing global memory accessing. 



2.We further parallelize the locality-aware GS algorithm that leverages modern hardware synchronization utilities, significantly reducing the number of atomic operations under high memory contention. As a result, the synchronization efficiency is significantly improved in parallel GS processing, particularly for workloads with high conflicts in proposals between man and woman groups.



3.Combining the locality-aware data structure with a hardware synchronization facility, we have developed a framework called Balanced-SMP for the parallel computation of SMP. This framework seamlessly integrates CPU and GPU resources to maximize their complementary strengths. This integration allows us to adaptively switch between the two devices for different workloads, optimizing both the parallel performance and the execution efficiency in non-parallel sections.



4.By comprehensive experimental evaluations, we demonstrate that Balanced-SMP consistently outperforms all the existing parallel algorithms by 2.4x to 28.3x across a wide range of workloads. These results also show the effectiveness of Balanced-SMP and its robust ability to adapt to different computational demands of SMPs.  



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
The GS algorithm begins with all participants being unmatched. In each iteration, an unmatched man proposes to the highest-ranked woman on his preference list who has not previously rejected him. If the woman is unmatched or prefers the new proposer over her current partner, she tentatively accepts the proposal, freeing her current partner if necessary. If she prefers her current partner, she rejects the new proposal, and the man remains unmatched. This process is repeated until all participants are matched.

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
\cite{raman2014gs}
The implementation details of the GS algorithm are described in Algorithm 1.

In the preprocessing phase, the algorithm initializes a matrix called \( \text{WomanRank} \), which shows the rank of each man in the women's preference lists. For each man, the algorithm assigns ranks to all women based on his preference list. This matrix, known as the rank matrix, provides a quick way to determine the preference order of any individual in constant time. For example, \( \text{RankMtxW}[w, m] \) gives the rank of man \( m \) in woman \( w \)’s preference list.

The \( \text{FreeManQueue} \) is a queue that keeps track of free men. Initially, all men are free and added to the queue. The \( \text{Next} \) array records, for each man, the rank of the highest-priority woman who hasn't rejected him yet. This array allows each man to propose to women in his preference list in order without rechecking previously rejected proposals. At the start, each man proposes to the woman he prefers the most, so all ranks stored in \( \text{Next} \) are set to 1. The \( \text{PartnerRank} \) array stores the rank of the current partner of each woman. Initially, the partner rank for each woman is set to \( n+1 \), indicating they are all unmatched.


During the execution phase, the algorithm runs a main loop until there are no free men left in the queue. In each iteration, a man \( m \) is taken from the queue to propose to the highest-priority woman who hasn't rejected him yet. After each proposal, the man increments his rank to move to the next woman on his preference list for future proposals.

The algorithm then checks the rank of this man in the woman’s preference list and compares it to the rank of her current partner. If the woman's current partner is ranked higher (lower numerical value) than the proposing man, the proposing man (\( m \)) remains free and is added back to the queue. Otherwise, the proposing man's partner rank is updated to \( m\_rank \). If the woman is already paired (i.e., \( p\_rank \neq n + 1 \)), the previous partner (\( p \)), identified from the woman's preference list, becomes free and is added back to the queue.

Once the main loop finishes, the algorithm constructs the final stable matching list \( S \) by pairing each woman with her final partner according to the \( \text{PartnerRank} \) list. 

The initialization of the \( \text{RankMatrix} \) and the proposal process, both having \( O(n^2) \) complexity, ensure that the overall time complexity of the algorithm is \( O(n^2) \).


The initialization of entries in the \( \texttt{RankMatrix} \) and the postprocessing of \( \texttt{PartnerRank} \) are completely independent for each entry. This independence allows these phases to be fully parallelized, meaning that with sufficient processing units, they can be done in constant time. Therefore, we focus on the execution phase in the performance analysis presented in this paper.
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





## The Mcvitie-Wilson Algorithm

The algorithm proposed by McVitie and Wilson is essentially another implementation of the Gale-Shapley algorithm, based on the principle that the proposal order does not affect the resulting stable matching. 

The key distinctions between the MW and GS algorithms lie in their execution phases. The MW algorithm iterates through every man and invokes a recursive procedure for free men to make proposals. When a man enters this recursive procedure, he proposes to his highest-ranked woman who has not yet rejected him. If the woman is unpaired, her partner rank is updated as in the GS algorithm.

The main difference is in how rejected proposals are handled. In the MW algorithm, if a proposer is rejected by the woman he is proposing to, he immediately moves on to propose to the next woman on his list, rather than being added back to a queue. Similarly, if a woman accepts a new proposal, her previous partner will continue to propose to his next preference, instead of being pushed back to a queue. This approach eliminates the need for a queue and changes the flow of the algorithm compared to the GS method, streamlining the proposal process and reducing the complexity of managing free individuals.



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





, together with the observation that the order in which the suitors propose does not change the set of matched vertice.

The key difference between the Gale-Shapley and McVitie-Wilson algorithms is in how they handle proposals.The Gale-Shapley algorithm selects a free man from the queue and makes proposals on his behalf until he is matched.In contrast, the McVitie-Wilson algorithm also selects a free man from the queue. If he proposes to a woman who is already paired, the rejected man then makes proposals. This process continues until a man proposes to an unpaired woman, ensuring no man is left unmatched.

Consider the preference lists in Figure 1. The execution of the Mcvitie-Wilson algorithm proceeds as follows:

Initially, M1 proposes to W2. W2 tentatively accepts M1's proposal, forming the initial pair (M1, W2). Since no man has been rejected yet, the algorithm proceeds to the next free man, M2.

M2 then proposes to W2. W2 prefers M2 over M1, so she accepts M2's proposal and rejects M1. The new pairing is (M2, W2). Now free again, M1 proposes to W1. W1 tentatively accepts M1, resulting in the pairs (M1, W1) and (M2, W2). The algorithm then moves on to the next free man, M3.

M3 proposes to W2, but W2 prefers M2, so she rejects M3. M3 then proposes to W1. W1 prefers M3 over M1, so she accepts M3's proposal and rejects M1. The pairs are now (M3, W1) and (M2, W2). M1, now free, proposes to W3, who tentatively accepts. The final pairs are (M1, W3), (M3, W1), and (M2, W2).

This results in a stable matching identical to the man-optimal stable marriage produced by the Gale-Shapley algorithm.



# Bottleneck

To illustrate the bottlenecks in GS computation, we characterize 4 type of SMP workloads that are:

**Best Case**

In the best case scenario, all men have distinct first choices, ensuring all of them will be paired at the first round of proposals.



**Solo Case**

In the singular case, almost every man is paired with a partner immediately, with only one man facing rejection and remaining unpaired for all subsequent proposals. This scenario highlights the inefficiency of parallism.



**Clustered Case**

The clustered case involves clustering preferences into groups, where groups are preferred in a specific order, but the preferences within each group are randomized. This case examines the algorithm’s performance when preferences are not entirely unique.



There are two speical cases for clustered case: 

(1) **Congetsed Case**: each group has only one woman, since groups are preferred in the same order, thus All men have exactly the same preference lists.

(2) **Randomized Case**:  there is only one group containing all women, then  All men have completely randomized  preference lists



To elucidate the bottlenecks in GS computation, we characterize four types of SMP workloads reflected real-world applications and included different configurations of participants and preference lists. that in Figure \ref{fig:4Workloads}:

These scenarios were designed to reflect real-world applications and included different configurations of participants and preference lists.



# Issues with Data Movement

In this section, we explore the various bottlenecks encountered in GS computation. We first provide an in-depth look at the implementation of the GS algorithm, analyzing its inefficient memory access patterns and identifying the bottlenecks caused by frequent and costly data movements. 



We then observe that efficiently parallelizing the GS algorithm is challenging due to synchronization needs. Common methods like locks and barriers are inefficient, and while atomicCAS is lightweight, it suffers from high contention. 



Finally, we highlight the difficulties of implementing the GS algorithm on GPUs, focusing on their high memory access latency and the algorithm's inherent sequential dependencies, which make GPUs less efficient than CPUs for this task.



## Data Movements

The GS algorithm is memory-intensive because it requires frequent and repeated accesses to the men's preference lists ($MenPref$), the women's rank matrix ($WomanRank$), and the next array ($Next$). As shown in Algorithm 1, each proposal involves minimal computation but requires a man to access the $Next$ array on line 14 to find the rank of the best woman who has not yet rejected him, and the $WomanRank$ matrix on line 16 to determine his rank in the woman's preference list. This makes memory access the primary bottleneck.

Figure 2 shows the access patterns of the men's preference lists and the women's rank matrix. The access pattern for the men's preference lists can be optimized by using an additional while-loop to allow the proposer to immediately propose to the next woman instead of being pushed back into the queue on line 18.



In the GS algorithm, dependencies are hidden in logic programs and data structures due to the dynamic nature of the matchmaking process, where the specific interactions and preferences are only revealed during execution. These dependencies, such as which proposals will be made and which rejections will occur, are not known until the algorithm runs with a specific set of inputs. This runtime detection is crucial because the memory accesses to the men's preference lists ($MenPref$) and the women's rank matrix ($WomanRank$) depend on the current state of the matching process, which evolves as proposals are made and accepted or rejected. The workload dependency arises because different sets of preference lists result in different memory access patterns and dependencies. For instance, the order and frequency with which the $WomanRank$ matrix and the $Next$ array are accessed vary based on the input data, causing non-sequential and unpredictable memory jumps that disrupt efficient caching. These dynamic and input-dependent behaviors make the dependencies inherent in the GS algorithm detectable only during runtime, highlighting the challenge of optimizing memory access patterns for efficient execution.



However, optimizing memory access patterns of women's rank matrix remains challenging. The $WomanRank$ matrix is accessed in a non-linear order because the IDs of the men proposing and the women being proposed to are dynamically determined. Even with optimized access patterns for the men's preference lists, the randomization of the proposed women's IDs results in non-sequential accesses to the $WomanRank$ matrix. When the number of participants (n) is very large, this non-sequential nature of access causes significant memory jumps, disrupting efficient caching and prefetching mechanisms. These scattered and unpredictable accesses lead to poor memory usage and slower access times.



### Workload

##### To illustrate the importance of optimizing memory access, we tested the GS algorithm across diverse workloads to measure the impact of memory accesses to the $WomanRank$ matrix and the $Next$ array. 

As shown in Figure 3, the most significant portion of the execution time is attributed to accessing the $WomanRank$ matrix to retrieve a man’s rank in a woman’s preference list and the $Next$ array to get the rank of the next woman to propose to.

On average, these accesses account for over 60% of the total execution time across all workloads. 

(The specific details of these workloads will be explained in Section 6; for now, just note this fact.)”





## Uesless Content

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





# Issues with Synchronization

Although the GS algorithm naturally lends itself to parallelization because multiple men can propose simultaneously \cite{mcvitie1971stable}, efficiently parallelizing the GS algorithm is a non-trivial task.

In a multi-core system or GPU, each thread can represent a man, allowing men to make their proposals independently. While multiple threads can read the partner's rank of the same woman without synchronization, updating the partner's rank must be done carefully to prevent simultaneous changes by other threads, ensuring that the woman is paired with her best choice.

Specifically, in Algorithm 1, the operation on line 17 can be executed without synchronization, but the operation on line 21 requires synchronization to ensure that the woman accepts the best proposal.

While it may seem straightforward to ensure that each woman accepts the best proposal using common synchronization methods such as locks, barrier synchronization, and atomic operations, these approaches are inherently inefficient for this purpose.





### Lock

To address data races in the GS algorithm, one common approach is to use locks. Each thread locks the data before updating it, ensuring exclusive access to the critical section for each woman. However, this method introduces significant overhead due to the frequent acquisition and release of locks, particularly in a highly concurrent environment. The GS algorithm's need for frequent and fine-grained updates makes locks inefficient, as they cause excessive waiting times and performance overhead, rendering them unsuitable for efficient parallelization.



### Barrier Synchronization

Another approach is barrier synchronization, where all threads must reach a specific point before any can proceed. Applied to the GS algorithm, this means making all threads wait at a barrier, allowing each woman to accept the best proposal and reject the rest before letting all threads continue. However, the dynamic nature of the GS algorithm limits this approach. Some men may be rejected and not participate in the updating process, while others may be accepted without competition, making synchronization unnecessary for them. Consequently, some threads finish their tasks sooner and must wait at the barrier, leading to idle time and poor resource utilization. Barrier synchronization's rigidity and the resulting delays negate the benefits of parallelization in the GS algorithm.



### Summary for Lock and Barrier

While it may seem straightforward to use common synchronization methods such as locks and barrier synchronization to ensure that each woman accepts the best proposal, both methods inherently hinder the efficiency and scalability of parallelizing the GS algorithm.

Locks ensure exclusive access to the partner rank for each woman by requiring all threads to lock the data before updating the state of the match. Since the GS algorithm requires frequent and fine-grained updates to the partner rank for each woman, this method introduces significant overhead due to the frequent acquisition and release of locks.

On the other hand, barrier synchronization forces all threads to wait at fixed points before any can proceed. In the context of the GS algorithm, this means making all men wait at a barrier after making proposals, allowing each woman to accept the best proposal and reject the rest before letting all threads continue. However, not all threads need to be synchronized simultaneously when parallelizing the GS algorithm. Some men may be rejected and need to propose again, while others are accepted without competition. As a result, using barrier synchronization leads to idle time and poor resource utilization.



### AtomicCAS

The atomicCAS (Compare-And-Swap) operation is an atomic instruction used to compare a memory location's current value with an expected value and, if they match, swap it with a new value. If they do not match, the operation returns the old value, indicating the update was unsuccessful. This operation is performed atomically, ensuring no other thread can interfere during the process.



```
Algorithm 2 is a parallel implementation of lines 21-26 from Algorithm 1 and is a critical component used in both the parallel GS (Gale-Shapley) and parallel MW (McVitie-Wilson) algorithms to ensure that updates to \texttt{partnerRank} are done atomically, preventing race conditions. The way atomicCAS makes sense is that if a thread finds that \texttt{m\_rank} is lower than the partner's rank, it attempts to update \texttt{partnerRank} with \texttt{m\_rank} using atomicCAS. If the returned \texttt{partner\_rank} does not match \texttt{p\_rank} and \texttt{m\_rank} is still lower, the operation fails and will be retried with the returned partner rank.
```



```
The only difference between these two parallel versions of GS algorithms lies in handling the rejected man on line 7. In the parallel GS algorithm, if the returned rank of the current partner \texttt{p\_rank2} matches the expected \texttt{p\_rank}, the operation succeeds, and the rejected man is pushed to the \texttt{FreeManQueue} for further proposals. To prevent data races, each thread has its own \texttt{FreeManQueue}. In contrast, the parallel MW algorithm allows the thread representing the rejected man to propose again.
```



```
# Parallel Gale-Shapely Algorithm
while (p_rank > m_rank) {
	p_rank2 = atomicCAS(&partnerRank, p_rank, m_rank)
	if (p_rank2 == p_rank) {
		if (p_rank != n + 1) {
			p <- WomenPref[w, p_rank]
			FreeManQueue.Push(p) // each thread has its own FreeManQueue to prevent data races
														// m < - p for Parallel Mcvitie-Wilson Algorithm
		}
		p_rank = m_rank
	} else {
		p_rank = p_rank2
	}
}
```

While atomicCAS is a lightweight and fine-grained synchronization approach seemingly suitable for the frequent updates in the GS algorithm, parallel GS and parallel MW algorithms may perform poorly under high contention due to frequent CAS failures.



```
According to Lemma 2, in the worst-case scenario where all men have the same preference lists and processing units are sufficient, the number of atomicCAS operations can reach \( O(n^3) \), offsetting the benefits of parallelization since the time complexity of the GS algorithm is only \( O(n^2) \).
```



Therefore, GPUs, with their large number of parallel units, can even exacerbate the contention problem, diminishing the potential advantages of parallel execution. 



```
\section*{Lemma 1: AtomicCAS Operations for Finding the Minimum Value}

To find the minimum value among \( n \) numbers using \( n \) threads and atomicCAS to update a shared memory location, where the initial value is greater than any of the \( n \) numbers, the number of atomicCAS operations is \( O(n^2) \).

\subsection*{Proof}

Let the initial value in the shared memory location be \( v_{n+1} \), and the values proposed by the threads be \( v_1, v_2, \ldots, v_n \), sorted such that \( v_1 < v_2 < \ldots < v_n < v_{n+1} \). The thread proposing the smallest value \( v_1 \) will execute atomicCAS only once. On its first attempt, it will either succeed with the original maximum value or find a smaller value and stop. The thread proposing the second smallest value \( v_2 \) will execute atomicCAS at most twice. On its first attempt, it will fail and read out \( v_1 \) after \( v_1 \) has updated the memory location. On its second attempt, it will either succeed or read out a value smaller than \( v_2 \) and stop. Similarly, the \( k \)-th smallest value \( v_k \) can perform up to \( k \) attempts, as it will fail for each smaller value that has already updated the location. Thus, the total number of atomicCAS executions \( T(n) \) for \( n \) values is the sum of these attempts:

\[
T(n) = \sum_{k=1}^{n} k = 1 + 2 + 3 + \ldots + n = \frac{n(n+1)}{2} = O(n^2)
\]

```



```
\section*{Lemma 2: AtomicCAS Operations for SMP Instance}

For an SMP instance with \( n \) men and \( n \) women, the total number of atomicCAS executions is \( O(n^3) \).

\subsection*{Proof}

In the worst-case scenario where contention is maximized, all \( n \) men have identical preference lists, as shown in Figure 4. In the first round of proposals, all \( n \) men and corresponding \( n \) threads will contend to update the same memory location to set the minimum value. Based on Lemma 1, the total number of atomicCAS for this round of proposals is \( O(n^2) \). In the second round, \( n-1 \) men will make proposals since 1 man will already be paired. This results in \( O(n) \) men, also leading to \( O(n^2) \) atomicCAS operations. This pattern continues for all \( n \) rounds of proposals. Thus, the total number of atomicCAS executions in the worst-case scenario is \( O(n^3) \).
```



The limitations of traditional synchronization methods lead to the question: **Can we leverage advanced hardware functions to further optimize synchronization performance in GS parallel processing?**



### Unused Content

The GS algorithm naturally lends itself to parallelization, as multiple proposers (men) can make proposals simultaneously. For example, by assigning each thread to simulate a man making proposals when implemented on an actual multithreading hardware, all men will initially propose to their preferred women. However, for the GS algorithm to make progress, it is crucial for threads to communicate with each other. Considering the preference lists given in Figure\ref{perferences}, men m1, m3, m5, and m6 will be paired with their proposed women directly whereas m2 and m7, as well as m4 and m8, will communicate to resolve conflicts if they are proposing to the same woman simultaneously.

In parallel computing, atomic operations are essential for managing shared memory access without data races. 

In CUDA, atomicCAS guarantees correctness by allowing only one thread to successfully update the memory location at a time.





## Existing Methods

To our knowledge, the parallel versions of both the Gale-Shapley (GS) and McVitie-Wilson (MW) algorithms are the only parallel algorithms that run faster than the sequential GS when implemented on CPUs. The speedup achieved is about 10 times with 72 threads. 

However, both of parallel GS and parallel MW algorithm fail to acheive speedup when implemented on GPU compared to their CPU counterparts.

First of all, the two problems mentioned above will be exacerated when implmented on GPU.  CPUs are better at handling irregular memory access patterns due to their more flexible memory hierarchy and caching mechanisms. GPUs, on the other hand,  are optimized for regular, contiguous memory access patterns to maximize memory throughput. Irregular memory accesses lead to poor memory performance on GPUs because they cannot fully leverage their high-bandwidth memory architecture in such scenarios.

In addition, the need for frequent and coordinated synchronization makes GPUs less efficient for implementing the parallel GS algorithm. The parallel Gale-Shapley (GS) algorithm requires global synchronization across multiple threads to ensure the correct redistribution of unmarried men among threads for load balancing. GPUs are not well-suited for global synchronization because it involves significant overhead and latency, disrupting the parallel execution flow and leading to performance degradation. 



## Unused Content

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





# Issues with GPU

GPUs (Graphics Processing Units) and CPUs (Central Processing Units) are both critical components in computing, each designed for specific types of tasks. CPUs, with their complex control logic, multi-level cache hierarchies (L1, L2, L3), and higher clock speeds, are optimized for general-purpose computing and can handle a wide range of tasks efficiently, including those requiring quick memory access and low latency. GPUs, on the other hand, are designed for highly parallel tasks, such as rendering graphics or performing large-scale computations. They feature a simpler two-level caching system and lower clock speeds, prioritizing bandwidth and the ability to process large volumes of data in parallel. This straightforward memory hierarchy, while effective for parallel processing, results in higher latency for memory access operations compared to CPUs.

Efficiently implementing the massively parallel Gale-Shapley (GS) algorithm on a GPU presents significant challenges due to its inherently sequential nature for certain workloads. In specific SMP instances, such as the one illustrated in Figure 5, after the initial round of proposals, only one individual may remain free and ready to make another proposal. This scenario leaves no opportunity for parallelism, as each subsequent proposal depends on the outcomes of previous steps. This sequential dependency complicates the effective use of the massively multithreaded architecture of GPUs for the GS algorithm.

As presented in Figure 6, we conducted a performance comparison between the sequential GS on a CPU, sequential MW on a GPU, and the parallel GS algorithm on a CPU, as well as the parallel MW algorithm on both CPU and GPU, using an SMP instance of size 10,000 with a preference list pattern similar to that in Figure 5. We did not implement the parallel GS algorithm on a GPU because, when processing units are sufficient, each queue can only maintain at most one free man, making this implementation equivalent to the parallel MW algorithm. The results clearly show that the GPU's performance is inferior to the CPU's for the GS algorithm, highlighting the inefficiency of using GPUs for this algorithm under these conditions.



**Figure 5: SMP Instance with 10,000 Participants Highlighting Sequential Dependency**



**Figure 6: Performance Comparison of Sequential and Parallel GS and MW Algorithms on CPU and GPU**





# Section-Bamboo

## Overview

Bamboo-SMP is a parallel framework developed to optimize the performance of algorithms on modern heterogeneous computing systems by effectively addressing prevalent challenges such as memory access patterns and contention. This framework employs a combination of advanced data structures, atomic operations, and a hybrid CPU-GPU execution model to achieve notable improvements in both efficiency and scalability.

The core principles of Bamboo-SMP involve several innovative strategies. Firstly, the use of PRNodes optimizes memory access by ensuring that related data elements are stored together, thereby reducing latency and enhancing data locality. Secondly, the framework utilizes the \texttt{atomicMin} operation in CUDA to efficiently resolve contention, minimizing the need for repeated retries and reducing overhead associated with atomic transactions. Lastly, Bamboo-SMP leverages a hybrid CPU-GPU approach, enabling it to capitalize on the complementary strengths of GPUs and CPUs. This hybrid execution model ensures that high parallelism and complex control flows are handled optimally, further contributing to the framework's scalability and efficiency.

Through these strategies, Bamboo-SMP demonstrates a significant advancement in the performance of parallel algorithms on heterogeneous computing systems.

![FlashSMP-Overview-2](/Users/jiaxinliu/Desktop/FlashSMPEvaluation/Figures/FlashSMP-Overview-2.jpg)

As show in Figure-5, FlashSMP operates in three main stages:



Initialization of PRNodes on GPU1: FlashSMP begins by initializing PRNodes on the first GPU (GPU1). These nodes contain the  information to perform the SMP computations in a regular access pattern.



Main Procedure of thread1: 

After initialization, thread1 starts execution of MIN Locality Unified CUDA Kernel on GPU1: FlashSMP then launches the MIN Locality Unified CUDA Kernel on GPU1. This kernel processes the PRNodes in parallel, leveraging the GPU's computational power to handle the locality constraints and perform initial matching operations efficiently.



Main Procedure of thread2: 

The main procedure of thread2 involves the use of both the second GPU (GPU2) and the CPU to finalize the matching process. At the beginning, GPU2 is used to continuously check whether only one free man is left by launching the `CheckLessThanNUnified` kernel, which processes each woman in parallel and updates the ranks. When it is determined that only one free man remains, the algorithm transitions to the CPU. The CPU then handles the final stage of the matching process, utilizing its low latency to speed up the completion of the remaining tasks without the need for synchronization, ensuring a rapid convergence to a stable matching.



### Unused

we introduce a data structure called PRMatrix and present a new sequential algorithm that enhances performance by optimizing memory access patterns.



# Locality-Aware Implementation of the GS Algorithm

we recognize a critical relationship between the recipient index and the rank of the proposer in the recipient’s preference list. Our finding enables us to implement a preprocessing step that eliminates data dependencies, allowing related data to be accessed together. This preprocessing step lays the foundation for a new data structure for the sequential algorithm implementation so that spatial locality can be fully exploited to significantly reduce the data accessing latency. 



We have developed a new data structure for implementing the GS algorithm that effectively exploits data locality This locality-aware approach ensures that all necessary rank references are accessible locally during the proposing procedure, eliminating the need for data movement. 



## Depdendent Data Access Pattern

```
As discussed in Section 2, the primary overhead in the GS algorithm arises from accessing the data structures, specifically the rank matrix \texttt{RankMatrixW} and the \texttt{Next} array. To identify key points where optimizations in the organization of these two data structures are possible, it is essential to clarify the dependent relationship between data access patterns.

In Algorithm 1, after retrieving the ID of the best woman who has yet to reject the proposer from his preference list on line 16, the rank matrix is accessed on line 17 to determine the man's rank in the woman's preference list. Specifically, when accessing the men's preference list entry for man \texttt{m} at rank \texttt{r} (denoted as \texttt{PrefListM[m, r]}), we obtain woman \texttt{w}. This necessitates a subsequent access to the rank matrix entry for woman \texttt{w} and man \texttt{m} (denoted as \texttt{RankMatrixW[w, m]}) to determine the man's rank in her list. This process illustrates a direct one-to-one correspondence between the men's preference list (\texttt{PrefListM}) and the women's rank matrix (\texttt{RankMatrixW}). Each man's decision on which specific woman to propose to is directly mapped to the rank of the proposer in the woman's preference list. Thus, each entry in the men's preference list is intrinsically linked to a unique entry in the women's rank matrix. If these data structures are stored together, both pieces of information can be accessed with a single load instruction, eliminating the need to access \texttt{RankMatrixW} separately. This optimization can significantly reduce the overhead associated with data access in the GS algorithm.

Similarly, there is a one-to-one correspondence between the access of the women's preference list \texttt{PrefListW} and the men's rank matrix texttt{RankMatrixM}. By constructing \texttt{RankMatrixM} in a similar way to \texttt{RankMatrixW}, we can optimize the data access pattern of the \texttt{Next} array. When a woman accepts a new proposal and is already paired with a man ranked \texttt{p_r} on her preference list, the women's preference list is accessed by \texttt{PrefListW[w, p_r]} on line 24 to determine the ID of the rejected partner \texttt{p}. Subsequently, the algorithm accesses \texttt{Next[p]} to get the rank of the next woman who has yet to reject the partner on line 14 for future proposals. However, accessing \texttt{Next[p]} directly is not always necessary. Since \texttt{w} is paired with \texttt{p}, \texttt{w} is the last woman that \texttt{p} proposed to. Therefore, the rank of the last woman \texttt{p} proposed to is stored in \texttt{RankMatrixM[p, w]}. By accessing \texttt{RankMatrixM[p, w]}, we can determine the rank of the best woman who has yet to reject \texttt{p} by simply adding one to this value, resulting in \texttt{RankMatrixM[p, w] + 1}. Given that this occurs after accessing \texttt{PrefListW[w, p_r]} and identifying \texttt{p}, it becomes evident that there is a one-to-one correspondence between \texttt{PrefListW[w, p_r]} and \texttt{RankMatrixM[p, w]}.

```



## PRMatrix

```
To optimize the data access patterns discussed above, we introduce a specialized data structure called PRMatrix, which integrates both the preference lists and the rank matrices. This integration provides opportunities to significantly reduce overhead by streamlining the data retrieval process and eliminating separate data accesses.

There are two types of PRMatrix serving distinct purposes: PRMatrixM and PRMatrixW. PRMatrixM combines information from the men's preference lists with the women's rank matrix to facilitate the determination of the proposer rank , while PRMatrixW integrates the women's preference lists with the men's rank matrix to accelerate the identification of the next viable partner.

Both of these PRMatrice contains \(n \times n\) entries, referred to as PRNodes. Each PRNode includes one element from the preference lists and one element from the rank matrices, combining these two pieces of information into a single structure. Because the preference lists and rank matrices are both of size \(n \times n\), where \(n\) represents the number of participants, PRMatrix also has \(n \times n\) entries, ensuring efficient organization and access to all necessary data.

In PRMatrixM, each PRNode includes an entry from the men's preference list, indicating the woman a specific man would propose to at a given rank, along with the corresponding entry from the women's rank matrix, specifying the rank of that man on the woman’s preference list. By storing these two elements together, they can be accessed simultaneously with a single load instruction.

Similarly, each PRNode in PRMatrixW includes an entry from the women's preference list and the corresponding entry from the men's rank matrix. This configuration allows a single access to retrieve both the ID of the current partner and the rank of the his last proposed woman.	
```



## PRMatrix Init

```
Setting up PRMatrix involves two main steps in the preprocessing phase, as shown in Algorithm 2: constructing the rank matrices and then configuring the PRNodes.

Rather than constructing only \textit{RankMatrixW} as done in Algorithm 1, both \textit{RankMatrixW} and \textit{RankMatrixM} will be built using the same mechanisms. Once these rank matrices are in place, the algorithm proceeds to configure the PRMatrices.

For each man \(m\) and each rank \(r_w\), the algorithm retrieves the woman \(w\) corresponding to rank \(r_w\) in the man's preference list. It then retrieves \(r_m\), which is the rank of man \(m\) in the woman's preference list from \textit{RankMatrixW}. The PRMatrixM at position \((m, r_w)\) is then assigned the pair \((w, r_m)\).

Similarly, for each woman \(w\) and each rank \(r_m\), the algorithm retrieves the man \(m\) corresponding to rank \(r_m\) in the woman's preference list. It then retrieves \(r_w\), which is the rank of woman \(w\) in the man's preference list from \textit{RankMatrixM}. The PRMatrixW at position \((w, r_m)\) is then assigned the pair \((m, r_w)\).

Since the configuration of each PRNode is independent of the others, this process can be fully parallelized, much like the construction of the rank matrices. By parallelizing these steps, the preprocessing phase remains efficient and avoids becoming a major source of overhead.

```



```
We illustrate the initialization of PRMatrix using Figure 7, focusing on the process for the first column of PRMatrixM, based on the preference lists depicted in Figure 1.

The process begins by constructing \textit{RankMatrixW} from \textit{PrefListsW}. Following this, we configure the first column of PRMatrixM using \textit{PrefListsM} and \textit{RankMatrixW}.

To begin with, the PRNodes \texttt{PRMatrixM[M1, rank1]}, \texttt{PRMatrixM[M2, rank1]}, and \texttt{PRMatrixM[M3, rank1]} are assigned the ID of the best candidate for each man. These IDs come from the corresponding entries in \textit{PrefListsM}: \texttt{PrefListsM[M1, rank1]}, \texttt{PrefListsM[M2, rank1]}, and \texttt{PrefListsM[M3, rank1]}. Since all these entries correspond to W2, W2 will be stored in all these PRNodes.

Next, each PRNode retrieves the rank of the man in W2's preference list from \texttt{RankMatrix[W2, M1]}, \texttt{RankMatrix[W2, M2]}, and \texttt{RankMatrix[W2, M3]}, which correspond to rank2, rank1, and rank3, respectively. Consequently, these PRNodes are configured as (W2, rank2), (W2, rank1), and (W2, rank3).

By following this procedure, we can set up all PRNodes in PRMatrixM and PRMatrixW once \textit{RankMatrixW} is established.
```



```
// Initializartion of Rank Matrices
for m = 1 to n:
	for r_w = 1 to n:
		w = prefListsM[m, r_w]
		rankMatrixM[m, w] = r_w
		
for w = 1 to n:
	for r_m = 1 to n:
		m = prefListsW[w, r_m]
		rankMatrixW[w, m] = r_m
	
		
// Initializartion of PRMatrices
for m = 1 to n:
	for r_w = 1 to n:
		w = prefListsM[m, r_w]
		r_m = rankMatrixW[w, m]
		PRNodesM[m, r_w] = (w, r_m)
		
for w = 1 to n:
	for r_m = 1 to n:
		m = prefListsW[w, r_m]
		r_w = rankMatrixM[m, w]
		PRNodesW[w, r_m] = (m, r_w)

for i = 1 to n:
	parterRank[i] = n + 1
```



```
\begin{algorithm}
\caption{Building the Rank Matrix}
\label{InitRankMatrix}
\begin{algorithmic}[1]
\State \textbf{Input:} \text{prefLists}
\State \textbf{Output:} \text{rankMatrix}
\For{$i = 1$ to $n$}
    \For{$r = 1$ to $n$}
        \State $j \gets \text{prefLists}[i, r]$
        \State $\text{rankMatrix}[i, j] \gets r$
    \EndFor
\EndFor
\end{algorithmic}
\end{algorithm}
```



```
\begin{algorithm}
\caption{Building the PR Matrix}
\begin{algorithmic}[1]
\State \textbf{Input:} \text{prefLists}, \text{rankMatrix}
\State \textbf{Output:} \text{PRMatrix}
\For{$i = 1$ to $n$}
    \For{$r = 1$ to $n$}
        \State $j \gets \text{prefLists}[i, r]$
        \State $r' \gets \text{rankMatrix}[j, i]$
        \State $\text{PRMatrix}[i, r] \gets (j, r')$
    \EndFor
\EndFor
\end{algorithmic}
\end{algorithm}
```



## Locality-Aware implementation of GS(MW) algorithm

```
The \texttt{PRMatrix} structure eliminates the need for separate accesses to the rank matrix and the next array, laying the foundation for a more efficient locality-aware sequential implementation of the GS algorithm.

To implement this new locality-aware approach, we begin with the preprocessing phase, where we construct \texttt{PRMatrices} as previously discussed, along with the \texttt{partnerRank} data structure.

Following the initialization, the execution phase involves iterating through each man who has not yet made a proposal and invoking the \texttt{performLocalityAwareMatching} procedure for each man.

Within \texttt{performLocalityAwareMatching}, we initialize \texttt{done} to \texttt{False} and \texttt{w\_rank} to 1, as the man \texttt{m} has not been rejected by any woman yet and can propose to the highest-ranked woman on his list. Similar to the MW algorithm, after each iteration, \texttt{performLocalityAwareMatching} handles the rejected man from the previous iteration, continuing until a proposal is accepted, indicated by \texttt{done} being set to \texttt{True}.

During each iteration, we retrieve the woman \texttt{w} and the rank \texttt{m\_rank} from \texttt{PRNodesM} for the current man \texttt{m} and increment \texttt{w\_rank}. We then check the current partner's rank \texttt{p\_rank} for woman \texttt{w} from \texttt{partnerRank}.

If \texttt{p\_rank} is greater than \texttt{m\_rank}, meaning the woman \texttt{w} prefers the current proposer \texttt{m} over her current partner, we update \texttt{partnerRank[w]} to \texttt{m\_rank}. If \texttt{p\_rank} equals \texttt{n + 1}, indicating the woman was previously unpaired and no man is rejected, we set \texttt{done} to \texttt{True} to terminate the main loop. If \texttt{p\_rank} is not equal to \texttt{n + 1}, meaning the woman is currently paired with another partner she prefers less, we retrieve the ID of that partner and the rank of his last proposed woman from \texttt{PRNodesW}.

Then, \texttt{w\_rank} is incremented by 1 to indicate the next rank of the woman the current man will propose to in the next iteration. The loop then checks whether a rejected man exists at the end of the loop to determine if it should terminate or continue.

```



```
for m = 1 to n:
	LocalityAwareProcedure(m)
	
Procedure LocalityAwareProcedure(m)
  bool done = false
  w_rank = 1
  while (not done) {
    w, m_rank = PRNodesM[m, w_rank]
    p_rank = partnerRank[w]
    if (p_rank > m_rank) {
      partnerRank[w] = m_rank
      if (p_rank == n + 1){
        done = true
      } else {
        m, w_rank = PRNodesW[w, m_rank]
      }
    }
    w_rank = w_rank + 1
  }
```



### Unused

Both `RankMatrixW` and the `Next` array exhibit a direct mapping between entries in the preference lists and the corresponding rank matrices. This observation underscores the potential for optimizing memory access patterns by leveraging the inherent structure of the GS algorithm.

Specifically, we need to understand the one-to-one correspondence between entries in the preference list of men and entries in the rank matrix of women, and vice versa.

The first one-to-one correspondence is between the men's preference list (`PrefListM`) and the women's rank matrix (`RankMatrixW`).



This rank is crucial for deciding whether the woman will accept or reject the proposal based on her current partner's rank.



The \texttt{performLocalityAwareMatching} procedure is designed to efficiently manage the proposing process for the man and any subsequently rejected men by leveraging the locality-aware PRMatrix.



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



This ensures that if the woman rejects the current proposer, the algorithm can efficiently determine the next man to propose to her by referencing the updated rank position. This encapsulation of data ensures that when the Gale-Shapley algorithm runs, each access to a PRNode provides both the woman to whom a proposal should be made and her ranking of the proposer in a single operation.



During the execution of the GS algorithm, a proposer accessing their PRNode can retrieve both the woman to propose to and the relevant rank information in a single memory operation. Similarly, when a woman accesses the PRNode, she can retrieve both the current partner she is paired with and the rank information of herself on the man's preference list in a single memory operation. This integrated approach significantly optimizes the data access patterns, improving the overall performance of the GS algorithm.



As a result, this implementation significantly reduces the execution latency of the GS algorithm by minimizing global memory accessing.



```latex
\section*{Phase 1: Initializing the Rank Matrices}

In this phase, the algorithm initializes the rank matrices using parallel processing to ensure efficiency. Each processing unit handles a specific element in the preference lists for men and women.

For the men's rank matrix, the algorithm iterates over each man \(m\) and each rank \(r\) in parallel. It retrieves the woman \(w\) from the men's preference list at position \((m, r)\) and assigns the rank \(r\) to the men's rank matrix at position \((m, w)\). This indicates that woman \(w\) is the \(r\)-th preference of man \(m\). The women's rank matrix is generated in a similar way. By leveraging parallel processing, the algorithm ensures that both men's and women's preferences are accurately represented in the rank matrices.

\section*{Phase 2: Initializing the PRNodes}

Once the rank matrices are initialized, the algorithm proceeds to the second phase: initializing the PRNodes. This phase further leverages the information established in the first phase to create a more efficient data structure.

For each man \(m\) and each rank \(r_w\), the algorithm retrieves the woman \(w\) corresponding to rank \(r_w\) in man \(m\)'s preference list. It then retrieves \(r_m\), which is the rank of man \(m\) in woman \(w\)'s preference list from the women's rank matrix. The PRNode matrix at position \((m, r_w)\) is then assigned the pair \((w, r_m)\). This encapsulation of data ensures that when the Gale-Shapley algorithm runs, each access to a PRNode provides both the woman to whom a proposal should be made and her ranking of the proposer in a single operation.

By organizing the data in this manner, the PRNodes effectively encapsulate the necessary entries from the preference lists and rank matrices, ensuring that related data is closely coupled and can be accessed efficiently. The use of parallel processing in both phases allows the algorithm to handle large datasets quickly and efficiently, optimizing memory access patterns and reducing the frequency and impact of memory jumps.

```



```

\textbf{Phase 1: Initializing the Rank Matrices}

In this phase, the algorithm initializes the rank matrices using parallel processing to ensure efficiency. Each processing unit handles a specific element in the preference lists for men and women.

For the men's rank matrix, the algorithm iterates over each man \(m\) and each rank \(r\) in parallel. It retrieves the woman \(w\) from the men's preference list at position \((m, r)\) and assigns the rank \(r\) to the men's rank matrix at position \((m, w)\). This indicates that woman \(w\) is the \(r\)-th preference of man \(m\). The women's rank matrix is generated in a similar way. By leveraging parallel processing, the algorithm ensures that both men's and women's preferences are accurately represented in the rank matrices.

\textbf{Phase 2: Initializing the PRNodes}

Once the rank matrices are initialized, the algorithm proceeds to the second phase: initializing the PRNodes. This phase further leverages the information established in the first phase to create a more efficient data structure.

For each man \(m\) and each rank \(r_w\), the algorithm retrieves the woman \(w\) corresponding to rank \(r_w\) in man \(m\)'s preference list. It then retrieves \(r_m\), which is the rank of man \(m\) in woman \(w\)'s preference list from the women's rank matrix. The PRNode matrix at position \((m, r_w)\) is then assigned the pair \((w, r_m)\). This encapsulation of data ensures that when the Gale-Shapley algorithm runs, each access to a PRNode provides both the woman to whom a proposal should be made and her ranking of the proposer in a single operation.

By organizing the data in this manner, the PRNodes effectively encapsulate the necessary entries from the preference lists and rank matrices, ensuring that related data is closely coupled and can be accessed efficiently. The use of parallel processing in both phases allows the algorithm to handle large datasets quickly and efficiently, optimizing memory access patterns and reducing the frequency and impact of memory jumps.

This two-phase preprocessing algorithm processes $O(n^2)$ entries in each phase. The independence of each entry during processing allows for significant parallelization. Theoretically, with a sufficient number of processors, the entire preprocessing can be accomplished in constant time. By utilizing the large number of SIMD threads provided by a GPU, the algorithm can efficiently handle large datasets, quickly initializing the PRNodes and optimizing the overall execution of the Gale-Shapley algorithm.


```



**Conclusion**

This two-phase preprocessing algorithm processes 𝑂(𝑛2)*O*(*n*2) entries in each phase. The independence of each entry during processing allows for significant parallelization. Theoretically, with a sufficient number of processors, the entire preprocessing can be accomplished in constant time. By utilizing the large number of SIMD threads provided by a GPU, the algorithm can efficiently handle large datasets, quickly initializing the PRNodes and optimizing the overall execution of the Gale-Shapley algorithm.



# Massive Parallelism

```
As previously mentioned, in parallelized GS algorithms, each woman needs to select the best proposal with the minimum numerical value when multiple proposals are made simultaneously. However, traditional synchronization methods can be inefficient when updating \texttt{partnerRank} due to the high cost of coarse-grained synchronization and wasted work from \texttt{atomicCAS} failures under high memory contention.

To overcome this problem, we need a fine-grained hardware primitive that handles high memory contention efficiently. Modern CPUs still rely on \texttt{atomicCAS} implementations to perform specific arithmetic functions. In contrast, modern GPU architectures, such as NVIDIA's CUDA, offer a comprehensive set of atomic functions for arithmetic operations. Among these, \texttt{atomicMin} effectively addresses the challenges of synchronization and high contention in parallelized GS algorithms.

The \texttt{atomicMin} function in CUDA reads the 32-bit or 64-bit word \texttt{old} at the address in global or shared memory, computes the minimum of \texttt{old} and \texttt{val}, stores the result back to memory at the same address—all in one atomic transaction. The function then returns \texttt{old} so the caller can determine whether the value has been updated. If \texttt{old} is larger, the caller knows the value has been updated to \texttt{val}; otherwise, no update has occurred.

By leveraging the atomic functions provided by modern GPU architectures, a parallel version of the Locality-Aware \texttt{GS} algorithm in Algorithm can efficiently solve \texttt{SMP} instances associated with high contention. The parallel algorithm inherits most of the logic from its sequential version to exploit locality using \texttt{PRMatrix}, but the key difference lies in how it ensures mutual exclusion and prevents race conditions by using \texttt{atomicMin} to update the shared data structure \texttt{partnerRank}.

```



```
Each thread, representing a man \(m\), starts by proposing to the highest-ranked woman on his preference list that he has not yet proposed to. After retrieving the current partner's rank \(p\_rank\) for woman \(w\) from \texttt{partnerRank[w]}, the algorithm checks if \(p\_rank\) is greater than \(m\_rank\). If \(p\_rank > m\_rank\), meaning the woman \(w\) prefers the current proposer \(m\) over her current partner, we attempt to update \texttt{partnerRank[w]} to \(m\_rank\) using \texttt{atomicMin(\&partnerRank[w], m\_rank)}. 


If the update is unsuccessful, as indicated by the returned value being not larger than \(m\_rank\), \(m\) will be rejected and will have to propose to the next woman on his preference list in the next iteration. 

Otherwise, there are two scenarios to consider:

1. If \(p\_rank\) equals \(n + 1\), indicating the woman was previously unpaired and no man is rejected, the variable \texttt{done} is set to \texttt{true} to terminate the main loop.

2. If \(p\_rank\) is not equal to \(n + 1\), meaning the woman is currently paired with another partner she prefers less, the ID of that partner and the rank of his last proposed woman are retrieved from \texttt{PRNodesW[w, m\_rank]}.
```



The advantage of \texttt{atomicMin} in parallelizing GS is that it does not require an expected value to proceed only if the expected value matches the \texttt{old}. This ensures that each thread performs the operation only once, eliminating the need for repeated retries. Specifically, even if the returned value mismatches the previously read one but is still larger than \texttt{val}, \texttt{atomicMin} can proceed to update the minimum value with \texttt{val}, whereas \texttt{atomicCAS} would need to repeat the operation.



As a result, \texttt{atomicMin} significantly reduces the number of atomic operations compared to using \texttt{atomicCAS}. According to Lemma 5.1, for a Stable Marriage Problem (SMP) instance with \(n\) men and \(n\) women, the total number of \texttt{atomicMin} operations is \(O(n^2)\), which is significantly smaller than the \(O(n^3)\) operations required by \texttt{atomicCAS}.



Massive Parallelism of Locality-Aware GS



```
\begin{lemma}
For a Stable Marriage Problem (SMP) instance with \( n \) men and \( n \) women, the total number of \texttt{atomicMin} executions is \( O(n^2) \).
\end{lemma}

\begin{proof}
Let the initial value in the shared memory location be \( v_{n+1} \), and the values proposed by the threads be \( v_1, v_2, \ldots, v_n \), sorted such that \( v_1 < v_2 < \ldots < v_n < v_{n+1} \). Each thread will execute \texttt{atomicMin} only once since there won't be failures—each thread writes the minimum of the proposed value and the value stored in the memory location. Thus, the total number of \texttt{atomicMin} executions to determine the minimum value among \( n \) values is \( n \). This pattern continues for all \( n \) rounds of proposal, resulting in a worst-case scenario of \( O(n^2) \) \texttt{atomicMin} executions.
\end{proof}

```





### Unused

A straightforward solution is to use barrier synchronization. In parallel computing, a barrier is a method that forces threads or processes to wait until all participating threads reach a certain point in the code to ensure synchronized behavior. However, this approach can lead to high communication traffic due to all threads repeatedly accessing a global variable to check their status, diminishing scalability. An alternative method, as utilized in \cite{lerring2017parallel}, involves the use of an atomic instruction known as compare-and-swap (CAS) for synchronization in multithreading. CAS works by taking two values: a new value to be written to a memory location and a comparison value to ensure the operation's validity. It reads the old value from the memory, compares it with the provided comparison value, and, if they match, writes the new value to the memory location—all in a single atomic operation. The old value is returned, indicating whether the substitution was successful based on whether the return value matches the comparison value. Nevertheless, CAS can lead to inefficiencies in high-contention scenarios, such as when multiple threads (simulating men proposing to the same woman) compete to update a shared resource. In such cases, only one thread succeeds, while the others must retry, leading to wasted efforts due to CAS failures and significant overhead from frequent synchronization among many processors.



# Bamboo-SMP

## Overview

While \texttt{atomicMin} on a GPU is effective at managing contention by minimizing retries and ensuring efficient updates, it remains an expensive operation due to the high overhead associated with atomic transactions. As discussed in Section 3.3, this overhead becomes particularly pronounced in scenarios with high contention, such as when the preference lists resemble those depicted in Figure 5. In such cases, the advantages of parallel execution diminish, and the costs associated with atomic operations can outweigh their benefits, leading to inefficiencies.



To address this limitation, we propose a parallel framework that leverages a hybrid CPU-GPU execution model. This model employs locality-aware algorithms to achieve significant improvements in efficiency and scalability by capitalizing on the strengths of both GPU and CPU. By integrating the complementary capabilities of GPUs and CPUs, the framework aims to optimize performance under varying conditions of parallelism and contention. A crucial aspect of this hybrid model is the effective transfer of execution from the GPU to the CPU. Ensuring a seamless transition between these processing units is essential for maintaining overall efficiency. This transfer requires addressing two fundamental questions: (1) when to switch and (2) how to switch.



**When to Switch:** 

The guiding principle for switching from GPU to CPU execution is when the number of active threads reduces to one. In scenarios where only a single thread remains active on the GPU, the synchronization overhead and high latency inherent to GPU operations become significant bottlenecks. Transitioning to CPU execution at this point allows for efficient handling of high parallelism when many threads are active, while avoiding the inefficiencies associated with reduced parallelism on the GPU. The critical aspect of this switch is detecting when there is only one proposer left, signifying that only one thread remains active. This situation marks the transition from massively parallel GPU execution to more suitable sequential execution on the CPU.



**How to Switch:** 

```
To effectively switch to the CPU, two key sub-questions must be addressed to determine the appropriate timing and method:
\begin{enumerate}
    \item How to ascertain if only one man remains unpaired.
    \item How to identify the free man's ID to proceed with the sequential algorithm.
\end{enumerate}

Determining if only one thread remains active relies on the \texttt{partnerRank} data structure, which is used during the execution of the parallel locality-aware GS algorithm. Since each woman's partner rank is initialized to \(n+1\), any rank value smaller than \(n+1\) indicates that the woman is paired, implying the presence of a paired man. If exactly one woman's partner rank is \(n+1\), it signifies that only one proposer remains free.

Identifying the ID of the free man involves additional computations. After reading the partner ranks of all women to confirm that only one woman is unpaired, the algorithm calculates the total sum of IDs of all men, which is \(1+2+\ldots+n=\frac{n(n+1)}{2}\). By subtracting the IDs of the paired men from this total sum, the algorithm determines the ID of the free man.

```

The above calculations are repeated until it is confirmed that only one proposer remains active and the free man is identified. At this point, the computation transitions from the GPU to the CPU to efficiently handle the remaining sequential steps. This is accomplished by copying the \texttt{partnerRank} from device memory to host memory and invoking the procedure in Algorithm 5 for the free man to make further proposals based on the existing \texttt{partnerRank}.



This transition leverages the CPU's strengths in managing tasks with limited parallelism and more complex control flow, thereby maintaining the overall efficiency of the GS algorithm execution.



## Description of Framework

The main procedure of this algorithm involves using both GPU and CPU to efficiently solve the Stable Marriage Problem (SMP) with a hybrid approach.

In Phase 1, the algorithm begins by initializing the number of unpaired women to \(n\) and the free man ID to the sum of all men's IDs. It then launches a kernel named \texttt{CheckMatchStatus} on GPU2. This kernel processes each woman in parallel. For each woman, it fetches the current match rank from GPU1 and stores it in another array on GPU2. If the woman's match rank is equal to \(n+1\), indicating that she is unpaired, an atomic operation decrements a counter for unpaired women, which was initialized to \(n\). Otherwise, the ID of the matched man is subtracted from the free man ID using an atomic subtraction based on the woman’s preference list.

After launching the \texttt{CheckMatchStatus} kernel, the algorithm copies the number of paired men, which is the same as the number of paired women, from the device to the host. If there is exactly one free man, the algorithm proceeds to copy the ID of the free man from the device to the host and then enters Phase 2. If not, the algorithm reinitializes the number of unpaired women and the free man ID, and launches the \texttt{CheckMatchStatus} kernel again to check if only one free man remains.

In Phase 2, the algorithm transitions to the CPU to handle the remaining tasks using a normal sequential Gale-Shapley algorithm. It identifies the free man and initializes the proposal rank.

This hybrid approach ensures that the initial parallel processing on the GPU efficiently handles the bulk of proposals, while any remaining complex decisions are managed on the CPU. This balance of workload leads to efficient computation and optimal performance.



## Unused

To illustrate, consider the following match ranks for the women:

- W1: 3 (paired with M3)
- W2: 𝑛+1*n*+1 (unpaired)
- W3: 1 (paired with M1)

In this example, the partner rank of W2 is 𝑛+1*n*+1, indicating that W2 is unpaired. We need to determine which man is free. First, read the partner ranks of all women: W1 is 3, W2 is 𝑛+1*n*+1 (unpaired), and W3 is 1. Confirm that only one woman is unpaired by checking that only one rank equals 𝑛+1*n*+1. Identify the indices of the paired men from the partner ranks of the women: W1 is paired with M3, so M3 is paired; W2 is unpaired; W3 is paired with M1, so M1 is paired. Calculate the total sum of indices of all men, which is 1+2+3=3(3+1)2=61+2+3=23(3+1)=6. Subtract the indices of the paired men from the total sum: Paired men indices are 1 (M1) + 3 (M3) = 4. The free man index is 6−4=26−4=2. Therefore, the free man is M2.



As show in Figure-5, Bamboo-SMP operates in three main stages:



Initialization of PRNodes on GPU1: Bamboo-SMP begins by initializing PRNodes on the first GPU (GPU1). These nodes contain the  information to perform the SMP computations in a regular access pattern.



Main Procedure of thread1: 

After initialization, thread1 starts execution of MIN Locality Unified CUDA Kernel on GPU1: Bamboo-SMP then launches the MIN Locality Unified CUDA Kernel on GPU1. This kernel processes the PRNodes in parallel, leveraging the GPU's computational power to handle the locality constraints and perform initial matching operations efficiently.



Main Procedure of thread2: 

The main procedure of thread2 involves the use of both the second GPU (GPU2) and the CPU to finalize the matching process. At the beginning, GPU2 is used to continuously check whether only one free man is left by launching the `CheckLessThanNUnified` kernel, which processes each woman in parallel and updates the ranks. When it is determined that only one free man remains, the algorithm transitions to the CPU. The CPU then handles the final stage of the matching process, utilizing its low latency to speed up the completion of the remaining tasks without the need for synchronization, ensuring a rapid convergence to a stable matching.



```
\begin{algorithm}
\caption{Hybrid GPU-CPU Algorithm for SMP}
\begin{algorithmic}[1]
\State \textbf{Input:} PRNodes, Preference lists for women, Rank matrix for men
\State \textbf{Output:} Women's Match Ranks, an array with $n$ entries, all initialized to $n+1$, indicating unpaired women

\State Initialize: number of unpaired women $\gets n$, free man ID $\gets \sum_{i=1}^{n} i$

\Repeat
    \State Launch `CheckMatchStatus` kernel on GPU2

    \For{each woman $w$ in parallel}
        \State Fetch the current match rank from GPU1
        \State Store the match rank in an array on GPU2
        \If{woman's match rank == $n+1$}
            \State Atomic decrement: unpaired women counter
        \Else
            \State Atomic subtraction: update free man ID based on woman’s preference list
        \EndIf
    \EndFor

    \State Copy the number of paired men from the device to the host
\Until{number of unpaired women == 1}

\State Copy the free man ID from the device to the host


\State \textbf{Phase 2: Sequential CPU Processing}

\State Identify the free man
\State Initialize proposal rank

\While{there are unpaired women}
    \State Free man proposes to the next woman on his list
    \State Increment current proposal rank
    \State Check the rank of the woman's current match
    \If{woman's current match has a better (lower) rank}
        \State Update node information for the next proposal
    \Else
        \If{woman's current match == $n+1$}
            \State Woman is paired, exit loop
        \Else
            \State Update current man ID to the woman's previous match
            \State Set the rank index for the new man
            \State Continue the while loop with the new man's preference list
        \EndIf
    \EndIf
\EndWhile

\end{algorithmic}
\end{algorithm}

% \begin{algorithm}[H]
% \caption{Main Procedure for Hybrid Relay Tailing with GPU to CPU Transition}
% \begin{algorithmic}[1]
% \State \textbf{Input:} $husband\_rank, cur\_p\_rank, n, split\_device\_pref\_list\_w$
% \State \textbf{Output:} Identify the free man and switch to CPU for remaining tasks

% \While{true}
%     \State Launch kernel \Call{CheckLessThanNUnified}{...}
%     \State Copy $temp\_result\_host$ from device to host

%     \If{$temp\_result\_host == 1$}
%         \State Copy $free\_man\_host$ from $free\_man\_device$ to host
%         \State \Call{HybridRelayTailingCPU}{$free\_man\_host$}
%         \State \textbf{break}
%     \EndIf
% \EndWhile

% \Procedure{CheckLessThanNUnified}{$husband\_rank, cur\_p\_rank, n, split\_husband\_rank, split\_cur\_p\_rank, free\_man\_idx, split\_device\_pref\_list\_w$}
%     \For{each woman $wi$ in parallel}
%         \State $hr \gets husband\_rank[wi]$
%         \State $split\_husband\_rank[wi] \gets hr$
%         \If{$hr == n$}
%             \State $atomicAdd(num\_unproposed, 1)$
%         \Else
%             \State $atomicSub(free\_man\_idx, split\_device\_pref\_list\_w[wi \cdot n + hr])$
%         \EndIf
%     \EndFor
% \EndProcedure

% \Procedure{HybridRelayTailingCPU}{$free\_man$}
%     \State $mi \gets free\_man$
%     \State Initialize $w\_rank \gets 0$
%     \State $node \gets split\_host\_node\_vector[mi \cdot n + w\_rank].node$
%     \State $w\_idx \gets node.w\_idx0$
%     \State $mi\_rank \gets node.m\_rank0$

%     \While{true}
%         \State $w\_rank \gets w\_rank + 1$
%         \State $mj\_rank \gets split\_husband\_rank[w\_idx]$
        
%         \If{$mj\_rank < mi\_rank$}
%             \State $node \gets split\_host\_node\_vector[mi \cdot n + w\_rank].node$
%             \State $w\_idx \gets node.w\_idx0$
%             \State $mi\_rank \gets node.m\_rank0$
%             \State \textbf{continue}
%         \EndIf
        
%         \State $split\_husband\_rank[w\_idx] \gets mi\_rank$
        
%         \If{$mj\_rank == n$}
%             \State \textbf{return}
%         \EndIf
        
%         \State $mj \gets split\_host\_pref\_list\_w[w\_idx \cdot n + mj\_rank]$
%         \State $mi \gets mj$
%         \State $w\_rank \gets smp.rank\_matrix\_m[mi][w\_idx] + 1$
        
%         \State $node \gets split\_host\_node\_vector[mi \cdot n + w\_rank].node$
%         \State $w\_idx \gets node.w\_idx0$
%         \State $mi\_rank \gets node.m\_rank0$
%     \EndWhile
% \EndProcedure
% \end{algorithmic}
% \end{algorithm}

```



# Section-Experiment

This section presents a comprehensive set of experiments conducted to demonstrate the performance of Bamboo-SMP and verify its superiority over existing algorithms



## Platforms / Experimental Environment

All implementations were evaluated on a desktop node at the Ohio Supercomputer Center (OSC), equipped with 2 AMD EPYC 7643 CPUs totaling 96 cores, 2 NVIDIA Tesla A100 GPUs, and 1TB of memory. The software environment included g++ version 11.2.0, cmake version 3.25.2, and nvcc version 12.3.52.



## Implementation / Baseline

Next, we developed state-of-the-art parallel versions of the GS and MW algorithms to demonstrate Bamboo-SMP’s high performance and superiority over existing algorithms across different scenarios. Specifically, the parallel MW algorithm was implemented for both the CPU using the C++ thread library and the GPU using CUDA. Similarly, the parallel GS algorithm was implemented on the CPU. These implementations serve as parallel baselines, providing a robust foundation for comparison.

In addition to the hybrid system used by Bamboo-SMP, we also implemented the Locality-Aware GS algorithm on both the CPU and GPU. For the GPU implementation, we created two versions of the Locality-Aware GS algorithm: one using `atomicCAS` as a contrast, and the other using `atomicMin`. This was done to specifically illustrate the effectiveness of the `atomicMin` function in resolving contention and enhancing efficiency.

By incorporating these techniques, we demonstrate that they are essential to Bamboo-SMP and significantly enhance its overall performance. The results confirm that the combination of locality-aware optimizations, advanced synchronization methods, and a heterogeneous computing system greatly improves the algorithm's efficiency, showcasing the robustness and superiority of Bamboo-SMP as a comprehensive solution.



## Workloads

To convincingly demonstrate the robustness of Bamboo-SMP and the effectiveness of the techniques employed, we tested it against baseline algorithms in various scenarios discussed in Section 3.1. By focusing on more complex and representative scenarios, we highlighted significant performance improvements and the versatility of Bamboo-SMP across different types of workloads. The best-case scenario was excluded due to its trivial nature, ensuring that our evaluations remained rigorous and meaningful.



### Solo Case

In the solo case, we tested algorithms with participant sizes ranging from 5,000 to 30,000, following the pattern shown in Figure 3. The preference lists for men and women were arranged such that, given n participants, there would be 
n^2−(n−1) proposals in total, with only n proposals made in parallel while the rest must be made serially.We test algorithms on Congested cases , as the same pattern as showed in Figure 3, of size with participants from 5000 to 30000.

All men have the exactly the same preference lists and no preference lists of woman are randomized.

And each preference lists is a randomly shifted list with all integers from 1 to n



### Congested Case

For the congested case, we also tested algorithms with participant sizes from 5,000 to 30,000, as shown in Figure 3. In this scenario, all men had identical preference lists, and the preference lists of women were randomized, with each list being a randomly shifted sequence of integers from 1 to n.



### Clustered Cases

In the clustered cases, we evaluated all implementations using real-world datasets from three distinct domains, processing them into three types of SMP instances: TAXI, ADM, and JOB. To simulate real-world SMP handling, agents were ordered by one main factor and divided into fixed groups, with the ranks of agents within each group randomized to reflect other factors influencing their judgments. 

In the TAXI instance, we simulate a common matching problem using real-world data from a mobility startup that allows users to book rides and data from the New York City Taxi and Limousine Commission. On the user side, participants rank drivers based on their ratings, creating groups for every 0.2 score interval. Conversely, drivers rank users by the number of orders, forming groups for every five orders.

For the ADM instance, we simulate the university admissions process using data about Indian applicants, which includes information on their education and experience gathered from candidate signups and enrollments.  Students are ranked by GPA, with groups formed for every 0.5 GPA interval. Universities are selected based on the top 50 rankings, each allotted 400 quotas. These quotas create groups of students, randomized within each group to simulate additional influencing factors.

The JOB instance simulates the job matching process using a dataset for data scientist positions and a dataset for candidate information. In this scenario, recruiters group applicants based on a three-order sort: major, degree, and work experience. These categories include groups such as "STEM - PhD - Has relevant experience" and "Non-STEM." Jobs are then ranked by salary, forming groups for every $10,000 interval.

All original datasets have been expanded to 20,000 participants using machine learning techniques (GAN model) or by proportional scaling. This expansion ensures the generality of the datasets and provides an extensive test environment to better reflect the performance of the algorithms.





# Parallel Results

The following sections present the results of our parallel algorithm implementations across different scenarios. These results highlight the performance benefits and trade-offs associated with the Locality-Aware GS implementation and underscore the robustness of Bamboo-SMP.

Bamboo-SMP’s intelligent switching mechanism and efficient utilization of both CPU and GPU resources ensure it maintains high performance across various scenarios, demonstrating its superiority as a comprehensive solution.



## Solo Case

In the sequential case, the sequential Locality-Aware GS on the CPU, as well as Bamboo-SMP, show the best performance. The parallel Locality-Aware GS on the CPU outperforms its GPU counterpart due to the CPU's low latency. In this scenario, parallelism does not offer a significant advantage; in fact, the synchronization method used by the parallel algorithm incurs additional overhead, causing the sequential Locality-Aware GS to outperform the parallel version. Its superior performance compared to other algorithms is attributed to efficient data movements. Bamboo-SMP maintains comparable performance by intelligently switching to the CPU when a certain threshold is reached, leveraging the strengths of both the CPU and GPU to optimize performance.



## Congested Case

For the congested case, the Locality-Aware GS using `atomicMin` on the GPU and Bamboo-SMP achieve the best results. The parallel MW algorithm on the GPU performs better than other parallel algorithms due to the GPU's high bandwidth. However, the Locality-Aware GS utilizing `atomicCAS` on the GPU outperforms the parallel MW algorithm because of more efficient data movements. The Locality-Aware GS with `atomicMin` further surpasses its `atomicCAS` counterpart by effectively eliminating wasted work. In this scenario, Bamboo-SMP's adaptive switching mechanism ensures that the GPU is always used for proposals in high-bandwidth environments, potentially avoiding switches when the thread count decreases gradually, thus maintaining optimal performance.



## Clustered Case

In the clustered case, the Locality-Aware GS using `atomicCAS` on the GPU, the Locality-Aware GS using `atomicMin` on the GPU, and Bamboo-SMP deliver the best performance. Although the degree of parallelism decreases, bandwidth remains critical, allowing the GPU to have a significant impact. Thanks to more efficient data movements, these implementations outperform the parallel MW algorithm on the GPU. Bamboo-SMP's ability to adaptively leverage both CPU and GPU resources ensures consistently high performance even as parallelism decreases, highlighting its robustness and flexibility across varying workloads.



# Sequential Experiement

To assess performance and illustrate the advantages of our locality-aware implementation of the GS algorithm, we implemented sequential versions of the GS algorithm and the MW algorithm in C++ as baselines. This comparison highlights the optimization of data access patterns in our locality-aware GS implementation.



To convincingly demonstrate the effectiveness of PRMatrix to exploit locality, we tested it against baseline algorithms in various scenarios discussed in Section 3.1. The best-case scenario was excluded due to its trivial nature. 



Figure 5 illustrates the overall performance of the three sequential algorithm implementations across 4 types of workloads as mentioned in section 3.1.

A key factor in this performance is that the preprocessing steps for initializing both the Rank Matrix and PRMatrix are completely independent and executed in GPU memory to utilize the high bandwidth of GPU for optimal speedup. This independence allows for concurrent processing, significantly reducing time overhead. 

As shown in Figure 6, although executing the GS algorithm on the CPU requires data transfer from the GPU to the CPU, which incurs a transfer cost,  this method can still achieve up to a 1000x speedup, which is crucial; otherwise, the preprocessing overhead would overshadow the execution phase. 

```
 current size is 100
1: Time to preprocess PRMatrices is 0.417014
1: Copy into GPU spends 0.035216 ms Initialization: Launch 79 blocks
1: GS InitNode spends 1.57369 ms
1: Copy back CPU spends 0.030678 ms Total number of threads is 12
1:
1:  current size is 500
1: Time to preprocess PRMatrices is 9.301425
1: Copy into GPU spends 0.121047 ms Initialization: Launch 1954 blocks
1: GS InitNode spends 0.027452 ms
1: Copy back CPU spends 0.115607 ms Total number of threads is 12
1:
1:  current size is 1000
1: Time to preprocess PRMatrices is 45.535019
1: Copy into GPU spends 0.30883 ms Initialization: Launch 7813 blocks
1: GS InitNode spends 0.044604 ms
1: Copy back CPU spends 0.826143 ms Total number of threads is 12
1:
1:  current size is 5000
1: Time to preprocess PRMatrices is 1876.570338
1: Copy into GPU spends 5.57246 ms Initialization: Launch 195313 blocks
1: GS InitNode spends 0.668707 ms
1: Copy back CPU spends 12.5789 ms Total number of threads is 12
1:
1:  current size is 10000
1: Time to preprocess PRMatrices is 7991.967678
1: Copy into GPU spends 19.8625 ms Initialization: Launch 781250 blocks
1: GS InitNode spends 2.65986 ms
1: Copy back CPU spends 50.4556 ms Total number of threads is 12
1:
1:  current size is 30000
1: Time to preprocess PRMatrices is 95754.668630
1: Copy into GPU spends 177.376 ms Initialization: Launch 7031250 blocks
1: GS InitNode spends 23.9874 ms
1: Copy back CPU spends 453.622 ms Total number of threads is 12
```





The Locality-Aware GS implementation includes an additional preprocessing step for PRMatrix initialization, resulting in extra overhead. Despite this slight increase in preprocessing time, the Locality-Aware GS consistently outperforms all other solutions. This minor overhead is negligible when compared to the substantial performance gains achieved.

In all three scenarios, the locality-aware implementation demonstrates over 50% faster execution times than the locality-unaware version. This significant improvement underscores the importance of optimizing data movement, as discussed in Section 3. These results confirm that addressing inefficient data movement can lead to remarkable enhancements in overall algorithm performance. Thus, the Locality-Aware GS implementation not only compensates for its initial overhead but also provides substantial runtime benefits.

we highlighted that the locality-aware implementation of GS algorithm achieves significant performance improvements in execution phase and that performance improvement outweighs the extra step to initialize PRMatrix in the preprocessing phase.   



# TODOs

*You need to label every figure/table/section as a variable so that you will connect to that variable instead of calling Figure X.*



*The latex file needs to be separated by sections instead of a single file.*



*Can you convert all the figures to standard ones without drawing?*



**GS algorithm is very intuitive to reach to the stable situation. In the last 60 years, are there any improved GS algorithms available. If so, readers may ask why don’t you parallelize the improved algorithms?**



**In your example explanation in 2.2., the concept of iterations is not very clear. You start from “first iteration”, but not other iterations are mentioned. In the GS algorithm continue until the last free man is matched. In the example of Figure 1, the number of iterations is 3 + 2is my understanding correct?**



**This example has an education purpose. The best case is n proposal times to end. The worst case is n^2 times. Your case is in the middle. If we use an example to cover all these cases, it would be nice. You don’t need to go over the worst case, but just give the preference ranks for man and each woman.**  



**In the paper we state that we will have a pre-processing step. This is a serious claim. Is this workload dependent? If so, for a given workload, we preprocess the sequential GS algorithm to determine data dependencies.**



**How much time do you need for this preprocessing on a single processor, what is the complexity for a group of n men and n woman. If n is one million.**



**What is the percentage of time of this preprocessing in the total execution time.**



**If we spend x seconds for preprocessing, and y seconds for parallel processing, what is x/(x+y)? Is it trivial?**



**If you add the parallel preprocessing and execution times together, what is the performance improvement percentage over the existing ones? We need to consider this preprocessing cost. Exploiting locality is a vehicle, not the goal. The goal is to significantly reduce the execution time.**  



**We need to argue the preprocessing time for locality is valuable so that overall performance is significantly reduced.**





**Each figure is an n*n array, it is easy to explain. For example, in the initiation stage, the first column of the matrix is accessed for each free man to propose to his top choice. You don’t need circles and squares with different colors to trace.**



## Unused / Backup

The specific methods for generating clustered preference lists with these groups are detailed in Table 1.



### Bike

We use bike sharing data2 to calculate distances from a start point to an end point as agent preferences on the 𝑋 side.
Agent preferences on the 𝑌 side are the values of orders for a bike on its start point; order values of follow a uniform distribution.



values of orders must range from the highest to lowest.

Due to the uniform distribution, there can be duplicate value of orders. Especially for those values that are quite similar.



We can randomize ranks that correspond to order with those similar values.



calculate distances from a start point to an end point as agent preferences on the 𝑋 side.

(1) Divide into Groups: criteria for vehicle types

(2) Distance: each group is further divided into groups for distances.

Those groups will randomize ranks and all nodes inside Each group for distances will randomize the rank



### TAXI

Matching agents with drivers is also a classical matching problem.



Driver Data:

This dataset coming from mobility startup that lets any user to book a ride to from any point A to any point B within the city using a smartphone.

https://kaggle.com/datasets/marcusrb/uber-peru-dataset



User data: 

data generated by The New York City Taxi and Limousine Commission (TLC)'s licensees to observe changing trends in the industry and inform decisions made by our agency and the City

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page



(1) User Side

The user will rank all drivers from highest rate to lowest rate. They will create a group for every 0.2 score interval.

all drivers that fall into the same interval will be considered as a group.



(2) Driver Side

The driver will rank all users from highest amount of order to lowest one.

They will create group for every 5 amount.

All users will fall into the same interval will be considered as a group.





### ADM

Matching students with universities is also a classical matching problem.



Student Data:

The dataset contains several parameters which are considered important during the application for Masters Programs.

https://www.kaggle.com/datasets/mohansacharya/graduate-admissions



(1) University Side:

Since the number of students (500) provided in this data set is quite limited, we use Machine Learning technique to expand the number of students to 20000,

then students will be ranked by their GPA, every 0.5 will form a group. 

Inside each group with close GPA, the ranks of students will be randomized to simulate other factor that affect the 



(2) Student Side:

We only choose top50 schools, and give each school 400 quotas, one quota for one student.

so the top school will have id from 1 to 400, which form a group. all students that matched with id from 1 to 400 will get enrolled in the first top school.

and second will have 401 to 800

The school will be listed from highest rank to lowest rank and students will randomize the ids inside each groups. Since all of them are the same, randomize the order won't affect which school to choose.



### JOB

Matching candidates with jobs



Job Data:

This dataset was created by picklesueat and contains more than 3900 job listing for data scientist positions, with features such as Salary Estimate

https://www.kaggle.com/datasets/andrewmvd/data-scientist-jobs



Applicant Data:

Information about indian applicants related to education, experience are in hands from candidates signup and enrollment.

https://www.kaggle.com/datasets/arashnic/hr-analytics-job-change-of-data-scientists





(1) Recruiter Side:

Group the applicants into categories by a three-order sort: major-degree-work experience, that are:     group_order = [
        "STEM - Phd - Has relevent experience",
        "STEM - Phd - No relevent experience",
        "STEM - Masters - Has relevent experience",
        "STEM - Masters - No relevent experience",
        "STEM - Graduate - Has relevent experience",
        "STEM - Graduate - No relevent experience",
        "Non-STEM Group"
    ]



(2) Worker Side:

Jobs will be ranked by Salary, every 10000 dollars will form a group



# Related Work

Newest Lu

\cite{wynn2024selection}





# Preprocessing

You need to answer the following questions for the preprocessing step:

1.Why the dependencies are hidden in logic programs and data structures, and can only be detected at the runtime execution, and why is it workload dependent?

"For efficient implementation of the basic Gale-Shapely algorithm", we need to be able to determine, in constant time, whether or  not woman prefers m to m' for arbitrary w, m and m'""

This can be achieved by using rank Matrix



2.After then, how is the new data structure created to exploit locality for parallel SMP execution?

Section-4.1



3.How much you can gain by this approach (speedup, latency reduction)?

on average 2.5x -> experimental



4.The preprocessing can also be done in parallel, what is the speedup?



5.are the preprocessing and parallel processing done one by one without reloading programs?

Yes



# Meeting

Problem: use the figure that we draw

Goal; give a question: Can we eliminate the time

Identify: talk about the dependency

New data structure: How to 

For reader: does this new data structure takes more overhead?

No free lunch

Space: constant increasement

Preprocessing Time: overhead is slow, why?

Totally independent + GPU => so super fast

And the best case is rare.
