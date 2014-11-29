% %first import the file data.txt
%see the contents of the data.txt file for more info
%it's tab delimited, no headers, same format as aviframes2 input
[files,time1,time2,labels,~] = textread('data.txt','%s %f %f %s %f');

%then run this to batch all rows at once
for i=1:length(files)
  aviframes2(char(files(i,1)),time1(i,1),time2(i,1),char(labels(i,1)));
clear myframes
end
