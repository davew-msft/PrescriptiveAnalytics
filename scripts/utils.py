##
## Default formats
font_title = 20
format = '{:0.1%}'
format_dollar = '${:,.2f}'
p_value = '{:0.4f}'

##
## DataFrame styles
tbl_styles = [ {
    'selector': 'caption',
    'props': [
        ('color', 'darkblue'),
        ('font-size', '18px')
    ] } ]

##
## helper functions
def printbold( s1, s2 = None ):
    """
    Print text in bold and then return to normal.
    Args:
        s1 = string
        s2 = string, usually an f-string
    """
    bold = '\033[1m'
    normal = '\033[0m'
    if s2 == None:
        print( sc.red( s1, 'bold' ) )
    else:
        print( sc.red( s1, 'bold' ) + s2 )

def df_size( df ):
    """
    Display DataFrame size as nice output: rows and columns.
    
    Args:
        df: DataFrame handle.
    """
    data = { 'Count': [ df.shape[ 0 ], df.shape[ 1 ] ] }
    format_dict = { 'Count':'{0:,.0f}' }
    idx = [ 'Number of Rows', 'Number of Columns' ]
    display( pd.DataFrame( data, index = idx ).style.set_caption( 'DataFrame Dimensions' ).\
            set_table_styles( tbl_styles ).format( format_dict ) )


def column_check( df ):
    """
    Purpose: Counts number of characters on DataFrame column names and number of leading and trailing white spaces.
    """
    cols = df.columns
    n = len( cols )
    ##
    lgh = [ len( cols[ i ] ) for i in range( n ) ]
    lead = [ len( cols[ i ] ) - len( cols[ i ].lstrip() ) for i in range( n ) ]
    trail = [ len( cols[ i ] ) - len( cols[ i ].rstrip() ) for i in range( n ) ]
    ##
    dt = { 'Column Name':cols, '#Characters':lgh, 'Leading White Spaces':lead, 'Trailing White Spaces':trail}
    df_whs = pd.DataFrame( dt )
    df_whs.set_index( [ 'Column Name', '#Characters' ], inplace = True )
    ##
    base = 'Base: n = ' + str( n ) + ' columns'
    display( df_whs.style.bar( subset = [ 'Leading White Spaces', 'Trailing White Spaces' ], vmin = 0 ).\
        set_caption( 'DataFrame Column Check for DataFrame ' + get_df_name( df ) ).set_table_styles( tbl_styles ) )
    print( base )

def get_df_name( df ):
    """
    Purpose: Get DataFrame name
    Return: DataFrame name as string
    """
    name = [ x for x in globals() if globals()[ x ] is df ][ 0 ]
    return name

def highlight_fct( x, when):
    """
    Highlight DataFrame cells of forecast.
    
    Args:
        x
        when = last period of actual (T).
    """
    a = x.name.strftime('%Y')
    a = float( a )
    if a > when:
        return ['background-color: yellow']
    else:
        return ['background-color: white'] 

def footer():
    """
    Footer for graphs.  Display base and sample size.
    
    Args:
        None.  Assumes footer statement is defined as base = 'XXX'.
    """
    ax.annotate( base, ( 0, 0 ), ( 0, -0.3 ), xycoords = 'axes fraction' )

def tick_labels( tick ):
    """
    Modify graph ticks.
    
    Args:
        tick: axis x or y (lowercase).
    """
    if tick == 'y':
        vals = ax.get_yticks()
        ax.set_yticklabels( format.format( x ) for x in vals )
    else:
        vals = ax.get_xticks()
        ax.set_xticklabels( format.format( x ) for x in vals )

def leg( ax, ttl = None ):
    """
    Standardize location of legends.
    
    Args:
        ax: ax handle for graph.
        ttl: legend title.
    """
    ax.legend( title = ttl, loc = 'upper right', frameon = False, bbox_to_anchor=(1.25, 1.0) )

def mvReport( df ):
    """
    Calculate and display missing value report.
    Use sidetable package accessor stb.
    
    Args:
        df: dataFrame handle.
    """
    x = df.stb.missing( )
    ##
    ## Reorder columns and capitalize
    ##
    cols = [ 'total', 'missing', 'percent' ]
    x = x[ cols ]
    x.columns = x.columns.str.capitalize()
    ##
    ## Display
    ##
    base = 'Base: n = ' + str( df.shape[ 0 ] )
    fmt_dict = { 'Missing':'{:,.0f}', 'Total':'{:,.0f}', 'Percent':'{:.3}%' }
    display( x.style.set_caption( 'Missing Value Report').\
        format( fmt_dict ).set_table_styles( tbl_styles ) )
    print( base )

print("done running utils.py")