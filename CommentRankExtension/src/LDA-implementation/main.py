import sys
import csv
from LDA import LDA

import os
print(os.listdir("code"))  # Check if "attempt.csv" appears
print(os.listdir("data"))
print(os.getcwd())

print("Enter the path of the file: ('m' for manual data entry)")
path = input() # ../data/Female_lizards.csv
if path != "m":
    with open(path.strip(), 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)

        print("\nEnter the variables you wish to use, separate by comma: ('!' to ignore)")
        print("All variables: "+str(header[1:]))
        temp = input()
        if temp.strip() != "!":
            includes_list = temp.split(",")
            for i in range(len(includes_list)):
                includes_list[i] = includes_list[i].strip()
                includes_list[i] =  includes_list[i][1:] if includes_list[i][0] == "\'" else includes_list[i]
                includes_list[i] =  includes_list[i][:-1] if includes_list[i][-1] == "\'" else includes_list[i]
                if includes_list[i] not in header[1:]:
                    raise ValueError(str(includes_list[i])+" is not in the header of the input file.")
        else:
            includes_list = header[1:]
        variables_selected = includes_list
        
        data = []
        type_labels = []
        all_types = set()
        for row in reader:
            data.append([float(value) for i, value in enumerate(row) if header[i] in includes_list])
            type_labels.append(row[0])
            all_types.add(row[0])
else:
    type_labels = []
    data = []
    all_types = set()
    i = 0
    print("\nEnter data "+ str(i) + ": ('!' to end data entry)")
    temp = input().strip()
    while(temp != "!"):
        entered_str =  temp.split(",")
        vec = []
        for col in range(len(entered_str)):
            if col == 0:
                type_labels.append(entered_str[col].strip())
                all_types.add(entered_str[col].strip())
            else:
                vec.append(float(entered_str[col].strip()))
        data.append(vec)
        i += 1
        print("\nEnter data "+ str(i) + ": ('!' to end data entry)")
        temp = input().strip()

                


print("\nEnter the number of categories you wish to classify the dataset into, at least 2: ('!' to ignore)")
temp = input()
categories = []
if temp != "!":
    num_cat = int(temp)
    if num_cat < 2:
        raise ValueError(str(num_cat)+"is not valid for the number of categories")
    print("All types: " + str(all_types))
    for cat_index in range(num_cat):
        print("Enter the types you wish to be classified as Category " + str(cat_index)  + ", separated by comma: ")
        includes_list = input().split(",")
        for i in range(len(includes_list)):
            includes_list[i] = includes_list[i].strip()
            includes_list[i] =  includes_list[i][1:] if includes_list[i][0] == "\'" else includes_list[i]
            includes_list[i] =  includes_list[i][:-1] if includes_list[i][-1] == "\'" else includes_list[i]
            if includes_list[i] not in all_types:
                raise ValueError(str(includes_list[i])+" is not in the types listed in the input file.")
        categories.append(includes_list)
lda = LDA(data = data, type_label = type_labels, categories = categories)
print("\nDataset loaded successfully!")

print(
    "\nSelect the classification method you wish to use:"+
    "\n* 'm' for midpoint method: midpoint method is simpler and more concise(by default)"+
    "\n* 'z' for z-score method: assume the dataset is normally distributed; better prediction on large dataset,"+
    "\n\t but with more complicated rules."+
    "\n>", end=""
)
temp = input()
isStddev = True if temp.strip() == "z" else False
print()

lda.classify_all(isStddev)
lda.Classification_Result()

print("\nEnter the path of the output file: ('!' to ignore)")
output_path = input()
if output_path.strip() != '!':
    with open(output_path.strip(),"w") as file:
        sys.stdout = file
        if path != 'm':
            print("All variables: "+str(header[1:]))
            print("Variables selected: "+str(variables_selected))
            print()
            print("All types:"+str(all_types))
            for cat_index in range(len(categories)):
                print("Category "+str(cat_index)+": "+str(categories[cat_index]))
            method = "Z-score" if isStddev == True else "Midpoints"
            print("\nClassification method used: "+method)
            print()
            lda.Classification_Result()
    
 
