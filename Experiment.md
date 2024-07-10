

This section presents a comprehensive set of experiments conducted to demonstrate the performance of Bamboo-SMP and verify its superiority over existing algorithms.



# Introduction

This section presents a comprehensive set of experiments conducted to demonstrate the performance of Bamboo-SMP, validate effectiveness of three techniques that it use in section 4, and verify its superiority over all existing algorithms.



# Experimental Setup

Other names: Platform, Experimental Environment

All implementations were evaluated on a desktop node at the Ohio Supercomputer Center (OSC), equipped with 2 AMD EPYC 7643 CPUs totaling 96 cores, 2 NVIDIA Tesla A100 GPUs, and 1TB of memory. The software environment included g++ version 11.2.0, cmake version 3.25.2, and nvcc version 12.3.52.





## Baseline Algorithms

To fairly compare the  performance and illustrate the effectiveness of all innovative techniques that we used in this paper, We have implemented 5  baseline algorithms:

    \item \textbf{GS-sequential-CPU}: A sequential GS on CPU.
    \item \textbf{MW-sequential-GPU}: A sequential MW on CPU.
    \item \textbf{GS-parallel-CPU}: A parallel GS on CPU.
    \item \textbf{MW-parallel-CPU}: A parallel MW on CPU.
    \item \textbf{MW-parallel-GPU}: A parallel MW on {\bf GPU}.



Specifically, the parallel MW algorithm was implemented for both the CPU using the C++ thread library and the GPU using CUDA. Similarly, the parallel GS algorithm was implemented on the CPU. These implementations serve as parallel baselines, providing a robust foundation for comparison.



## Datasets

Since there is no real-world SMP workloads exists, all of our experiements used synthesized data.  we have generated the workload of all types as described in the Figure 2 and of size up to size 30000, which is the largest data that we can use in our experiemal GPU.



# Performance

## Locality

To assess performance and illustrate the advantages of our locality-aware implementation of the GS algorithm (LA), we implemented sequential versions of the GS algorithm and the MW algorithm in C++ as baselines.



After tested the Locality-Aware (LA) implementation against baseline algorithms in various scenarios discussed in Section 3.1, excluding the perfect case scenario due to its trivial naturem, we provide a detailed analysis of the effectiveness of PRMatrix in exploiting locality and The overall performance is recorded in Table 1.



In section 3, we analyzed that the random access to rank matrix leads to inefficiency. After introducing PRMatrix, the locality-aware implementation achieves a significant speedup of in execution time in In all scenarios as described in Table1. 

After comparing the proportion of operation to read rank matrix in Figure 2 and the correspodning speedup in Table 1, the speedup matches the time.

This substantial improvement confirms that addressing inefficient data movement can lead to remarkable enhancements in overall algorithm performance.



## Contention Resolver

To validate the effectiveness of atomicMin in its ability in resolving the contention, we 

In addition to BambooKernel, we also implemented another versions of parallel-MW-GPU: 

original one still using `atomicCAS` as baseline, and the other using `atomicMin` to contrast : 

They are named parallel-MW-GPU(the-state-of-art algorithm) and parallel-MW-GPU-MIN, respectively.

To contrast the effectiveness of atomicMin over atomicCAS in its capability of eliminating wasted work and improve the efficency, 



we tested the parallel-MW-GPU, BambooKernel, and BambooKernel-noLocality on the congested cases from size 500 to 30000 and recorded the result in Figrue 6.

As we can see, in the Figure 6, the workload of 30000, the parallel-MW-GPU-CAS takes 366.280640ms, with the help to atomicMin, parallel-MW-GPU-MIN signifcantly reduces the number of retries of atomicCAS and achieves  188.755493 ms.

Further, thanks to the locality-exploitation,  BambooKernel reduces to 163.357407 ms.



## Hybrid

we tested all state-of-the-art both sequential and parallel versions of the GS and MW algorithms to compare it with Bamboo-SMP in congested case, random case, and solo case and the resulting the time of execution phase and the time of all phases,  recorded these. times in Table 3, 4, and 5 respectively.

These times demonstrate Bamboo-SMP’s high performance and superiority over existing algorithms across different scenarios. 

