import copy
import pickle
from tkinter import messagebox
#------------------------------Driver Class------------------------------------

class ScheduleMaker:
    def __init__(self):
            self.ScheduleList=[]
            self.ScheduleList.append(Schedule())
            self.currentSchedule=0 #This will have the index num of the
                                    #currently loaded schedule in the mainwindow
            
    def MakeAlternateSchedule(self,oldcourse):
        alternateSchedule=copy.deepcopy(self.ScheduleList[self.currentSchedule])
        self.DeleteCourse(oldcourse.name,alternateSchedule)
        self.ScheduleList.append(alternateSchedule)
        return alternateSchedule

    def CheckClash(self,course1): 
            for i in self.ScheduleList[self.currentSchedule].data:
                if len(self.ScheduleList[self.currentSchedule].data[i])!=0:
                    for course2 in self.ScheduleList[self.currentSchedule].data[i]:
                        for i in course1.days:
                            for j in course2.days:
                                if i==j:
                                    if course1.StartTime==course2.StartTime or course1.EndTime==course2.EndTime:
                                        print('1 Clash in '+course1.name+' and '+course2.name)
                                        return (True,course2)
                                    if course1.StartTime<course2.StartTime and course1.EndTime>course2.EndTime:
                                        print('2 Clash in '+course1.name+' and '+course2.name)
                                        return (True,course2)
                                    if course1.StartTime>course2.StartTime and course1.EndTime<course2.EndTime:
                                        print('3 Clash in '+course1.name+' and '+course2.name)
                                        return (True,course2)
                                    if (course1.StartTime<course2.StartTime and course1.EndTime> course2.StartTime) and course1.EndTime<course2.EndTime:
                                        print('4 Clash in '+course1.name+' and '+course2.name)
                                        return (True,course2)
                                    if (course1.StartTime>course2.StartTime and course1.StartTime<course2.EndTime) and course1.EndTime>course2.EndTime:
                                        print('5 Clash in '+course1.name+' and '+course2.name)
                                        return (True,course2)

            return(False,None)

    def AddCourse(self,courseobj): #Adds a new course in either the current schedule or in an alternate one, according to cls
        x=self.CheckClash(courseobj)
        if x[0]:
            new=self.MakeAlternateSchedule(x[1]) #This will make an alternate schedule
            new.AddCourse(courseobj) #This will add the new course in the alternate schedule created
            new.courselst.append(courseobj.name)
            
        else:
            self.ScheduleList[self.currentSchedule].AddCourse(courseobj)
            self.ScheduleList[self.currentSchedule].courselst.append(courseobj.name)

    def DeleteCourse(self,coursename,schedule):
        if coursename=="":
            return
        else:
            schedule.DeleteCourse(coursename)
            schedule.courselst.remove(coursename)

    def Next(self): #moves to next schedule in backend
        if len(self.ScheduleList)>1 and self.currentSchedule!=len(self.ScheduleList)-1:
            self.currentSchedule+=1
            return True
        else:
            return False

    def Previous(self): #moves to previous schedule in backend
        if len(self.ScheduleList)>1 and self.currentSchedule!=0:
            self.currentSchedule-=1
            return True
        else:
            return False

    def GetCourseNames(self):
        return self.ScheduleList[self.currentSchedule].courselst

    def DeleteSchedule(self):
        if len(self.ScheduleList)>1:
            if self.currentSchedule==len(self.ScheduleList)-1:
                self.ScheduleList.pop(self.currentSchedule)
                self.currentSchedule=0
                return True
            else:
                self.ScheduleList.pop(self.currentSchedule)
                self.Next()
                return True
        else:
            for i in self.ScheduleList[self.currentSchedule].data:
                for j in self.ScheduleList[self.currentSchedule].data[i]:
                    self.DeleteCourse(j.name,self.ScheduleList[self.currentSchedule])
            return True

    def Save(self,filename): 
        file=str(filename)+".pickle"
        pickle_file=open(file,"wb")
        newScheduleMaker=copy.deepcopy(self)
        currentSchedule=newScheduleMaker.ScheduleList.pop(newScheduleMaker.currentSchedule)
        newScheduleMaker.ScheduleList=[]
        newScheduleMaker.ScheduleList.append(currentSchedule)
        newScheduleMaker.currentSchedule=0
        pickle.dump(newScheduleMaker,pickle_file)
        pickle_file.close()

    def Load(self,filename):
        if filename[-1:-8]!='.pickle':
            filename=str(filename)+".pickle"
        pickle_file=open(filename,"rb")
        loaded=pickle.load(pickle_file)
        pickle_file.close()
        return loaded
    

            

