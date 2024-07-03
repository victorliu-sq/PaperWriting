# SMP

The Stable Marriage Problem (SMP) involves two groups of participants, often referred to as men and women. Each participant has a ranked preference list of all members from the opposite group. Figure \ref{fig:GSExecution} gives a simple SMP example to match three men and three women, where the two groups are \(\{M_1, M_2, M_3\}\) for men and \(\{W_1, W_2, W_3\}\) for women. Each member in \(\{M_1, M_2, M_3\}\) ranks all members in \(\{W_1, W_2, W_3\}\) in a strict order, and vice versa.



Given these two groups, a matching is a one-to-one correspondence from participants in one group to those in the other. A blocking pair in a given matching is a pair of participants from opposite groups who would both prefer each other over their current partners. If such a pair exists, the matching is unstable because these two participants would be motivated to leave their assigned partners and pair up with each other instead. The goal of the SMP is to find a stable matching, where no blocking pairs exist. In other words, a matching is stable if no two participants prefer each other over their current partners.



# Sequential 

## GS

The Gale-Shapley (GS) algorithm, also known as the Deferred Acceptance algorithm, is a foundational method for solving the Stable Marriage Problem (SMP). Proposed by David Gale and Lloyd Shapley in 1962, the GS algorithm guarantees finding a stable matching between two equally sized sets of participants, typically referred to as men and women, each with their own preference lists. The GS algorithm begins with all participants being unmatched. In each iteration, an unmatched man proposes to the highest-ranked woman on his preference list who has not previously rejected him. If the woman is unmatched or prefers the new proposer over her current partner, she tentatively accepts the proposal, freeing her current partner if necessary. If she prefers her current partner, she rejects the new proposal, and the man remains unmatched. This process is repeated until all participants are matched.





The GS algorithm has 4 stages:

1.the beginning step

In the beginning step, each participant selects their preferred option from their preference lists, and a corresponding match is established. If all participants have unique top choices, the matching is considered stable, making further steps unnecessary and resulting in an overall time complexity of O(n). Otherwise, the process moves to the initialization step to prepare data structures for further proposals.



The GS algorithm begins with all participants being unmatched. 



2.the initialization step

In this step, the algorithm creates a matrix called  \textbf{Rank Matrix} , which allows the algorithm to determine the rank of a man in a woman’s preference list in constant time. For instance,  \text{RankMatrix}[w, m]  gives the rank of man  $m$  in woman  $w$ ’s preference list. In addition, the GS algorithm initializes with all participants being unmatched. 



3.the execution step

After the initialization step, the algorithm runs a loop until all participants are matched. In each iteration, an unmatched man proposes to the highest-ranked woman on his preference list who has not previously rejected him. If the woman is unmatched or prefers the new proposer over her current partner, she tentatively accepts the proposal, freeing her current partner if necessary. If she prefers her current partner, she rejects the new proposal, and the man remains unmatched. 



This process is repeated until all participants are matched.



4.the postprocessing step

Once the main loop finishes, each woman looks up her current partner’s rank in her preference list to identify her final partner to construdct the final stable matching.





Initial preparation for workload related data structures, including RankMatrix, Pref-List and others. This process is required for each SMP processing. We call this process *initialization.*

Prechecking whether the workload is a perfect case or not. We call this process *prechecking*





The implementation details of the GS algorithm are described in Algorithm \texttt{\ref{Algo:GSAlgo}}. 







Both the initialization of the RankMatrix and the main loop have \(O(n^2)\) complexity. Therefore, the overall time complexity of the algorithm is \(O(n^2)\).



The initialization of entries in the \( \texttt{RankMatrix} \) and the postprocessing of \( \texttt{PartnerRank} \) are completely independent for each entry. This independence allows these phases to be fully parallelized, meaning that with sufficient processing units, they can be done in constant time. Therefore, we focus on the execution phase in the performance analysis presented in this paper.



