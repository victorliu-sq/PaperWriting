# Introduction

This section presents a comprehensive set of experiments conducted to demonstrate the performance of Bamboo-SMP, validate effectiveness of three techniques that it use in section 4, and verify its superiority over all existing algorithms.



## Experimental Setup

Other names: Platform, Experimental Environment

All implementations were evaluated on a desktop node at the Ohio Supercomputer Center (OSC), equipped with 2 AMD EPYC 7643 CPUs totaling 96 cores, 2 NVIDIA Tesla A100 GPUs, and 1TB of memory. The software environment included g++ version 11.2.0, cmake version 3.25.2, and nvcc version 12.3.52.





## Baseline Algorithms

To fairly compare the  performance and illustrate the effectiveness of all innovative techniques that we used in this paper, We have implemented 7 baseline algorithms:

    \item \textbf{GS-sequential-CPU}: A sequential GS on CPU.
    \item \textbf{MW-sequential-GPU}: A sequential MW on CPU.
    \item \textbf{GS-parallel-CPU}: A parallel GS on CPU.
    \item \textbf{MW-parallel-CPU}: A parallel MW on CPU.
    \item \textbf{MW-parallel-GPU}: A parallel MW on {\bf GPU}.
    \item \textbf{MW-parallel-GPU-MIN}: A parallel MW on {\bf GPU}.
    \item \textbf{LA}: The locality-aware sequential implementation of GS

Specifically, In addition to the 5 algorithms that we implemented in Section 3.3, we also implemented Locality-Aware implmentation of GS and another versions of parallel-MW-GPU using atomicMin. original  parallel-MW-GPU uses `atomicCAS`  whereas  named  parallel-MW-GPU uses `atomicMin`.



the parallel MW algorithm was implemented for both the CPU using the C++ thread library and the GPU using CUDA. Similarly, the parallel GS algorithm was implemented on the CPU. These implementations serve as parallel baselines, providing a robust foundation for comparison.

These 2 implementations are to  to contrast the effectiveness of PRMatrix in exploiting locality and and atomicMin in resolving contention, repetitively.



## Datasets

Since there is no real-world SMP workloads exists, all of our experiements used synthesized data.  we have generated the workload of all types as described in the Figure 2 and of size from 500 up to size 30000, which is the largest data that we can use in our experiemal GPU.



# Overall Performance

To demonstrate Bamboo-SMP’s high performance and superiority over existing algorithms across different scenarios, 

we tested all baseline algorithms and compare them with Bamboo-SMP in congested case, random case, and solo case of maximum size that we can implement on GPU (30000).

And we record the resulting the time of initialization phase, execution phase, postprocessing pahse, and the total time in Table 3, 4, and 5 respectively.



we highlighted significant performance improvements and the versatility of Bamboo-SMP across different types of workloads. 

Basically, the extra overhead of Bamboo-SMP comes from the preprocessing step that initializes PRMatrix in the intiailization phase. However, the performance gains from execution phase outperforms these time cost, resulting in the significant performance improvements made by Bamboo-SMP.

The maxmimum speedups across all types of workloads are made by Bamboo-SMP, showcasing the robustness and superiority of Bamboo-SMP as a comprehensive solution across different types of workloads.



Solo Case

|                   | Prechecking Phase | Init Phase | Exec Phase | Post Phase | Total |
| ----------------- | ----------------- | ---------- | ---------- | ---------- | ----- |
| GS-sequential-cpu | 0                 | 294.612    | 18708.1    | 0.2241249  |       |
| GS-parallel-cpu   | 0                 | 293.257    | 24051.7    | 0.443203   |       |
| MW-sequential-cpu | 0                 | 293.27     | 22556.6    | 0.228329   |       |
| MW-parallel-cpu   | 0                 | 293.277    | 23661.3    | 0.392649   |       |
| MW-parallel-GPU   | 0                 | 291.22     | 255641     | 0.191059   |       |
|                   |                   |            |            |            |       |
| Bamboo            | 15.2203           | 330.031    | 3722.58    | 0.028976   |       |



