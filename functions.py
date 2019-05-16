import numpy as np 
import cv2 as cv
from math import log10 as log, pow
from matrix import r_l, l_r, l_a, a_l


""" All the functions for our color transfert """



def color_transfert():

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

	print("{} saved.".format(name))


def rgb2alpha(img):

	""" Everything is in the title, this function is a gate from rgb to l alpha beta colorspace,
		which is closer to how us, mere mortal humans perceive colors.
	"""
	### First of all we need the size of our picture to make the transforms

	x = len(img) ; y = len(img[0])
	alpha = np.full((x, y, 3), 0, dtype = float)		## This will be the transformed image

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

	### First of all we need the size of our picture to make the transforms

	x = len(img) ; y = len(img[0])
	rgb = np.full((x, y, 3), 0, dtype = float)		## This will be the transformed image

	### Now we gotta access each pixel of the picture

	for i, vi in enumerate(img):
		for j, px in enumerate(vi):
			### There we are

			# Step 1 : LMS transform, for that we use l_r

			rgb[i][j] = np.matmul(a_l, px)

			# Step 2 : power em all (power 10)

			rgb[i][j][0] = pow(10, rgb[i][j][0])
			rgb[i][j][1] = pow(10, rgb[i][j][1])
			rgb[i][j][2] = pow(10, rgb[i][j][2])

			# Step 3 : rgb, by using l_r

			rgb[i][j] = np.matmul(l_r, rgb[i][j])

	return rgb


def make_up(trg, src):

	""" We apply the src colors to target here, in the l alpha beta colorspace,
		using mean and standart deviation."""

	######### First step is to compute the means standart deviation of 
	######### each channel of the images. Reminder : we are in the l alpha beta space here

	## We gotta reshape em First

	rs_trg = np.reshape(trg, (len(trg)*len(trg[0]), 3))
	rs_src = np.reshape(src, (len(src)*len(src[0]), 3))

	## mean 

	m_trg = np.mean(rs_trg, axis = 0, dtype = np.float64)		## This returns a array of three values which are
	m_src = np.mean(rs_src, axis = 0, dtype = np.float64)		## the means of each channel

	## Standart deviation

	sd_trg = np.std(rs_trg, axis = 0, dtype = np.float64)		## Same with standart deviation
	sd_src = np.std(rs_src, axis = 0, dtype = np.float64)		## We use 64bits floats for more accuracy


	######## Now we've got all we need, next step is to perform the make
	######## up operations on each pixel

	x = len(trg) ; y = len(trg[0])
	mu_trg = np.full((x, y, 3), 0, dtype = float)		## This will be the transformed target mu = make up

	for i, vi in enumerate(trg):
		for j, px in enumerate(vi):
			for k, val in enumerate(px):

				mu_trg[i][j][k] = (sd_src[k]/sd_trg[k])*(val - m_trg[k]) + m_src[k]

	return mu_trg


