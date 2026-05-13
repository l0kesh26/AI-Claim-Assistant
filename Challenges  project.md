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



**->**After going through all the possibilities I have decided to use OCR 

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





**3.Phase-3 : Prompt Issue in Ollama**



**Challenges:**

1.This is biggest challenge I have faced while doing the project every llm will have this exception whenever we are using the llm everyone major concern is about the selecting the prompt.

2.I have also gone through this issue.

3.Firstly I have given the prompt with 300 words or character 





&#x20;