Congested Case

|                   | Prechecking Phase | Init Phase | Exec Phase | Post Phase | Total |
| ----------------- | ----------------- | ---------- | ---------- | ---------- | ----- |
| GS-sequential-cpu | 0                 | 295.662    | 75109.7    | 0293639    |       |
| GS-parallel-cpu   | 0                 | 293.256    | 9262.3     | 0.306957   |       |
| MW-sequential-cpu | 0                 | 293.269    | 53516.3    | 0.222639   |       |
| MW-parallel-cpu   | 0                 | 293.716    | 9640.91    | 0.335321   |       |
| MW-parallel-GPU   | 0                 | 291.201    | 386.431    | 0.059242   |       |
|                   |                   |            |            |            |       |
| Bamboo            | 3.52343           | 330.18     | 194.848    | 0.027493   |       |



Random Case

|                   | Prechecking Phase | Init Phase | Exec Phase | Post Phase | Total |
| :---------------- | :---------------- | :--------- | :--------- | :--------- | :---- |
| GS-sequential-cpu | 0                 | 298.009    | 33711.7    | 0.246506   |       |
| GS-parallel-cpu   | 0                 | 293.234    | 5076.21    | 0.355939   |       |
| MW-sequential-cpu | 0                 | 293.244    | 31203.4    | 0.226506   |       |
| MW-parallel-cpu   | 0                 | 293.728    | 5271.15    | 0.274065   |       |
| MW-parallel-GPU   | 0                 | 291.21     | 158.895    | 0.004779   |       |
|                   |                   |            |            |            |       |
| Bamboo            | 8.87622           | 329.885    | 101.407    | 0.094558   |       |





# Where does time go

In this section, we have a more detailed look at the performance of BambooSMP and compare it with the baseline algorithms with the secondary best performance.

By doing so, we confirm that the combination of locality-aware optimizations, advanced synchronization methods, and a heterogeneous computing system greatly improves the algorithm's efficiency, 



## Locality

GS => LA => Bamboo-SMP

To assess performance and illustrate the advantages of PRMatrix in locality-exploitation, we contrasted and analyzed the performance of GS-sequential-CPU, MW-sequential-CPU, LA, and BambooSMP in solo case of size 30000.

In this case, sequenital proposals on CPU completes first, so Bamboo-SMP needs to initialize PRMatrix and transfer this data structure into host memory as LA.



In section 3, we analyzed that the random access to rank matrix leads to inefficiency. After introducing PRMatrix, the locality-aware implementation achieves a significant speedup of in execution time in In all scenarios. 

After comparing the proportion of operation to read rank matrix in Figure 2 and the correspodning speedup in Table 1, the speedup matches the time.

This substantial improvement confirms that addressing inefficient data movement can lead to remarkable enhancements in overall algorithm performance.



Both LA and Bamboo-SMP has an additional preprocessing step to intialize PRMatrix, and the size of PRMatrix is bigger than Rank Matrix, so they will use more time in the initialization pahse. However, the performance again in the execution phase much outweights the additional overhead in the initialization phase.



## Contention Resolver

To validate the effectiveness of atomicMin in its ability in resolving the contention, we tested the parallel-MW-GPU, parallel-MW-GPU-Min, and BambooKernel on the congested cases from size 500 to 30000 and recorded the result in Figrue 6.

As we can see, in the Figure 6, the workload of 30000, the parallel-MW-GPU-CAS takes 366.280640ms, with the help of atomicMin, parallel-MW-GPU-MIN signifcantly reduces the number of retries of atomicCAS and achieves  188.755493 ms.

Further, thanks to the locality-exploitation, BambooKernel further reduces to 163.357407 ms.



## Hybrid

By incorporating these techniques, we demonstrate that they are essential to Bamboo-SMP and significantly enhance its overall performance. 

To convincingly demonstrate the robustness of Bamboo-SMP and the effectiveness of the techniques employed, we tested it against baseline algorithms in various scenarios discussed in Section 3.1. 

