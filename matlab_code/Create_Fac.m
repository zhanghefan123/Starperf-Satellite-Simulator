function Create_Fac(conid)
    % this function is used to establish ground facility such as ground stations
    disp('settings of Fac');
    global No_fac Lat Long; % No_fac : number of facilities Lat : list of latitude Long : list of longitude
    Long = [116.3 -74 -0.10 150.53];
    Lat = [39.9 40.42 51.30 -33.55];
    No_fac=length(Long);
    % traverse each facility
    for i=1:No_fac
        % name of the facility
        info_facility=strcat('Fac',num2str(i));
        stkNewObj('*/','Facility',info_facility);
        lat=Lat(i);
        long=Long(i);
        % createStkFacility by latitude and longtitude
        info_facility=strcat('Scenario/Matlab_Basic/Facility/',info_facility);
        stkSetFacPosLLA(info_facility, [lat*pi/180; long*pi/180; 0]);
        % we here set constraint that the elevation Angle min 20 
        % SetConstraint <ObjectPath> <ConstraintName> <Parameters>
        stkConnect(conid,'SetConstraint',info_facility,'ElevationAngle Min 20');
        num_fac(i)=i;
    end
    save('Num_fac.mat','num_fac');
    end