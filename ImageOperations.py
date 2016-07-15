#

from PIL import Image
import numpy as np


from PIL import ImageFilter, ImageMath, ImageChops
import math as math

class ImageOperations:

 def __init__(self, imgs):
     self.imgs = imgs

 def compCandidate(self):
     pass

 def isValid(self):
     pass

 def isRowValid(self):
     pass

 def similarity(self, im1, im2):
     im1 = im1.convert(mode='1')
     im2 = im2.convert(mode='1')
     p_a = list(im1.getdata())
     #print(p_a)
     p_b = list(im2.getdata())
     #print(p_b)
     ab = list(np.absolute(np.array(p_a)) - np.absolute(np.array(p_b)))
     #print(ab)
     #print(sum(ab))
     err = abs(float(sum(ab) / 255)/len(ab))
     return 1 - err

 def getImgVal(self, imgs):
      vals = []
      for i in range(0,len(imgs)):
          img1 = self.getArr(imgs[i])
          vals.append(np.sum(img1)/255)
      return vals


 def getArr(self, img):
     (width, height) = img.size
     o1_arr = np.array(list(img.getdata())).reshape((height, width))
     return o1_arr

 def getEdgeOnlyRow(self, imgs):
      out = []
      for img in imgs:
        out.append(img.filter(ImageFilter.FIND_EDGES))
      return out

 def getEdgeOnlyBlock(self,frames):
     out = []
     for i in range(0,len(frames)):
        out.append(self.getEdgeOnlyRow(frames[i]))
     return out

 def getEdgeOnlyChoices(self, dictOfImgs):
    out = dictOfImgs.copy()
    for key in dictOfImgs:
        out[key]=dictOfImgs[key].filter(ImageFilter.FIND_EDGES)
    return out


class noOp(ImageOperations):

  #def __init__(self, im1, im2):
  #  super(ImageOperations,self).__init__(im1,im2)
  def is_valid(self, im1, im2, thresh=0.99):
      out = False
      if self.similarity(im1, im2) >= thresh:
          out= True
      return out

  def isValid(self, imgRow, thresh=0.99):
      out = True
      for i in range(0,len(imgRow)-1):
          img1 = imgRow[i]
          img2 = imgRow[i+1]
          if self.similarity(img1,img2) < thresh:
              out = False
              break
      return out

  def getFillFactorRow(self,imgs):
      return imgs

  def compCandidate(self, imgs, choice):
      out = False
      newRow = imgs[:]
      newRow.append(choice)
      if self.isValid(newRow):
          out = True
      return out


class sameSetOp(noOp):
    def getFillFactorRow(self, imgs,setImgs):
        rowValsSet = self.getImgVal(setImgs)
        rowSet = sorted(rowValsSet)
        rowVals = self.getImgVal(imgs)
        row1 = sorted(rowVals)
        return [rowSet,row1]

    def isValid(self, rows, thresh=0.99):
        out = True
        out = True
        for i in range(0, len(rows[0])):
            val = 1-float(abs(rows[0][i]-rows[1][i]))/min(rows[0][i],rows[1][i])

            if val<=thresh:
                out = False
                break
        return out

    def compCandidate(self, imgs, choice, setImgs):
          out = False
          newRow = imgs[:]
          newRow.append(choice)
          rows = self.getFillFactorRow(newRow,setImgs)
          if self.isValid(rows):
              out = True
          return out