##----------------------------Schedule Class-----------------------------------

class Schedule:
    def __init__(self):
        self.data={}
        self.clearSchedule()
        self.courselst=[]

    def AddCourse(self,courseobj):
        for i in courseobj.days:
            self.data[i].append(courseobj)
##        for i in self.data:
##            print(i,end=' ')
##            for j in self.data[i]:
##                print(j.name,end=',')
##            print()

    def DeleteCourse(self,coursename):
        for i in self.data:
            for j in self.data[i]:
                if j.name==coursename:
                    self.data[i].remove(j)

    def clearSchedule(self):
        weekday=["M","T","W","R","F"]
        for i in weekday:
            self.data[i]=[]
                    

#-----------------------------Course Class-------------------------------------

class Course:
    def __init__(self,name,code,days,stimehour,stimemin,stimeam,etimehour,etimemin,etimeam,color):
        self.name=name #string
        self.code=code #string
        self.days=self.getdays(days) #List  #This calls the method that gets the days from the list of 0's and 1's.
        self.StartTime=Time(int(stimehour),int(stimemin),stimeam)
        self.EndTime=Time(int(etimehour),int(etimemin),etimeam)
        self.Color=color
        self.TotalMinutes=self.CountMinutes(self.StartTime,self.EndTime)
        self.TimeFromStart=self.CountTimeBefore()

    def CountTimeBefore(self): 
        return self.CountMinutes(Time(8,00,'AM'),self.StartTime)

    def getdays(self,days): 
        lstday=[]
        weekday=["M","T","W","R","F"]
        for i in range(len(days)):
            if days[i]==1:
                lstday.append(weekday[i])
        return lstday

    def CountMinutes(self,t1,t2):
        if t1.daytime==t2.daytime:
            if t1.hour==t2.hour:
                return t2.min-t1.min
            
            if t2.hour==12:
                    return ((((t2.hour-t1.hour)*60)-t1.min)+t2.min)
            elif t1.hour==12:
                    return ((((t1.hour-12)+t2.hour)*60-t1.min)+t2.min)
            else:
                if t1.hour>t2.hour:
                    return ((((t1.hour-self.t2.hour)*60)-t1.min)+t2.min)
                else:
                    return ((((t2.hour-t1.hour)*60)-t1.min)+t2.min)

        if t1.daytime=="AM" and t2.daytime=="PM":
                    if t2.hour!=12:
                        return (((((12-t1.hour)+t2.hour)*60)-t1.min) + t2.min)
                    else:
                        return ((((12-t1.hour)*60)-t1.min)+t2.min)
            
        if t1.daytime=="PM" and t2.daytime=="AM":
            if t1.hour>t2.hour:
                if t2.hour!=12:
                    return (((((12-t1.hour)+t2.hour)*60)-t1.min) + t2.min)
                else:
                    return ((((12-t1.hour)*60)-t1.min)+t2.min)

#------------------------------Time Class---------------------------------------
class Time:
    def __init__(self,hour,minutes,dt):
        self.hour=hour
        self.min=minutes
        self.daytime=dt

    def __eq__(a,b):
        if a.daytime==b.daytime and a.hour==b.hour and a.min==b.min:
            return True
        else:
            return False

    def __lt__(a,b):
        if a.daytime=="AM" and b.daytime=="PM":
            return True
        if a.daytime=="PM" and b.daytime=="AM":
            return False

        if a.daytime == b.daytime:
            if a.hour<b.hour:
                if b.hour!=12:
                    return True
                else:
                    return False
            elif a.hour==b.hour:
                if a.min<b.min:
                    return True
                else:
                    return False
            else:
                if a.hour!=12:
                    return False
                else:
                    return True

    def __gt__(a,b):
        return not(Time.__lt__(a,b))

    def __le__(a,b):
        return (Time.__lt__(a,b)) or (Time.__eq__(a,b))

    def __ge__(a,b):
        return (Time.__gt__(a,b)) or (Time.__eq__(a,b))

    def __ne__(a,b):
        return not(Time.__eq__(a,b))
    
#----------------------------------------------------------------------------
