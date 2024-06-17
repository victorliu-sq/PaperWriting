# Requirements

Can you rewrite these sentences to make it more academical? 

You can insert sentences, deleted sentences and reorder sentences, (also for words) to strengthen the connections between sentences.



 These paragraphs also have too many duplicated information / words. Please make it concise and easy to read



# Q1

**In section 2.3, we need a citation for the MW implementation for the GS algorithm.  If the streamlining proposal approach is used in our method, we should make the statement in this section.** 



The McVitie and Wilson (MW) algorithm is essentially another implementation of the GS algorithm, based on the principle that the proposal order does not affect the resulting stable matching. The key distinctions between the MW and GS algorithms lie in their execution phases. The MW algorithm iterates through every man and invokes a recursive procedure for free men to make proposals. When a man enters this recursive procedure, he proposes to his highest-ranked woman who has not yet rejected him. If the woman is unpaired, her partner rank is updated as in the GS algorithm. Additionally, the way rejected proposals are handled is a major difference. In the MW algorithm, if a proposer is rejected by the woman he is proposing to, he immediately moves on to propose to the next woman on his list, rather than being added back to a queue. Similarly, if a woman accepts a new proposal, her previous partner will continue to propose to his next preference, instead of being pushed back to a queue.

As a result, the need for a queue to manage free individuals is eliminated, thereby reducing the time overhead associated with this task. This streamlined proposal process is employed in our algorithm to enhance efficiency, and it also provides opportunities for further optimization.



# Q2 

**In section 3.1, in the end of sentence of “When the number of participants is very large, this non-sequential nature of access …”, cite the following paper:** 

 

https://dl.acm.org/doi/pdf/10.1145/360128.360134



Thank you! The relative content in  Section 2.3 and Section 3.1 has been updated