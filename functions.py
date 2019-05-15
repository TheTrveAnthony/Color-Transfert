import numpy as np 
import cv2 as cv
from math import log10 as log, pow
from matrix import r_l, l_r, l_a, a_l


""" All the functions for our color transfert """



def transert():

	""" "Main" function that regroups everything """


	n_target = input("Tell me which picture wants a new make up.\n\n")
	n_source = input("And now tell me which one she wanna look like \n\n")

	target = cv.imread(n_target, 1)
	source = cv.imread(n_source, 1)

	### So basically, target will get new colors from source

	## First let's convert them into the l alpha beta color space

	t_alpha = rgb2alpha(target)
	s_alpha = rgb2alpha(source)


	## Now let's make up our target thanks to some statistical operations

	m_target = make_up(t_alpha, s_alpha)


	## Finally we gonna convert target back to rgb space

	m_target = alpha2rgb(m_target)

	## And save it, so let's name it, you don't have to give the format, we'll add it here

	name = input("What's the name of the new picture ? \n")

	name += ".png"

	cv.imwrite(name, m_target)		# You can now post your new picture to instagramm and let
									# your followers believe that you are a skilled photograph.	
									# I personally don't use this shit so fuck it.

	print("{} saved.".format(nom))

def rgb2alpha(img):

	""" Everything is in the title, this function is a gate from rgb to l alpha beta colorspace,
		which is closer to how us, mere mortal humans perceive colors.
	"""
	### First of all we need the size of our picture to make the transforms

	x = len(img) ; y = len(img[0])
	alpha = np.full((x, y, 3), 0)		## This will be the transformed image

	### Now we gotta access each pixel of the picture

	for i, vi in enumerate(img):
		for j, px in enumerate(vi):
			### There we are

			# Step 1 : LMS transform, for that we use r_l

			alpha[i][j] = np.matmul(r_l, px)

			# Step 2 : log em all (decimal log)

			alpha[i][j][0] = log(alpha[i][j][0])
			alpha[i][j][1] = log(alpha[i][j][1])
			alpha[i][j][2] = log(alpha[i][j][2])

			# Step 3 : l alpha beta transform, by using l_a

			alpha[i][j] = np.matmul(l_a, alpha[i][j])

	return alpha






def alpha2rgb(img):

	""" Same as rgb2alpha but in the opposite way. """

def make_up(trg, src):

	""" We apply the src colors to target here, in the l alpha beta colorspace,
		using mean and standart deviation."""