Let us consider the preference lists in Figure \ref{fig:GSExecution} to understand the execution flow of the Gale-Shapley algorithm. Initially, all participants are free. In the beginning step, each man proposes to his top choice in the first column of the matrix in Figure \ref{fig:GSExecution}. Thus, \(M_1\) proposes to \(W_2\), the highest-ranked woman on on his list. \(W_2\) tentatively accepts because she does not have anyone to compare although this is not her best choice, resulting in the tentative match \((M_1, W_2)\). Next, \(M_2\) proposes to \(W_2\). Since \(W_2\) prefers \(M_2\) over \(M_1\), she accepts \(M_2\)'s proposal and rejects \(M_1\), thereby freeing \(M_1\). The tentative match is now \((M_2, W_2)\). Then, \(M_3\) proposes to \(W_2\), but \(W_2\) prefers \(M_2\) over \(M_3\), so she rejects \(M_3\). The tentative match remains \((M_2, W_2)\). After the beginning step, if no man is rejected, this is called the best case of stable matching with a complexity of $O(n)$, where $n$ is the number of participants. However, this scenario is not only rare, but also does not have any challenge in parallel processing due to its  parallelism property. In the case of Figure \ref{fig:GSExecution}, after the initiation, as a free (rejected) man, \(M_1\) proposes to \(W_1\), the next highest-ranked woman who has yet to reject him in the second column in Men's preference Lists in Figure \ref{fig:GSExecution}. \(W_1\) tentatively accepts, resulting in the match \((M_1, W_1)\) alongside \((M_2, W_2)\). Subsequently, free man \(M_3\) proposes to \(W_1\). Since \(W_1\) prefers \(M_3\) over \(M_1\), she accepts \(M_3\)'s proposal and rejects \(M_1\). The tentative matches are now \((M_3, W_1)\) and \((M_2, W_2)\). Becoming a free man again, \(M_1\) proposes to \(W_3\), the next available woman on his list. \(W_3\) accepts \(M_1\)'s proposal as her best choice, resulting in the match \((M_1, W_3)\) alongside \((M_3, W_1)\) and \((M_2, W_2)\). Now every participant has been matched, so the algorithm terminates with the following stable matching: \((M_1, W_3), (M_2, W_2), \text{ and } (M_3, W_1)\).
 In this matching, there are no blocking pairs because no two individuals prefer each other over their current partners, ensuring that the matching is stable.



### Unused

The \( \text{Q} \) is a queue that keeps track of free men. Initially, all men are free and added to the queue. 

The \( \text{Next} \) array records, for each man, the rank of the highest-priority woman who hasn't rejected him yet. This array allows each man to propose to women in his preference list in order without rechecking previously rejected proposals. At the start, each man proposes to the woman he prefers the most, so all ranks stored in \( \text{Next} \) are set to 1. The \( \text{PartnerRank} \) array stores the rank of the current partner of each woman. Initially, the partner rank for each woman is set to \( n+1 \), indicating they are all unmatched.



After intialization step, data structures are prepared, the algorithm runs a main loop until there are no free men left in the queue. In each iteration, a man \( m \) is taken from the queue to propose to the highest-priority woman who hasn't rejected him yet. After each proposal, the man increments his rank to move to the next woman on his preference list for future proposals. The algorithm then checks the rank of this man in the woman’s preference list and compares it to the rank of her current partner. If the woman's current partner is ranked higher (lower numerical value) than the proposing man, the proposing man (\( m \)) remains free and is added back to the queue. Otherwise, the proposing man's partner rank is updated to \( m\_rank \). If the woman is already paired (i.e., \( p\_rank \neq n + 1 \)), the previous partner (\( p \)), identified from the woman's preference list, becomes free and is added back to the queue. 





For each man, the algorithm tracks the highest-priority woman who hasn’t rejected him yet, allowing him to propose sequentially according to his preference list without repeating proposals. At the start, each man proposes to his top choice. Additionally, the algorithm keeps track of each woman’s current partner and their rank in her preference list. Initially, all women are considered unmatched, indicating they have no current partner.



