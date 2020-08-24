#!/usr/local/bin/

#Contents = Brands to be run [brands = custom input list in file .brands.csv]
file2="./brands.csv"

#Output of cleanse items, then loaded to DB
Product_Cleanse_Load="./product_cleanse.js"

colourjs="./product_amend_list.js"
colour_url_js="./product_amend_list_url.js"
url_colour_names="./url_colour_names.csv"
colour_colour_match="./colour_colour_match.csv"
file3="./00_Category_Reassignment.csv"
subcatjs="./subcat_amend.js"
file7="./CategoryIds.csv"
CatIdsjs="./catIds_reassign.js"
image_colour="./image_url_colour.js"
AI_colour_load_file="./AI_colour_output.js"
AI_colour_input_file="./remaining_colour_match"
image_resize_file_load="./"

#COLOUR AI
BOT_COLOUR_FILE=./AI_products.csv
image_input=./curl_image.png
AI_input_file=./final_AI_colour_list.csv

#DuplicateCleanse
duplicate_cleanse="./duplicate_cleanse.js"

#Cleanse products that contain below phrases
declare -a cleanse
cleanse=(
"Gift Card Gift Card"
"Gift Card"
"Gift Card "
"gift card"
)

#Colour assignment 
declare -A colours
colours=(
['ROSE']='Pink'
['FLAMINGO']='Pink'
['Poppy']='Red'
['LEOPARD']='Leopard'
['NUDE']='Nude'
['FAWN']='Nude'
['Burgundy']='Red'
['Emerald']='Green'
['PHANTOM']='Black'
['INK']='Black'
['Silver']='Silver'
['WHITE']='White'
['NAVY']='Navy'
['MATADOR RED']='Red'
['FATIGUE']='Green'
['LAGOON']='Green'
['BLUE COASTAL']='Blue'
['CHARCOAL']='Grey'
['BLANC']='White'
['ULTRA MARINE']='Blue'
['BLUE MIRAGE']='Blue'
['BLACK']='Black'
['BLUE STONE']='Blue'
['VINO']='Red'
['JUNGLE']='Green'
['DARK DENIM']='Navy'
['SUNSHINE']='Yellow'
['GREEN BLACK']='Black'
)


