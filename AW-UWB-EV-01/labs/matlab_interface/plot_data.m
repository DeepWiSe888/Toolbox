close all;
%%
delete(instrfindall);

if exist('s','var')
    delete(s);
end
s = serialport("COM3",4000000);
configureTerminator(s,"CR/LF")


if 0 == set_dev(s)
    demo_1(s);
    
    % demo_2(s) 
end

function demo_1(s)
    %defaults paramters,you can modify the value in the function "set_dev"
    fps = 40; %fps
    sec = 6;  %seconds to plot
    step = 1; %plot data step
    
    last_fn = 0;

    datas = [];
    figure(1)
    set(gcf,'position',[450, 450,900, 250])
    while 1
        data = parse_pack(s);
        datas = [datas;data.i + 1i*data.q];
        
        if data.frame_no - last_fn > 1
            fprintf('frame no error,last frame no:%d,frame no:%d.',last_fn,data.frame_no);
        end
        last_fn = data.frame_no;
        
        if length(datas) >= sec * fps
            x = datas(end - sec * fps + 1:end,:);
            
            org_abs = abs(x);
            
            iq_data = x - mean(x,1);
            iq_abs = abs(iq_data);
            
            iq_bin_sum = sum(iq_abs,1);


            subplot(1,3,1)
            imagesc(org_abs)
            xticks([]);
            yticks([]);
            xlabel("fast time")
            ylabel("slow time")
            
            subplot(1,3,2)
            imagesc(iq_abs)
            xticks([]);
            yticks([]);
            xlabel("fast time")
            ylabel("slow time")
            
            subplot(1,3,3)
            plot(iq_bin_sum)
            xticks([]);
            yticks([]);
            xlabel("fast time")
            ylabel("amplitude")
            
            datas = datas(end -(sec - step)* 40 + 1:end,:);
        end
        
    end
end

function demo_2(s)
    configureCallback(s,"byte",1024,@serial_callback)
    pause
    configureCallback(s,"off")
end

function serial_callback(s,~)
    figure(1)
    data = parse_pack(s);
    plot(abs(data.i + 1i*data.q))
end

function data = parse_pack(s)
    
    flag = [233,207,147,114];
    packs = [];
    cnt = 1;
    while cnt <=4
        f = read(s,1,'uint8');
        if f == flag(cnt)
            cnt = cnt + 1;
        else
            cnt = 1;
        end
    end
    %frame no
    data.frame_no = read(s,1,'uint32');
    %timestamp from start up
    data.timestamp = read(s,1,'uint64');
    %buff size
    data.buff_size = read(s,1,'uint16');
    %frame size
    frame_size = read(s,1,'uint16');
    data.frame_size = frame_size;

    i_org = read(s,100,'single');
    q_org = read(s,100,'single');

    %i channel
    data.i = i_org(1:frame_size / 2);
    %q channel
    data.q = q_org(1:frame_size / 2);
    
    X = sprintf('frame no:%d,timestamp:%d,buff size:%d,frame size:%d.',data.frame_no,data.timestamp,data.buff_size,data.frame_size);
    %disp(X);
end

function status = set_dev(s)
    status = 0;
    %stop;
    if send_cmd(s,"AT+STOP")
        disp("STOP Dev Error.")
        status = -1;
        return 
    end
    %get the version
%     if "VERSION:1.1" ~= get_version(s,"AT+VER")
%         disp("The software and hardware versions do not match.")
%         status = -1;
%         return 
%     end
    
    if send_cmd(s,"AT+FPS 40")
        disp("Set fps Error.")
        status = -1;
        return 
    end
    
    if send_cmd(s,"AT+PPS 128")
        disp("Set pps Error.")
        status = -1;
        return 
    end

    if send_cmd(s,"AT+ITER 16")
        disp("Set iter Error.")
        status = -1;
        return 
    end

    if send_cmd(s,"AT+DMIN 949")
        disp("Set Dac min Error.")
        status = -1;
        return 
    end

    if send_cmd(s,"AT+DMAX 1100")
        disp("Set Dac max Error.")
        status = -1;
        return 
    end

    if send_cmd(s,"AT+DIST 0.2,5.0")
        disp("Set Distance Error.")
        status = -1;
        return 
    end

    if send_cmd(s,"AT+START")
        disp("Start Error.")
        status = -1;
        return 
    end
end

function resp = get_version(s,cmd)
    resp = writeread(s,cmd);
end

function status = send_cmd(s,cmd)
    resp = writeread(s,cmd);
    status = check_status(resp);
end

function status = check_status(resp,cmd)
    status = 0;
    if contains(resp,"OK")
        status = 0;
    else
        status = -1;
    end
end




