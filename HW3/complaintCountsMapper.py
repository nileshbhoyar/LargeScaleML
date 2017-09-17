#!/usr/bin/env python
# START STUDENT CODE HW31MAPPER
import sys
separator = ','
for line in (sys.stdin):
        fields = line.split(separator)
        if 'Complaint ID' != fields[0] :
           
            # we have a real record, so do some mapping
            counter_name = None
            if (fields[1].lower() == 'debt collection' or \
                fields[1].lower() == 'mortgage'):
                counter_name = fields[1].strip().lower()
            else:
                counter_name = 'other'
            # update the counter
            sys.stderr.write("reporter:counter:Category Counters,{0},1\n".format(counter_name))
       

# END STUDENT CODE HW31MAPPER