#! /usr/bin/python

from pyproj import Proj         # Used to convert lat/lon to UTM

class Lane():
    def __init__(self, lane_num):
        self.lane_num = lane_num 
        self.num_waypoints = None
        self.lane_width = None 
        self.left_boundary = None 
        self.right_boundary = None
        self.checkpoints = []
        self.exits = []
        self.stops = []
        self.waypoints = []

    def check_yo(self):
        if len(self.waypoints) > self.num_waypoints:
            print "ERROR: Lane " + str(self.lane_num) + " has too many waypoints."
        elif len(self.waypoints) < self.num_waypoints:
            print "ERROR: Lane " + str(self.lane_num) + " has too few waypoints."
        return len(self.waypoints) == self.num_waypoints


class Segment():
    def __init__(self, seg_num=0, num_lanes=0, name=""):
        self.seg_num = seg_num
        self.num_lanes = num_lanes
        self.name = name
        self.lanes = [] 

    def check_yo(self):
        retval = True
        for lane in self.lanes:
            retval = retval and lane.check_yo()
        if len(self.lanes) > self.num_lanes:
            print "ERROR: Segment " + str(self.seg_num) + " has too many lanes."
            retval = False
        elif len(self.lanes) < self.num_lanes:
            print "ERROR: Segment " + str(self.seg_num) + " has too few lanes."
            retval = False
        return retval

    
        

class RNDF:
    def __init__(self, filename, zone=17):
        self.filename = filename
        f = open(self.filename)
        
        self.UTM_zone = zone

        self.lines = []
        for line in f.readlines():
            self.lines.append(line.split())

        self.segments = []
       
        idx = 0
        while idx < len(self.lines): 
            line = self.lines[idx]
 
            if   line[0] == 'RNDF_name':
                self.RNDF_name = line[1]
            elif line[0] == 'num_segments':
                self.num_segments = int(line[1])
            elif line[0] == 'num_zones':
                self.num_zones = int(line[1])
            elif line[0] == 'format_version':
                self.format_version = float(line[1])
            elif line[0] == 'creation_date':
                self.creation_date = line[1]
            elif line[0] == 'segment':
                seg_num = int(line[1])
                self.segments.append(Segment())
            elif line[0] == 'num_lanes':
                self.segments[-1].num_lanes = int(line[1])
            elif line[0] == 'segment_name':
                self.segments[-1].seg_name = line[1]
            elif line[0] == 'lane':
                new_lane = Lane(float(line[1]))
                idx = idx + 1
                while self.lines[idx][0] != 'end_lane':
                    if self.lines[idx][0] == 'num_waypoints':
                         new_lane.num_waypoints = int(self.lines[idx][1])
                    elif self.lines[idx][0] == 'lane_width':
                         new_lane.lane_width = int(self.lines[idx][1])
                    elif self.lines[idx][0] == 'left_boundary':
                         new_lane.left_boundary = self.lines[idx][1]
                    elif self.lines[idx][0] == 'right_boundary':
                         new_lane.right_boundary = self.lines[idx][1]
                    elif self.lines[idx][0] == 'exit':
                         new_lane.exits.append(self.lines[idx][1:2])
                    elif self.lines[idx][0] == 'checkpoint':
                         new_lane.checkpoints.append(self.lines[idx][1:2])
                    elif self.lines[idx][0] == 'stop':
                         new_lane.stops.append(self.lines[idx][1])
                    else:
                         lonlat2UTM = Proj(proj='utm', zone=self.UTM_zone, ellps='WGS84')
                         UTMx, UTMy = lonlat2UTM(float(self.lines[idx][2]), float(self.lines[idx][1]))
                         new_lane.waypoints.append( (UTMx, UTMy, self.lines[idx][0]) )
                    idx = idx + 1
                self.segments[-1].lanes.append(new_lane) 
            else:
                # Parsing Error on line x!
                pass
            idx = idx + 1
        # Do some error checking to make sure you captured 
        # the correct number of segments and lanes.
        self.check_yo()

    def check_yo(self):
        retval = True
        for s in self.segments:
            retval = retval and s.check_yo()
        if retval == False:
            print "ERROR: Failed to parse " + self.filename + "."
            
    def summary(self):
        print "RNDF_name: ", self.RNDF_name
        print "num_segments: ", self.num_segments
        print "num_zones: ", self.num_zones
        print "format_version: ", self.format_version
        print "creation_date: ", self.creation_date
        

if __name__ == "__main__":
    rndf = RNDF("scenarios/SchenleyNonStopClockwise/RNDF.txt")
    rndf.summary()
    
            


    
