#! /bin/bash
# TODO Put steps from full_dataset to enhancer
# GET A LIST FROM ALL RESULTS

result_path="./resources/results_all"

list_of_results=$(find $result_path -name "*.json")

tokenized_results="resources/results_all_tokenized" 
dobjs_results="resources/results_all_dobjs"
output_results="resources/results__all_filtered"
# echo $list_of_results
# FOR EACH ELEMENT IN LIST
mkdir $dobjs_results
mkdir $tokenized_results
mkdir $output_results

python3 ./enhancer/tokenizer.py -i $result_path -o "$tokenized_results"
#java -jar -Xmx40g  ./enhancer/find-dobjs.jar -inputFile "$tokenized_results" -outputFile "$dobjs_results" -directory    


for RESULT in $list_of_results 
do
    echo $RESULT
    PROJECT=$(basename $RESULT .json)
    echo $PROJECT    
    #call tokenizer with one result and output path
    # python3 ./enhancer/tokenizer.py -f -i $RESULT -o "$tokenized_results/$PROJECT.json"
    #CALL Filter DOBJ & First sentence with one result and one output path
    java -jar -Xmx40g  ./enhancer/find-dobjs.jar -inputFile "$tokenized_results/$PROJECT.json" -outputFile "$dobjs_results/$PROJECT.json"    
    # python3 ./enhancer/filter.py -f -i "$dobjs_results/$PROJECT.json" -o "$output_results/$PROJECT.json" -m 30 -n 100
    
done
