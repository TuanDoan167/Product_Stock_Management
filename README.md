# Warehouse_inventory_management
A program written in Python to help with warehouse inventory

When the program starts, it asks the user the name of the file containing the product information and stores it in a dictionary (dict). Where the product code (int) is the key and the payload is a Product type object.

Each product should contains the following information:

  CODE: a unique product code in int type 
  NAME: the name of the product in str type
  CATEGORY: the product category in str type
  PRICE: the price of the product in € float type
  STOCK: the quantity of the items in stock in int type
  
The program allows the following commands to makes changes or look up the products information:
  print: Prints all known products in ascending order by product code.
  print a_product_code: Prints the information of the product specified by the code.
  change a_product_code amount: Changes the inventory amount of the product indicated by the code by the amount.
  delete a_product_code: Deletes the product identified by the code from the warehouse inventory. Only a product whose quantity in the inventory is 0 or less can be  deleted.
  low: Prints all products in ascending order by product code whose inventory quantity has fallen below a preset limit. The preset limit is 30. In the code template this is expressed with the constant LOW_STOCK_LIMIT.
combine a_product_code another_product_code: Combines two producsts with the same price in the same category into one.
sale a_category sale_percentage: Sets all the products belonging to the category on sale for sale_percentage%.
