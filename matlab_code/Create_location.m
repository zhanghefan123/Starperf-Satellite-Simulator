function [position, position_cbf]=Create_location(dT)
global No_leo  No_fac tStart tStop No_snap Lat Long;
load('Num_leo.mat'); % load saved num_leo variable 
load('Num_fac.mat'); % load saved num_fac variable
index=1;
position = cell(No_leo + No_fac,1); % create (No_leo + No_fac) * 1 cell array
position_cbf = cell(No_leo + No_fac,1);
% traverse leo satellites
for i=1:No_leo
    % get path of the object
    leo_info=strcat('*/Satellite/Sat',num2str(num_leo(i)));
    % stkReport <path> <report type> 
    % LLA represent Latitude Longitude and Altitude
    [secData, secName] = stkReport(leo_info,'LLA Position',tStart, tStop, dT);
    lat = stkFindData(secData{1}, 'Lat');
    long = stkFindData(secData{1}, 'Lon');
    alt = stkFindData(secData{1}, 'Alt');
    llapos = zeros(3,No_snap); % [lat long high] * snapshotCount
    for j = 1:No_snap
        llapos(1,j) = llapos(1,j)+ lat(j)*180/pi; % latitude
        llapos(2,j) = llapos(2,j)+ long(j)*180/pi; % longtitude
        llapos(3,j) = llapos(3,j) + alt(j); % altitude
    end
    position{index} = llapos;
    position_cbf{index} = Lla2Cbf(position{index,1});
    index=index+1;
    
end
% traverse facilities
for i=1:No_fac
    llapos = zeros(3,No_snap);
    llapos(1,:) = llapos(1,:)+Lat(i);
    llapos(2,:) = llapos(2,:)+Long(i);
    position{index} = llapos;
    position_cbf{index} = Lla2Cbf(position{index,1});
    index=index+1;
end
end