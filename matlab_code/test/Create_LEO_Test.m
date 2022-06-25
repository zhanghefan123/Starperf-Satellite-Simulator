clear all; close all; clc;
global No_leo cycle No_snap tStop constellation dT tStart;
path = '../../etc/parameter-StarLink.xlsx'
dT = 0;
tStart = 0;
parameter = readtable(path); % read parameters from xlsx file
parameter = parameter.Value; 
constellation = parameter{1,1}; % first line first column
Altitude = str2num(parameter{2,1}); % second line first column 
cycle = str2num(parameter{3,1});
No_snap = floor(cycle/dT)+1;
tStop = cycle;
dtr = pi/180;
inc = str2num(parameter{4,1})*dtr;
F = str2num(parameter{5,1});
leo_plane = str2num(parameter{6,1});
no = str2num(parameter{7,1});
meanAnomoly = [0:360/no:360/no*(no-1)]
result = [1 2 3 4] .* 2;
temp = cell(3,1);
