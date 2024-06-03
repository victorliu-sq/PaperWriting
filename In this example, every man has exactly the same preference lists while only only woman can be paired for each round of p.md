In this example, every man has exactly the same preference lists while only only woman can be paired for each round of proposals. Thus the total number of proposals to each woman  will be n + n -1 + n -2 + ... +1 = O(n^2). Therefore, on the complexity side, we don’t have much space to improve, but others.



In this example, each man has identical preference lists, but only one woman can be matched in each round of proposals. Thus the number of men making proposals will decrement by one when moving to next round of proposals to next woman. 



Since each unpaired man will propose sequentially to all the women based on their preference lists, As a result, the total number of proposals to each woman will be 𝑛+(𝑛−1)+(𝑛−2)+…+1=𝑂(𝑛2)*n*+(*n*−1)+(*n*−2)+…+1=*O*(*n*2). Therefore, in terms of complexity, there isn't much room for improvement in reducing the number of proposals.



To guarantee the absence of blocking pair, unpaired men must propose sequentially based on their preference lists.

In the 3 by 3 matrix example, each man has identical preference lists, thus only one of them can be matched with a woman in each round of proposals. Therefore, the total number of proposals to each woman must be 𝑛+(𝑛−1)+(𝑛−2)+…+1=𝑂(𝑛2)*n*+(*n*−1)+(*n*−2)+…+1=*O*(*n*^2) and  there isn't much room for complexity improvement.



Currently, I am still working on Section 2 and 3. For Section 4, I have not updated it with my latest verion so it can be ignored for now.



To guarantee the absence of blocking pairs, unpaired men must propose sequentially based on their preference lists. In the 3x3 matrix example, each man has identical preference lists, so only one of them can be matched with a woman in each round of proposals. Therefore, the total number of proposals to each woman is 𝑛+(𝑛−1)+(𝑛−2)+…+1=𝑂(𝑛2)*n*+(*n*−1)+(*n*−2)+…+1=*O*(*n*2), leaving no room for complexity improvement.

Currently, I am still working on Sections 2 and 3. As for Section 4, it hasn't been updated with my latest version yet, so it can be ignored for now.