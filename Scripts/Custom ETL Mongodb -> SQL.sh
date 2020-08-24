#!/usr/local/bin/

#current path
DIR=$(pwd)
ps=`##Removedforsecurity`

dateyes=`date -d yesterday '+%Y-%m-%d'`
date=`date '+%Y-%m-%d'`
mongodbdate="${date}T00:00:00Z"
mongodbdateyes="${dateyes}T00:00:00Z"


echo "$mongodbdateyes"
echo "$mongodbdate"

mongoexport --uri="mongodb+srv://##Removedforsecurity" --collection=product --out="Product Data.json"
#mongoexport --uri="mongodb+srv://##Removedforsecurity" --collection=product --out="Product Data.json" 
#mongoexport --uri="mongodb+srv://##Removedforsecurity" --collection=user -q "{ 'firstName' : '', 'lastName' : '' }" --out="User Data.json" 

# Mongodb json data for ETL to MYSQL
mv $DIR/Product\ Data.json $DIR/input/
mv $DIR/User\ Data.json $DIR/input/
#mv $DIR/Product\ Data1.json $DIR/input/
#mv $DIR/User\ Data1.json $DIR/input/




sql="mysql -h ##Host -D ##Database -P 3306 -u##User -p##Password -e"


##########PRODUCT###########
###JSON  --->  CSV START####
function products_json_to_csv() {
	cat $DIR/input/Product\ Data.json | \

	jq -rc '[._id[]] + [.brand] + [.urlString] + [.isDelete] + [.category] + [.subcategory] + [.name] + [.gender] + [.currency] + [.price] + [.salePrice] + [.color] + [.region] + [.createdOn[]] + [.crawlerUrlId] + [.homeUrl] + [.subCategoryId] + [.categoryId] + [.wardrobeCount] + [.deleteCount] + [.date[]] | @csv' > $DIR/output/product_data.csv
}
###JSON  --->  CSV END####
##########PRODUCT###########


##########USER###########
###JSON  --->  CSV START####
function users_json_to_csv() {
	cat $DIR/input/User\ Data.json | \

	jq -rc '[._id[]] + [.firstName] + [.lastName] + [.email] + [.ageRange] + [.gender] + [.countryCode] + [.mobileNo] + [.region] + [.isActive] + [.createdDate[]] + [.enabled] +  [.pushNotification] | @csv' > $DIR/output/user_data.csv

}
###JSON  --->  CSV END####
##########USER###########

##########RIGHT SWIPES###########
###JSON  --->  CSV START####
function rightswipes_json_to_csv() {
	cat $DIR/input/User\ Data.json | \

	jq -rc '[._id[]] + (.wardrobeProduct[] | [.productId] + [.favourite] + [.date[]]) | @csv' > $DIR/output/rightswipe_data.csv
}
###JSON  --->  CSV END####
##########RIGHT SWIPES###########


##########LEFT SWIPES###########
###JSON  --->  CSV START####
function leftswipes_json_to_csv() {
	cat $DIR/input/User\ Data.json | \

	jq -rc '[._id[]] + (.deleteProduct[] | [.productId] + [.date[]]) | @csv' > $DIR/output/leftswipe_data.csv
}

###JSON  --->  CSV END####
##########LEFT SWIPES###########


function insert_products_sql() {
   sed 's/["]//g' "$DIR/output/product_data.csv" | while IFS=$',' read id brand urlString isDelete category subcategory productName gender currency price salePrice color region createdOn crawlerUrlId homeUrl subCategoryId categoryId wardrobeCount deleteCount date
    do
      if [ -z "$id" ]
        then
            echo "End of Document"
            echo "Kingswoop"
        else
			
			
			SUB="'"
			
			if [[ "$brand" == *"$SUB"* ]]; 
				
				then 
				
				brand="${brand//$SUB/}"
				echo "$brand"
					
					
			elif [[ "$coverImageUrl" == *"$SUB"* ]]; 
				then
				  coverImageUrl="${coverImageUrl//$SUB/}"
				  echo "$coverImageUrl"
				  
			elif [[ "$productName" == *"$SUB"* ]]; 
				then
				  productName="${productName//$SUB/}"
				  echo "$productName"
				
			fi
               
            echo "$id"
            $sql "INSERT INTO PRODUCTS
            (productId,brand,urlString,isDelete,category,subcategory,productName,gender,currency,price,salePrice,color,region,createdOn,crawlerUrlId,homeUrl,subCategoryId,categoryId,wardrobeCount,deleteCount,date,lastUpdated) 
            VALUES 
            ('$id', '$brand' ,'${urlString}','$isDelete', '$category','$subcategory',\"${productName}\",'$gender','$currency','$price','$salePrice','$color','$region','$createdOn','$crawlerUrlId','${homeUrl}','$subCategoryId','$categoryId','$wardrobeCount','$deleteCount','$date',NOW())
			ON DUPLICATE KEY UPDATE productId=VALUES(productId);" 
      fi
    done
}


function insert_users_sql() {
   sed 's/["]//g' "$DIR/output/user_data.csv" | while IFS=$',' read id firstName lastName email ageRange gender countryCode mobileNo region isActive createdDate enabled pushNotification roles
    do
      if [ -z "$id" ]
        then
            echo "End of Document"
            echo "Kingswoop"
        else
		
			#######REMOVE ' which causes error in run#######
			SUB="'"
			
			if [[ "$lastName" == *"$SUB"* ]]; 
				
				then 
				
				lastName="${lastName//$SUB/}"
				echo "$lastName"
					
					
			elif [[ "$firstName" == *"$SUB"* ]]; 
				then
				  firstName="${firstName//$SUB/}"
				  echo "$firstName"
				
			fi
			
			
               
               echo "$id"
            $sql "INSERT INTO USERS
            (userid,firstName,lastName,email,ageRange,gender,countryCode,mobileNo,region,isActive,createdDate,enabled,pushNotification,roleName,lastUpdated) 
            VALUES 
            ('$id','${firstName}','${lastName}','${email}','${ageRange}','$gender','$countryCode','$mobileNo','$region','$isActive','$createdDate','$enabled','$pushNotification','$roles',NOW())
			ON DUPLICATE KEY UPDATE userid=VALUES(userid);"
      fi
    done
}



function insert_rightswipes_sql() {
   sed 's/["]//g' "$DIR/output/rightswipe_data.csv" | while IFS=$',' read userid productId favourite date
    do
      if [ -z "$userid" ]
        then
            echo "End of Document"
            echo "Kingswoop"
        else
               
               echo "$id"
            $sql "INSERT INTO SWIPES
            (userid,productId,direction,favourite,date,lastUpdated) 
            VALUES 
            ('$userid','$productId','right','$favourite','$date',NOW());" 
      fi
    done
}

function insert_leftswipes_sql() {
   sed 's/["]//g' "$DIR/output/leftswipe_data.csv" | while IFS=$',' read userid productId favourite date
    do
      if [ -z "$userid" ]
        then
            echo "End of Document"
            echo "Kingswoop"
        else
               
               echo "$userid"
            $sql "INSERT INTO SWIPES
            (userid,productId,direction,favourite,date,lastUpdated) 
            VALUES 
            ('$userid','$productId','left',null,'$date',NOW());" 
      fi
    done
}





################
######MAIN######
################
products_json_to_csv
users_json_to_csv
rightswipes_json_to_csv
leftswipes_json_to_csv

insert_products_sql
insert_users_sql
insert_rightswipes_sql
insert_leftswipes_sql

#E
