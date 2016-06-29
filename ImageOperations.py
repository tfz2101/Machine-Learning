

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

 def getArr(self, img):
     (width, height) = img.size
     o1_arr = np.array(list(img.getdata())).reshape((height, width))
     return o1_arr

 def getEdgeOnlyRow(self, imgs):
      out = []
      for img in imgs:
        out.append(img.filter(ImageFilter.FIND_EDGES))
      return out

class noOp(ImageOperations):

  #def __init__(self, im1, im2):
  #  super(ImageOperations,self).__init__(im1,im2)

  def isValid(self, im1, im2):
      out = False
      if self.similarity(im1, im2) >= 0.99:
          out= True
      return out

  def isRowValid(self, imgRow):
      out = True
      for i in range(0,len(imgRow)-1):
          img1 = imgRow[i]
          img2 = imgRow[i+1]
          if self.similarity(img1,img2) < 0.99:
              out = False
              break
      return out

  def compCandidate(self, imgs, choice):
      out = False
      newRow = imgs[:]
      newRow.append(choice)
      if self.isRowValid(newRow):
          out = True
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

      def getFillFactorRow(self, imgs):
          factors = []
          for i in range(0,len(imgs)-1):
              img1 = imgs[i]
              img2 = imgs[i+1]
              factors.append(self.getFillFactor(img1, img2))
          return factors

      def compCandidate(self, imgs, choice):
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


      def getPixelDiff(self, im1, im2):
          p_a = self.getArr(im1)
          p_b = self.getArr(im2)
          pixelDiff = (np.sum(p_b)-np.sum(p_a))/255

          return pixelDiff

      def getPixelDiffRow(self, imgs):
          diffs = []
          for i in range(0,len(imgs)-1):
              img1 = imgs[i]
              img2 = imgs[i+1]
              diffs.append(self.getPixelDiff(img1, img2))
          return diffs

      def isValid(self, factorRow,thresh=10):
          out = True
          for i in range(0,len(factorRow)-1):
            if abs(factorRow[i+1]-factorRow[i]) >= thresh:
                out = False
                break
          print(out)
          return out

      def compCandidate(self, imgs, choice):
          out = False
          row = imgs[:]
          row.append(choice)
          row = self.getEdgeOnlyRow(row)
          for i in range(0, len(row)):
              row[i].save(str(i),'JPEG')

          pixelFactor = self.getPixelDiffRow(row)
          print("pixel factor")
          print(pixelFactor)
          if self.isValid(pixelFactor) == True:
              out = True
          return out


class divideImage(ImageOperations):

    def getSegments(self,img, rows, cols):
        (width, height) = img.size
        num = rows * cols
        rowInc = float(width/rows)
        colInc = float(height/cols)
        out = []
        for i in range(0,rows):
            for j in range(0,cols):
                left = int(rowInc*i)
                top = int(colInc*j)
                right = int(rowInc*(i+1))
                bottom = int(colInc*(j+1))
                temp = img.crop(box=(left,top, right, bottom))
                out.append(temp)
        return out




'''
class rotateOp(ImageOperations):

    #def __init__(self, im1, im2):
        #super(ImageOperations,self).__init__(im1,im2)


    def compCandidate(self):
        return self.im2

    def rotateAction(self):
        #self.im2.show()
        newImg= self.im2.rotate(20)
        return newImg
'''







