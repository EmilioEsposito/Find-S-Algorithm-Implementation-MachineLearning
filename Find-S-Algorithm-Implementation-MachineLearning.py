# Emilio Esposito
# Machine Learning
# Part A Find-S Algorithm

import sys

with(open("9Cat-Train.labeled", "r")) as f:
    trainDoc = f.read()

# this fcn takes a document after read() and converts it into 2 lists-of-lists
# first return is is is form df[row][column] and second is dfT[column][row]
def dataframe(doc):
    lines = doc.split("\n")

    df = []

    # read file into list of lists
    for r in range(0, len(lines)):
        # make sure it's not a null line
        if lines[r] != "":
            # split record into distinct attributes
            attr = lines[r].split("\t")
            # create an empty list to hold row contents
            df.append([])
            # iterate through each attr pair and only store the value
            for c in range(0, len(attr)):
                df[r].append(attr[c].split(" ")[1].rstrip())

    # get transposed df: dfT
    dfT = []
    for c in range(0, len(df[0])):
        dfT.append([])
        for r in range(0, len(df)):
            dfT[c].append(df[r][c])

    return df, dfT

# first return is is is form df[row][column] and second is dfT[column][row]
train, trainT = dataframe(trainDoc)

# find input space size |x|
xLen = 1
# find unique values of each X input (exclude last output col)
for attr in trainT[:len(trainT)-1]:
    xLen *= len(set(attr))

# find concept space size |C|
cLen = 2 ** xLen
digitsC = len(str(cLen))

# find hyp space size |h|
hLen = 1
for attr in trainT[:len(trainT)-1]:
    hLen *= len(set(attr)) + 1
# add null set case
hLen += 1

# output PART A 1-3
sys.stdout.write(str(xLen)+"\n")
sys.stdout.write(str(digitsC)+"\n")
sys.stdout.write(str(hLen)+"\n")

# PART A4
partA4 = open("partA4.txt", "w")
hyp = []
cnt = 0
# Implement Find-S algorithm
for obs in train:
   # print(obs)
    cnt += 1
    if obs[len(obs) - 1] == "high":
        x = obs[:len(obs) - 1]
     #   print(x)
        # reinitialize hypothesis with pos x if it's empty
        if len(hyp)==0:
            hyp = x
        # otherwise compare hypothese
        else:
            for i in range(0,len(hyp)):
                if x[i] != hyp[i]:
                    hyp[i] = "?"
    # write every 30 hypothesis
    if cnt % 30 == 0:
        partA4.write("\t".join(hyp))
        partA4.write("\n")
#print(hyp)

# PART A5 - Dev
with(open("9Cat-Dev.labeled", "r")) as f:
    devDoc = f.read()
    
dev, devT = dataframe(devDoc)

# this function takes a df[row][col] and a hypothesis[col] and returns a pred[row] list
def get_pred(df, hyp):
    # make empty list to hold predications
    pred = []
    for obs in df:
        outcome = True
        for i in range(0, len(hyp)):
            # check if hypothesis is satisfied
            if hyp[i] == "?" or obs[i] == hyp[i]:
                outcome *= True
            else:
                outcome *= False
            #sys.stdout.write(str(outcome)+"\t"+dfVal+"\t"+hVal+"\n")
        # predict "high" if hypothesis is satisfied
        if outcome:
            pred.append("high")
        else:
            pred.append("low")
    return pred

pred = get_pred(dev, hyp)
truth = devT[len(devT)-1]

miss = []
for p, t in zip(pred, truth):
    if p == t:
        miss.append(0)
    else:
        miss.append(1)
missRate = sum(miss)/float(len(miss))

# output A5 miss rate
sys.stdout.write(str(missRate)+"\n")


# PART A6 - Testing
with(open(sys.argv[1], "r")) as f:
    testDoc = f.read()

test, testT = dataframe(testDoc)

pred = get_pred(test, hyp)

# output A6 pred
print(str("\n".join(pred)))
