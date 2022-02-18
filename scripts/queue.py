import pandas as pd
import numpy as np
import random
import sys
args = sys.argv

def ts_update( time_series, data ):
    generated_events =  pd.DataFrame( data )
    time_series = pd.concat( [ time_series, generated_events ] )
    ##
    ## sort events by time
    ##
    time_series = time_series.sort_values( [ 'time' ] )
    time_series.reset_index( drop = True, inplace = True )
    ##
    ## event number is assigned by time order
    ##
    time_series[ 'event' ] = list( range( 1, time_series.shape[ 0 ] + 1 ) )
    return( time_series )

def queue_run( arrival_lambd, service_lambd, n_events, seed = 42 ):
    ##
    ## set random seed
    ##
    np.random.seed( seed )
    ##
    ## initialize event counter
    ##
    event = 0
    ##
    ## at event zero, time is also zero
    ##
    time_ = 0
    ##
    ## create counters for arrived and served customers
    ##
    arrived_customer = 0
    served_customer = 0
    departed_customer = 0
    ##
    ## generate random variables for next events
    ##
    ##interarrival_time = np.random.uniform( inter_arrival_min, inter_arrival_max )
    interarrival_time = random.expovariate( arrival_lambd )
    next_arrival_time = time_ + interarrival_time
    server_status = "idle"
    queue = 0
    arrived_customer += 1
    ##
    ## event zero done
    ##
    event += 1  
    ##
    ## create timeseries and populate with event 1 details
    ##
    data = { 'event':[ event ], 
             'time':[ next_arrival_time ],
             'type':[ 'arrival' ], 
             'arrived_customer':[ arrived_customer ], 
             'served_customer':[ served_customer ], 
             'departed_customer':[ departed_customer ],
             'queue':[ queue ] }
    time_series =  pd.DataFrame( data ) 
    ##
    ## main loop
    ##
    while event <= n_events:
        ##
        ## event starts
        ##
        ## set parameters at event t
        ##
        event_type = time_series[ 'type' ].iloc[ event - 1 ]
        time_ = time_series[ 'time' ].iloc[ event - 1 ]
        ##
        ## IF EVENT IS AN ARRIVAL
        ##
        if event_type == "arrival":
            ##
            ## arrival event generate by default next arrival time
            ## counter of arrived customers increases by 1
            ##
            arrived_customer += 1
            ##
            ## generate next arrival time
            ##
            ##interarrival_time = np.random.uniform( inter_arrival_min, inter_arrival_max )
            interarrival_time = random.expovariate( arrival_lambd )
            next_arrival_time = time_ + interarrival_time  
            ##
            ## if server status is idle customer is served immediatly 
            ## and generates service time
            ##
            if server_status == "idle":
                ##
                ## customer is served and counter of served customer increases by 1
                ##
                served_customer += 1
                ##
                ## this customer number is added to the 'served customer' column at event n
                ##
                time_series[ 'served_customer' ].iloc[ event - 1 ] = served_customer
                ##
                ## generate next events (service and departure time)
                ##
                ##service_time = np.random.uniform( service_time_min, service_time_max )
                service_time = random.expovariate( service_lambd )
                departure_time = time_ + service_time
                departed_customer += 1 #same customer that is served at arrival time departs at departure time
                ##
                ## add generated events to existing time series
                ##
                data = { 'event':[ 99, 99 ], 
                         'time':[ departure_time, next_arrival_time ],
                         'type':[ 'departure', 'arrival' ], 
                         'arrived_customer':[ 0, arrived_customer ], 
                         'served_customer':[ 0, 0 ], 
                         'departed_customer':[ departed_customer, 0 ],
                         'queue':[ 0, 0 ] }
                time_series = ts_update( time_series, data )
                ##
                ## event is finished and event counter increases
                ##
                event += 1 
            ##    
            ## if server status is busy increase queue and only generate arrival activity
            ##
            if server_status == "busy":
                queue += 1
                #add generated events to existing time series
                data = { 'event':[ 99 ], 
                         'time':[ next_arrival_time ],
                         'type':[ 'arrival' ], 
                         'arrived_customer':[ arrived_customer ], 
                         'served_customer':[ 0 ],
                         'departed_customer':[ 0 ],
                         'queue':[ 0 ] }
                time_series = ts_update( time_series, data )
                time_series[ 'queue' ].iloc[ event - 1 ] = queue
                ##
                ## event is finished and event counter increases
                ##
                event += 1 
        ##
        ## IF EVENT IS A DEPARTURE
        ##
        if event_type == "departure":
            ##
            ## if queue is zero and customer departs, server status remains idle 
            ## and next event is an arrival
            ##
            if queue == 0 :
                server_status = "idle"
                ##
                ## event is finished and event counter increases
                ## nothing else happens until next arrival
                ##
                event += 1
            ##
            ## if there are customers in queue ( > 0 ), server changes to busy and queue decreases by one
            ##
            if queue != 0 :
                ##
                ## customer is served and counter of served customer increases by 1
                ##
                served_customer += 1
                ##
                ## this customer number is added to the 'served customer' column at event n
                ##
                time_series[ 'served_customer' ].iloc[ event - 1 ] =  served_customer           
                ##
                ## queue decreases by one
                ##
                queue -= 1
                server_status = "busy"
                ##
                ## generate next events (service and departure time)
                ##
                ##service_time = np.random.uniform( service_time_min, service_time_max )
                service_time = random.expovariate( service_lambd )
                departure_time = time_ + service_time
                departed_customer += 1 #same customer that is served at arrival time departs at departure time
                ##
                ## add generated events to existing time series
                ##
                data = { 'event':[ 99 ], 
                         'time':[ departure_time ],
                         'type':[ 'departure' ], 
                         'arrived_customer':[ 0 ], 
                         'served_customer':[ 0 ],
                         'departed_customer':[ departed_customer ],
                         'queue':[ 0 ] }
                time_series = ts_update( time_series, data )
                time_series[ 'queue' ].iloc[ event - 1 ] = queue
                ##
                ## event is finished and event counter increases
                ##
                event += 1 
        ##
        ## once event is finished, determine server status for next event
        ## if the next arrival if before the departure of current customer, server will be busy at arrival
        ##
        if next_arrival_time < departure_time:
            server_status = "busy" 
        else: 
            server_status = "idle"
    return( time_series )