class moveOp(noOp):

  #def __init__(self, im1, im2):
  #  super(ImageOperations,self).__init__(im1,im2)

  def getFillFactor(self,im1):
      #arr1 = self.getArr(im1)
      #out =  np.sum(arr1)/255
      width,height = im1.size
      area = width * height
      arr1 = self.getArr(im1)
      out =  float(np.sum(arr1)/255)/area

      return out

  def getFillFactorRow(self, imgs):
    diffs = []
    for i in range(0,len(imgs)):
      img1 = imgs[i]
      diffs.append(self.getFillFactor(img1))
    return diffs

  def getFillFactorBlock(self,frames):
    out = []
    for i in range(0,len(frames)):
        temp = self.getFillFactorRow(frames[i])
        out.append(temp)
    return out

  def isSegmentSame(self, factorRow, segmentInd, frameInd, thresh=0.015):
      out = False
      print(abs(factorRow[segmentInd[0]][frameInd[0]] - factorRow[segmentInd[1]][frameInd[1]]))
      if abs(factorRow[segmentInd[0]][frameInd[0]] - factorRow[segmentInd[1]][frameInd[1]]) <= thresh:
          out = True
      return out

  def isSegmentSameBlock(self,frames, segmentInd, frameInd, thresh=6):
      out = True
      for i in range(0,len(frames)):
        if self.isSegmentSame(frames[i],segmentInd,frameInd,thresh):
          out = False
          break
      return out

class fillOp(ImageOperations):

      def getDiffArray(self, im1, im2):
          (width, height) = im1.size
          p_a = self.getArr(im1)
          p_b = self.getArr(im2)
          ab = np.resize((p_a-p_b),[width, height])
          return ab

      def getDiffHistogram(self, im1, im2):
          diff = ImageChops.difference(im1,im2).getdata()
          out =  np.sum(diff)/255
          return out

      def isValid(self, factorRow,thresh=.01):
          out = True
          for i in range(0,len(factorRow)-1):
            if float((abs(factorRow[i+1]-factorRow[i]))/float(max(abs(factorRow[i]),abs(factorRow[i+1])))) >= thresh:
                out = False
                break
          print(out)
          return out

      def getFillFactorRowHist(self,imgs):
          out = []
          for i in range(0, len(imgs)-1):
              out.append(self.getDiffHistogram(imgs[i],imgs[i+1]))
          return out

      def getFillFactor(self, im1, im2):
          width, height = im1.size
          div = width * height
          size1 = float(np.sum(abs(self.getArr(im1)))/255)
          size2 = float(np.sum(abs(self.getArr(im2)))/255)
          fillFactor = size2/size1
          #print(fillFactor)
          return fillFactor

      def getFillFactorRow(self, imgs, thresh=100):
          factors = []
          for i in range(0,len(imgs)-1):
              img1 = imgs[i]
              img2 = imgs[i+1]
              factors.append(self.getFillFactor(img1, img2))
          return factors

      def compCandidate(self, imgs, choice, thresh=100):
          out = False
          row = imgs[:]
          row.append(choice)

          choiceFactor = self.getFillFactorRow(row)
          print("choice factor")
          print(choiceFactor)
          if self.isValid(choiceFactor) == True:
              out = True
          return out


class transformOp(fillOp):
      def getFillFactor(self, im1, im2):
          p_a = self.getArr(im1)
          p_b = self.getArr(im2)
          pixelDiff = (np.sum(p_b)-np.sum(p_a))/255

          return pixelDiff

      def getFillFactorRow(self, imgs):
          diffs = []
          for i in range(0,len(imgs)-1):
              img1 = imgs[i]
              img2 = imgs[i+1]
              diffs.append(self.getFillFactor(img1, img2))
          print('diffs')
          print(diffs)
          return diffs

      def isValid(self, factorRow,thresh=10):
          out = True
          for i in range(0,len(factorRow)-1):
            if abs(factorRow[i+1]-factorRow[i]) >= thresh:
                out = False
                break
          print('isValid?')
          print(out)
          return out


      def isOneDirection(self,factorRow):
        out = False
        row = np.array(factorRow)
        if (row>0).all(axis=0) or (row<0).all(axis=0):
            out = True
        return out

      def compCandidate(self, imgs, choice):
          out = False
          row = imgs[:]
          row.append(choice)
          #row = self.getEdgeOnlyRow(row)
          '''
          for i in range(0, len(row)):
              row[i].save(str(i),'JPEG')
          '''

          pixelFactor = self.getFillFactorRow(row)
          print("pixel factor")
          print(pixelFactor)
          if self.isValid(pixelFactor) == True:
              out = True
          return out

