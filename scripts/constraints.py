import numpy as np
import matplotlib.pyplot as plt
##
x = np.linspace( 0, 7, 100 )
plt.ylim( -0.5, 7 )
##
y1 = 6 - (1/3)*x
y2 = 8 - x
y3 = 14 - 2*x
##
plt.plot( x, y1, '--k' )
plt.plot( x, y2, '--k' )
plt.plot( x, y3, '--k' )
##
y4 = ( 13/2 ) - ( x/2 )
plt.plot( x, y4, '-r', linewidth = 3 )
##
plt.plot( 0, 6, 'ko' )
plt.annotate( 'A', ( -0.1, 5.5 ) )
plt.plot( 3, 5, 'ko' )
plt.annotate( 'B', ( 2.8, 4.5 ) )
plt.plot( 6, 2, 'ko' )
plt.annotate( 'C', ( 5.8, 1.5 ) )
plt.plot( 7, 0, 'ko' )
plt.annotate( 'D', ( 6.5, 0 ) )
##
plt.annotate( 'Objective Function', ( 5, 5.1 ) )
plt.annotate( '', xy = ( 5.5, 3.8 ), xytext = ( 6, 5 ),
            arrowprops = { 'facecolor':'black', 'shrink':0.05 } )
plt.annotate( 'Feasible Region', ( 2, 2.5 ) )
plt.annotate( 'Optimal Solution\n$Q^0 = 13$', ( 4, 6.0 ), ha = 'center' )
plt.annotate( '', xy = ( 3.05, 5.2 ), xytext = ( 3.8, 5.9 ),
            arrowprops = { 'facecolor':'black', 'shrink':0.05 } )
##
plt.plot( [ 0, 3 ], [ 6, 5 ], '-k', linewidth = 2 )
plt.plot( [ 3, 6 ], [ 5, 2 ], '-k', linewidth = 2 )
plt.plot( [ 6, 7 ], [ 2, 0 ], '-k', linewidth = 2 )
plt.plot( [3, 3], [ 0, 5 ], ':k' )
plt.plot( [0, 3], [ 5, 5 ], ':k' )
##
plt.xlabel( '$Q_1$ Output' )
plt.ylabel( '$Q_2$ Output' )
##
plt.suptitle('Constrained Solution', fontsize = 24, y = 1.25 )
plt.title('Maximize $Q = Q_1 + 2 \\times Q_2$\n \
    Subject to:\n \
    $Q_1 + 3 \\times Q_2 \leq 18$ Factor $X_1$\n \
    $Q_1 + Q_2 \leq 8$ For Factor $X_2$\n \
    $2 \\times Q_1 + Q_2 \leq 14$ For Factor $X_3$\n \
    $Q_1, Q_2 \geq 0$', fontsize = 'small' )
plt.show()