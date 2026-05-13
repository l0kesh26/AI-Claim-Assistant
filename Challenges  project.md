**Challenges faced while doing the project :**



**1.Phase-1 :Selecting the better Solution**



**Challenges:**



\->In phase-1 of the project firstly we thought of sending the image directly to the ollama model

\->So to do that we have used Ollama LLava model

&#x09;->In ollama LLava model is used for the image and multi-text processing



\->We have tried with it but the output is not as expected

\->Later we have tried with gemini it is good and giving the accurate output

\->But the problem with gemini model is it is too expensive and required money for the api call

\->We got struck in this phase

\->Later I verified all the possibilities to create a model and I found this lib called OCR

**->OCR(Optical Character Recognition)**



**Solution:**



\*\*->\*\*After going through all the possibilities I have decided to use OCR

\->Firstly we will be extracting all the data present in the image by using OCR and later we will be saving that in a list and then we can use the ollama model.

\->This solved the issue in the phase-1.





**2.Phase-2 :OCR Implementation**



**Challenges:**



\->In Phase-2 of the project there was challenges we faced with OCR

\->Initially we have used Easy OCR lib to extract the data from the image

\->But the issue was Easy OCR is not predicting the letter accurately

&#x09;->For example if the image as letter "N" it is predicting as "O"

\->This is creating the confusion in the model for suppose we wanted to print the name of the person after OCR the model is not able to print as it consider "N" as "O".

\->Then I have gone through alternative of Easy OCR

&#x09;->I have found alternatives for Easy OCR

&#x09;	**->1. Tesseract OCR**

&#x09;	**->Paddle OCR**

&#x09;	**->Keras OCR**

&#x09;	**->Amazon Textract**

&#x09;	**->Google Vision**



\->Initially I have tried using Tesseract OCR the lib is good but the predication and accuracy is not as expected

\->Later we have used Paddle OCR the results are good in it

\->And finally we have used Keras OCR the results are not upto mark





**Solution :**



\->Finally we have decided to go with the Paddle OCR

\->The accuracy and predicting format is good and expected.

\->Hence the problem is resolved



**3. Phase-3 : Prompt Issue in Ollama**



**Challenges:**



1.This was one of the biggest challenges I faced while working on the project. In every LLM-based application, prompt selection is one of the major concerns.

2.I also faced the same issue during the development phase.

3.Initially, I provided a prompt with around 300 words/characters, and the model was unable to predict the output correctly (“You can verify the incorrect prompt in the prompt file available on GitHub”).

4.Then, I removed all the unnecessary parts from the prompt and provided a simplified version to the model.

5.Even after modifying the prompt, I still faced the same issue.

6.In the initial phase of the project, I planned to classify medicines and charges based on their names.

For example:

\->If the bill contained “bed charges,” it would be classified under hospitalization charges.

However, due to prompt-related issues, I decided not to continue with that approach.

7.In the prompt, I had also included the list of hospitals supported by the organization/company.

8.Later, the prompt itself became too large and started affecting the model performance.

9.So, I decided to send the JSON file directly to the LLM and then verify the required details from it.

10.This approach helped in reducing both the processing time and the space complexity of the model.







**Solution:**





1.First, I stored all the required data in a JSON file.

2.The stored JSON data was then sent to the Ollama model.

3.After that, I wrote a smaller and more optimized prompt that only verifies:

\->Whether the doctor and hospital are present or not

\->Whether the doctor’s name is valid or not

5.The hospital list was provided separately in list format for easier validation.





















&#x20;