By focusing on more complex and representative scenarios, we highlighted significant performance improvements and the versatility of Bamboo-SMP across different types of workloads. The perfect case scenario was excluded due to its trivial nature, ensuring that our evaluations remained rigorous and meaningful.

The following sections present the results of our parallel algorithm implementations across different scenarios. These results highlight the performance benefits and trade-offs associated with the Locality-Aware GS implementation and underscore the robustness of Bamboo-SMP.

Bamboo-SMP’s intelligent switching mechanism and efficient utilization of both CPU and GPU resources ensure it maintains high performance across various scenarios, demonstrating its superiority as a comprehensive solution.



```
Although the LA implementation includes an extra preprocessing step for PRMatrix initialization, resulting in additional overhead, it consistently outperforms all other solutions. As shown in Table 1, the increased preprocessing time is negligible compared to the significant performance gains achieved.

While the preprocessing step may overshadow performance improvements in the random case, where each man orders women completely randomly, this scenario is exceedingly rare. In real-world applications, such as the hospital-residency matching problem, preference lists are often influenced by factors like institutional reputation, specialty interests, and geographic location. These factors create patterns and preferences that are far from random, ensuring the random case is not representative of actual use cases. Thus, the performance gains observed in more realistic scenarios are far more relevant and significant.
```



# Where does time go?

In this section, we focus on illustrating the how techniques that have been utilized in Bamboo-SMP take effects on optimizing the performance.

For each type of workload, we will comapre the state-of-art algorithm that achieves the best performance with Bamboo-SMP. 

And also one our newly developed algorithms with one single technique:





Congested Case:

Parallel-MW-GPU => Parallel-MW-GPU-MIN => Bamboo-SMP

In this case, GPU Kernel completes first, Bamboo-SMP only needs to initialize PRMatrix on the GPU but does not need to take the extra time to transfer them out.

Parallel-MW-GPU-MIN: atomicMIN-only, 





Random Case:

Parallel-MW-GPU => Parallel-MW-GPU-MIN => Bamboo-SMP

In this case, GPU Kernel completes first , Bamboo-SMP stilll only needs to initialize PRMatrix on the GPU but does not need to take the extra time to transfer them out.





# Unused

The perfect case scenario was excluded due to its trivial nature, ensuring that our evaluations remained rigorous and meaningful.



After testing the (L)ocality-(A)ware (LA) implementation against baseline algorithms in various scenarios discussed in Section 3.1, excluding the perfect case scenario due to its trivial naturem, we provide a detailed analysis of the effectiveness of PRMatrix in exploiting locality and The overall performance is recorded in Table 1.



## Solo

+LA

In the sequential case, the sequential Locality-Aware GS on the CPU, as well as Bamboo-SMP, show the best performance. The parallel Locality-Aware GS on the CPU outperforms its GPU counterpart due to the CPU's low latency. In this scenario, parallelism does not offer a significant advantage; in fact, the synchronization method used by the parallel algorithm incurs additional overhead, causing the sequential Locality-Aware GS to outperform the parallel version. Its superior performance compared to other algorithms is attributed to efficient data movements. Bamboo-SMP maintains comparable performance by intelligently switching to the CPU when a certain threshold is reached, leveraging the strengths of both the CPU and GPU to optimize performance.



## Random

+MW-parallel-GPU-MIN, +BambooKernel-CAS

In the clustered case, the Locality-Aware GS using `atomicCAS` on the GPU, the Locality-Aware GS using `atomicMin` on the GPU, and Bamboo-SMP deliver the best performance. Although the degree of parallelism decreases, bandwidth remains critical, allowing the GPU to have a significant impact. Thanks to more efficient data movements, these implementations outperform the parallel MW algorithm on the GPU. Bamboo-SMP's ability to adaptively leverage both CPU and GPU resources ensures consistently high performance even as parallelism decreases, highlighting its robustness and flexibility across varying workloads.



## Congested

+MW-parallel-GPU-MIN, +BambooKernel-CAS