class transformOpBySet(transformOp):
      def getFillFactorRow(self, imgs, setImgs):
          diffs = transformOp.getFillFactorRow(self,imgs)
          diffsSet = transformOp.getFillFactorRow(self,setImgs)
          diffSq = np.array(diffs)-np.array(diffsSet)
          diffSq = diffSq.tolist()
          print('diffSq')
          print(diffSq)
          return diffSq

      def isValid(self, diffsRow,thresh=10):
          out = True
          for i in range(0,len(diffsRow)):
            print('difference')
            print(abs(diffsRow[i]))
            if abs(diffsRow[i]) > thresh:
                out = False
                break
          print('isValid?')
          print(out)
          return out

      def compCandidate(self, imgs, choice,setImgs):
          out = False
          row = imgs[:]
          row.append(choice)
          #row = self.getEdgeOnlyRow(row)
          pixelFactor = self.getFillFactorRow(row, setImgs)
          print("pixel factor")
          print(pixelFactor)
          if self.isValid(pixelFactor) == True:
              out = True
          return out


class divideImage(ImageOperations):

    def getSegments(self,img, rows, cols):
        (width, height) = img.size
        rowInc = float(height/rows)
        colInc = float(width/cols)
        '''
        print('width')
        print(width)
        print('hieght')
        print(height)
        print('rowinc')

        print(rowInc)
        print('colinc')
        print(colInc)
        '''
        out = []


        for j in range(0,rows):
            for i in range(0,cols):
                left = int(round(colInc*i))
                #print('left')
                #print(left)
                right = int(round(colInc*(i+1)))
                #print('right')
                #print(right)
                top = int(round(rowInc*j))
                #print('top')
                #print(top)
                bottom = int(round(rowInc*(j+1)))
                #print('bottom')
                #print(bottom)
                temp = img.crop(box=(left,top, right, bottom))
                #temp.save(str(j)+str(i)+'.JPEG','JPEG')
                out.append(temp)

        '''
        out = []
        t1 =  img.crop(box=(0,0,92,92))
        t2 =  img.crop(box=(92,0,184,92))
        t3 =  img.crop(box=(0,92,92,184))
        t4 =  img.crop(box=(92,92,184,184))
        out = [t1,t2,t3,t4]
        '''

        return out

    def groupSegments(self, imgs, rows, cols):
        storage = []
        for i in range(0,len(imgs)):
            temp = self.getSegments(imgs[i],rows, cols)
            storage.append(temp)
        out = []
        for i in range(0,(rows*cols)):
            temp = []
            for j in range(0,len(imgs)):
                temp.append(storage[j][i])
            out.append(temp)
        return out

    def isRowValid(self, opObj, objs, thresh):
       flag = True
       for i in range(0,len(objs)):
           print("baselines")
           #objs[i]=transObj.getEdgeOnlyRow(objs[i])
           temp  = opObj.getFillFactorRow(objs[i])
           print(temp)
           #flag = opObj.isValid(temp,thresh)
       return flag