In addition to the hybrid system used by Bamboo-SMP, we also implemented the Locality-Aware GS algorithm on both the CPU and GPU. For the GPU implementation, we created two versions of the Locality-Aware GS algorithm: one using `atomicCAS` as a contrast, and the other using `atomicMin`. This was done to specifically illustrate the effectiveness of the `atomicMin` function in resolving contention and enhancing efficiency.

By incorporating these techniques, we demonstrate that they are essential to Bamboo-SMP and significantly enhance its overall performance. The results confirm that the combination of locality-aware optimizations, advanced synchronization methods, and a heterogeneous computing system greatly improves the algorithm's efficiency, showcasing the robustness and superiority of Bamboo-SMP as a comprehensive solution.



To convincingly demonstrate the robustness of Bamboo-SMP and the effectiveness of the techniques employed, we tested it against baseline algorithms in various scenarios discussed in Section 3.1. By focusing on more complex and representative scenarios, we highlighted significant performance improvements and the versatility of Bamboo-SMP across different types of workloads. The best-case scenario was excluded due to its trivial nature, ensuring that our evaluations remained rigorous and meaningful.



The following sections present the results of our parallel algorithm implementations across different scenarios. These results highlight the performance benefits and trade-offs associated with the Locality-Aware GS implementation and underscore the robustness of Bamboo-SMP.

Bamboo-SMP’s intelligent switching mechanism and efficient utilization of both CPU and GPU resources ensure it maintains high performance across various scenarios, demonstrating its superiority as a comprehensive solution.



```
Although the LA implementation includes an extra preprocessing step for PRMatrix initialization, resulting in additional overhead, it consistently outperforms all other solutions. As shown in Table 1, the increased preprocessing time is negligible compared to the significant performance gains achieved.

While the preprocessing step may overshadow performance improvements in the random case, where each man orders women completely randomly, this scenario is exceedingly rare. In real-world applications, such as the hospital-residency matching problem, preference lists are often influenced by factors like institutional reputation, specialty interests, and geographic location. These factors create patterns and preferences that are far from random, ensuring the random case is not representative of actual use cases. Thus, the performance gains observed in more realistic scenarios are far more relevant and significant.
```



# Where does time go?



# Unused

## Solo

In the sequential case, the sequential Locality-Aware GS on the CPU, as well as Bamboo-SMP, show the best performance. The parallel Locality-Aware GS on the CPU outperforms its GPU counterpart due to the CPU's low latency. In this scenario, parallelism does not offer a significant advantage; in fact, the synchronization method used by the parallel algorithm incurs additional overhead, causing the sequential Locality-Aware GS to outperform the parallel version. Its superior performance compared to other algorithms is attributed to efficient data movements. Bamboo-SMP maintains comparable performance by intelligently switching to the CPU when a certain threshold is reached, leveraging the strengths of both the CPU and GPU to optimize performance.



## Random

In the clustered case, the Locality-Aware GS using `atomicCAS` on the GPU, the Locality-Aware GS using `atomicMin` on the GPU, and Bamboo-SMP deliver the best performance. Although the degree of parallelism decreases, bandwidth remains critical, allowing the GPU to have a significant impact. Thanks to more efficient data movements, these implementations outperform the parallel MW algorithm on the GPU. Bamboo-SMP's ability to adaptively leverage both CPU and GPU resources ensures consistently high performance even as parallelism decreases, highlighting its robustness and flexibility across varying workloads.



## Congested

For the congested case, the Locality-Aware GS using `atomicMin` on the GPU and Bamboo-SMP achieve the best results. The parallel MW algorithm on the GPU performs better than other parallel algorithms due to the GPU's high bandwidth. However, the Locality-Aware GS utilizing `atomicCAS` on the GPU outperforms the parallel MW algorithm because of more efficient data movements. The Locality-Aware GS with `atomicMin` further surpasses its `atomicCAS` counterpart by effectively eliminating wasted work. In this scenario, Bamboo-SMP's adaptive switching mechanism ensures that the GPU is always used for proposals in high-bandwidth environments, potentially avoiding switches when the thread count decreases gradually, thus maintaining optimal performance.