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

     '''
     im1 = objs[0][0].filter(ImageFilter.FIND_EDGES)
     im2 = objs[0][1].filter(ImageFilter.FIND_EDGES)
     '''


     '''
     # Try no manipulation
     testSame = ImageOperations.noOp(objs)
     same = True
     for i in range(0,(len(objs)-1)):
         if testSame.isRowValid(objs[i]) == False:
            same = False
            break
     if same == True:
         for choice in choices:
                 if testSame.compCandidate(objs[len(objs)-1], choices[choice]) == True:
                     out = int(choice)


     # Try fills
     if out < 0:
       fillsFlag = True
       fillObj = ImageOperations.fillOp(objs)
       for i in range(0,len(objs)-1):
           temp  = fillObj.getFillFactorRow(objs[i])
           fillsFlag = fillObj.isValid(temp)


       if fillsFlag == True:
          for choice in choices:
              print(choice)
              print(objs[len(objs)-1])
              if fillObj.compCandidate(objs[len(objs)-1], choices[choice]) == True:
                  print(choice,"is right")
                  out = int(choice)
     '''

     # Try transform
     if out < 0:
       transFlag = True
       transObj = ImageOperations.transformOp(objs)
       for i in range(0,len(objs)-1):
           print("baselines")
           objs[i]=transObj.getEdgeOnlyRow(objs[i])
           temp  = transObj.getPixelDiffRow(objs[i])
           print(temp)
           transFlag = transObj.isValid(temp,thresh=10)


       if transFlag == True:
          for choice in choices:
              print(choice)
              if transObj.compCandidate(objs[len(objs)-1], choices[choice]) == True:
                  print(choice,"is right")
                  out = int(choice)


     '''
       factor =  fillObj.getFillFactorRow(fillObj.getEdgeOnlyRow(objs[0]))
       factor1 =  fillObj.getFillFactorRow(fillObj.getEdgeOnlyRow(objs[1]))
       print(factor)
       print(factor1)
     '''

     '''
       fillObj.storeFillFactor(factor)
       for choice in choices:
           if fillObj.compCandidate(objs[1][0], choices[choice]) == True:
               out = int(choice)
     '''
     '''
     # Try transforms
     if out < 0:
           transObj = ImageOperations.transformOp(objs)
           pixDiff =  transObj.getPixelDiffRow(transObj.getEdgeOnlyRow(objs[0]))
           pixDiff1 =  transObj.getPixelDiffRow(transObj.getEdgeOnlyRow(objs[1]))
           print(pixDiff)
           print(pixDiff1)
           transObj.storePixelDiff(pixDiff)
           print("A and B pix diff")
           print(pixDiff)
           for choice in choices:
               print(choice)
               if transObj.compCandidate(obj3, choices[choice]) == True:
                   out = int(choice)
     '''

     '''
     diff = ImageChops.difference(A, B)

     a_s = A.split()
     # print(a_s[0].getpixel((0,0)))
     # print(self.similarity(A,B))
     '''

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


    if problem.hasVisual == True:
        try:
            out = self.solveVerbal(problem,prob_mat)
        except:
            out = -1


    if out < 0:
        out = self.solveVisual(problem, prob_mat)


    #out = self.solveVerbal(problem, prob_mat)
    #out = self.solveVisual(problem,prob_mat)



    print(out)
    return out














