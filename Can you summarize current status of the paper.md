1. 1. 

   2. 	1.	Have you addressed all the suggestions from Professor Xia?
      	•	Yes.
      	2.	Have you finished all the experiments?
      	•	Not yet. All classes and methods have been implemented, but there are still many figures to complete.
      	3.	Are you happy with the results?
      	•	Yes, I believe we have outperformed all state-of-the-art algorithms.
      	4.	Is the PRMatrix creation cost acceptable for all cases, including the perfect case?
      	•	Yes, in the perfect case where the best algorithm takes 400ms, it only adds an extra 40ms.
      	5.	If we measure the total execution time as preprocessing time plus parallel processing time, can you report the speedups for each case? What is the best case, and what is the worst case?
      	•	We can report speedups for three types of cases: congested cases, solo cases, and a mixture of congested and solo cases.
      	•	For the clustered case, there is no speedup, but also no negative impact.
      	•	For the random case and the perfect case, there is a negative impact of an additional 40ms, resulting in a total of 440ms if the best algorithm takes 400ms.



LA is short-name for "Locality-Aware" and it is a sequentai algorithm run on CPU using PRMatrix. Bamboo is a hybrid-system parallel framework that uses both sequneital LA on CPU and parallel LA on GPU

MW is a sequential algorithm, so it has similar performance as GS

I've not updated those numbers yet, I am trying to create another figure that can makes the preprocessing phase of LA