## MW

The McVitie and Wilson (MW) algorithm is essentially another implementation of the GS algorithm, based on the principle that the proposal order does not affect the resulting stable matching. 

In the GS algorithm, all unmatched men will be placed into a queue. For each iteration in the main loop, a unmatched man must be take from that queue before make proposals and the rejected man will be re-added back to the queue.

In the MW algorithm, however, if a proposer is rejected by the woman he is proposing to, he immediately moves on to propose to the next woman on his list, rather than being added back to a queue. Similarly, if a woman accepts a new proposal, her previous partner will continue to propose to his next preference, instead of being pushed back to a queue. 

This streamlined proposal process eliminates the need for a queue to manage unmatched individuals.Also , it provides opportunities for further optimization  and is employed in our algorithm to achieve massive paralleism on GPU.



### Unused

thereby reducing the time overhead associated with this task. 

The key distinctions between the MW and GS algorithms lie in their execution phases. The MW algorithm iterates through every man and invokes a recursive procedure for free men to make proposals. When a man enters this recursive procedure, he proposes to his highest-ranked woman who has not yet rejected him. If the woman is unpaired, her partner rank is updated as in the GS algorithm. Additionally, the way rejected proposals are handled is a major difference. 







# Parallel

Both GS and MW algorithm can be parallelized using the same techqniue called atomicCAS.





## PGS-CPU or PMW-CPU





## PMWKernel-GPU

Implementing the Gale-Shapley algorithm on the GPU
presents additional challenges compared to the McVitie-
Wilson algorithm. In a Gale-Shapley algorithm the threads
would have to be grouped so that each thread group operates
on one common queue, where the size of the group could
be either a subset of threads in a warp or all the threads
in one thread block. As the number of free men monoton-
ically decreases between rounds, there should initially be
more men than threads assigned to the same queue, some-
thing that would complicate the algorithm. Also, having sev-
eral threads operate on one common queue would require
synchronization which can be time consuming on the GPU.
For this reason we chose not to implement the Gale-Shapley
algorithm using CUDA.





## Draft

```
Although the GS algorithm exhibit certain parallelism because multiple men can propose simultaneously \cite{mcvitie1971stable}, efficiently parallelizing it is a non-trivial task. In a multi-core system or a GPU system, each thread can represent a man, allowing men to make their proposals independently. While multiple threads can read the partner's rank of the same woman without synchronization, updating the partner's rank must be done carefully to prevent simultaneous changes by other threads, ensuring that the woman is paired with her best choice. 

Specifically, in Algorithm \ref{Algo:GSAlgo}, the operation on line 18 can be executed without synchronization, but the operation on line 22 requires synchronization to ensure that the woman accepts the best proposal. 

While it may seem to be straightforward to use locks and barrier synchronization to ensure that each woman accepts the best proposal, both methods inherently hinder the efficiency and scalability of parallelizing the GS algorithm. Locks ensure exclusive access to the partner rank for each woman by requiring all threads to lock the data before updating the state of the match. 

Since the GS algorithm requires frequent and fine-grained updates to the partner rank for each woman, this method introduces significant overhead due to the frequent acquisition and release of locks. On the other hand, barrier synchronization forces all threads to wait at fixed points before any can proceed. In the context of the GS algorithm, this means making all men wait at a barrier after making proposals, allowing each woman to accept the best proposal and reject the rest before letting all threads continue. However, not all threads need to be synchronized simultaneously when parallelizing the GS algorithm. Some men may be rejected and need to propose again, while others are accepted without competition. As a result, using barrier synchronization leads to idle time and poor resource utilization.

The atomicCAS (Compare-And-Swap) operation is an atomic instruction used to compare a memory location's current value with an expected value and, if they match, swap it with a new value. If they do not match, the operation returns the old value, indicating the update was unsuccessful. This operation is performed atomically, ensuring no other thread can interfere during the process.

Algorithm \ref{Algo:parallelGS} is a parallel implementation of lines 19-27 from Algorithm \ref{Algo:GSAlgo} and is a critical component used in both the parallel GS and parallel MW algorithms to ensure that updates to \texttt{partnerRank} are done atomically, preventing race conditions. The way atomicCAS makes sense is that if a thread finds that \texttt{m\_rank} is lower than the partner's rank, it attempts to update \texttt{partnerRank} with \texttt{m\_rank} using atomicCAS. If the returned \texttt{partner\_rank} does not match \texttt{p\_rank} and \texttt{m\_rank} is still lower, the operation fails and will be retried with the returned partner rank. The only difference between these two parallel versions of GS algorithms lies in handling the rejected man on line 7. In the parallel GS algorithm, if the returned rank of the current partner \texttt{p\_rank2} matches the expected \texttt{p\_rank}, the operation succeeds, and the rejected man is pushed to the \texttt{FreeManQueue} for further proposals. To prevent data races, each thread has its own \texttt{FreeManQueue}. In contrast, the parallel MW algorithm allows the thread representing the rejected man to propose again.


```







