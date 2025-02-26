### Abstract
Rubber Duck program is an rulebased chat bot. This chatbot is designed as a debugging companion for python code. Its primary goal is to assist users in resolving 
their coding issues by engaging in conversational, natural language interactions. Users can input queries, problem descriptions, or even snippets of code needing assistance.
The core functionality lies in its ability to classify and interpret the provided code snippets or textual descriptions. This project employs code analysis
algorithms to identify syntax errors, common programming constructs, and potential logic flaws. It then responds in a friendly and informative manner, guiding users through step-by-step solutions or suggesting alternative
approaches to address the issues at hand.<br/>

### Utilized Methods
-	**Natural Language Processing (NLP):** The NLTK library is used for text processing, including tokenization, stop word removal, and keyword matching. <br/>


-	**Regular Expressions:** Regular expressions are utilized to match code keywords, identify patterns, and extract information from user input. <br/>


-	**Abstract Syntax Tree (AST) Parsing:** The `ast` module is employed to parse and analyze the structure of Python code, enabling the identification of assignments, loops, conditions, and functions. <br/>


###	Debugging Conversation Transcript

Case 1

**Ducky** : Hello there, I am Ducky Duck. How may I help you today.<br/>
**You** : i am facing issue with my code <br/>
**Ducky** : Can you please provide the code? <br/>
**You** : 
```
          x=5 
          y=10 
          result = x+y
          print(f"The result before the loop is: {result}") for i in range(1,6):
	        if i%2==0:
	           print(f"Even number : {i}")
	        else:
	           print(f"Odd number : {i}") final_result = result-2

          print(f"The result after the loop is: {final_result}
```
 
 
**Ducky** : Here is the summary of your code: The result before the loop is: 15 Odd number : 1<br/>
Even number : 2 Odd number : 3 Even number : 4 Odd number : 5<br/>
The result after the loop is: 13 Your code does not have any syntax errors<br/>
**Ducky** : Do you want to check anything further <br/>
**You** : yes<br/>
**Ducky** : Do you wish to assign x to 5<br/> 
**You** : yes<br/>
**Ducky** : Do you wish to assign y to 10 <br/>
**You** : no <br/>
**Ducky**: Consider checking your assignment operation <br/>
**Ducky** : Do you want to continue checking code? <br/>
**You** : yes <br/>
**Ducky** : Do you wish to assign x+y to result <br/>
**You** : no <br/>
**Ducky**: Consider checking your assignment operation  <br/>
**Ducky** : Do you want to continue checking code? <br/>
**You** : no <br/>
**Ducky** : Hope I helped you debugging the code. Happy Coding <br/>

Case 2
**Ducky** : Hello there, I am Ducky Duck. How may I help you today. <br/>
**You** : i am facing issue with my code  <br/>
**Ducky** : Can you please provide the code? <br/>
**You** : 
```
reverse_num = 0 num = 12345
while num > 0:
	digit = num % 10

	reversed_num = reversed_num * 10 + digit
	num = num // 10

print(f"The reverse of {number} is: {reversed_result}
```
**Ducky** : You did not define reversed_num before using it <br/>
**Ducky** : Do you still want to go further? <br/>
**You** : No <br/>
**Ducky** : Hope I helped you debugging the code. Happy Coding <br/>



