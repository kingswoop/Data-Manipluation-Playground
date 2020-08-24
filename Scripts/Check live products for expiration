#!/usr/local/bin/

#Phrase to poll for
text="sold out"

date1=$(date '+%Y-%m-%d')
file1=./product_names_sold_out_script.csv 
ps=`##removed for security`
## reset the removal list at the start of each run
rm ./product_names_sold_out_script.csv 
rm ./sold_out_list.csv 

mongo mongodb+srv://##removedforsecurity --username ##removedforsecurity --password ##removedforsecurity --quiet --eval "db.getSiblingDB('##removedforsecurity').product.find({}, {_id: 0, urlString: 1}).toArray()"  > ./product_names_sold_out_script.csv

# Loop mongodb product extract and curl for phrase. If phrase exists in curl output then product is sold out and should be removed from live environment.
sed -e '7d;s/urlString//g;s/,//g;s/["]//g;s/[]{}]//g;s/^[[:space:]]*//;s/[[:space:]]*$//;s/[ \t]*$//;/^$/d;s/^.\{2\}//' "$file1" | while IFS=$',' read -a Product_Name_url
								    		do
								    			
										    	#for i in "${Product_Name[@]}";
										    		#do
										    			if
										    				[[ -z "$Product_Name_url" ]]
										    				then
										    					echo "$Product_Name_url"
										    					echo "end of product names"
															else
																echo "$Product_Name_url"
																curl -s "$Product_Name_url" >> ./output.txt
																
																		
																if grep -q -i *"$text"* ./output.txt;
																	then
																		echo "$Product_Name_url" >> ./sold_out_list.csv
																		
																		
																		##ELSE IF LOOK FOR THE WEBSITE PHRASE 'out of products' then check that. e.g boohooMan
																		
																	else

																		echo "Not Found"
	
																fi
														fi
														
														#
										    			
										    		#done
									    		
										    done
											
cp ./sold_out_list.csv ./backups/sold_out_list_${date1}.csv 