# Code

```
\begin{algorithm}
\caption{The Gale-Shapley Algorithm}
\label{Algo:GSAlgo}
\footnotesize  % Makes the text smaller
\begin{algorithmic}[1]

\newcommand{\StateNoLine}[1]{\Statex \hspace*{-\algorithmicindent} #1}
\newcommand{\CommentNoLine}[1]{\hfill \(\triangleright\) #1}

\StateNoLine{\textbf{Input:}  $PrefListsM$ and $PrefListsW$} \CommentNoLine{Preference Lists}
\StateNoLine{\textbf{Output:} $S$}  \CommentNoLine{The stable matching}

% \StateNoLine{\textbf{Preprocessing Phase:}}
\Procedure{GS}{}
    \State $done$ $\gets$ \Call{beginGS}{ }
    \If{$done$ $\neq$ True}
        \State \Call{initGS}{ }
        \State \Call{execGS}{ }
        \State \Call{postProcGS}{ }
    \EndIf
    % \State \Return $S$
\EndProcedure

\vspace{0.5\baselineskip}  % Add vertical space here

\Function{beginGS}{}
    \State $W \gets \emptyset$
    \State $done \gets \text{True}$
    \For{$m = 1$ to $n$}
        \State $w \gets PrefListsM[m, 1]$
        \If{$w \in W$}
            \State $done \gets \text{False}$
        \EndIf
        \State $W.\text{add}(w)$
        \State $S[w] \gets m$
    \EndFor
    \State \Return $done$
\EndFunction

\vspace{0.5\baselineskip}  % Add vertical space here

\Procedure{initGS}{}
    \State $RankMtxW$ $\gets$ \Call{initRankMatrix}{ }
    \State $Q \gets \emptyset$
    \For{$i = 1$ to $n$}
        \State $Next[i] \gets 1$
        \State $Q$.Push($i$)
        \State $PartnerRank[i] \gets n + 1$
    \EndFor
\EndProcedure

\vspace{0.5\baselineskip}  % Add vertical space here

\Procedure{initRankMatrix}{}
    \For{$i = 1$ to $n$}
        \For{$r = 1$ to $n$}
            \State $j \gets PrefListsM[i, r]$
            \State $RankMtxW[i, j] \gets r$
        \EndFor
    \EndFor
\EndProcedure

\vspace{0.5\baselineskip}  % Add vertical space here

\Procedure{execGS}{}
    \While{$Q \neq \emptyset$} \CommentNoLine{Main Loop}
        \State $m \gets Q$.Pop()
        \State $w \gets PrefListsM[m, Next[m]]$
        \State $r \gets RankMtxW[w, m]$
        \If{$PartnerRank[w] < r$}
            \State $Q$.Push($m$)
        \Else
            \If{$PartnerRank[w] \neq n + 1$} \CommentNoLine{$w$ is free}
                \State $m' \gets PrefListsW[w, PartnerRank[w]]$
                \State $Q$.Push($m'$) \CommentNoLine{Previous partner $m'$ becomes free}
            \EndIf
            \State $PartnerRank[w] \gets r$
        \EndIf
        \State $Next[m] \gets Next[m] + 1$ \CommentNoLine{Move to the next woman}
    \EndWhile
\EndProcedure

\vspace{0.5\baselineskip}  % Add vertical space here

\Procedure{postProcGS}{}
    \For{$w = 1$ to $n$}
        \State $m \gets PrefListsW[w, PartnerRank[w]]$
        \State $S[w] \gets m$ 
    \EndFor
\EndProcedure

\end{algorithmic}
\end{algorithm}

```