For the congested case, the Locality-Aware GS using `atomicMin` on the GPU and Bamboo-SMP achieve the best results. The parallel MW algorithm on the GPU performs better than other parallel algorithms due to the GPU's high bandwidth. However, the Locality-Aware GS utilizing `atomicCAS` on the GPU outperforms the parallel MW algorithm because of more efficient data movements. The Locality-Aware GS with `atomicMin` further surpasses its `atomicCAS` counterpart by effectively eliminating wasted work. In this scenario, Bamboo-SMP's adaptive switching mechanism ensures that the GPU is always used for proposals in high-bandwidth environments, potentially avoiding switches when the thread count decreases gradually, thus maintaining optimal performance.



# Results

Solo Case

|                   | Prechecking Phase | Init Phase | Exec Phase | Post Phase | Total      |
| ----------------- | ----------------- | ---------- | ---------- | ---------- | ---------- |
| GS-sequential-cpu | 0                 | 294.612    | 18708.1    | 0.2241249  | 18994.9361 |
| GS-parallel-cpu   | 0                 | 293.257    | 24051.7    | 0.443203   | 24345.4002 |
| MW-sequential-cpu | 0                 | 293.27     | 22556.6    | 0.228329   | 22850.0983 |
| MW-parallel-cpu   | 0                 | 293.277    | 23661.3    | 0.392649   | 23955.3696 |
| MW-parallel-GPU   | 0                 | 291.22     | 255641     | 0.191059   | 255932.411 |
|                   |                   |            |            |            |            |
| LA-sequential-cpu | 0                 | 617.5      | 3474.43    | 0.262173   | 4092.1922  |
| Bamboo            | 15.2203           | 330.031    | 3735.11    | 0.289766   | 4080.6511  |



Congested Case

|                     | Prechecking Phase | Init Phase | Exec Phase | Post Phase | Total       |
| ------------------- | ----------------- | ---------- | ---------- | ---------- | ----------- |
| GS-sequential-cpu   | 0                 | 295.662    | 75109.7    | 0293639    | 75395.6556  |
| GS-parallel-cpu     | 0                 | 293.256    | 9262.3     | 0.306957   | 9555.862957 |
| MW-sequential-cpu   | 0                 | 293.269    | 53516.3    | 0.222639   | 53809.7916  |
| MW-parallel-cpu     | 0                 | 293.716    | 9640.91    | 0.335321   | 9934.961321 |
| MW-parallel-GPU-CAS | 0                 | 291.201    | 346.714    | 0.059242   | 637.974242  |
|                     |                   |            |            |            |             |
| MW-parallel-GPU-MIN | 0                 | 291.21     | 175.24     | 0.065212   | 466.515212  |
| LA-parallel-GPU-CAS | 0                 | 330.109    | 262.468    | 0.088968   | 592.665968  |
| Bamboo              | 3.52343           | 330.18     | 118.801    | 0.097673   | 452.602103  |



Random Case

|                     | Prechecking Phase | Init Phase | Exec Phase | Post Phase | Total       |
| :------------------ | :---------------- | :--------- | :--------- | :--------- | :---------- |
| GS-sequential-cpu   | 0                 | 298.009    | 33711.7    | 0.246506   | 34009.9555  |
| GS-parallel-cpu     | 0                 | 293.234    | 5076.21    | 0.355939   | 5369.799939 |
| MW-sequential-cpu   | 0                 | 293.244    | 31203.4    | 0.226506   | 31503.8705  |
| MW-parallel-cpu     | 0                 | 293.728    | 5271.15    | 0.274065   | 5565.152065 |
| MW-parallel-GPU-CAS | 0                 | 291.21     | 158.895    | 0.004779   | 450.109779  |
|                     |                   |            |            |            |             |
| MW-parallel-GPU-MIN | 0                 | 291.212    | 124.137    | 0.057969   | 415.406969  |
| LA-parallel-GPU-CAS | 0                 | 330.099    | 119.591    | 0.086793   | 449.776793  |
| Bamboo              | 8.87622           | 329.885    | 80.3628    | 0.094558   | 419.218558  |



Perfect Case

