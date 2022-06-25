clear all; close all; clc;
global cycle No_snap No_fac No_leo tStart tStop dT constellation
dT = 1.0; %  width of time slot
tStart = 0; % scenario start time
dtr = pi/180; % degree to radian
rtd = 180/pi; % radian to degree
remMachine = stkDefaultHost; % default localhost:5001
delete(get(0,'children'));
conid=stkOpen(remMachine); % consID return the handle of stk connection

scen_open = stkValidScen; % if the scene already exist then return 1 otherwise return 0
if scen_open == 1
    rtn = questdlg('Close the current scenario?');
    if ~strcmp(rtn,'Yes')
        stkClose(conid)
    else
        stkUnload('/*')
    end
end
% now we are going to create a new scenario
disp('Create a new scenario'); % display message
stkNewObj('/','Scenario','Matlab_Basic'); % create new Scenario
disp('Set scenario time period'); % display message
stkSetTimePeriod('1 Dec 2019 0:00:00.0','1 Dec 2019 10:00:00.0','GREGUTC'); % set time
stkSetEpoch('1 Dec 2019 0:00:00.0','GREGUTC'); % set scenario epoch
cmd1 = ['SetValues "1 Dec 2019 0:00:00.0" ' mat2str(dT)]; % [] is used to store matrix or vector in matlab
cmd1 = [cmd1 ' 0.1'];
rtn = stkConnect(conid,'Animate','Scenario/Matlab_Basic',cmd1); % send connect command to stk
rtn = stkConnect(conid,'Animate','Scenario/Matlab_Basic','Reset'); 
disp('Set up the propagator and nodes for the satellites');
[parameter] = Create_LEO(conid,'../etc/parameter-StarLink.xlsx');
Create_Fac(conid); % call Create_Fac to create Facilities
inc = str2num(parameter{4,1})*dtr; % inclination of orbit

disp('save position info');
[position, position_cbf]=Create_location(dT);
filename = [constellation '\position.mat'];
save(filename,'position','position_cbf');
disp('save delay info');
for t = 1:cycle
    [delay] = Create_delay(position_cbf,t,inc);
end
stkExec( conid, 'Animate Scenario/Matlab_Basic  Reset' );
stkExec( conid, 'Animate Scenario/Matlab_Basic  Start' );

stkClose(conid)
stkClose
