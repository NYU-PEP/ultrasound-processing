function aviframes2(filename,starttime,endtime,label)

%
% AVIFRAMES2(FILENAME,STARTTIME,ENDTIME,LABEL) reads an AVI file &
% outputs the frames between STARTTIME & ENDTIME, appends the
% extension LABEL to the output as JPG frames
%
% For example,
%
% >> aviframes2('hm104-2-2-3.avi',0.984,1.149,'ktW');
%
% will find the frame closest to STARTTIME 0.984 and round down,
% and the frame closest to ENDTIME 1.149 and round up, then
% output the following files based on FILENAME, the STARTTIME & ENDTIME
% and the LABEL:
%
%   hm104-2-2-3_029_ktW.jpg
%   hm104-2-2-3_030_ktW.jpg
%   hm104-2-2-3_031_ktW.jpg
%   hm104-2-2-3_032_ktW.jpg
%   hm104-2-2-3_033_ktW.jpg
%   hm104-2-2-3_034_ktW.jpg
%   hm104-2-2-3_035_ktW.jpg

obj = VideoReader(filename);
fps = obj.FrameRate;

%now convert input seconds to output frames
startframe=floor(starttime*fps);
endframe=ceil(endtime*fps);
%indices=[startframe,endframe];
indices=(startframe:endframe);

% import the frames
myframes = read(obj,[startframe,endframe]);

% How many digits are in the highest frame index?
max_index = get(obj,'NumberOfFrames');
str_max_index = int2str(max_index);
max_num_digits = length(str_max_index);

[t,r] = strtok(fliplr(filename),'.');
imfilebase = strtok(fliplr(r),'.');

for i=1:length(indices)
    % Pull .avi extension off of filename

    % How many digits in the current frame index?
    str_index = int2str(indices(i));
    num_digits = length(str_index);
    num_zeros = max_num_digits - num_digits;

    imfilename = strcat(imfilebase,'_');
    for j=1:num_zeros
        imfilename = strcat(imfilename,'0');
    end
    %imfilename = strcat(imfilename,str_index);
    imfilename = strcat(imfilename,str_index,'_',label);
    imfilename = strcat(imfilename,'.jpg')
    
    mov(i).cdata = myframes(:,:,:,i);

    imwrite(mov(i).cdata,imfilename,'jpeg','Quality',100);
end