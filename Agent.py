    # Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

from PIL import Image
import numpy as np


from PIL import ImageFilter, ImageMath, ImageChops
import math as math
import ImageOperations

class Agent:
# The default constructor for your Agent. Make sure to execute any
# processing necessary before your Agent starts solving problems here.
#
# Do not add any variables to this signature; they will not be used by
# main().
 def __init__(self):
     pass

# The primary method for solving incoming Raven's Progressive Matrices.
# For each problem, your Agent's Solve() method will be called. At the
# conclusion of Solve(), your Agent should return an int representing its
# answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints
# are also the Names of the individual RavensFigures, obtained through
# RavensFigure.getName(). Return a negative number to skip a problem.
#
# Make sure to return your answer *as an integer* at the end of Solve().
# Returning your answer as a string may cause your program to crash.


 def attributeComp(self, obj1, obj2, attrMap, obj1Number):
     map = {}
     comp1 = obj1
     comp2 = obj2
     for attributeName in comp1.attributes:

         if attributeName not in comp2.attributes:
             map[attributeName] = 'D'
         elif attributeName == 'inside' or attributeName == 'above':
             key = comp2.attributes[attributeName]
             print(key)
             print(attrMap)
             inside = attrMap[key]
             map[attributeName] = float(inside) - float(obj1Number)
         elif comp1.attributes[attributeName] == comp2.attributes[attributeName]:
             map[attributeName] = 'S'
         elif attributeName == 'angle':
             map[attributeName] = math.cos(float(comp2.attributes[attributeName]) - float(comp1.attributes[attributeName]))
         elif comp1.attributes[attributeName].isdigit() == True:
             map[attributeName] = float(comp2.attributes[attributeName]) - float(comp1.attributes[attributeName])
         elif comp1.attributes[attributeName].isdigit() == False:
             map[attributeName] = [comp1.attributes[attributeName], comp2.attributes[attributeName]]

     return map



 def objectComp(self, objs, attrMap):
     out = []
     for j in range(0,len(objs)-1):
         obj1 = objs[j]
         obj2 = objs[j+1]
         traits = []
         for i in range(0,len(obj1)):
              temp1 = obj1[i]
              if i > (len(obj2)-1):
                  traits.append({'Deleted':'YES'})
                  break
              else:
                  temp2 = obj2[i]
              AB = self.attributeComp(temp1, temp2,attrMap[j+1],i)
              traits.append(AB)
         out.append(traits)
     return out

 def dict2SortedList(self, obj):
     #obj is a dictionary of objects
     order = sorted(obj)
     sortObj = []
     counter = 0
     key2Num = {}
     for ob in order:
        sortObj.append(obj[ob])
        key2Num[ob]=counter
        counter =  counter +1
     return sortObj, key2Num


 def solveVerbal(self, problem, prob_mat):
     out = -1
     obj = []
     obj_s = []
     for m in prob_mat:
         obj1_t = []
         obj1_s_t = []
         for o in m:
             obj1, obj1_s = self.dict2SortedList(o.objects)
             obj1_t.append(obj1)
             obj1_s_t.append(obj1_s)
         obj.append(obj1_t)
         obj_s.append(obj1_s_t)

     nums = ['1', '2', '3', '4', '5', '6']
     choices = []
     attr_map = []
     #attr_map.update(obj2_s)
     #print(attr_map)

     for num in range(0, len(nums)):
        sortedObj, sortedObj_s = self.dict2SortedList(problem.figures[nums[num]].objects)
        attr_map.append(sortedObj_s)
        choices.append(sortedObj)
     #print("choices and sht")
     #print(choices)
     #print(attr_map)


     A_BComp = self.objectComp(obj[0], obj_s[0])
     #print("ABComp")
     #print(obj[0])
     #print(obj_s[0])
     #print(A_BComp)

     choiceNum = 0
     for i in range(0,len(choices)):
         choiceNum = choiceNum + 1
         c = obj[1][:]
         c.append(choices[i])
         a = obj_s[1][:]
         a.append(attr_map[i])

         C_d = self.objectComp(c, a)
         #print("C_d")
         #print(C_d)
         counter = 0
         for i in range(0,len(C_d)):
             if np.array_equal(np.array(C_d[i]), A_BComp[i]) == False:
                 break
             counter = counter + 1
         if counter == len(C_d):
             #print("Found it")
             out = choiceNum
             #print(C_d)
             break
     print(out)
     return out


 def solveVisual(self,problem, prob_mat):
     out = -1
     objs = []
     for m in prob_mat:
         temp = []
         for obj in m:
             temp.append(Image.open(obj.visualFilename).convert(mode='L'))
         objs.append(temp)

     nums = ['1','2','3', '4', '5', '6','7','8']
     choices = {}
     for num in nums:
         temp = problem.figures[num]
         obj = Image.open(temp.visualFilename).convert(mode='L')
         choices[num]=obj


     control = ImageOperations.framesControl()
     ansOp = ImageOperations.answerOp(objs)
     answers = choices.copy()

     #Build the operation frames depository
     sameSetObj = ImageOperations.sameSetOp(objs)
     fillObj = ImageOperations.fillOp(objs)
     sameObj = ImageOperations.noOp(objs)
     transObj = ImageOperations.transformOp(objs)
     transSetObj = ImageOperations.transformOpBySet(objs)
     transSetConst = ImageOperations.transformOpBySetConstantDiff(objs)
     transSetDiag = ImageOperations.transformOpBySetDiag(objs)
     objsE = transObj.getEdgeOnlyBlock(objs)
     choicesE = transObj.getEdgeOnlyChoices(choices)

     choiceCol = [objs[0][2],objs[1][2]]
     objsInv = []
     for i in range(0,(len(objs)-1)):
         objsInv.append(fillObj.getColImgs(objs,i))
     objsInv.append(choiceCol)




     #Constants/Helper Values
     checkFactor = np.average(fillObj.getFillFactorRow(objs[0]))
     diagRefImgs = []
     objsRef = []
     for i in range(0,len(objsInv)):
         objsRef.append(fillObj.getDiagonalMatrix(objsInv[i],objsInv[0]))
     diagRefImgs = objsRef[1]

     print('diag ref img')
     print(fillObj.getImgVal(diagRefImgs))



     args = [#(objs,sameSetObj,choices,sameSetObj.getFillFactorRow,sameSetObj.isValid,0.99,objs[0]),
             (objsInv,transSetDiag,choices,transSetDiag.getFillFactorRow,transSetDiag.isValid,20,objsInv[0],diagRefImgs)
             #(objs,transSetConst,choices,transSetConst.getFillFactorRow,transSetConst.isValid,20,objs[0]) #Solves 6
             #(objs,transSetObj,choices,transSetObj.getFillFactorRow,transSetObj.isValid,10,objs[0])#Solves 4,5
             #(objsE,transObj,choicesE,transObj.getFillFactorRow,transObj.isValid,10),
             #(objs,transObj,choices,transObj.getFillFactorRow,transObj.isValid,20)
             #(objs,sameObj,choices,sameObj.getFillFactorRow,sameObj.isValid,0.99),



             #(objs,fillObj,choices,fillObj.getFillFactorRow,fillObj.isValid,10000)
             ]

     choiceArgs = [#{'setImgs':objs[0]},
                   {'setImgs':objs[0],'refImgs':objs[0]},
                   #{'setImgs':objs[0]},
                   #{'setImgs':objs[0]},
                   {},
                   {},
                   {},

                   {}
                  ]
     tstArgs = [#{'fcn':ansOp.elimByPixels}#,
                #{'fcn':ansOp.elimBySimilarity,'thresh':.05},
                #{'fcn':ansOp.elimByFactor,'factor': checkFactor,'thresh':.02 },
                #{'fcn':ansOp.elimByFirstColumn,'factor': checkFactor,'thresh':3, 'compIdx':0 }

               ]



     # Try transform on Edge of figures, solve 1,2,4,5,6,
     if out < 0:
       argsIdx = 0
       while ansOp.isValid(answers) == False and argsIdx < len(args):
           answers = args[argsIdx][2].copy()
           transFlag = control.getProbRelation(*args[argsIdx])
           if transFlag == True:
              answers = control.testChoices(args[argsIdx][0],answers, args[argsIdx][1].compCandidate,**choiceArgs[argsIdx])
              if ansOp.isValid(answers):
                  out,value = answers.items()[0]
                  break
              else:
                  elimIdx = 0
                  while ansOp.isValid(answers) == False and elimIdx < len(tstArgs):
                    answers = control.elimByFcn(answers, **tstArgs[elimIdx])
                    if ansOp.isValid(answers):
                        out,value = answers.items()[0]
                    elimIdx =  elimIdx +1
           argsIdx = argsIdx + 1




     '''
     # Try transform top half and bottom half, solve 8,10,3
     if out < 0:
       fillOp = ImageOperations.fillOp(objs)
       checkFactor = fillOp.getFillFactorRow(objs[0])
       checkFactor=np.average(checkFactor)
       answers = {}
       transFlag = True
       transObj = ImageOperations.transformOp(objs)
       fourOp = ImageOperations.divideImage(objs)
       for i in range(0,len(objs)-1):
           print("baselines")
           objsE = objs[i]
           groupedSegments = fourOp.groupSegments(objsE,2,1)
           print("this is ",i)
           for h in range(0,len(groupedSegments)):
             temp  = transObj.getFillFactorRow(groupedSegments[h])
             print(temp)
             flag = transObj.isOneDirection(temp)
             if flag == False:
                 transFlag = False
                 break



       if transFlag == True:
          for choice in choices:
              print(choice)
              candidate = objs[len(objs)-1][:]
              candidate.append(choices[choice])
              choiceSegments = fourOp.groupSegments(candidate,2,1)
              for h in range(0,len(choiceSegments)):
                 temp  = transObj.getFillFactorRow(choiceSegments[h])
                 print(temp)
                 flag = transObj.isOneDirection(temp)
                 if flag == False:
                    break
              if flag:
                 print(choice,"is right")
                 ans = int(choice)
                 answers[ans]=candidate

       ansOp = ImageOperations.answerOp(objs)

       if ansOp.isValid(answers):
           out = ans
       else:
           filterAns = ansOp.elimByFirstColumn(answers,0,3)#ansOp.elimBySimilarity(answers)
           print('final answer')
           print(answers)
           if ansOp.isValid(filterAns):
               out,value = filterAns.items()[0]
               print(out)
           else:
               filterAns = ansOp.elimBySimilarity(answers)
               print('final answer')
               print(answers)
               if ansOp.isValid(filterAns):
                out,value = filterAns.items()[0]
                print(out)
               else:
                   filterAns = ansOp.elimByFactor(answers,checkFactor)
                   print('final answer')
                   print(answers)
                   if ansOp.isValid(filterAns):
                    out,value = filterAns.items()[0]
                    print(out)

     '''

     '''
     #Same Top half, P#11
     if out < 0:
         fourOp = ImageOperations.divideImage(objs)
         segmentInd = [0,0]
         frameInd = [1,2]
         moveFlag = True
         thresh = .015
         answers = {}
         for i in range(0,2):
             groupedSegments = fourOp.groupSegments(objs[i],2,1)
             print("this is ",i)
             moveObj = ImageOperations.moveOp(objs)
             factorRow = moveObj.getFillFactorBlock(groupedSegments)
             print(factorRow)
             flag = moveObj.isSegmentSame(factorRow,segmentInd,frameInd, thresh)

             print(flag)
             if flag == False:
                 moveFlag = False
                 break

         if moveFlag == True:
             for choice in choices:
                print(choice)
                candidate = objs[len(objs)-1][:]
                candidate.append(choices[choice])
                groupedSegments = fourOp.groupSegments(candidate,2,1)
                groupedBlock = moveObj.getFillFactorBlock(groupedSegments)
                print(groupedBlock)
                flag = moveObj.isSegmentSame(groupedBlock,segmentInd,frameInd,thresh)
                if flag == True:
                  print(choice,"is right")
                  ans = int(choice)
                  answers[ans]=candidate

         ansOp = ImageOperations.answerOp(objs)
         filterAns = ansOp.elimByPixels(answers)
         print('final answer')
         print(answers)
         print(filterAns)
         if ansOp.isValid(filterAns):
            out,value = filterAns.items()[0]
            print(out)






     #1st and last same pixels, mirror effect, P#7
     if out < 0:
         fourOp = ImageOperations.divideImage(objs)
         segmentInd = [0,1]
         frameInd = [0,2]
         moveFlag = True
         thresh = .015
         noOp = ImageOperations.noOp(objs)
         answers ={}
         for i in range(0,2):
             groupedSegments = fourOp.groupSegments(objs[i],1,2)
             #groupedSegments = fourOp.getEdgeOnlyBlock(groupedSegments)
             print("this is ",i)
             moveObj = ImageOperations.moveOp(objs)
             factorRow = moveObj.getFillFactorBlock(groupedSegments)
             print(factorRow)
             flag = moveObj.isSegmentSame(factorRow,segmentInd,frameInd, thresh) and noOp.isValid([objs[i][0],objs[i][len(objs[i])-1]])

             print(flag)
             if flag == False:
                 moveFlag = False
                 break

         if moveFlag == True:
             for choice in choices:
                print(choice)
                candidate = objs[len(objs)-1][:]
                candidate.append(choices[choice])
                #candidate = fourOp.getEdgeOnlyRow(candidate)
                groupedSegments = fourOp.groupSegments(candidate,1,2)
                #groupedSegments = fourOp.getEdgeOnlyBlock(groupedSegments)
                groupedBlock = moveObj.getFillFactorBlock(groupedSegments)
                print(groupedBlock)
                flag = moveObj.isSegmentSame(groupedBlock,segmentInd,frameInd,thresh) and noOp.isValid([candidate[0],candidate[len(candidate)-1]])
                if flag == True:
                  print(choice,"is right")
                  ans = int(choice)
                  answers[ans]=candidate

         ansOp = ImageOperations.answerOp(objs)
         if ansOp.isValid(answers):
               out = ans
         else:
               filterAns = ansOp.elimBySimilarity(answers)
               print('final answer')
               print(answers)
               if ansOp.isValid(filterAns):
                   out,value = filterAns.items()[0]
                   print(out)
               else:
                   filterAns = ansOp.elimByFactor(answers,checkFactor)
                   print('final answer')
                   print(answers)
                   if ansOp.isValid(filterAns):
                    out,value = filterAns.items()[0]
                    print(out)
                   else:
                    filterAns = ansOp.elimByVerticalReflection(answers, 0, 0.9)
                    print('final answer')
                    print(answers)
                    if ansOp.isValid(filterAns):
                        out,value = filterAns.items()[0]
                        print(out)


     #1st and last same pixels, mirror effect, P#12
     if out < 0:
         answers = {}
         fourOp = ImageOperations.divideImage(objs)
         segmentInd = [1,1]
         frameInd = [1,2]
         moveFlag = True
         thresh = .015
         transOp = ImageOperations.transformOp(objs)
         for i in range(0,2):
             groupedSegments = fourOp.groupSegments(objs[i],2,1)
             #groupedSegments = fourOp.getEdgeOnlyBlock(groupedSegments)
             print("this is ",i)
             moveObj = ImageOperations.moveOp(objs)
             groupedBlock = moveObj.getFillFactorBlock(groupedSegments)
             factorRow =  transOp.getFillFactorRow(groupedSegments[1])
             thresh = 200
             print('thresh')
             print(thresh)
             print(groupedBlock)
             print(factorRow)
             flag =  transOp.isValid(factorRow,thresh) #moveObj.isSegmentSame(groupedBlock,segmentInd,frameInd, thresh)

             print(flag)
             if flag == False:
                 moveFlag = False
                 break


         if moveFlag == True:
             for choice in choices:
                print(choice)
                candidate = objs[len(objs)-1][:]
                candidate.append(choices[choice])
                #candidate = fourOp.getEdgeOnlyRow(candidate)
                groupedSegments = fourOp.groupSegments(candidate,2,1)
                #groupedSegments = fourOp.getEdgeOnlyBlock(groupedSegments)
                groupedBlock = moveObj.getFillFactorBlock(groupedSegments)
                print(groupedBlock)
                factorRow =  transOp.getFillFactorRow(groupedSegments[1])
                print(factorRow)
                thresh = 200
                print('thresh')
                print(thresh)
                flag =  transOp.isValid(factorRow,thresh) #moveObj.isSegmentSame(groupedBlock,segmentInd,frameInd,thresh)

                if flag == True:
                    print(choice,"is right")
                    ans = int(choice)
                    answers[ans]=candidate

         ansOp = ImageOperations.answerOp(objs)
         filterAns = ansOp.elimByPixels(answers)
         print('final answer')
         print(answers)
         print(filterAns)
         if ansOp.isValid(filterAns):
             out,value = filterAns.items()[0]
             print(out)
     '''

     print('OUT')
     print(out)
     return out


 def Solve(self, problem):
    out = -1

    #out = self.solveVerbal(problem)
    prob_mat = []
    if problem.problemType == '2x2':
        m1 = [problem.figures['A'],problem.figures['B']]
        prob_mat.append(m1)
        m2 = [problem.figures['C']]
        prob_mat.append(m2)

    if problem.problemType == '3x3':
        m1 = [problem.figures['A'],problem.figures['B'],problem.figures['C']]
        prob_mat.append(m1)
        m2 = [problem.figures['D'],problem.figures['E'],problem.figures['F']]
        prob_mat.append(m2)
        m3 = [problem.figures['G'],problem.figures['H']]
        prob_mat.append(m3)

    '''
    if problem.hasVisual == True:
        try:
            out = self.solveVerbal(problem,prob_mat)
        except:
            out = -1


    if out < 0:
        try:
            out = self.solveVisual(problem, prob_mat)
        except:
            out = -1
    '''




    out = self.solveVisual(problem,prob_mat)



    print(out)
    return out













