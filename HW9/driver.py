#!/usr/bin/python

from pagerankalgo import pagerankalgo
from distweight import distweight
from topN import topN
from subprocess import call, check_output
from time import time
import sys, getopt, datetime, os

# parse parameter
if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hg:j:i:d:s:")
    except getopt.GetoptError:
        print "Issues"
        sys.exit(2)
    if len(opts) != 4:
       
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            
            sys.exit(2)
        elif opt == '-g':
            graph = arg
        elif opt == '-j':
            jump = arg
        elif opt == '-i':            
            n_iter = arg
     
        elif opt == '-s':
            n_node = arg
        
start = time()
FNULL = open(os.devnull, 'w')
n_iter = int(n_iter)
doInit = n_node=='0'


print "Initialization ..."
if doInit:
    # clear directory
    print str(datetime.datetime.now()) + ': clearing directory ...'
    call(['hdfs', 'dfs', '-rm', '-r', '/user/nileshbhoyar/in'], stdout=FNULL)
    call(['hdfs', 'dfs', '-rm', '-r', '/user/nileshbhoyar/out'], stdout=FNULL)
    
    # creat initialization job    
    init_job = pagerankalgo(args=[graph, '--i', '1', '-r', 'hadoop', '--output-dir', 'hdfs:///user/nileshbhoyar/out'])

    # run initialization job
    print str(datetime.datetime.now()) + ': running iteration 1 ...'
    with init_job.make_runner() as runner:    
        runner.run()

    # checking counters
    n_node = runner.counters()[0]['node_count']['nodes']
    n_dangling = runner.counters()[0]['dangling_mass']['mass']/1e10
    
    print '%s: initialization complete: %d nodes, %d are dangling!' %(str(datetime.datetime.now()), n_node, n_dangling)

    # run redistribution job
    call(['hdfs', 'dfs', '-mv', '/user/nileshbhoyar/out', '/user/nileshbhoyar/in'])
    dist_job = distweight(args=['hdfs:///user/nileshbhoyar/in/part*', '--s', str(n_node), '--j', jump, 
                                '--m', str(n_dangling), '-r', 'hadoop', '--output-dir', 'hdfs:///user/nileshbhoyar/out'])
    print str(datetime.datetime.now()) + ': distributing loss mass ...'
    with dist_job.make_runner() as runner:    
        runner.run()

# move results for next iteration
call(['hdfs', 'dfs', '-rm', '-r', '/user/nileshbhoyar/in'], stdout=FNULL)
call(['hdfs', 'dfs', '-mv', '/user/nileshbhoyar/out', '/user/nileshbhoyar/in'])

# create iteration job
iter_job = pagerankalgo(args=['hdfs:///user/nileshbhoyar/in/part*', '--i', '0', 
                              '-r', 'hadoop', '--output-dir', 'hdfs:///user/nileshbhoyar/out'])
# run pageRank iteratively
i = 2 if doInit else 1
while(1):    
    print str(datetime.datetime.now()) + ': running iteration %d ...' %i
    with iter_job.make_runner() as runner:        
        runner.run()
    
    # check counter for loss mass
    mass_loss = runner.counters()[0]['dangling_mass']['mass']/1e10
    
    # move results for next iteration
    call(['hdfs', 'dfs', '-rm', '-r', '/user/nileshbhoyar/in'], stdout=FNULL)
    call(['hdfs', 'dfs', '-mv', '/user/nileshbhoyar/out', '/user/nileshbhoyar/in'])
        
    # run redistribution job
    dist_job = distweight(args=['hdfs:///user/nileshbhoyar/in/part*', '--s', str(n_node), '--j', jump, 
                                '--m', str(mass_loss), '-r', 'hadoop', '--output-dir', 'hdfs:///user/nileshbhoyar/out'])
    print str(datetime.datetime.now()) + ': distributing loss mass %.4f ...' %mass_loss
    with dist_job.make_runner() as runner:    
        runner.run()
    
    if i == n_iter:
        break
    
    # if more iteration needed
    i += 1    
    call(['hdfs', 'dfs', '-rm', '-r', '/user/nileshbhoyar/in'], stdout=FNULL)
    call(['hdfs', 'dfs', '-mv', '/user/nileshbhoyar/out', '/user/nileshbhoyar/in'], stdout=FNULL)

# run sort job
print "Sorting and Top N job "
call(['hdfs', 'dfs', '-rm', '-r', '/user/nileshbhoyar/finalranks'], stdout=FNULL)
sort_job = topN(args=['hdfs:///user/nileshbhoyar/out/part*', '--s', str(n_node), '--n', '100',
                              '-r', 'hadoop', '--output-dir', 'hdfs:///user/nileshbhoyar/finalranks'])
with sort_job.make_runner() as runner:    
    runner.run()