def queue_summary( x ):
    ##
    ## create summary of customer data with results
    ##
    ## get arriving customers
    ##
    arrivals = x.query( "type == 'arrival'")[ [ 'time', 'arrived_customer' ] ]
    arrivals.columns = [ 'time', 'customer' ]
    ##
    ## get departing customers
    ##
    departure = x.query( "type == 'departure'")[ [ 'time', 'departed_customer' ] ]
    departure.columns = [ 'time', 'customer' ]
    ##
    ## get customers being served
    ##
    serving = x.query( "served_customer != 0")[ [ 'time', 'served_customer' ] ]
    serving.columns = [ 'time', 'customer' ]
    ##
    ## merge
    ##
    df_customer = arrivals.merge( departure, on = 'customer' )
    df_customer = df_customer.merge( serving, on = 'customer' )
    ##
    df_customer.columns = [ 'arrival time', 'customer', 'departure time', 'serving time' ]
    df_customer = df_customer[ [ 'customer', 'arrival time', 'serving time', 'departure time' ] ] 
    ##
    ## get time in queue
    ##
    df_customer[ 'time in queue' ] = df_customer[ 'serving time' ] - df_customer[ 'arrival time' ] 
    ##
    ## get time in server
    ##
    df_customer[ 'time in server' ] = df_customer[ 'departure time' ] - df_customer[ 'serving time' ] 
    ##
    ## get time in system
    ##
    df_customer[ 'time in system' ] = df_customer[ 'departure time' ] - df_customer[ 'arrival time' ] 
    ##
    ## round all floats to 2 digits
    ##
    df_customer = df_customer.round( 2 )
    ##
    return( df_customer )