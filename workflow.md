The goals of the paper:

Carry the BVA work to the next level, using the predictive model we have
Illustrate the “layered semantic elucidation” approach to argument mining (“deeper argument mining”)
Introduce / use LAMPS as research tool
 

The workflow / writeup within the paper:

Start with 10,003 BVA cases that no one has read or annotated (DONE)
Convert all 10,003 cases to LSJson, with sentence segmenting (DONE)
(DONE:) Using the previously trained models (which will have to be updated and retrained before the paper) batch enrich all sentences (N = 1,360,230) within the 10,003 cases, with ML automatic classification of:
Sentence type (5 types + other)
For all FindingSentences, polarity (3 types)
For all FindingSentences, rule condition (4 types)
Filter FindingSentences for containing “PTSD” (DONE, N = 4,225)
Using filtered sentences from (4), create a Sample of “high-hit” cases (DONE; for 10 hits or more, N = 33; for 7 hits or more, N = 124; for 4 hits or more, N = 449)
Using the Sub-Samples from (5), and Using LA-Search, conduct searches to retrieve cases to analyze, such as:
Cases with FindingSentences that [contain “PTSD” + “Presumption of Soundness” + mapped (by ML) to SC_1_1], to find “interesting” paragraphs containing reasoning, to send to LA-Pad for tagging
Cases with EvidenceSentences that contain “Vietnam” (and perhaps FindingSentences that contain “Vietnam”), to find “interesting” paragraphs containing reasoning, to send to LA-Pad for tagging (e.g., difficulties of proving PTSD for Vietnam vets)
 

Something like this! I can play around with step 6 to find something interesting, as long as LA-Search is working (or conduct queries with python code), and LA-Pad is working (and use LA-Marker to mark up the original cases for future search).

 

Also, the kind of experiment you were thinking of is possible (comparing the results of a “presumption of soundness” keyword search with the hopefully-smarter search in 6.a above, to see how much noise the ML system eliminates.

 

Thoughts?


Hi, Steve.

 

Good call yesterday. Hope you had a safe trip to the beach. Here’s the record / update from that call:

 

I shared the RoBERTa Colab notebook with you at knowtshare@gmail.com. Check that email account — I wrote our goals in the email message I used to share the file with you.

I created a stratified random sample (N = 25) from the set of 449 4+-Hit cases, and you will find the sample in the LegalApprenticStaging / LASearchLoader GitHub repo. You can access it there. THIS IS THE SET OF FILES WE EVENTUALLY WANT TO LOAD INTO ELASTICSEARCH, AFTER I HAVE CURATED THEM FOR ACCURACY. But in the meantime, you can set up the code to do this.

I have begun the curation process, using Marker. So far, so good. It will be slow, but I got the first one done today, after figuring out what kind of records I need to keep about changes. AFTER I GET A CURATED SAMPLE OF 25, I’LL LET YOU KNOW.

You are going to clean up my code in this mess (you had figured out what I was doing wrong). This is still useful for filtering of files, even though we agreed that what I was trying to do is better done by elasticsearch.


FROM MY EARLIER EMAIL:

·         bva3a_ … -> to find and copy in one folder (“/filterResults/bva10HitLRSentFilteredCases”) the full cases for those LegalRuleSentences, to be found in the cases stored in “/data/bvaEnriched-FilteredFSPTSD-10-Hit+Sample-N33” – but here I ran out of time and patience playing around with the file names!! If you get any chance, could you please look at this code (“bva3a-“)?

 

Anything else?
 

Bob