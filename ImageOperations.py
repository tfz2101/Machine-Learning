

from PIL import Image
import numpy as np


from PIL import ImageFilter, ImageMath, ImageChops
import math as math

class ImageOperations:

 def __init__(self, imgs):
     self.imgs = imgs

 def compCandidate(self):
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
     o1_arr = np.around(np.array(list(img.getdata())).reshape((height, width)))
     return o1_arr

 def getEdgeOnlyRow(self, imgs):
      out = []
      for img in imgs:
        out.append(img.filter(ImageFilter.FIND_EDGES))
      return out

class noOp(ImageOperations):

  #def __init__(self, im1, im2):
  #  super(ImageOperations,self).__init__(im1,im2)

  def isSame(self, im1, im2):
      out = False
      if self.similarity(im1, im2) >= 0.99:
          out= True
      return out

  def isRowSame(self, imgRow):
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
      if self.isRowSame(newRow):
          out = True
      return out

class fillOp(ImageOperations):

      def getDiffArray(self, im1, im2):
          (width, height) = im1.size
          p_a = self.getArr(im1)
          p_b = self.getArr(im2)
          ab = np.resize((p_a-p_b),[width, height])
          return ab

      def getFillFactor(self, im1, im2):
          width, height = im1.size
          div = width * height
          fillFactor = float((np.sum(abs(self.getDiffArray(im1,im2))))/255)/div
          #print(fillFactor)
          return fillFactor

      def getFillFactorRow(self, imgs):
          factors = []
          for i in range(0,len(imgs)-1):
              img1 = imgs[i]
              img2 = imgs[i+1]
              factors.append(self.getFillFactor(img1, img2))
          return factors

      def storeFillFactor(self, factor):
          self.fillFactor = factor

      def compCandidate(self, img, choice):
          out = False
          choiceFactor = self.getFillFactor(img, choice)
          print(abs(self.fillFactor- choiceFactor)/(self.fillFactor))
          if abs(self.fillFactor- choiceFactor)/(self.fillFactor) < 0.07:
              out = True
          return out


class transformOp(fillOp):

      def getPixelDiff(self, im1, im2):
          p_a = self.getArr(im1)
          p_b = self.getArr(im2)
          pixelDiff = (np.sum(p_a)-np.sum(p_b))/255
          return pixelDiff

      def getPixelDiffRow(self, imgs):
          diffs = []
          for i in range(0,len(imgs)-1):
              img1 = imgs[i]
              img2 = imgs[i+1]
              diffs.append(self.getPixelDiff(img1, img2))
          return diffs

      def storePixelDiff(self, pixdiff):
          self.pixelDiff = pixdiff

      def compCandidate(self, img, choice):
          out = False
          choiceDiff = self.getPixelDiff(img, choice)
          print("choice diff")
          print(choiceDiff)
          print(abs(self.pixelDiff)- abs(choiceDiff))
          if abs(self.pixelDiff- choiceDiff) < 5:
              out = True
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







