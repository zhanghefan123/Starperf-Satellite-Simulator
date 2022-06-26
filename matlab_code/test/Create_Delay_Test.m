clear all; close all; clc;
global No_leo leo_plane no;
No_leo = 288;
leo_plane = 12;
no = No_leo / leo_plane;
for i=1:leo_plane
    % traverse all leo satellites in each orbit
    for j=1:no
        % get cur leo satellite number
        cur_leo = (i-1)*no+j;
        % ~x == -(x+1)
        if j ~= no
            up_leo = (i-1)*no+j+1;
            disp(up_leo);
        else
             up_leo = (i-1)*no+1;
        end
        
    end
end
  