class answerOp(transformOp):

    def getAnswerRows(self, ans, given, choices):
        out = []
        for a in ans:
            temp = given[:]
            temp.append(choices[a])
            out.append(temp)
        return out

    def elimByPixels(self,answerDict):
        out = answerDict.copy()
        for a in answerDict:
            factorRow = self.getFillFactorRow(out[a])
            print(factorRow)
            factorRow = np.array(factorRow)

            if (factorRow>0).all(axis=0) or (factorRow<=0).all(axis=0):
                pass
            else:
                del out[a]

        return out

    def elimBySimilarity(self,answerDict,thresh=0.05):
        out = answerDict.copy()
        for a in answerDict:
            factorRow = self.getFillFactorRow(out[a])
            print(factorRow)
            factorRow = np.array(factorRow)
            print('factor')
            print(float(abs(factorRow[len(factorRow)-1] - factorRow[len(factorRow)-2]))/abs(factorRow[len(factorRow)-1]))

            if float(abs(factorRow[len(factorRow)-1] - factorRow[len(factorRow)-2]))/max(abs(factorRow[len(factorRow)-1]),abs(factorRow[len(factorRow)-2])) <= thresh :
                pass
            else:
                del out[a]

        return out


    def elimByFactor(self,answerDict,factor,thresh=0.02):
        out = answerDict.copy()
        print('checkFactor')
        print(factor)
        for a in answerDict:
            print('checking number')
            print(a)
            factorRow = self.getImgVal(out[a])
            print(factorRow)
            factorRow = np.array(factorRow)
            print('factor')
            myFactor = abs(float(factorRow[len(factorRow)-1])/factorRow[len(factorRow)-2])
            print(myFactor)
            if float(abs(myFactor - factor))/factor <= thresh :
                pass
            else:
                del out[a]

        return out

    def verticalReflection(self, img):
        img_dest = img.copy()
        (width,height)=img.size
        for x in range(0,width):
            for y in range(0,height):
                p = img.getpixel((x,y))
                img_dest.putpixel(((width/2-1+x)%width,y),p)
        img_dest.save("mirroor",'JPEG')
        return img_dest

    def imgCompare(self, img1,img2):
        img_dest = img1.copy()
        (width,height)=img1.size
        count  = 0
        for x in range(0,width):
            for y in range(0,height):
                p1 = img1.getpixel((x,y))
                p2 = img2.getpixel((x,y))
                if p1==p2:
                    count = count+1
        out = float(count) / (width*height)
        return out

    def elimByVerticalReflection(self,answerDict, compIdx, thresh=0.9):
        out = answerDict.copy()
        for a in answerDict:
            compImg = answerDict[a][compIdx]
            newImg = self.verticalReflection(answerDict[a][len(answerDict[a])-1])
            ratio = self.imgCompare(compImg,newImg)
            if ratio < thresh :
                del out[a]
        return out
    def countPixelsFirstColumn(self,img):
        (width,height)=img.size
        count  = 0
        goOn = True
        for x in range(0,width):
            if goOn == False:
                break
            for y in range(0,height):
                state = img.getpixel((x,y))
                if state < 255:
                    for y1 in range(0,height):
                        if img.getpixel((x,y1)) < 255:
                            count = count + 1
                    goOn= False
                    break
        return count

    def elimByFirstColumn(self,answerDict, compIdx, thresh=3):
        out = answerDict.copy()
        for a in answerDict:
            col1 = self.countPixelsFirstColumn(answerDict[a][compIdx])
            col2 = self.countPixelsFirstColumn(answerDict[a][len(answerDict[a])-1])
            diff = abs(col1 - col2)
            if diff > thresh:
                del out[a]
        return out

    def isValid(self, answers, thresh=1000):
        out =  False
        if len(answers) == 1:
            out = True
        return out

class rotateOp(ImageOperations):

    def rotateImg(self, img, deg):
        newImg= img.rotate(deg)
        return newImg

    def rotateRow(self, imgs, deg):
        out = []
        for i in range(0,len(imgs)):
            out.append(self.rotateImg(imgs[i],deg))

        return out



class framesControl():

    def getProbRelation(self,objs,opOP,choices,opFcn,opValid,thresh,*obArg):
        flag = True
        for i in range(0,len(objs)-1):
            temp  = opFcn(objs[i],*obArg)
            flag = opValid(temp,thresh)
            if flag ==False:
                break
        return flag

    def testChoices(self,objs,choices,compFcn,**choiceArgs):
        answers = {}
        for choice in choices:
              print(choice)
              if compFcn(objs[len(objs)-1], choices[choice],**choiceArgs) == True:
                  ans = int(choice)
                  candidate = objs[len(objs)-1][:]
                  candidate.append(choices[choice])
                  answers[ans]=candidate
        return answers

    def elimByFcn(self,answerDict, fcn,**args):
        return fcn(answerDict,**args)

