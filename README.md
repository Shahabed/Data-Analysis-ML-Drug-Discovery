# Data-Analysis and ML
Herein, the state of the art algorithems for different aspect of data analysis and ML are presented. 
# Introduction:
## 1.Data Collection algorithm.py
The first algorithm to run is "Data Collection algorithm.py". This algorithm handles the complex database where the raw data(which is already aggregated) are stored. It collects and combine the separately stored sets of futures. These features-sets are stored separate directory and files based on their barcodes and well-keys. 
## NOTE: 
    Rough estimate of the size of well features of all plates combined
    179*384*1500 * 8 / (10**6) = 825 MB for all plates  -->   4.6 MB per plate
    Assumption:
    Features are loaded as float64, therefore we assume 64/8 = 8 bytes per feature


    # --- Algoritm ---:
    #    for each plate:
    #       for each well of current plate:
    #           read the desired values from the well file
    #           ...
    #       combine-wells-of-current-plate
    #    combine-...
## 2.run_normalization.py
The normalization algorithm, "run_normalization.py", uses the collected and combined data as its input. The renown Z-score formula is used as a normalization method. 

## For the function zscore:
 ## NOTE:
     When out=None, locations within the returned array where the condition is False will remain uninitialized,
     and therefore could lead to unexpected random values appearing in those locations!
     'uninitialized' here means it could be an unexpected random value

     Usual code:
     norms = (well_features - means) / stds
     This could have unexpected results depending on the numpy.errstate settings
     If the error handling setting is so, division by zero throws an exception
## 3.function_common.py
The "function_common" contains a set of functions which are called in both above algorithms. 
## Goals of the project:
* A primary data extraction and basic filtering on FEARS database.
* Computation of important frequencies and selecting the matches between drug and ADRs beyond random reporting.
* Association and matching between FEARS data and screening data, so we can use the ADRs in FEARS database for classification of our screening data.
## Introduction:
Herein, a description of how to implement the series of Algorithems for the advers drug reaction project is given.The first step to start the process, is to run the  "adrs_data_processing.py". The adequet information for this particular algorithm can be found in the corresponding README. The explanation for the computational steps after "adrs_data_processing" follows as:
## 1. Frequency-Based data mining
Frequency data mining is a method used in the Pharmacovigilance. 
Here, we have used a method called Proportional Reporting Ratio (PRR) as a model for frequency data mining.
PRR is based on simple ratios of counts from a two-by-two table of presence/absence of a drug of interest and an event of interest.
It detects drug-adverse event combinations reported with a frequency that is disproportionately high with respect to some computed baseline.
First, we compute the simple frequencies in the FAERS data which is already prepared and filtered by the adrs_data_processing algorithm. The corresponding function for 
computation of these simple frequencies is `frequencies_calc`. Then we compute the PRR ratio by the `PRR-algorithm` function. 
The Chi-squared value (χ2 with Yates' correction) is also calculated to prove a non-normal distribution in the contingency table. The corresponding function for that is
`chi_squared_algorithm`. These functions, PRR_algorithm and chi_squared_ algorithm, use as an input the simple frequencies computed by `frequencies_calc`.
With the `Adrs_freq_table`, we add these ratios to the dataframe. `filt_Adrs_freq` function, filters the data based on these ratios. 

## 2. Similarity matching algorithm
This algorithm is designed to find the matching pairs between ADR reports in FEARS database and existing compound data used on assays in screening database.
The output is a data frame with information from both above databases where they drug names have matched. Here, we use the python library `jellyfish`. 
This library contains various distances for the computation of difference between two strings. 
The first function, `similarity_distance`, is to customize different definitions of distance between strings in jellyfish, where one can change the distance choices accordingly. 
Two main distance is computed here for the similarity comparison between strings. The first one is jaro_winkler_similarity and the second one is match_rating_comparison.
The later distance,match_rating_comparison, is based on phonetic encoding. In the function `get_similarity_table`,firstly, these two distances are computed.
Then based on some thresholds, these two distances are used to find the best matches between drug names in FEARS database and screening database. Finally, the
distance-based filtered data is produced, including the new columns for these two computed distances.
## 3. Pre-classification analysis
Before going through the classification process, it is desirable to analyze the result that obtained from the association between FEARS and screening databases. 
For that purpose, the ` Pre-classification analysis` algorithm is designed.
The first function, `ranking_adrs` is defined to explore the ranking between the reported ADRs effect. Another important function is `ADRs_drug_association`, where a representation of the association between ADRs and corresponding drugs is computed. There is a need to create a table with unique drugs which are similarly matched. This can be done by using the function ` unique_drug_matching`. We might want to find a drug matching between two databases for a specific ADR.
The function `drug_related_to_one_Adrs` is designed to handle exactly that calculation. A function for finding the compound drugs with the same ADRs is developed as `compound_drugs_with_same_ADR`. Finally, for the ranking between the compound drugs, the `ranking_compond_drugs` is proposed.
 
