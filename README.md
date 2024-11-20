# Heron Coding Challenge - File Classifier

Please see below for the original Heron Data Challenge ReadMe (from https://github.com/heron-data/join-the-siege)...  </br>
This 👇 is my write up for the challenge.

## Heron Data - Tech Take Home - Join The Siege - Project Write Up - Alan Donohoe


### Part 1: Enhancing the Classifier

**Q1) What are the limitations in the current classifier that's stopping it from scaling?**



1.a) Limitations of the Classifier

It is limited to 3 file types: "pdf", "png", "jpg" </br>
It is solely dependent on users including "drivers_license" etc in the file name  </br>
The file name may not reflect the actual type of document: eg: "alans_driving_license.png" may actually be alans bank statement, or malicious content. </br>

Re: Handling poorly named files </br>
Also there was a typo in the original classifier: https://github.com/AlanDonohoe/join-the-siege/pull/4  </br>
Meaning any users who misspell any of the categories it will fail to correctly classify the document.  </br>
This is extremely error prone, unreliable and not automatically extendable to other document types.  </br>

Re: How would the classifier scale under increased volume of traffic, assuming it's implementation was more complex than just checking a file name?  </br>
If the classifier was hosted on another machine (either our own model, or a 3rd party API call) (allowing the web service to act as a dedicated, light weight web service client) asyncio calls from the web service to the classifier service would also benefit from the asyncio IO calls at this point too…


1.b) Limitations of the Web Service </br>
We can migrate to FastAPI which runs on the ASGI (async server gateway interface) rather than the traditional WSGI, to handle a higher volume of web requests concurrently.
Depending on the design requirements and UX, we could allow asynchronous, single, or batch, requests which the web service would accept and respond to immediately to the web request but then enqueue a Celery task to be picked up by a separate instance dedicated to the classification process.



**Q2) How might you extend the classifier with additional technologies, capabilities, or features?** </br>
Typically I approach these kinds of projects by: </br>
Starting with the quickest, most simple solution, and evolve into more complexity if the simplest solution does not meet the requirements. </br>

The checking of the file name for presence of "drivers_licence", "bank_statement" or "invoice" is probably the most simplest, but is not reliable, nor extendable, and so is not meeting the requirements/ is a bad design. We can consider this:  </br>

_Solution # 1: A Classifier based solely on file name._</br>



