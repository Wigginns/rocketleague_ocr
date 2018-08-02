from PIL import Image
import pytesseract
import argparse
import cv2
import os

traineddata = ['Bourgeoisbook']

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
args = vars(ap.parse_args())

# load the example image and convert it to grayscale
image = cv2.imread(args["image"])
# gray = cv2.medianBlur(image,5)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# check to see if we should apply thresholding to preprocess the
# image
if args["preprocess"] == "thresh":
	th1 = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    ####adaptiveThreshold(	src, maxValue, adaptiveMethod, thresholdType, blockSize, C)
    # th1 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #         cv2.THRESH_BINARY_INV,31,1)

# make a check to see if median blurring should be done to remove
# noise
elif args["preprocess"] == "blur":
	gray = cv2.medianBlur(gray, 3)

# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, th1)

# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
for font in traineddata:
    text = pytesseract.image_to_string(Image.open(filename), lang=font)
    print("Font:{}| \n {} \n".format(font, text))

os.remove(filename)

# show the output images
cv2.imshow("Image", image)
# cv2.imshow("Gray", gray)
cv2.imshow("Output", th1)
cv2.waitKey(0)
