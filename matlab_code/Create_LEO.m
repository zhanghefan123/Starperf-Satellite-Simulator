function [parameter] = Create_LEO(conid,path)
% Create LEOs in STK
% input:
%   conid: used to connect to STK
%   path: configuration file path of mega-constellations

    global No_leo cycle No_snap tStop constellation dT;
    parameter = readtable(path); % read parameters from xlsx file : attention the first line and first column of the sheet are ignored
    parameter = parameter.Value; 
    constellation = parameter{1,1}; % first line first column
    Altitude = str2num(parameter{2,1}); % second line first column 
    cycle = str2num(parameter{3,1});% third line first column
    No_snap = floor(cycle/dT)+1; % snap shot count equals to 
    tStop = cycle; % simulation stop time
    dtr = pi/180; % degree to radian
    inc = str2num(parameter{4,1})*dtr; % orbit inclination
    F = str2num(parameter{5,1}); % shift
    leo_plane = str2num(parameter{6,1}); % orbit num
    no = str2num(parameter{7,1}); % sat_per_orbit
    % if orbit is polar orbit
    if (str2num(parameter{4,1}) > 80) && (str2num(parameter{4,1}) < 100)
        raan=[0:180/leo_plane:180/leo_plane*(leo_plane-1)]; % RAAN range from 0 ~ 180 [start:step:destination]
    else
        raan=[0:360/leo_plane:360/leo_plane*(leo_plane-1)]; % RAAN range from 0 ~ 360 [start:step:destination]
    end
    meanAnomaly1 = [0:360/no:360/no*(no-1)]; % mean anomaly specify the position of satellite [start:step:destination]
    raan = raan.*dtr; % [1 2 3 4] .* 2 = [2 4 6 8]
    No_leo = leo_plane*no; % total satellites
    disp('LEO:');
    disp(No_leo);
    % traverse each orbit plane
    for i =1:leo_plane
        % traverse each satellite in single orbit
        for j=1:no
            % get raan
            ra = raan(i);
            % mean anomoly should consider the phase shift 
            ma = (mod(meanAnomaly1(j) + 360*F/(leo_plane*no)*(i-1),360))*dtr;
            % get index of satellite-ID
            num = j+no*(i-1);
            sat_no = strcat('Sat',num2str(num));
            % create new Satellite in stk
            stkNewObj('*/','Satellite',sat_no);
            sat_no = strcat('*/Satellite/',sat_no);
            % 6371000m is the radius of earth equator
            stkSetPropClassical(sat_no,'J4Perturbation','J2000',0.0,tStop,dT,0,6371000 + Altitude * 10^3,0.0,inc,0.0,ra,ma);
            num_leo(num) = num;
        end
    end
    % save two variables called num_leo and leo_plane
    save('Num_leo.mat','num_leo','leo_plane');
    mkdir(strcat(constellation,'\\delay'))
end