# Implementation

```
\subsubsection{The Detailed Implementation}
The implementation details of the GS algorithm are described in Algorithm \texttt{\ref{Algo:GSAlgo}}. In the data preparation stage, the algorithm initializes a matrix called \( \text{WomanRank} \), which shows the rank of each man in the women's preference lists. For each man, the algorithm assigns ranks to all women based on his preference list. This matrix, known as the rank matrix, provides a quick way to determine the preference order of any individual in constant time. For example, \( \text{RankMtxW}[w, m] \) gives the rank of man \( m \) in woman \( w \)’s preference list. The \( \text{Q} \) is a queue that keeps track of free men. Initially, all men are free and added to the queue. The \( \text{Next} \) array records, for each man, the rank of the highest-priority woman who hasn't rejected him yet. This array allows each man to propose to women in his preference list in order without rechecking previously rejected proposals. At the start, each man proposes to the woman he prefers the most, so all ranks stored in \( \text{Next} \) are set to 1. The \( \text{PartnerRank} \) array stores the rank of the current partner of each woman. Initially, the partner rank for each woman is set to \( n+1 \), indicating they are all unmatched.

% \begin{algorithm}
% \footnotesize  % Makes the text smaller
% \caption{Initialization of Rank Matrix (\texttt{initRankMatrix})}
% \label{Algo:InitRankMtx}
% \begin{algorithmic}[1]
% \Function{initRankMatrix}{$\text{prefLists}$}
%     \State $\text{rankMatrix} \gets \text{new matrix of size } n \times n$
%     \For{$i = 1$ to $n$}
%         \For{$r = 1$ to $n$}
%             \State $j \gets \text{prefLists}[i, r]$
%             \State $\text{rankMatrix}[i, j] \gets r$
%         \EndFor
%     \EndFor
%     \State \Return $\text{rankMatrix}$
% \EndFunction
% \end{algorithmic}
% \end{algorithm}


After initial data structures are prepared, the algorithm runs a main loop until there are no free men left in the queue. In each iteration, a man \( m \) is taken from the queue to propose to the highest-priority woman who hasn't rejected him yet. After each proposal, the man increments his rank to move to the next woman on his preference list for future proposals. The algorithm then checks the rank of this man in the woman’s preference list and compares it to the rank of her current partner. If the woman's current partner is ranked higher (lower numerical value) than the proposing man, the proposing man (\( m \)) remains free and is added back to the queue. Otherwise, the proposing man's partner rank is updated to \( m\_rank \). If the woman is already paired (i.e., \( p\_rank \neq n + 1 \)), the previous partner (\( p \)), identified from the woman's preference list, becomes free and is added back to the queue. Once the main loop finishes, the algorithm constructs the final stable matching list \( S \) in the postprocessing by pairing each woman with her final partner according to the \( \texttt{PartnerRank} \) list. Both the initialization of the RankMatrix and the main loop have \(O(n^2)\) complexity. Therefore, the overall time complexity of the algorithm is \(O(n^2)\).

The initialization of entries in the \( \texttt{RankMatrix} \) and the postprocessing of \( \texttt{PartnerRank} \) are completely independent for each entry. This independence allows these phases to be fully parallelized, meaning that with sufficient processing units, they can be done in constant time. Therefore, we focus on the execution phase in the performance analysis presented in this paper.


```

