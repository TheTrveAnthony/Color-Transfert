"""

Here are the matrixes we gonna need to make the different transforms to 
go from a color space to another one

If we multiply r_l*l_r and a_l*l_a, we get I3 which is coherent, it is commutative as well

"""

import numpy as np 
from math import sqrt as s


############## From RGB to LMS : #######################


r_l = np.array([[0.3811, 0.5783, 0.0402],
				[0.1967, 0.7244, 0.0782],
				[0.0241, 0.1288, 0.8444]])


############## From LMS to RGB : #######################

l_r = np.array([[4.4679, -3.5873, 0.1193],
			    [-1.2186, 2.3809, -0.1624],
			    [0.0497, -0.2439, 1.2045]])


############## From LMS to l aplha beta : ################

# First some scalar values 

a = 1/s(3) ; b = 1/s(6) ; c = 1/s(2)

## Then the matrixes for the transform


abc = np.array([[a, 0, 0],
				[0, b, 0],
				[0, 0, c]])

m = np.array([[1, 1, 1],
			  [1, 1, -2],
			  [1, -1, 0]])

# Now The Matrix of the transform itself

l_a = np.matmul(abc, m)


############## from l alpha beta to LMS : ###################

# again, some scalar values 

x = s(3)/3 ; y = s(6)/6 ; z = s(2)/2

## Then the matrixes for the transform


xyz = np.array([[x, 0, 0],
				[0, y, 0],
				[0, 0, z]])

mm = np.array(m.transpose())		# It's faster this way

# Now The Matrix of the transform itself

a_l = np.matmul(mm, xyz)