_Solution #2: Google's Document AI API._ </br>
The quickest and simplest build on top of, or replacement of (would recommend replacing this basic version and it's too error prone), this would be just outsourcing the classification of documents to service that is already built and specialises in document classification: Google's Document AI.


If Google's Document AI meets all our requirements for accuracy, speed/latency, cost, traffic volume etc, then we could consider this a success: we have managed to outsource complexity, at a cost we are happy with, whilst saving valuable engineering time to work on more valuable problems, problems that other companies can not just buy off the shelf and give Heron Data an edge/ secret sauce / moat to differentiate from competitors.


Downsides of this approach: </br>
We would be subject to vendor lock in. </br>
If Google AI went down (albeit unlikely) - then we go down. </br>
Lack of control / ability to adjust the classifier if we needed to. </br>
Overhead / latency of calling an external API over the network. </br>
With this, outsourced/3rd party/ off the shelf approach, we could build in redundancy (in the unlikely event that Google Document AI API ever went down) by having a fall back integration with MS Azure Document AI (depending the outcome of a risk analysis to determine if we wanted to invest in this level of redundancy). </br>


Benchmarking Google's Document AI </br>
TODO: Post the 9 documents we have in our initial data sample to Google's Document AI API and measure latency. </br>
Refs: </br>
https://cloud.google.com/document-ai-workbench/?hl=en  </br>
https://learn.microsoft.com/en-gb/azure/ai-services/document-intelligence/overview?view=doc-intel-4.0.0#custom-classification-model </br>


For the sake of this exercise, let's go further to demonstrate some other ideas.</br>



_Solution #3: Fine-Tuning Google's Document AI API </br>_
The next solution (in order of increasing complexity) would be to fine-tune Google's Document AI model with our own data, rather than just using the pre-trained model off the shelf. </br>
As this exercise is an opportunity for me to showcase more of my skillset than calling Google's APIs, I will proceed with the next complex solution, fine-tuning a pre-trained CNN model. </br>
Refs:  </br>
https://cloud.google.com/document-ai/docs/ce-with-genai </br>
https://cloud.google.com/document-ai/docs/custom-classifier </br>



_Solution #4: Fine-Tuning A Pre-Trained CNN Model_ </br>
"ResNet-18 is a powerful and efficient CNN architecture. Its relatively shallow depth compared to other ResNet variants makes it suitable for tasks requiring lower computational resources while still providing strong performance on image classification tasks."


So we will start by fine-tuning a ResNet-18 model using PyTorch. </br>
https://colab.research.google.com/drive/1YZ1FJhMkddRZ7cNwDtJ3aE9GamG5k0oe?usp=sharing </br>
I was unable to, within the time constraint on this project, pull extra training data (images of bank statements, invoices, driving licenses) via my usual method (calls to DuckDuckGo) in the above Pytorch based Colab notebook.  </br>
So for speed I feel back to my usual fast and scrappy approach for these prototype projects: running my existing Kaggle Notebook that uses FastAI to collect training data and fine-tune ResNet18 with them. </br>
I collected around 100 images from each category and used these to fine-tune the model over the three categories. </br>
Again due to time constraints, I didn't spend too long cleaning the data, etc. </br>


I exported the fine-tuned model and it saved it in the same module at the class that calls it, here: </br>
src/services/files/classifiers/heron_data/v2/model.pkl


So now the HeronDataClassifierV2 is used to make classifications, not the original classifier. </br>
See full PR: https://github.com/AlanDonohoe/join-the-siege/pull/6


I have refactored the codebase so that the web layer is clearly separated / decoupled from all business logic, such as classifying a document. </br>


The controller only knows that it calls the "public" classifier, that encapsulates all other classifiers and their complexity:  </br>
```python
from src.services.files.classifiers.classifier import Classifier

...
file_class = Classifier.classify(request.files["file"])

```

https://github.com/AlanDonohoe/join-the-siege/blob/main/src/web/app.py#L3-L16C5 </br>
https://github.com/AlanDonohoe/join-the-siege/blob/main/src/services/files/classifiers/classifier.py </br>


This "public" classifier then calls any of the other classes within the services/files/classifiers namespace to execute the actual implementation of the classification. </br>
eg:  https://github.com/AlanDonohoe/join-the-siege/blob/main/src/services/files/classifiers/heron_data/v1/classifier.py  </br>


Or V2: </br>
https://github.com/AlanDonohoe/join-the-siege/blob/main/src/services/files/classifiers/heron_data/v2/classifier.py </br>
HeronData's V2 classifier first checks the mimetype of the file and if it's a pdf, converts each page to images, using the image of the first page to perform the classification. </br>
The image is then resized to the same dimensions as the images the model is trained on, and a prediction is made:


file_type,_,probability = model_v2.predict(img)


We log the file_type and its probability, and return the mapped filetype as to not break the contract with the client and keep the integration tests passing. </br>
https://github.com/AlanDonohoe/join-the-siege/blob/main/src/services/files/classifiers/heron_data/v2/classifier.py#L26-L38


I have designed the classifiers module to be extendable to other classifiers, and have, as examples of future classifiers that could be added, added Google Document AI and OpenAI placeholder modules. </br>


The main "public" classifier that is called in the web controller can swap out, or combine classifiers and the decoupling from the web layer means these implementation details will not require any change in the web controller. </br>


**(3) Processing larger volumes of documents.**
We could upload larger volumes of documents directly to S3 /  Google Storage, using a  pre-signed URL.. then trigger an event, Lambda, to process these documents.... This avoids our servers dealing with large volumes of large documents directly from users, we can choose how to process documents once we know their size/volume of docs in storage.

Or... make batch inferences of the model. </br>
There is likely a combination of model batch inferences, concurrency using Celery and Asyncio/Multiprocessing, etc that would allow us to scale significantly.


**Part 2: Productionising the Classifier**
_How can you ensure the classifier is robust and reliable in a production environment?_ </br>
Stress test locally and a staging env instance before release. </br>
How much traffic are we expecting? </br>
How open is the service to the public and potential malicious users? Do we need CloudFlare upfront? </br>
Replicate the last month's prod traffic in a test environment. </br>
Turn on service in prod in the background - forwarding documents to this new service in a background job and monitor for any anomalies. </br>
Logging and alerting (eg: Sentry, PagerDuty). </br>
How can you deploy the classifier to make it accessible to other services and users? </br>
Heron Data uses GCP, so can deploy either on CloudRun or GKE. </br>
I tried to deploy my service on GCP CloudRun, but ran out of time. </br>


**How I Typically Work** </br>
I would usually treat picking up a ticket, design thinking about a new feature, project, etc as an opportunity to discuss with other relevant parties - PM, architect, other engineers, etc. </br>
But as this is a tech challenge, I wouldn’t ask for a call to discuss this before I started work on it, as I would in the real world.

**General Ethos**
How simple can we make the solution?
That is, do we really need to shoehorn AI into this, or is there a simpler, more traditional approach?

**Broader Context Questions**
What is the business impact of this? </br>
How will end users use this feature? </br>
What is the shape of the project? Data? </br>
How detailed are the requirements - functional, non-functional, etc </br>
Limitations - assuming we have a CI/CD so it’s easy to deploy.  </br>
- What about if it's a large model being used for inference? </br>
- What type of server do we need for this? </br>
- On premises?  </br>
- Can we just treat this as a POC for now and host a fine tuned model on Hugging face, etc? </br>
- Or do we need to get this running on GCP? / on prem? </br>

Risks  </br>
- What if it classifies incorrectly? Repercussions? </br>
- Resulting Business/Reputational risks. </br>
- What does it look like if this goes wrong?  </br>
  - How to mitigate and or monitor for this. </br>
  - Have each risk mitigation and monitoring task assigned to an actual engineer who is accountable/ checks off each when it’s “done” (monitoring is set up, etc). </br>
Monitoring - exceptions and evaluating quality on unseen production data. </br>

Refs: </br>
Repo: https://github.com/AlanDonohoe/join-the-siege </br>
Project Kanban: https://github.com/users/AlanDonohoe/projects/2 </br>




## Original Heron Data Challenge ReadMe 👇
From: https://github.com/heron-data/join-the-siege</br>

## Overview

At Heron, we’re using AI to automate document processing workflows in financial services and beyond. Each day, we handle over 100,000 documents that need to be quickly identified and categorised before we can kick off the automations.

This repository provides a basic endpoint for classifying files by their filenames. However, the current classifier has limitations when it comes to handling poorly named files, processing larger volumes, and adapting to new industries effectively.

**Your task**: improve this classifier by adding features and optimisations to handle (1) poorly named files, (2) scaling to new industries, and (3) processing larger volumes of documents.

This is a real-world challenge that allows you to demonstrate your approach to building innovative and scalable AI solutions. We’re excited to see what you come up with! Feel free to take it in any direction you like, but we suggest:


### Part 1: Enhancing the Classifier

- What are the limitations in the current classifier that's stopping it from scaling?
- How might you extend the classifier with additional technologies, capabilities, or features?


### Part 2: Productionising the Classifier

- How can you ensure the classifier is robust and reliable in a production environment?
- How can you deploy the classifier to make it accessible to other services and users?

We encourage you to be creative! Feel free to use any libraries, tools, services, models or frameworks of your choice

### Possible Ideas / Suggestions
- Train a classifier to categorize files based on the text content of a file
- Generate synthetic data to train the classifier on documents from different industries
- Detect file type and handle other file formats (e.g., Word, Excel)
- Set up a CI/CD pipeline for automatic testing and deployment
- Refactor the codebase to make it more maintainable and scalable

## Marking Criteria
- **Functionality**: Does the classifier work as expected?
- **Scalability**: Can the classifier scale to new industries and higher volumes?
- **Maintainability**: Is the codebase well-structured and easy to maintain?
- **Creativity**: Are there any innovative or creative solutions to the problem?
- **Testing**: Are there tests to validate the service's functionality?
- **Deployment**: Is the classifier ready for deployment in a production environment?


## Getting Started
1. Clone the repository:
    ```shell
    git clone <repository_url>
    cd heron_classifier
    ```

2. Install dependencies:
    ```shell
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Run the Flask app:
    ```shell
    python -m src.web.app
    ```

4. Test the classifier using a tool like curl:
    ```shell
    curl -X POST -F 'file=@path_to_pdf.pdf' http://127.0.0.1:5000/classify_file
    ```

5. Run tests:
   ```shell
    pytest
    ```

## Submission

Please aim to spend 3 hours on this challenge.

Once completed, submit your solution by sharing a link to your forked repository. Please also provide a brief write-up of your ideas, approach, and any instructions needed to run your solution.
