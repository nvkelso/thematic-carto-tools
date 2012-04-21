﻿# http://www.doughellmann.com/PyMOTW/csv/# So we can set the intensity of the color valuesimport mathimport copyimport csv, sys#import flash.geom.ColorTransform#import flash.geom.Transform#include 'mappingTooltip.as'class Classify:    kct_valueArray = []    kct_theDataAttribute = ''    kct_sortOnAttribute = ''    kct_theNameAttribute = ''    kct_numclass = 0.0         # new Number()    kct_numclass_1 = 0.0       # new Number()    kct_numclass_2 = 0.0       # new Number()    kct_classifyType = ''        # prob. don't need this one    kct_classifyType_1 = ''        # prob. don't need this one    kct_classifyType_2 = ''        # prob. don't need this one    kct_manualBreaks = ''    kct_dataColors = [ '0xFFFF00', '0x71A1B7', '0xDF9E60', '0xBF5648' ]     # TODO: strings or not?        kct_minvalue = 0.0       # new Number()    kct_maxvalue = 0.0       # new Number()    # dataname$    # kind%    # Global yy%, z%, j%, kct_minvalue, kct_maxvalue, dataname$, kind%    kct_lowclass = []    kct_highclass = []    kct_m1 = []    kct_a1 = []    # Global kct_lowclass(), kct_highclass(), kct_m1(), kct_a1()    kct_sumx = 0.0        # new Number()    kct_sumxx = 0.0       # new Number()    kct_mean = 0.0        # new Number()    kct_sd = 0.0          # new Number()    # Global kct_cl(1000) As Integer, kct_sumx, kct_sumxx, kct_mean, kct_sd    # classkind$    # check%    kct_adder = 0.0       # new Number()    # Global classkind$, check%, kct_adder    # Private Sub Dir1_Change()    #####    # Store the results    kct_cl = []    kct_cl_2 = []    kct_cl_3 = []    kct_nclass = []    kct_nclass_2 = []    kct_nclass_3 = []    # Global kct_nclass() As Integer    #####    kct_gc_ratio = True    kct_gc_flannery = False        kct_gc_minValue = 0.0         # data value    kct_gc_maxValue = 100.0        # data value    kct_gc_minSize = 5.0            # pixel diameter, used to create scaler (2)    kct_gc_maxSize = 170.0        # pixel diameter, used to create scaler (50)    kct_gc_minArea = 0.0    kct_gc_maxArea  = 0.0        kct_gc_rangeValue = 0.0        # need to calculate using function    kct_gc_rangeSize  = 0.0        # need to calculate using function    kct_gc_rangeArea  = 0.0        kct_fromZero = False    kct_to100 = False        kct_alwaysDoQuantiles = False    kct_doQuantilesBreaks = 5.0        ########################/        # TODO: Use *args and **kwargs:     # http://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/        def __init__(self):        pass            def classInit(  self,                    dataArray,                     preserveData,                     sortOnAttributeInit,                     numclassInit,                     classifyTypeInit,                     manualBreaksInit,                     secondaryAttribute,                     numclass2ndInit,                     classifyType2ndInit,                     manualBreaks2ndInit                 ):                print '\nInitializing classification routines...'                 self.kct_sortOnAttribute = sortOnAttributeInit        self.kct_theNameAttribute = secondaryAttribute        self.kct_numclass_1 = numclassInit        self.kct_numclass_2 = numclass2ndInit                if classifyType2ndInit == 'Manual' or \           classifyType2ndInit == 'User defined' or \           classifyType2ndInit == 'Nominal' or \           classifyType2ndInit == 'Unique value' :                       if self.kct_numclass_2 != len(manualBreaks2ndInit):                self.kct_numclass_2 = len(manualBreaks2ndInit)            self.kct_classifyType_1 = classifyTypeInit         self.kct_classifyType_2 = classifyType2ndInit             # Store into class variables        # now get ready        self.kct_theDataAttribute = self.kct_sortOnAttribute        self.kct_numclass = self.kct_numclass_1                self.kct_classifyType = self.kct_classifyType_1                if preserveData:            self.kct_valueArray = copy.deepcopy( dataArray )            #self.kct_valueArray = dataArray.concat()        else:            self.kct_valueArray = dataArray            # This should never be very big so let's just duplicate it over        self.kct_manualBreaks = copy.deepcopy( manualBreaksInit )        #self.kct_manualBreaks = manualBreaksInit.concat()                # Make sure the data is in order        # do the result for timing issues        result = self.classSort()                # Zero out the tracking arrays for that range of data            self.kct_lowclass = [0] * self.kct_numclass        self.kct_highclass = [0] * self.kct_numclass        self.kct_nclass = [0] * self.kct_numclass        # HACK        self.kct_cl = [0] * len(self.kct_valueArray)        self.kct_cl_2 = [0] * len(self.kct_valueArray)        self.kct_cl_3 = [0] * len(self.kct_valueArray)                    # Make sure we are dividing up the data into classes        if (self.kct_numclass > 0) and (len(self.kct_valueArray) > 0):            # Then feed the data to the correct function for classing            if self.kct_classifyType == 'Equal Interval':                self.classBreaksEqualInterval( self.kct_cl, self.kct_nclass )            elif self.kct_classifyType == 'Quantiles':                self.classBreaksQuantiles( self.kct_cl, self.kct_nclass )            elif self.kct_classifyType == 'Standard Deviation':                self.classBreaksStdDeviation( self.kct_cl, self.kct_nclass )            elif self.kct_classifyType == 'Standard Deviation':                self.classBreaksStdDeviation( self.kct_cl, self.kct_nclass )            elif self.kct_classifyType == 'Minimum Variance' or self.kct_classifyType == 'Jenks' :                self.classBreaksMinVariance( self.kct_cl, self.kct_nclass )            elif self.kct_classifyType == 'Manual' or self.kct_classifyType == 'User Defined' :                self.classBreaksUserDefined( self.kct_cl, self.kct_nclass )            # NVK custom routines            elif self.kct_classifyType == 'Nominal':                self.classAssignNominal( self.kct_cl, self.kct_nclass )            elif self.kct_classifyType == 'Ratio' :                self.classAssignRatio( self.kct_cl )            elif self.kct_classifyType == 'Proportional Circle' :                 self.classAssignRatio( self.kct_cl )                self.classAssignProportional( self.kct_cl )            elif self.kct_classifyType == 'Graduated Circle' :                self.classAssignRatio( self.kct_cl )                self.classBreaksEqualInterval( self.kct_cl )                self.classAssignGraduated( self.kct_cl )            elif self.kct_classifyType == 'Unique value' :                # Useful if there is not a defined set of classes to match to                self.classUniqueValue( self.kct_cl )                        if classifyType2ndInit == 'Manual' or \               classifyType2ndInit == 'User defined' or \               classifyType2ndInit == 'Nominal' or \               classifyType2ndInit == 'Unique value' or \               classifyType2ndInit == 'Quantiles' or \               classifyType2ndInit == 'Ratio':                    print 'Examining the 2nd attribute...'                                # Store the secondary sort information                self.kct_theDataAttribute = self.kct_theNameAttribute                self.kct_numclass = self.kct_numclass_2                self.kct_classifyType = self.kct_classifyType_2                                self.kct_manualBreaks = copy.deepcopy( manualBreaks2ndInit )                #self.kct_manualBreaks = manualBreaks2ndInit.concat()                            # Zero out the tracking arrays for that range of data                    self.kct_nclass = [0] * self.kct_numclass                                # Make sure we are dividing up the data into classes                if (self.kct_numclass > 0) and (len(self.kct_valueArray) > 0):                    # Then feed the data to the correct function for classing                    if self.kct_classifyType == 'Quantiles':                        self.classBreaksQuantiles( self.kct_cl_2, self.kct_nclass_2 )                    elif self.kct_classifyType == 'Nominal':                        self.classAssignNominal( self.kct_cl_2, self.kct_nclass_2 )                    elif self.kct_classifyType == 'Ratio' :                        self.classAssignRatio( self.kct_cl_2 )                    elif self.kct_classifyType == 'Unique value' :                        self.classUniqueValue( self.kct_cl_2 )            else:                self.kct_cl_2 = [0] * len(self.kct_valueArray)                    # Zero out the tracking arrays for that range of data                    self.kct_nclass_2 = [0] * self.kct_numclass                        if self.kct_alwaysDoQuantiles:                print 'Developing quantile stats at %d breaks...' % (self.kct_doQuantilesBreaks)                                # Store the secondary sort information                self.kct_theDataAttribute = self.kct_sortOnAttribute                self.kct_numclass = self.kct_doQuantilesBreaks                self.kct_classifyType = 'Quantiles'                                        # Zero out the tracking arrays for that range of data                    self.kct_nclass_2 = [0] * self.kct_numclass                                                                    # Make sure we are dividing up the data into classes                if (self.kct_numclass > 0) and (len(self.kct_valueArray) > 0):                    self.classBreaksQuantiles( self.kct_cl_3, self.kct_nclass_3 )            else:                self.kct_cl_3 = [0] * len(self.kct_valueArray)                                        # Zero out the tracking arrays for that range of data                    self.kct_nclass_3 = [0] * self.kct_numclass                                                # then report out            self.classReport()            # now affect the map            #classDraw( wards_mc )            print 'would have classDraw()'            self.printCSS()        else:            print 'ERROR: There was no data or there needs to be at least 2 classes!'                                    def classSort( self ):        print 'Gathering initial statistics...'                #i = 0        #n = 0                #while Not EOF(1)        for j in range(len(self.kct_valueArray)):                    #i = i + 1            #Input #1, nameArray[i], self.kct_valueArray[i]            self.kct_sumx = self.kct_sumx + self.kct_valueArray[j][ self.kct_theDataAttribute ]            self.kct_sumxx = self.kct_sumxx + math.pow( self.kct_valueArray[j][ self.kct_theDataAttribute ], 2)            #n = n + 1            countElements = len(self.kct_valueArray)                #print 'countElements: ' + countElements + ' --- self.kct_sumx: ' + self.kct_sumx + ' --- self.kct_sumx: ' + self.kct_sumx                 self.kct_mean = self.kct_sumx / countElements        self.kct_sd = float( math.sqrt( ((countElements * self.kct_sumxx) - (math.pow(self.kct_sumx,2)))) / (countElements * (countElements - 1)) )                print 'Sorting . . .'                self.kct_valueArray = sorted( self.kct_valueArray, key=lambda item: item[ self.kct_theDataAttribute ])   # Sems to default to: Array.NUMERIC                #******************sort into ascending order******                """        yy = 1                #13042                 yy = 2 * yy                        while( yy < n ) {                    if( dontGoForever > 100 ) {                         break                    }                    #Then GoTo 13042                    yy = 2 * yy                    dontGoForever++                }                #13044                 yy = (yy - 1) / 2                #yy = Int((yy - 1) / 2)                        if( yy == 0 ) {                    #Then GoTo 13073                } else {                    yy = (yy - 1) / 2;                # eg # #13044                                         it = n - yy                                for( i = 1; i <= it; i++ ) {                                    j = i                        #13049                              z = j + yy                                    if( self.kct_valueArray[z] <= value[j] ) {                            #Then GoTo 13054                            break                        }                        #13051   Next i                                }                        #13052   GoTo 13044                            }                                #13054                   temp = self.kct_valueArray[z]                self.kct_valueArray[z] = self.kct_valueArray[j]                self.kct_valueArray[j] = temp                        tempor$ = nam$(z)                nam$(z) = nam$(j)                nam$(j) = tempor$                #13057                   j = j - yy                #13058                  if( j > 0 ) {                    #Then GoTo 13049                }                #13059   GoTo 13051                13073   Label2.Visible = 0        """            # Do the final bit of statistics        self.kct_minvalue = self.kct_valueArray[0][ self.kct_theDataAttribute ]        self.kct_maxvalue = self.kct_valueArray[ len(self.kct_valueArray) - 1 ][ self.kct_theDataAttribute ]                if self.kct_minvalue < 0:            self.kct_adder = self.kct_minvalue / 10        else:            self.kct_adder = 0.1                print 'Data successfully imported.'        print 'Data statisitcs computed.'                return True        # 100 equal interval***********************    def classBreaksEqualInterval( self, resultsArray, resultsSummaryArray ):        print 'Equal Interval: Developing class boundaries...'                Interval = float(self.kct_maxvalue - self.kct_minvalue) / self.kct_numclass        print 'Interval: ', Interval, ' self.kct_maxvalue: ', self.kct_maxvalue, ' self.kct_minvalue: ', self.kct_minvalue, ' (self.kct_maxvalue - self.kct_minvalue): ', (self.kct_maxvalue - self.kct_minvalue), 'self.kct_numclass: ', self.kct_numclass                for i in range(self.kct_numclass):            self.kct_lowclass[i] = self.kct_minvalue + (Interval * i )                    if i > 0:                self.kct_lowclass[i] = self.kct_lowclass[i] + self.kct_adder                    self.kct_highclass[i] = self.kct_minvalue + (Interval * (i + 1) )            #GoTo 600        self.classAssign( resultsArray, resultsSummaryArray )            # 200 quantiles****************************    def classBreaksQuantiles( self, resultsArray, resultsSummaryArray ):        print 'Quantiles: Developing class boundaries...'                lowval = 0        highval = 0                Interval = float(math.floor( len(self.kct_valueArray)) / self.kct_numclass)        # was Int()        dif = len(self.kct_valueArray) - (Interval * self.kct_numclass)            print 'Interval: %d  -- dif: %d' % (Interval, dif)                ncount = 0                print 'self.kct_numclass: ', self.kct_numclass                for i in range(self.kct_numclass):            lowval = ncount            highval = ncount + Interval - 1                    if dif > 0:                highval = highval + 1                    dif = dif - 1            ncount = highval + 1                        print "self.kct_valueArray[ lowval  ][ self.kct_theDataAttribute ]", int(lowval), self.kct_theDataAttribute            print "self.kct_valueArray[ highval  ][ self.kct_theDataAttribute ]", int(highval), self.kct_theDataAttribute                        self.kct_lowclass[i]  = self.kct_valueArray[ int(lowval)  ][ self.kct_theDataAttribute ]                            # was value(lowval)            self.kct_highclass[i] = self.kct_valueArray[ int(highval) ][ self.kct_theDataAttribute ]                    #GoTo 600        self.classAssign( resultsArray, resultsSummaryArray )            # 300 'standard deviation*******************    def classBreaksStdDeviation( self, resultsArray, resultsSummaryArray ):        print 'Standard Deviation: Developing class boundaries...'            n4not = self.kct_numclass        # n4! = self.kct_numclass                lowest = self.kct_mean - (self.kct_sd * (n4not / 2))                for i in range(self.kct_numclass):                    self.kct_lowclass[i] = lowest + (self.kct_sd * i)                self.kct_highclass[i] = self.kct_lowclass[i] + self.kct_sd                    if i > 0:                self.kct_lowclass[i] = self.kct_lowclass[i] + self.kct_adder                for i in range(len(self.kct_valueArray)):                    if self.kct_valueArray[ i ][ self.kct_theDataAttribute ] > self.kct_highclass[ self.kct_numclass - 1 ]:                self.kct_highclass[ self.kct_numclass - 1 ] = self.kct_valueArray[ i ][ self.kct_theDataAttribute ]                    if self.kct_valueArray[i][ self.kct_theDataAttribute ] < self.kct_lowclass[ 0 ]:                self.kct_lowclass[ 0 ] = self.kct_valueArray[ 0 ][ self.kct_theDataAttribute ]                #GoTo 600        self.classAssign( resultsArray, resultsSummaryArray )            # 400 'minimum variance*********************    # aka Jenks Optimal    def classBreaksMinVariance( self, resultsArray, resultsSummaryArray ):        print 'Minimum Variance (Jenks): Developing class boundaries...'                # ReDim self.kct_m1(n, self.kct_numclass), self.kct_a1(n, self.kct_numclass)        self.kct_a1 = [0] * len(self.kct_valueArray)                     # Creating an array of that length        self.kct_m1 = [0] * len(self.kct_valueArray)                for i in range(len(self.kct_valueArray)):            self.kct_a1[i] = [0] * self.kct_numclass            self.kct_m1[i] = [0] * self.kct_numclass                for i in range(self.kct_numclass):            self.kct_a1[ 0 ][ i ] = -1            self.kct_m1[ 0 ][ i ] = 0            #print 'self.kct_a1[ 0 ][ ', i, ' ]: ', self.kct_a1[ 0 ][ i ]            #print 'self.kct_m1[ 0 ][ ', i, ' ]: ', self.kct_m1[ 0 ][ i ]                                for j in range(len(self.kct_valueArray)):                        self.kct_a1[ j ][ i ] = 999999999999999                #print 'self.kct_a1[ ', j, ' ][ ', i, ' ]: ', self.kct_a1[ j ][ i ]                # need to keep track if this outside for loop        s1 = float()       # new Number()        s2 = float()       # new Number()        k1 = float()       # new Number()        v = float()       # new Number()                for i in range(len(self.kct_valueArray)):                    s1 = 0            s2 = 0            k1 = 0                    for i in range(i+1):                        #i3 = i - j                i3 = i - j + 1                s2 = s2 + math.pow( float(i3), 2 )                s1 = s1 + float(i3)                k1 = k1 + 1                v = s2 - math.pow(s1, 2) / k1                i4 = i3 - 1                #print 'i3: ', i3, ' -- s1: ', s1, ' -- s2: ', s2,  ' -- k1: ', k1, ' -- k1: ', k1, ' -- v: ', v, ' -- i4: ', i4                                if i4 == 0:                    #Then GoTo 1520                    #print 'i4 == 0, breaking'                    break                else:                    for z in range(self.kct_numclass):                        if z == 0:                            #Then GoTo 1510                            #print 'k == 0, continuing'                            continue                        else:                            if self.kct_a1[ i ][ z ] < ( v + self.kct_a1[ i4 ][ z - 1 ] ):                                #Then GoTo 1510                                #print 'self.kct_a1[ ', i, ' ][ ', z, ' ] < ( v + self.kct_a1[ i4 ][ z - 1 ] ), continuing'                                continue                            else:                                self.kct_m1[ i ][ z ] = i3                                self.kct_a1[ i ][ z ] = v + self.kct_a1[ i4 ][ z - 1 ]                                #print 'i3: ', i3, ' -- self.kct_m1[ ', i, ' ][ ', z, ' ]: ', self.kct_m1[ i ][ z ], ' -- v + self.kct_a1[ i4 ][ z - 1 ]: ', v, self.kct_a1[ i4 ][ z - 1 ], ' -- self.kct_a1[ ', i, ' ][ ', z, ' ]: ', self.kct_a1[ i ][ z ]            #1510 Next            #1520 Next                    self.kct_m1[ i ][ 0 ] = 0            self.kct_a1[ i ][ 1 ] = v            print 'setting v in self.kct_a1 @ 1... ', i, ' value: ', v        #Next                for i in range(self.kct_numclass):            for j in range(len(self.kct_valueArray)):                print 'self.kct_a1[ ', j, ' ][ ', i, ' ]: ', self.kct_a1[ j ][ i ]                i5 = int( len(self.kct_valueArray) )                for m in range(self.kct_numclass):            l2 = self.kct_numclass - m - 1            i6 = i5 - 1            print 'self.kct_m1[ i6 ][ l2 ]: ', self.kct_m1[ i6 ][ l2 ]            i5 = int( self.kct_m1[ i6 ][ l2 ] )            print 'l2: ', l2, ' -- i6: ', i6, ' -- i5: ', i5                    self.kct_lowclass[ l2 ] = float(i5)            self.kct_highclass[ l2 ] = float(i6)        #Next                print 'self.kct_lowclass: ', self.kct_lowclass        print 'self.kct_highclass: ', self.kct_highclass                #GoTo 600        self.classAssign( resultsArray, resultsSummaryArray )            # 500 user -defined************************    def classBreaksUserDefined( self, resultsArray, resultsSummaryArray ):        print 'User defined: Developing class boundaries...'                #user.Label2.Caption = Str$(self.kct_numclass)        #user.Text1.Text = ''        #user.Text2.Text = ''            for i in range(self.kct_numclass):            #user.List1.AddItem Str$(i)            self.kct_lowclass[i] = self.kct_manualBreaks[i].low            self.kct_highclass[i] = self.kct_manualBreaks[i].high                self.classAssign( resultsArray, resultsSummaryArray )            # 600 assign classes***********************    def classAssign( self, resultsArray, resultsSummaryArray ):        print 'Assigning classes to dataset elements...'                print 'resultsArray: ', resultsArray, ' len(self.kct_valueArray): ', len(self.kct_valueArray)        print 'resultsArray: ', resultsArray, ' len: ', len(resultsArray)        print 'resultsSummaryArray: ', resultsSummaryArray, ' len: ', len(resultsSummaryArray)            print 'self.kct_valueArray', self.kct_valueArray, ' len: ', len(self.kct_valueArray)        print 'self.kct_lowclass', self.kct_lowclass        print 'self.kct_highclass', self.kct_highclass            for i in range(len(self.kct_valueArray)):            #print 'i: ', i            for j in range(self.kct_numclass):                                                #print '\tj: ', j                # classify                if (self.kct_valueArray[i][ self.kct_theDataAttribute ] >= self.kct_lowclass[j]) and (self.kct_valueArray[i][ self.kct_theDataAttribute ] <= self.kct_highclass[j]):                    resultsArray[i] = j                # build the histogram (count how many in that class)                if (self.kct_valueArray[i][ self.kct_theDataAttribute ] >= self.kct_lowclass[j]) and (self.kct_valueArray[i][ self.kct_theDataAttribute ] <= self.kct_highclass[j]):                    resultsSummaryArray[j] = resultsSummaryArray[j] + 1                        print 'resultsArray: ', resultsArray        print 'resultsSummaryArray: ', resultsSummaryArray            #######################    # Begin NVK improvise    #######################        def classAssignNominal( self, resultsArray, resultsSummaryArray ):        print 'Assigning NOMINAL classes to dataset elements...'            for i in range(len(self.kct_valueArray)):            #print 'self.kct_valueArray[ ' + i + '][ ' + self.kct_theDataAttribute + ']: ' + self.kct_valueArray[i][ self.kct_theDataAttribute ]            for j in range(len(self.kct_manualBreaks)):                #print 'self.kct_numclass: ' + self.kct_numclass                for k in range(len(self.kct_manualBreaks[j])):                    #print ' with ' + len(self.kct_manualBreaks[j]) + ' subcategories'                    #print 'self.kct_manualBreaks[' + j + '][' + k + ']: ' + self.kct_manualBreaks[j][k]                    if str( self.kct_valueArray[i][ self.kct_theDataAttribute ]) == str(self.kct_manualBreaks[j][k]):                        #print 'found match'                        resultsArray[i] = j                        resultsSummaryArray[j] = resultsSummaryArray[j] + 1                        break        # from page 171 of Dent (table 8.2)    def classAssignRatio( self, resultsArray ):        print 'Assigning RATIO classes to dataset elements...'                if self.kct_fromZero:            gc_minValue = 0        else:            gc_minValue = self.kct_valueArray[0][ self.kct_theDataAttribute ]            if self.kct_to100:            gc_maxValue = 100        else:            gc_maxValue = self.kct_valueArray[ (len(self.kct_valueArray) - 1) ][ self.kct_theDataAttribute ]                # Do the value ranges        if self.kct_gc_maxValue > self.kct_gc_minValue:            self.kct_gc_rangeValue = self.kct_gc_maxValue - self.kct_gc_minValue        else:            self.kct_gc_rangeValue = self.kct_gc_minValue - self.kct_gc_maxValue                        print 'lowval: %f  -- highval: %f  -- dif: %f' % (self.kct_gc_minValue, self.kct_gc_maxValue, self.kct_gc_rangeValue)        print 'len(self.kct_valueArray: %d' % (len(self.kct_valueArray))                # assumes resultsArray[] is empty         for i in range(len(self.kct_valueArray)):            resultsArray[i] = float( self.kct_valueArray[i][ self.kct_theDataAttribute ] ) / self.kct_gc_maxValue                print 'resultsArray: ', resultsArray        def setGraduatedCircleRanges( self ):        """        # cirlce size diameters from Dent p 175, fig. 8.11        0    .05"    3.6 pts        1    .09"    6.48 pts        2    .13"    9.36 pts        3    .22"    15.84 pts        4    .34"    24.48 pts        5    .49"    35.28 pts        6    .76"    54.72 pts        7    1.02"    73.44 pts        8    1.19"    85.68 pts        """                # Do the Size ranges        if self.kct_gc_maxSize > self.kct_gc_minSize:            self.kct_gc_rangeSize = self.kct_gc_maxSize - self.kct_gc_minSize        else:            self.kct_gc_rangeSize = self.kct_gc_minSize - self.kct_gc_maxSize                # calculate the areas        self.kct_gc_minArea = math.pi * self.kct_gc_minSize * self.kct_gc_minSize        self.kct_gc_maxArea = math.pi * self.kct_gc_maxSize * self.kct_gc_maxSize                # Do the Area ranges        if self.kct_gc_maxArea > self.kct_gc_minArea:            self.kct_gc_rangeArea = self.kct_gc_maxArea - self.kct_gc_minArea        else:            self.kct_gc_rangeArea = self.kct_gc_minArea - self.kct_gc_maxArea                        return True        def classAssignProportional( self, resultsArray ):        result = self.setGraduatedCircleRanges()                if self.kct_gc_flannery:            # apparent magnitude scaling            for i in range(len(self.kct_valueArray)+1):                resultsArray[i] = 2 * ( self.kct_gc_minSize / math.pow( self.kct_gc_minValue / self.kct_valueArray[i][ self.kct_theDataAttribute ], .5716 ) )        elif gc_graduatedCircle:            # linear scaling            for i in range(len(self.kct_valueArray)+1):                resultsArray[i] = 2 * ( self.kct_gc_minSize / math.sqrt( self.kct_gc_minValue / self.kct_valueArray[i][ self.kct_theDataAttribute ] ) )        elif gc_graduatedSquare:            # TODO: not implemented            # See Dent pp 171 - 173            pass                    #    'report classing results**************    def classReport(self):        print '\nReporting classes of dataset elements...'            print '\nThe ', self.kct_classifyType_1, ' class breaks (', self.kct_classifyType_2, ' 2ndary ), based on ', self.kct_sortOnAttribute, ':'            for i in range(self.kct_numclass_1):            theClassTemp = i+1            print 'Class %s: %d - %d' % (theClassTemp, self.kct_lowclass[i], self.kct_highclass[i])                        # HACK        print '\nkct_valueArray: ', self.kct_valueArray, ' len: ', len(self.kct_valueArray)        print 'kct_cl: ', self.kct_cl, ' len: ', len(self.kct_cl)        print 'kct_cl_2: ', self.kct_cl_2, ' len: ', len(self.kct_cl_2)        print 'kct_cl_3: ', self.kct_cl_3, ' len: ', len(self.kct_cl_3)                print '\nname', '\t', 'value', '\t', 'class1', '\t', 'class2', '\t', 'class3'        for n in range(len(self.kct_valueArray)):            print '%s\t%s\t%s\t%s\t%s' % (self.kct_valueArray[n]['name'], self.kct_valueArray[n][self.kct_sortOnAttribute], self.kct_cl[n], self.kct_cl_2[n], self.kct_cl_3[n])                            def printCSS(self):        print '\n...CSS...'        print 'The ', self.kct_classifyType_1, ' class breaks (', self.kct_classifyType_2, ' 2ndary ), based on ', self.kct_sortOnAttribute, ':\n'            layerID = '#' + self.kct_sortOnAttribute        zoom = '[zoom=8]'        filterPrefix = '[' + self.kct_sortOnAttribute        filterPostfix = ']'        style = '{ polygon-fill: #ededed; }'                for i in range(self.kct_numclass_1):            if i < (self.kct_numclass_1 - 1):                print layerID + filterPrefix + '>=' + str(self.kct_lowclass[i]) + filterPostfix + filterPrefix + '<' + str(self.kct_highclass[i]) + filterPostfix            else:                print layerID + filterPrefix + '>=' + str(self.kct_lowclass[i]) + filterPostfix + filterPrefix + '<=' + str(self.kct_highclass[i]) + filterPostfix                print ''                    """        #water-bodies[zoom=8][area>50000000] { polygon-fill: #000; }        #water-bodies[zoom=9][area>10000000] { polygon-fill: #000; }        #water-bodies[zoom=10][area>2500000] { polygon-fill: #000; }        """    def unitTests(self):            #**************************************************************************/        # Unit tests - START        #**************************************************************************/                gasPriceTest = [    {'name':'test0', 'gasPrice': 55, 'pumpType':'diesel' },                            {'name':'test1', 'gasPrice': 25, 'pumpType':'diesel' },                            {'name':'test2', 'gasPrice': 36, 'pumpType':'diesel' },                            {'name':'test3', 'gasPrice': 37, 'pumpType':'other' },                            {'name':'test4', 'gasPrice': 36, 'pumpType':'gas' },                            {'name':'test5', 'gasPrice': 35, 'pumpType':'gas' },                            {'name':'test6', 'gasPrice': 35, 'pumpType':'gas' },                            {'name':'test7', 'gasPrice': 15, 'pumpType':'gas' },                            {'name':'test8', 'gasPrice': 1, 'pumpType':'diesel' },                            {'name':'test9', 'gasPrice': 100, 'pumpType':'diesel' },                            {'name':'test10', 'gasPrice': 65, 'pumpType':'gas' },                            {'name':'test11', 'gasPrice': 66, 'pumpType':'gas' },                            {'name':'test12', 'gasPrice': 68, 'pumpType':'diesel' },                            {'name':'test13', 'gasPrice': 70, 'pumpType':'gas' }                        ]                print 'len(gasPriceTest): %s' % len(gasPriceTest)                 wardTest = [   {'name':'ward1', 'gasPrice': 80, 'pumpType':'diesel' },                        {'name':'ward2', 'gasPrice': 25, 'pumpType':'diesel' },                        {'name':'ward3', 'gasPrice': 36, 'pumpType':'diesel' },                        {'name':'ward4', 'gasPrice': 75, 'pumpType':'other' },                        {'name':'ward5', 'gasPrice': 36, 'pumpType':'gas' },                        {'name':'ward6', 'gasPrice': 55, 'pumpType':'gas' },                        {'name':'ward7', 'gasPrice': 35, 'pumpType':'gas' },                        {'name':'ward8', 'gasPrice': 15, 'pumpType':'gas' }                    ]                        testBreaks = [  {'low':0,  'high':20},                        {'low':20, 'high':50},                        {'low':50, 'high':100}                       ]                            testNominalBreaks = [ [['diesel']],[['gas']],[['other']] ]                print 'gasPriceTest: ', gasPriceTest        #dataAttrName = 'gasPrice'              dataAttrName = 'LTV'        f = open('/Users/nvkelso/Documents/Stamen/2012/zillow/data/NegEquity2011Q4.csv', 'rt')        f_dict = []        try:            reader = csv.DictReader(f)            for row in reader:                #print row                #print type( row )                f_dict.append( row )        finally:            f.close()                    for row in f_dict:            row[dataAttrName] = float( row[dataAttrName] )            row['name'] = row['RegionName']                #print reader                dataTest = f_dict                #print dataTest        #print dataAttrName                        #**************************************************************************/        # END Unit tests        #**************************************************************************/                #self.classInit( dataTest, False, dataAttrName, 4, 'Equal Interval', testBreaks, dataAttrName, 2, 'None', testNominalBreaks  )        self.classInit( dataTest, False, dataAttrName, 5, 'Quantiles', testBreaks, dataAttrName, 2, 'None', testNominalBreaks  )        #self.classInit( dataTest, False, dataAttrName, 3, 'Quantiles', testBreaks, dataAttrName, 2, 'None', testNominalBreaks  )        #self.classInit( dataTest, False, dataAttrName, 3, 'Standard Deviation', testBreaks, dataAttrName, 2, 'None', testNominalBreaks  )                #TODO: fix        #self.classInit( dataTest, False, dataAttrName, 3, 'Minimum Variance', testBreaks, dataAttrName, 2, 'Ratio', testNominalBreaks  )        #self.classInit( dataTest, False, dataAttrName, 3, 'Manual', testBreaks, dataAttrName, 2, 'Ratio', testNominalBreaks )                #self.classInit( dataTest, False, dataAttrName, 3, 'Ratio', testBreaks, 'pumpType', 2, 'Nominal', testNominalBreaks )        #self.classInit( dataTest, False, dataAttrName, 3, 'Ratio', testBreaks, 'pumpType', 4, 'None', testNominalBreaks )        #self.classInit( dataTest, False, dataAttrName, 4, 'Equal Interval', testBreaks, 'pumpType', 2, 'Nominal', testNominalBreaks  )                 if __name__ == "__main__":    c = Classify()        c.unitTests()    """    def classDraw(self, _masterMap:MovieClip ):        print '\nDrawing the colors onto the map...'                for i in range(len(self.kct_valueArray)):            # This for non-standard numbering systems that require pre zeros like myName003 and myName030 and myName300            #if (i < 10) { mNum = '00' + i; } else if (i < 100 and i > 9) { mNum = '0' + i; } else { mNum = i }            thisGeography = self.kct_valueArray[i]['name']            #print self.kct_valueArray[i]['name'] )                        # Store the actual element name            _masterMap[ thisGeography ].self.kct_displayName = self.kct_valueArray[i]['name']            # Store the actual data value            _masterMap[ thisGeography ].self.kct_dataValue = self.kct_valueArray[i][self.kct_sortOnAttribute]            # Store the color percentage            _masterMap[ thisGeography ].self.kct_classValue = self.kct_cl[i]            if self.kct_alwaysDoQuantiles:                # Store the data Quantile                _masterMap[ thisGeography ].self.kct_quantileValue = self.kct_cl_3[i]                                colorClassShade:ColorTransform = new ColorTransform()            #print colorClassShade )                        #shadeColor:Color = new Color( _masterMap[ thisGeography ] )            thisColorCounter = 0            thisColorRGB                        if self.kct_classifyType_1 == 'Ratio':                thisColorCounter = self.kct_cl_2[i]            else:                thisColorCounter = self.kct_cl[i]                #print 'the color counter should be: ' + thisColorCounter            if thisColorCounter >= 0 and thisColorCounter < self.kct_numclass_2:                #print 'was able to set color'                 thisColorRGB = self.kct_dataColors[ thisColorCounter ]                                colorClassShade.rgb = thisColorRGB                        print colorClassShade                        if self.kct_classifyType_1 == 'Ratio':                colorClassShade.redOffset *= 1 - self.kct_cl[i]                colorClassShade.greenOffset *= 1 - self.kct_cl[i]                colorClassShade.blueOffset *= 1 - self.kct_cl[i]                colorClassShade.alphaOffset = 1                        print colorClassShade                        if colorClassShade != undefined and colorClassShade.rgb != 0xFFFFFF:                #shadeColor.setRGB( thisColorRGB )                _masterMap[ thisGeography ].transform.colorTransform = colorClassShade                _masterMap[ thisGeography ].self.kct_cColor = colorClassShade                                activateGeography( _masterMap[ thisGeography ] )                                # DISPLAY THE TOOLTIP                labelText1 = ''                labelText2 = ''                labelText3 = ''                labelText1 = _masterMap[ thisGeography ].self.kct_displayName                labelText2 = self.kct_sortOnAttribute + ': \t' + _masterMap[ thisGeography ].self.kct_dataValue                if self.kct_alwaysDoQuantiles:                    if self.kct_doQuantilesBreaks == 5:                        labelText3 = 'Rank: '                        if _masterMap[ thisGeography ].self.kct_quantileValue == 0:                                 labelText3 += 'Worst 1/5th'                        elif _masterMap[ thisGeography ].self.kct_quantileValue == 1:                            labelText3 += 'Above average 2/5th'                        elif _masterMap[ thisGeography ].self.kct_quantileValue == 2:                            labelText3 += 'Average 3/5th'                        elif _masterMap[ thisGeography ].self.kct_quantileValue == 3:                            labelText3 += 'Below average 4/5th'                        elif _masterMap[ thisGeography ].self.kct_quantileValue == 4:                            labelText3 += 'Best 5/5th'                    else:                        labelText3 = '(Class: \t' + _masterMap[ thisGeography ].self.kct_quantileValue + ')'                else:                    labelText3 = '(Class: \t' + _masterMap[ thisGeography ].self.kct_classValue + ')'                                _masterMap[ thisGeography ].self.kct_myTooltip = new Array(3)                                            _masterMap[ thisGeography ].self.kct_myTooltip[0] = labelText1                _masterMap[ thisGeography ].self.kct_myTooltip[1] = labelText2                _masterMap[ thisGeography ].self.kct_myTooltip[2] = labelText3            else:                colorClassShade.rgb = 0xFFFFFF                _masterMap[ thisGeography ].self.kct_cColor = colorClassShade                _masterMap[ thisGeography ].enabled = False    """