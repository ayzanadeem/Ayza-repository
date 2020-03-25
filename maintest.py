from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from ScheduleMaker import *
import random
#----------------------------------------------------------------------------
class MainWindow:
    def __init__(self):
        self.SMaker= ScheduleMaker()
        self.mainwindow=Tk()
        self.mainwindow.title("Course Schedule Maker")
        self.mainwindow.geometry("1204x654+30+30")
        self.ButtonDisplay=False
        self.DeleteEnable=True
        self.Opened=False
                                                 
        def CreateSchedule(): #creates a new schedule template
            self.LoadWindow()
            self.ButtonDisplay=True
            self.DeleteEnable=True
            if self.Opened==True:
                self.SMaker=ScheduleMaker()
                self.Opened=False

            
        def ViewSchedule(): #loads un-editable schedule
            self.canvas.delete('welcome')
            self.DeleteEnable=False
            if self.ButtonDisplay==True:
                self.b.destroy()
                self.delc.destroy()
                self.dels.destroy()
                self.b1.destroy()
                self.b2.destroy()
                self.b3.destroy()
                self.b4.destroy()
            self.Load()
            self.CreateTemplate(True,self.SMaker.ScheduleList[self.SMaker.currentSchedule].data)
            

        def OpenSchedule(): #loads editable schedule
                self.Opened=True
                self.DeleteEnable=True
                self.ButtonDisplay=True
                self.LoadWindow()
                self.Load()

        def About():
            showinfo("About","This software is designed by Ayza and Joshua ™ \nThis software creates course schedules for students.")



        menu = Menu(self.mainwindow)
        self.mainwindow.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Create Schedule",command=CreateSchedule)
        filemenu.add_command(label="Open Schedule",command=OpenSchedule)
        filemenu.add_command(label="View Schedule", command=ViewSchedule)
        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...",command=About)
        self.BGimg=PhotoImage(file="assets/blue.gif")
        self.canvas = Canvas(self.mainwindow, width = 1200, height = 650)
        self.canvas.place(x=0,y=0)
        self.canvas.focus_set()
        
        self.canvas.create_image(0,0,image=self.BGimg,anchor="nw")
        self.welcome=self.canvas.create_text(600,230,fill="White",font="Helvetica 20 bold italic",text="Welcome to Schedule Planner\n\nOpen File menu on top of the screen to begin.",tags=('welcome'),justify='center')
        self.mainwindow.mainloop()

    def LoadWindow(self): #loads all the contents of the main window 
        self.canvas.delete('welcome')
        title=self.canvas.create_text(600,75,fill="White",font="Helvetica 16 bold italic",text="Course Schedule Planner\n\nworkspace",justify='center')
        self.b=Button(self.mainwindow, text="Add Course",width=13, fg="Blue",font="system 11", command= self.AddCourse)
        self.b.place(x=17,y=180)
        self.delc=Button(self.mainwindow,text="Delete Course",width=13,fg="Blue",font="system 11",command=self.DeleteCourse,state=DISABLED)
        self.dels=Button(self.mainwindow,text=" Delete Schedule ",width=13,fg="Blue",font="system 11",command=self.DeleteSchedule,state=DISABLED)
        self.b1=Button(self.mainwindow,text="Save Schedule",width=13,font="system 11",fg="Blue",command=self.Save)
        self.b1.place(x=17,y=340)
        self.b2=Button(self.mainwindow,text="Load Schedule",width=13,font="system 11",fg="Blue",command=self.Load)
        self.b2.place(x=17,y=393)
        self.b3=Button(self.mainwindow,text="Next",width=10,fg="Blue", font="system 15",command=self.Next)
        self.b3.place(x=500,y=500)
        self.b4=Button(self.mainwindow,text="Previous",width=10,fg="Blue", font="system 15",command=self.Previous)
        self.b4.place(x=630,y=500)
        self.delc.place(x=17,y=235)
        self.dels.place(x=17,y=288)
        self.CreateTemplate()
       
        

    def CreateTemplate(self,fill=False,Scheduledict=None): #if fill is false, it will create empty template, if fill is true, refreshed template with courses in it will be created
        times = ["8:00AM", "9:00AM", "10:00AM", "11:00AM", "12:00PM", "1:00PM", "2:00PM", "3:00PM", "4:00PM"]
        rects = []
        self.lst=[]
       
        #Vertical lines
        self.canvas.create_line(180,130, 180, 460)
        self.canvas.create_line(290, 130, 290, 460)
        self.canvas.create_line(380, 130, 380, 460)
        self.canvas.create_line(470, 130, 470, 460)
        self.canvas.create_line(560, 130, 560, 460)
        self.canvas.create_line(650, 130, 650, 460)
        self.canvas.create_line(740, 130, 740, 460)
        self.canvas.create_line(830, 130, 830, 460)
        self.canvas.create_line(920, 130, 920, 460)
        self.canvas.create_line(1010, 130, 1010, 460)
        self.canvas.create_line(1100, 130, 1100, 460)
        
        #Horizontal lines
        self.canvas.create_line(180, 130, 1100, 130)
        self.canvas.create_line(180, 160, 1100, 160)
        self.canvas.create_line(180, 220, 1100, 220)
        self.canvas.create_line(180, 280, 1100, 280)
        self.canvas.create_line(180, 340, 1100, 340)
        self.canvas.create_line(180, 400, 1100, 400)
        self.canvas.create_line(180, 460, 1100, 460)

        x = 230
        y = 190
        for i in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:

            l = self.canvas.create_text(x, y, text = i)
            y += 60
            
        x = 335
        y = 145
        for i in times:
            l = self.canvas.create_text(x, y, text = str(i))
            x += 90

                
        if fill==False: #creation of empty template
            y = 160
            while y != 460:
                x = 290     
                while x <= 1010:
                    self.canvas.create_rectangle(x, y, x+90, y+60, fill = 'white')     
                    rects.append([x, y, x+90, y+60])
                    x += 90
                y += 60

            
        else: #creation of filled template when fill=True
            y = 160 #original white rectangle creation
            while y != 460:
                x = 290     
                while x <= 1010:
                    self.canvas.create_rectangle(x, y, x+90, y+60, fill = 'white')     
                    rects.append([x, y, x+90, y+60])
                    x += 90
                y += 60

            y=160

            for i in Scheduledict:
                for j in Scheduledict[i]:
                    starttime= str(j.StartTime.hour).zfill(2)+':'+str(j.StartTime.min).zfill(2)
                    endtime= str(j.EndTime.hour).zfill(2)+':'+str(j.EndTime.min).zfill(2)
                    if y !=460:
                        x=290+j.TimeFromStart*1.5
                        self.round_rectangle(x+1, y+1, x+j.TotalMinutes*1.5, y+60, fill = j.Color)
                        self.canvas.create_text((x+(x+j.TotalMinutes*1.5))//2, y+14, text=j.name)
                        self.canvas.create_text((x+(x+j.TotalMinutes*1.5))//2, y+30, text=j.code)
                        self.canvas.create_text((x+(x+j.TotalMinutes*1.5))//2, y+48, text=starttime+' - '+endtime)
                        rects.append([x, y, j.TotalMinutes*1.5, y+60])
                y+=60

            if self.DeleteEnable==True:
                if len(self.SMaker.ScheduleList[self.SMaker.currentSchedule].courselst)!=0:
                    self.delc['state']='normal'
                    self.dels['state']='normal'
                else:
                    self.delc['state']='disabled'
                    self.dels['state']='disabled'
                    


            
    def AddCourse(self): #adds course and refreshes template
        def Confirm(): #This will check if the name of the course are alphabets and then proceeds to make a course object

            if name.get().isalpha():
                self.ValidateColor()
                courseObj= Course(name.get(),code.get(),[c1v.get(),c2v.get(),c3v.get(),c4v.get(),c5v.get()],m1.get(),m2.get(),m3.get(),m4.get(),m5.get(),m6.get(),self.clrVar.get())
                self.SMaker.AddCourse(courseObj)
                self.CreateTemplate(True,self.SMaker.ScheduleList[self.SMaker.currentSchedule].data)
            course.destroy()


                
        course= Tk() #window configuration
        course.title("Add Course")
        course.geometry("400x350+380+240")
        course.focus_force()
        Confirm=Button(course,text ="Confirm",font="bold",width=8,command=Confirm).place(x=85,y=280) #Confirm button
        quit=Button(course,text="Quit",font="bold",width=8,command=course.destroy).place(x=183,y=280) #quit button
        hour,minute= [8,9,10,11,12,1,2,3,4], list(range(0,60))
        self.colordict={'Purple':'MediumPurple2', 'light Green':'aquamarine', 'Blue':'cornflower blue', 'Red':'IndianRed1','Yellow':'LightGoldenrod1', 'Green':'Turquoise','Pink':'hot pink', 'Creme':'lemon chiffon'}

        
        Label(course,text="Name:").place(x=10,y=10)     #Labels
        Label(course,text="Course Code:").place(x=160,y=10)
        Label(course,text="Days:",font=12).place(x=15,y=50)
        Label(course,text="Select a time:",font=12).place(x=15,y=118)
        Label(course,text= "Start Time: ").place(x=19,y=152)
        Label(course,text=":",font='Helvetica 14 bold').place(x=130,y=146)
        Label(course,text="End Time: ").place(x=19,y=196)
        Label(course,text=":",font='Helvetica 14 bold').place(x=130,y=194)
        Label(course,text="*All fields are mandatory*",fg="grey",font="Helvitca 11 italic").place(x=115,y=325)
        Label(course,text="Pick a colour:").place(x=19,y=240)


        name=Entry(course,width=12)#Entries
        code=Entry(course,width=12)
        name.place(x=55,y=13)
        code.place(x=240,y=13)
        
        m1= IntVar(course) #optionmenu vars
        m2= IntVar(course)
        m3= StringVar(course)
        m4=IntVar(course)
        m5=IntVar(course)
        m6=StringVar(course)
        self.clrVar= StringVar(course)
        c1v=IntVar(course) #Checkbutton vars
        c2v=IntVar(course)
        c3v=IntVar(course)
        c4v=IntVar(course)
        c5v=IntVar(course)

        Checkbutton(course,text='M',variable=c1v, onvalue="1").place(x=56,y=80) #Checkbuttons and Drop-Down lists
        Checkbutton(course,text='T',variable=c2v, onvalue="1").place(x=97,y=80)
        Checkbutton(course,text='W',variable=c3v, onvalue="1").place(x=136,y=80)
        Checkbutton(course,text='R',variable=c4v, onvalue="1").place(x=176,y=80)
        Checkbutton(course,text='F',variable=c5v, onvalue="1").place(x=214,y=80)
        OptionMenu(course,m1,*hour).place(x=80,y=146)
        OptionMenu(course,m2,*minute).place(x=140,y=146)
        OptionMenu(course,m3,'AM','PM').place(x=198,y=146)
        OptionMenu(course,m4,*hour).place(x=80,y=194)
        OptionMenu(course,m5,*minute).place(x=140,y=194)
        OptionMenu(course,m6,'AM','PM').place(x=198,y=194)
        colours= OptionMenu(course,self.clrVar,*self.colordict.keys()).place(x=95,y=238)
        self.clrVar.set(random.choice(list(self.colordict.keys())))
        m1.set(8)
        m2.set(f"{00:02d}")
        m3.set('AM')
        m4.set(8)
        m5.set(f"{00:02d}")
        m6.set('AM')

    
    def DeleteCourse(self): #deletes course and refreshes template
        def Confirm(): #this will confirm whether user wants to delete or not,
                       #if yes it proceeds to delete and update the drop down menu
                       #otherwise, nothing happens.
            answer = messagebox.askyesno("Question","Are you sure you want to delete this course?")
            if answer:
                if self.var.get()=="Course Names":
                    self.var.set('') #this is because scheduleMaker delete course simply returns when no course name is selected
                self.SMaker.DeleteCourse(self.var.get(),self.SMaker.ScheduleList[self.SMaker.currentSchedule])
                self.CreateTemplate(True,self.SMaker.ScheduleList[self.SMaker.currentSchedule].data)
                options=self.SMaker.GetCourseNames()
                if len(options)==0:
                    options.append("Course Names")
                OptionMenu(delete,self.var,*options).place(x=10,y=45)
                self.var.set("Course Names")
                delete.destroy()

            
        options= self.SMaker.GetCourseNames()
        if len(options)==0:
            options.append("Course Names")
        delete=Tk()
        delete.title("Delete Course")
        delete.geometry("330x120+380+240")
        delete.focus_force()
        Label(delete,text="Choose a course to delete:",font="Helvetica 12").place(x=10,y=10)
        self.var=StringVar(delete)
        OptionMenu(delete,self.var,*options).place(x=10,y=45)
        self.var.set('Course Names')
        Button(delete,text="Confirm",font="Ariel 12 bold",width=6,command=Confirm).place(x=110,y=80)
        Button(delete,text="Quit",font="Ariel 12 bold",width=6,command=delete.destroy).place(x=180,y=80)

    def DeleteSchedule(self): #deletes currently loaded schedule
        x=self.SMaker.DeleteSchedule()
        if not x:
            messagebox.showerror("Error!","Cannot delete. There is no alternate schedule.")    
        else:
            self.CreateTemplate(True,self.SMaker.ScheduleList[self.SMaker.currentSchedule].data)
        
        
    def Next(self): #loads next schedule, if there is one otherwise gives error
        x=self.SMaker.Next()
        if not x:           # This is the case if there is no next schedule to go to
            messagebox.showerror("Error!","There is no next schedule")
        else:
            self.CreateTemplate(True,self.SMaker.ScheduleList[self.SMaker.currentSchedule].data)

    def Previous(self): #loads previous schedule, if there is one otherwise gives error
        x=self.SMaker.Previous()
        if not x:           # This is the case if there is no previous schedule to go to
            messagebox.showerror("Error!","There is no previous schedule")
        else:
            self.CreateTemplate(True,self.SMaker.ScheduleList[self.SMaker.currentSchedule].data)
 
        
    def Save(self): #saves currently loaded schedule
            def Confirm():
                self.SMaker.Save(name.get())
                save.destroy()
                
            save= Tk() 
            save.title("Save Schedule")
            save.geometry("400x320+380+240")
            save.focus_force()
            Confirm=Button(save,text ="Confirm",font="bold",width=20,command=Confirm)
            namelbl= Label(save,text="Name:")
            name= Entry(save,width=12)
            namelbl.place(x=10,y=10)
            name.place(x=55,y=13)
            Confirm.place(x=85,y=245)
            
            
    def Load(self):
        def Confirm():
            self.SMaker=self.SMaker.Load(name.get())
            self.CreateTemplate(True,self.SMaker.ScheduleList[self.SMaker.currentSchedule].data)
            load.destroy()
            
        load= Tk() 
        load.title("Load Schedule")
        load.geometry("400x320+380+240")
        load.focus_force()
        Confirm=Button(load,text ="Confirm",font="bold",width=20,command=Confirm)
        namelbl= Label(load,text="Name:")
        name= Entry(load,width=12) 
        namelbl.place(x=10,y=10)
        name.place(x=55,y=13)
        Confirm.place(x=85,y=245)


    def ValidateColor(self): #changes original python colour names to understandable colour names (eg: rodbrown1 to yellow)
        for i in self.colordict.keys():
            if i==self.clrVar.get():
                self.clrVar.set(self.colordict[i])
                break
            


    def round_rectangle(self,x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]

        return self.canvas.create_polygon(points, **kwargs, smooth=True)

##my_rectangle = round_rectangle(50, 50, 163, 110, radius=20, fill="turquoise")




#-----------------------------------------------------------------------------

x = MainWindow()