# Read ./brands.csv and assignment brand with the type of assignment [Colour_script + Image_resize_script]
sed '1d;s/^[[:space:]]*//;s/[[:space:]]*$//' "$file2" | while IFS=$',' read Brands_Array Colour_Script Size
	do
			echo "@@@$Brands_Array@@@"
			
			#Products with Colour to be reallocated
			rm ./product_amend_list.js
			#Remove Unwanted Products
			rm ./product_cleanse.js
			#Remove Unwanted Products
			rm ./duplicate_cleanse.js
			#Remove AI files
			#	rm ./final_colour_output.csv
			#	rm ./AI_colour_output.js
			#	rm ./final_AI_colour_list.csv
			#	rm ./input_data_json.js 
			##PRODUCT CATEGORY AMENDMENT
			rm ./subcat_amend.js
			rm ./catIds_reassign.js
			##Category AMENDMENT FILE
			rm ./catIds_reassign.js
			##Image Resize 
			rm ./image_size_update.js
			
			
	
			################Cleanse misc items from lists##################
			for i in "${cleanse[@]}"
				do
					echo "db.getSiblingDB('##Removedforsecurity').product.remove({brand:\"$Brands_Array\"," >> product_cleanse.js
				   	echo "name:/"$i"/})" >> product_cleanse.js
				   	echo " ~ Cleansing $brand - $i ~ "
				done
				
			mongo mongodb+srv://##removedforsecurity --username /##removedforsecurity --password /##removedforsecurity --quiet --eval "load(\"$Product_Cleanse_Load\")"		
			
			echo "##### Product Cleanse Done #####"
			###############################################################

			
			
			################Delete Duplicates per brand category and subcategory based on imageUrl##################
			
			echo "db.getSiblingDB('/##removedforsecurity').product.aggregate( [" >> ./duplicate_cleanse.js
			echo "{" >> ./duplicate_cleanse.js
			echo "\$match: {" >> ./duplicate_cleanse.js
			echo "brand: \"$Brands_Array\"" >> ./duplicate_cleanse.js
			echo "}" >> ./duplicate_cleanse.js
			echo "}," >> ./duplicate_cleanse.js
			echo "{ " >> ./duplicate_cleanse.js
			echo "\$group: {" >> ./duplicate_cleanse.js
			echo "_id: { n: \"\$name\", i: \"\$imageUrl\", c: \"\$category\", s: \"\$subCategory\"}," >> ./duplicate_cleanse.js
			echo "all_ids: { \$addToSet: \"\$_id\" }" >> ./duplicate_cleanse.js	  
			echo "}" >> ./duplicate_cleanse.js
			echo "}," >> ./duplicate_cleanse.js
			echo "{ " >> ./duplicate_cleanse.js
			echo "\$project: {"  >> ./duplicate_cleanse.js
			echo "dup_ids: { \$slice: [ \"\$all_ids\", 1, 9999999 ] }," >> ./duplicate_cleanse.js	  
			echo "_id: 0" >> ./duplicate_cleanse.js 
			echo "}" >> ./duplicate_cleanse.js
			echo "}" >> ./duplicate_cleanse.js
			echo "] ).forEach( doc => db.getSiblingDB('##removedforsecurity').product.deleteMany( { _id: { \$in: doc.dup_ids } } ) )" >> ./duplicate_cleanse.js
			
			mongo mongodb+srv:///##removedforsecurity  --username /##removedforsecurity --password ##removedforsecurity --quiet --eval "load(\"$duplicate_cleanse\")"
			
			################Cleanse misc items from lists##################
			
			
			

			##################Fixed Colour Assignment##################
			echo "Start Colour Script"
      
      # If Colour in Product Field Colour
			if [[ "$Colour_Script" == "Colour" ]]
				then
						
					brand="$Brands_Array"
					
					mongo mongodb+srv://##removedforsecurity  --username ##removedforsecurity --password ##removedforsecurity --quiet --eval "db.getSiblingDB('##removedforsecurity').product.find({brand:\"$brand\"}, {_id:0,name:1}).toArray()" > ./colour_colour_match.csv
		
					
					
					for assigned in "${!colours[@]}";
						do
							
							newcolour=${colours[$assigned]}
							
							#Create the file to load amendments
							echo "db.getSiblingDB('##removedforsecurity').product.updateMany(" >> ./product_amend_list.js
							echo "{brand:\"$brand\"," >> ./product_amend_list.js
							
							echo "##### $brand - $assigned >>> $newcolour #####"

							sed -e '/2020/d;s/://g;s/name//g;s/["]//g;s/[]{}]//g;s/^[[:space:]]*//;s/[[:space:]]*$//;/^$/d' "$colour_colour_match" | while IFS=$',' read -a Results_Array 
								do
									
									for i in "${Results_Array[@]}";
										do
											if

												[[ $i == *"$assigned"* ]]
												then
													product_name=$i
													echo "$product_name"
											fi
										done
								done
							
              # Echo results to ./product_amend_list.js, Product Name + the colour of assignment
							echo "color:/$assigned/," >> ./product_amend_list.js
							echo "}, { \$set: {color:\"$newcolour\"}}" >> ./product_amend_list.js
							echo ")" >> ./product_amend_list.js
						done
				
        # LOAD Results into DB
				mongo mongodb+srv://##Removedforsecurity  --username ##Removedforsecurity --password ##Removedforsecurity --quiet --eval "load(\"$colourjs\")"
													
							
      # If Colour in UrlString Field
			elif [[ "$Colour_Script" == "urlString" ]]
				then

					##REFRESH AMEND PRODUCT FILE
					echo "$Brands_Array"
					rm ./product_amend_list_url.js

					brand="$Brands_Array"
					mongo mongodb+srv://##Removedforsecurity  --username ##Removedforsecurity --password ##Removedforsecurity --quiet --eval "db.getSiblingDB('##Removedforsecurity').product.find({brand:\"$brand\"}, {_id:0,name:1}).toArray()" > ./colour_colour_match.csv
		
					
					
					for assigned in "${!colours[@]}";
						do
							#echo "$assigned - ${colours[$assigned]}"
							newcolour=${colours[$assigned]}
							echo "db.getSiblingDB('##Removedforsecurity').product.updateMany(" >> ./product_amend_list.js
							echo "{brand:\"$brand\"," >> ./product_amend_list.js
							
							echo "##### $brand - $assigned >>> $newcolour #####"

							sed -e '/2020/d;s/://g;s/name//g;s/["]//g;s/[]{}]//g;s/^[[:space:]]*//;s/[[:space:]]*$//;/^$/d' "$colour_colour_match" | while IFS=$',' read -a Results_Array 
								do
									
									for i in "${Results_Array[@]}";
										do
											if

												[[ $i == *"$assigned"* ]]
												then
													product_name=$i
													echo "$product_name"
													
											fi

											
										done
									
								done

							echo "urlString:/$assigned/," >> ./product_amend_list.js

							echo "}, { \$set: {color:\"$newcolour\"}}" >> ./product_amend_list.js
							echo ")" >> ./product_amend_list.js
						done
				

					mongo mongodb+srv://##Removedforsecurity  --username ##Removedforsecurity --password ##Removedforsecurity --quiet --eval "load(\"$colourjs\")"
							
								
      # If Colour in imageUrl Field
			elif [[ "$Colour_Script" == "imageUrl" ]]
				then

					##REFRESH AMEND PRODUCT FILE

							echo "$Brands_Array"
							rm ./image_url_colour.js

							brand="$Brands_Array"
							mongo mongodb+srv://##Removedforsecurity  --username ##Removedforsecurity --password ##Removedforsecurity --quiet --eval "db.getSiblingDB('##Removedforsecurity').product.find({brand:\"$brand\"}, {_id:0,name:1}).toArray()" > ./colour_colour_match.csv
				
							
							
							for assigned in "${!colours[@]}";
								do
									#echo "$assigned - ${colours[$assigned]}"
									newcolour=${colours[$assigned]}
									echo "db.getSiblingDB('##Removedforsecurity').product.updateMany(" >> ./product_amend_list.js
									echo "{brand:\"$brand\"," >> ./product_amend_list.js
									
									echo "##### $brand - $assigned >>> $newcolour #####"

									sed -e '/2020/d;s/://g;s/name//g;s/["]//g;s/[]{}]//g;s/^[[:space:]]*//;s/[[:space:]]*$//;/^$/d' "$colour_colour_match" | while IFS=$',' read -a Results_Array 
										do
											
											for i in "${Results_Array[@]}";
												do
													if

														[[ $i == *"$assigned"* ]]
														then
															product_name=$i
															echo "$product_name"
															
													fi

													
												done
											
										done

									echo "imageUrl:/$assigned/," >> ./product_amend_list.js

									echo "}, { \$set: {color:\"$newcolour\"}}" >> ./product_amend_list.js
									echo ")" >> ./product_amend_list.js
								done
						

						mongo mongodb+srv://##Removedforsecurity  --username ##Removedforsecurity --password ##Removedforsecurity --quiet --eval "load(\"$colourjs\")"

			# If Colour in Name Field
			elif [[ "$Colour_Script" == "Name" ]]
				then
			
							##REFRESH AMEND PRODUCT FILE

							echo "$Brands_Array"
							rm ./product_amend_list_url.js

							brand="$Brands_Array"
							mongo mongodb+srv://##Removedforsecurity  --username ##Removedforsecurity --password ##Removedforsecurity --quiet --eval "db.getSiblingDB('##Removedforsecurity').product.find({brand:\"$brand\"}, {_id:0,name:1}).toArray()" > ./colour_colour_match.csv
				
							
							
							for assigned in "${!colours[@]}";
								do
									#echo "$assigned - ${colours[$assigned]}"
									newcolour=${colours[$assigned]}
									echo "db.getSiblingDB('##Removedforsecurity').product.updateMany(" >> ./product_amend_list.js
									echo "{brand:\"$brand\"," >> ./product_amend_list.js
									
									echo "##### $brand - $assigned >>> $newcolour #####"

									sed -e '/2020/d;s/://g;s/name//g;s/["]//g;s/[]{}]//g;s/^[[:space:]]*//;s/[[:space:]]*$//;/^$/d' "$colour_colour_match" | while IFS=$',' read -a Results_Array 
										do
											
											for i in "${Results_Array[@]}";
												do
													if

														[[ $i == *"$assigned"* ]]
														then
															product_name=$i
															echo "$product_name"
															
													fi

													
												done
											
										done

									echo "name:/$assigned/," >> ./product_amend_list.js

									echo "}, { \$set: {color:\"$newcolour\"}}" >> ./product_amend_list.js
									echo ")" >> ./product_amend_list.js
								done
						

								mongo mongodb+srv://##Removedforsecurity  --username ##Removedforsecurity --password ##Removedforsecurity --quiet --eval "load(\"$colourjs\")"
			
				else
					
					echo "skip colour reassignment"
								
			fi
			##################End Fixed Colour Assignment##################
			
      
      ## Commented Out, in Beta
			##################start ai colour match########################
			#		echo "Start AI Colour Assignment"
			#		#mongo mongodb+srv://##Removedforsecurity  --username ##Removedforsecurity --password ##Removedforsecurity --quiet --eval "db.getSiblingDB('##Removedforsecurity').product.find({brand:\"$brand\"}, {_id:0,name:1}).toArray()" > ./remaining_colour_match.csv
			#		#mongo mongodb+srv://##Removedforsecurity  --username ##Removedforsecurity --password ##Removedforsecurity --quiet --eval "db.getSiblingDB('##Removedforsecurity').product.find({brand:\"$Brands_Array\", color:""}, {_id:0,urlString:1}).toArray()" > ./remaining_colour_match.csv
			#		
			#		echo "$Brands_Array"
			#		echo "$Brands_Array" > ./script_output_brand.csv
			#		
			#		bash ./script_ai_color.sh 
			#		
			#		echo "$AI_input_file"
			#		sed -e '' "$AI_input_file" | while IFS=$',' read product_url product_image_long
			#			do
			#				product_image=$(echo $product_image_long | sed 's/n .*//')
			#				echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
			#				echo "$product_url"
			#				echo "$product_image"
			#				curl $product_image > ./curl_image.png
			#				output="$(./color-extractor ./color-extractor-master/color_names.npz $image_input)"
			#				echo "$output"
			#				echo "${output^}"
			#				C_output="${output^}"
			#				echo "$product_image,$C_output" >> ./final_colour_output.csv
			#				
			#				#Prepare .js File to load into DB
			#				echo "db.getSiblingDB('##Removedforsecurity').product.updateMany(" >> ./AI_colour_output.js
			#				echo "{brand:\"$Brands_Array\"," >> ./AI_colour_output.js 
			#				echo "urlString:\"$product_url\"," >> ./AI_colour_output.js
			#				##might need to add image_url otherwise products with same url but different image/colours will not overwrite all. will probably have to use /image_url/ incase of multiple images
			#				echo "}, { \$set: {color:\"$C_output\"}}" >> ./AI_colour_output.js
			#				echo ")" >> ./AI_colour_output.js	
			#			done 
			#
			#		mongo mongodb+srv://##Removedforsecurity  --username ##Removedforsecurity --password ##Removedforsecurity --quiet --eval "load(\"$AI_colour_load_file\")"
			#		echo "End AI Colour Assignment"
			##################End ai colour match########################


      
			##################Start Category amendment###################
              Standardise Product Categories from the web
      #############################################################
			echo "Start Categories Amended"
			echo "$file3" #./00_Category_Reassignment.csv
			sed '1d' "$file3" | while IFS=$',' read Brand GENDER CRAWLED_CAT BRAND_SUB PARENT SUB
				do	
				
					#@@@@@@@Recently added@@@@@@@@@#
					if [[ "$Brand" == "$Brands_Array" ]]
						then
							echo "db.getSiblingDB('##Removedforsecurity').product.updateMany({gender:\"$GENDER\", brand:\"$Brand\", category:\"$CRAWLED_CAT\", name:/$BRAND_SUB/}, { \$set : {category:\"$PARENT\", subcategory:\"$SUB\"}})" >> ./subcat_amend.js
							
							##remove category_Id file for new brand
							
							
						
						echo "CategoriesIDs Amended"
						
					fi
				done
				
			sed '1d' "$file7" | while IFS=$',' read Gender1 Category_Name Category_Id Subcategory_Name Subcategory_Id
				do
					echo "db.getSiblingDB('##Removedforsecurity').product.updateMany({brand:\"$Brands_Array\", gender:\"$Gender1\", category:\"$Category_Name\", subcategory:\"$Subcategory_Name\"}, { \$set : {categoryId:\"$Category_Id\", subCategoryId:\"$Subcategory_Id\"}})" >> ./catIds_reassign.js
				
					echo "$Brand-$Gender-$Category_Name-$Subcategory_Name"
				
				done		
					
				
			
			#Load Category Adjustments
			mongo mongodb+srv://##Removedforsecurity  --username ##Removedforsecurity --password ##Removedforsecurity --quiet --eval  "load(\"$subcatjs\")"
			mongo mongodb+srv://##Removedforsecurity --username ##Removedforsecurity --password ##Removedforsecurity --quiet --eval  "load(\"$CatIdsjs\")"
			
			echo "End Categories Amended"
			
			##################End Category amendment###################

			
			##################Start Resize Images where required#######
			echo "HERE"
			if [[ -z "$Size" ]]
				then
					echo "No size input"
				else
					echo	"db.getSiblingDB('##Removedforsecurity').product.aggregate([" >> ./image_size_update.js
					echo	"  {" >> ./image_size_update.js
					echo	"	\$match: {" >> ./image_size_update.js
					echo	"	  imageUrl: {" >> ./image_size_update.js
					echo	"		\$regex: \"$Size\"" >> ./image_size_update.js
					echo	"	  }," >> ./image_size_update.js
					echo	"	  brand: \"$Brands_Array\"" >> ./image_size_update.js
					echo	"	}" >> ./image_size_update.js
					echo	"  }," >> ./image_size_update.js
					echo	"  {" >> ./image_size_update.js
					echo	"	\$addFields: {" >> ./image_size_update.js
					echo	"	  imageUrl: {" >> ./image_size_update.js
					echo	"		\$reduce: {" >> ./image_size_update.js
					echo	"		  input: {" >> ./image_size_update.js
					echo	"			\$slice: [" >> ./image_size_update.js
					echo	"			  {" >> ./image_size_update.js
					echo	"				\$split: [" >> ./image_size_update.js
					echo	"				  \"\$imageUrl\"," >> ./image_size_update.js
					echo	"				  \"$Size\"" >> ./image_size_update.js
					echo	"				]" >> ./image_size_update.js
					echo	"			  }," >> ./image_size_update.js
					echo	"			  1," >> ./image_size_update.js
					echo	"			  {" >> ./image_size_update.js
					echo	"				\$size: {" >> ./image_size_update.js
					echo	"				  \$split: [" >> ./image_size_update.js
					echo	"					\"\$imageUrl\"," >> ./image_size_update.js
					echo	"					\"$Size\"" >> ./image_size_update.js
					echo	"				  ]" >> ./image_size_update.js
					echo	"				}" >> ./image_size_update.js
					echo	"			  }" >> ./image_size_update.js
					echo	"			]" >> ./image_size_update.js
					echo	"		  }," >> ./image_size_update.js
					echo	"		  initialValue: {" >> ./image_size_update.js
					echo	"			\$arrayElemAt: [" >> ./image_size_update.js
					echo	"			  {" >> ./image_size_update.js
					echo	"				\$split: [" >> ./image_size_update.js
					echo	"				  \"\$imageUrl\"," >> ./image_size_update.js
					echo	"				  \"$Size\"" >> ./image_size_update.js
					echo	"				]" >> ./image_size_update.js
					echo	"			  }," >> ./image_size_update.js
					echo	"			  0" >> ./image_size_update.js
					echo	"			]" >> ./image_size_update.js
					echo	"		  }," >> ./image_size_update.js
					echo	"		  in: {" >> ./image_size_update.js
					echo	"			\$concat: [" >> ./image_size_update.js
					echo	"			  \"\$\$value\"," >> ./image_size_update.js
					#Monitor below::::
					echo	"			  \"_850x\"," >> ./image_size_update.js
					echo	"			  \"\$\$this\"" >> ./image_size_update.js
					echo	"			]" >> ./image_size_update.js
					echo	"		  }" >> ./image_size_update.js
					echo	"		}" >> ./image_size_update.js
					echo	"	  }" >> ./image_size_update.js
					echo	"	}" >> ./image_size_update.js
					echo	"  }" >> ./image_size_update.js
					echo	"]).forEach( doc => db.getSiblingDB('##Removedforsecurity').product.updateOne( { _id: doc._id }, { \$set: { imageUrl: doc.imageUrl } } ) )" >> ./image_size_update.js	

					mongo mongodb+srv://##Removedforsecurity  --username ##Removedforsecurity --password ##Removedforsecurity --quiet --eval "load(\"$image_resize_file_load\")"
			 
			fi
			
			

			##################End Resize Images where required#######
			
			
			
			
			echo "@@Crawler DONE - $Brands_Array@@"
			
			
	done
