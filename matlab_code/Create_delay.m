function [ delay ] = Create_delay(position_cbf,time, inc)
% Calculate delay between LEOs and facilities
% input:
%   position_cbf: used to connect to STK
%   delay: two-dimensional matrix, delay(i,j) denotes 
    global No_fac  No_leo constellation;
    load('Num_leo.mat')
    load('Num_fac.mat');
    % calculate arbitrary two nodes's distance and delay
    distance = zeros(No_fac+No_leo,No_fac+No_leo);
    delay = zeros(No_fac+No_leo,No_fac+No_leo);
    %calculate the distance and delay between leo and others(include leo)
    no = No_leo/leo_plane;
    % traverse all leo orbit planes
    for i=1:leo_plane
        % traverse all leo satellites in each orbit
        for j=1:no
            % get cur leo satellite number
            cur_leo = (i-1)*no+j;
            % ~x == -(x+1)
            if j ~= no % in matlab '!=' is '~='
                up_leo = (i-1)*no+j+1;
            else
                 up_leo = (i-1)*no+1; % assume there are 24 sats in per orbit, then the up_sat of orbit_24 is orbit_1
            end
            % now we should calculate the distance between the sat and its up_sat
            % now calculate the distance between (x1,y1,z1) and (x2,y2,z2)
            distance(cur_leo,up_leo) = sqrt((position_cbf{cur_leo,1}(1,time) - position_cbf{up_leo,1}(1,time))^2 + (position_cbf{cur_leo,1}(2,time) - position_cbf{up_leo,1}(2,time))^2 + (position_cbf{cur_leo,1}(3,time) - position_cbf{up_leo,1}(3,time))^2);
            % distance from a to b equals b to a
            distance(up_leo,cur_leo) = distance(cur_leo,up_leo);
            % calculate delay
            delay(cur_leo,up_leo) = distance(cur_leo,up_leo) / (3 * 10^5);
            delay(up_leo,cur_leo) = delay(cur_leo,up_leo);
            % find right leo
            if i ~= leo_plane
                right_leo = i*no+j;
                
            else
                % if the orbit is polar orbit , it has seam
                if inc > 80 && inc < 100
                    continue;
                % if the orbit is inclined orbit, it has no seam
                else
                    right_leo = j;
                end
            end
            % calculate distance and delay
            distance(cur_leo,right_leo) = sqrt((position_cbf{cur_leo,1}(1,time) - position_cbf{right_leo,1}(1,time))^2 + (position_cbf{cur_leo,1}(2,time) - position_cbf{right_leo,1}(2,time))^2 + (position_cbf{cur_leo,1}(3,time) - position_cbf{right_leo,1}(3,time))^2);
            distance(right_leo,cur_leo) = distance(cur_leo,right_leo);
            delay(cur_leo,right_leo) = distance(cur_leo,right_leo) / (3 * 10^5);
            delay(right_leo,cur_leo) = delay(cur_leo,right_leo);
        end
    end
    % traverse all satellites
    for i = 1:No_leo
        % traverse all ground facilities  
        for j = No_leo + 1:No_fac+No_leo
            distance(i,j) = sqrt((position_cbf{i,1}(1,time) - position_cbf{j,1}(1,time))^2 + (position_cbf{i,1}(2,time) - position_cbf{j,1}(2,time))^2 + (position_cbf{i,1}(3,time) - position_cbf{j,1}(3,time))^2);
            distance(j,i) = distance(i,j);
            delay(i,j) = distance(i,j) / (3 * 10^5);
            delay(j,i) = delay(i,j);
        end
    end
    filename = [constellation '\delay\'];
    filename = strcat(filename,num2str(time));
    filename = strcat(filename,'.mat');
    save(filename,'delay') 
end

