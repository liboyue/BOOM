import sys

if len(sys.argv) != 2:
    print("Please pass the path to the result file as an argument!")
    sys.exit()

fi = open(sys.argv[1])

best_rouge = 0
best_config = None

for i, line in enumerate(fi):
   if i > 1:
       config, score = line.split(",")
       score = float(score)
       if score > best_rouge:
           best_config = config
           best_rouge = score 

fi.close()
print("Best rouge:", best_rouge)
print("Best config:", best_config)
